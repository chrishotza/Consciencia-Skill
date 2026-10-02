from __future__ import annotations

import hashlib
import os
import socket
import time
from pathlib import Path

from dotenv import load_dotenv

from src.consciousness_server.client import ConsciousnessClient
from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.provider import OpenAICompatibleProvider
from src.ontto.storage import MemoryStore

load_dotenv()


def _build_consciousness_client(
    agent_id: str,
) -> tuple[ConsciousnessClient | None, str | None]:
    base_url = os.environ.get("CONSCIOUSNESS_SERVER_URL", "").strip()
    if not base_url:
        return None, None

    timeout = float(os.environ.get("CONSCIOUSNESS_SERVER_TIMEOUT", "2.5"))
    node_id = os.environ.get(
        "CONSCIOUSNESS_NODE_ID",
        f"node-{socket.gethostname().lower()}",
    )
    client = ConsciousnessClient(base_url, timeout=timeout)

    try:
        client.health()
        client.ensure_instance(agent_id, identity=agent_id)
        client.register_node(
            node_id=node_id,
            endpoint=base_url,
            capabilities=["continuity", "events", "organism-runtime"],
        )
    except Exception as exc:
        print(f"[consciousness-server] unavailable at startup: {exc!r}")
        return None, node_id

    print(
        f"[consciousness-server] connected | url={base_url} | "
        f"instance={agent_id} | node={node_id}"
    )
    return client, node_id


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


def main() -> None:
    api_key = os.environ.get("ONTTO_API_KEY", "")
    if not api_key:
        raise SystemExit("Falta ONTTO_API_KEY")

    agent_id = os.environ.get("ONTTO_AGENT_ID", "consciencia-001")
    poll_seconds = int(os.environ.get("ONTTO_POLL_SECONDS", "10"))
    error_backoff_seconds = int(
        os.environ.get("ONTTO_ERROR_BACKOFF_SECONDS", "30")
    )
    autonomous_when_idle = os.environ.get(
        "ONTTO_AUTONOMOUS_WHEN_IDLE", "true"
    ).lower() in {"1", "true", "yes", "on"}

    store = MemoryStore(
        Path(os.environ.get("ONTTO_DB_PATH", "data/ontto.db"))
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
    consciousness_client, node_id = _build_consciousness_client(agent_id)

    _emit(
        consciousness_client,
        agent_id,
        "START",
        {
            "node_id": node_id,
            "organism_mode": organism.state.mode,
            "boot_count": organism.state.boot_count,
        },
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
            store.save_state(agent_id, organism.state)
            time.sleep(error_backoff_seconds)


if __name__ == "__main__":
    main()
