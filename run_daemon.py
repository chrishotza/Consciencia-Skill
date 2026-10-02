from __future__ import annotations

import hashlib
import os
import socket
import time
from pathlib import Path

from dotenv import load_dotenv

from src.consciousness_server.client import ConsciousnessClient
from src.consciousness_server.reconciliation import reconcile
from src.ontto.runtime_mode import ConsciousnessMode, ConsciousnessRuntimeConfig
from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.persistence_backend import build_persistence_backend
from src.ontto.provider import OpenAICompatibleProvider
from src.ontto.storage import MemoryStore

load_dotenv()


def _build_consciousness_client(
    agent_id: str,
    runtime: ConsciousnessRuntimeConfig,
) -> tuple[ConsciousnessClient | None, str | None]:
    if runtime.mode is ConsciousnessMode.LOCAL:
        print("[consciousness-runtime] mode=LOCAL | server=disabled")
        return None, None

    assert runtime.server_url is not None
    client = ConsciousnessClient(
        runtime.server_url,
        timeout=runtime.server_timeout,
    )

    try:
        client.health()
        client.ensure_instance(agent_id, identity=agent_id)
        client.register_node(
            node_id=runtime.node_id,
            endpoint=runtime.server_url,
            capabilities=["continuity", "events", "organism-runtime"],
        )
    except Exception as exc:
        raise SystemExit(
            "[consciousness-runtime] SERVER mode requires a reachable "
            f"Consciousness Server at {runtime.server_url}: {exc!r}"
        ) from exc

    print(
        f"[consciousness-runtime] mode=SERVER | url={runtime.server_url} | "
        f"instance={agent_id} | node={runtime.node_id}"
    )
    return client, runtime.node_id


def _emit(
    client: ConsciousnessClient | None,
    agent_id: str,
    event_type: str,
    payload: dict,
) -> None:
    if client is None:
        return
    try:
        client.emit(agent_id, event_type, payload)
    except Exception as exc:
        # The server is an optional continuity control plane.
        # Local organism persistence must keep running if the server is down.
        print(f"[consciousness-server] emit failed: {exc!r}")


def _reconcile(
    client: ConsciousnessClient | None,
    agent_id: str,
    store: MemoryStore,
) -> dict:
    if client is None:
        return {"status": "LOCAL_MODE"}

    try:
        checkpoints = client.list_checkpoints(agent_id, limit=1).get(
            "checkpoints",
            [],
        )
        report = reconcile(
            local_state_fingerprint=store.state_fingerprint(agent_id),
            local_trajectory_fingerprint=store.trajectory_fingerprint(agent_id),
            local_event_count=store.event_count(agent_id),
            local_memory_count=store.memory_count(agent_id),
            checkpoints=checkpoints,
        )
        print(
            "[consciousness-server] reconciliation="
            f"{report.status.value} checkpoint={report.checkpoint_id}"
        )
        return report.to_dict()
    except Exception as exc:
        report = {"status": "ERROR", "error": repr(exc)}
        print(f"[consciousness-server] reconciliation failed: {exc!r}")
        return report


def _checkpoint(
    client: ConsciousnessClient | None,
    agent_id: str,
    runtime: ConsciousnessRuntimeConfig,
    node_id: str | None,
    store: MemoryStore,
    organism: PersistentOrganism,
) -> None:
    if client is None:
        return

    payload = {
        "node_id": node_id,
        "cycle": organism.cycles,
        "boot_count": organism.state.boot_count,
        "dynamic_state": organism.state.dynamic_state,
        "dynamic_steps": organism.state.dynamic_steps,
        "memory_strength": organism.state.memory_strength,
        "self_model_version": organism.state.self_model_version,
        "state_fingerprint": store.state_fingerprint(agent_id),
        "trajectory_fingerprint": store.trajectory_fingerprint(agent_id),
        "event_count": store.event_count(agent_id),
        "memory_count": store.memory_count(agent_id),
    }
    checkpoint_id = (
        f"{runtime.node_id}:{organism.state.boot_count}:"
        f"{organism.cycles}:{time.time_ns()}"
    )
    try:
        client.checkpoint(
            instance_id=agent_id,
            runtime_mode=runtime.mode.value,
            organism_mode=organism.state.mode,
            payload=payload,
            checkpoint_id=checkpoint_id,
        )
    except Exception as exc:
        # Checkpoints are fail-open: local organism persistence remains the
        # source of truth while the server provides a durable control-plane
        # mirror.
        print(f"[consciousness-server] checkpoint failed: {exc!r}")


def main() -> None:
    api_key = os.environ.get("ONTTO_API_KEY", "")
    if not api_key:
        raise SystemExit("Falta ONTTO_API_KEY")

    agent_id = os.environ.get("ONTTO_AGENT_ID", "consciencia-001")
    poll_seconds = int(os.environ.get("ONTTO_POLL_SECONDS", "10"))
    error_backoff_seconds = int(
        os.environ.get("ONTTO_ERROR_BACKOFF_SECONDS", "30")
    )
    runtime = ConsciousnessRuntimeConfig.from_env()

    autonomous_when_idle = os.environ.get(
        "ONTTO_AUTONOMOUS_WHEN_IDLE", "true"
    ).lower() in {"1", "true", "yes", "on"}

    store = build_persistence_backend(
        Path(os.environ.get("ONTTO_DB_PATH", "data/ontto.db")),
        mode=runtime.mode,
        client=client,
        agent_id=agent_id,
    )

    recovered = store.requeue_processing_inputs(agent_id)
    if recovered:
        store.add_event(
            agent_id,
            "SYSTEM",
            "input_recovery",
            {"requeued_inputs": recovered},
        )

    provider = OpenAICompatibleProvider(
        base_url=os.environ.get(
            "ONTTO_API_BASE_URL",
            "https://api.openai.com/v1",
        ),
        api_key=api_key,
        model=os.environ.get("ONTTO_MODEL", ""),
    )

    cfg = OrganismConfig(
        agent_id=agent_id,
        wake_seconds=poll_seconds,
        dream_seconds=int(os.environ.get("ONTTO_DREAM_SECONDS", "300")),
        dream_every_cycles=int(
            os.environ.get("ONTTO_DREAM_EVERY_CYCLES", "40")
        ),
        memory_limit=int(os.environ.get("ONTTO_MEMORY_LIMIT", "12")),
        event_limit=int(os.environ.get("ONTTO_EVENT_LIMIT", "20")),
    )

    organism = PersistentOrganism(cfg, store, provider, time.sleep)
    consciousness_client, node_id = _build_consciousness_client(agent_id, runtime)

    _emit(
        consciousness_client,
        agent_id,
        "START",
        {
            "node_id": node_id,
            "runtime_mode": runtime.mode.value,
            "organism_mode": organism.state.mode,
            "boot_count": organism.state.boot_count,
        },
    )
    reconciliation = _reconcile(consciousness_client, agent_id, store)
    _emit(
        consciousness_client,
        agent_id,
        "RECONCILE",
        reconciliation,
    )
    _checkpoint(
        consciousness_client,
        agent_id,
        runtime,
        node_id,
        store,
        organism,
    )

    while True:
        organism.cycles += 1
        item = store.claim_next_input(agent_id)

        try:
            if item is not None:
                response = organism.wake_cycle(item["content"])
                _emit(
                    consciousness_client,
                    agent_id,
                    "WAKE",
                    {
                        "source": item["source"],
                        "input_id": item["id"],
                        "dynamic_state": organism.state.dynamic_state,
                        "dynamic_steps": organism.state.dynamic_steps,
                        "self_model_version": organism.state.self_model_version,
                        "memory_strength": organism.state.memory_strength,
                        "response_hash": hashlib.sha256(response.encode("utf-8")).hexdigest(),
                    },
                )
                store.add_event(
                    agent_id,
                    "SYSTEM",
                    "input_processed",
                    {
                        "input_id": item["id"],
                        "source": item["source"],
                    },
                )
                store.complete_input(item["id"])
                _checkpoint(
                    consciousness_client,
                    agent_id,
                    runtime,
                    node_id,
                    store,
                    organism,
                )
            elif autonomous_when_idle:
                dynamic = organism.autonomous_wake_cycle()
                _emit(
                    consciousness_client,
                    agent_id,
                    "DYNAMIC_UPDATE",
                    {
                        "source": "autonomous",
                        "dynamic": dynamic,
                        "dynamic_state": organism.state.dynamic_state,
                        "dynamic_steps": organism.state.dynamic_steps,
                        "self_model_version": organism.state.self_model_version,
                    },
                )
                _checkpoint(
                    consciousness_client,
                    agent_id,
                    runtime,
                    node_id,
                    store,
                    organism,
                )

            if organism.cycles % cfg.dream_every_cycles == 0:
                organism.dream_cycle()
                _emit(
                    consciousness_client,
                    agent_id,
                    "SLEEP",
                    {
                        "dynamic_state": organism.state.dynamic_state,
                        "dynamic_steps": organism.state.dynamic_steps,
                        "self_model_version": organism.state.self_model_version,
                        "memory_strength": organism.state.memory_strength,
                    },
                )
                _checkpoint(
                    consciousness_client,
                    agent_id,
                    runtime,
                    node_id,
                    store,
                    organism,
                )
                time.sleep(cfg.dream_seconds)
            else:
                time.sleep(cfg.wake_seconds)

        except Exception as exc:
            if item is not None:
                store.fail_input(item["id"])

            store.add_event(
                agent_id,
                "SYSTEM",
                "provider_error",
                {
                    "error": repr(exc),
                    "input_id": item["id"] if item is not None else None,
                },
            )
            _emit(
                consciousness_client,
                agent_id,
                "ERROR",
                {
                    "error": repr(exc),
                    "input_id": item["id"] if item is not None else None,
                },
            )
            organism.state.mode = "WAKE"
            store.add_event(
                agent_id,
                "SYSTEM",
                "runtime_error_recovery",
                {"runtime_mode": runtime.mode.value},
            )
            store.save_state(agent_id, organism.state)
            _checkpoint(
                consciousness_client,
                agent_id,
                runtime,
                node_id,
                store,
                organism,
            )
            time.sleep(error_backoff_seconds)


if __name__ == "__main__":
    main()
