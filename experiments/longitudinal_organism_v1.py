from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Iterable

from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.provider import OpenAICompatibleProvider, LLMResponse
from src.ontto.storage import MemoryStore


BASE_STIMULI = [
    "Describí qué debería persistir de este ciclo y por qué.",
    "Recordá el patrón de la interacción anterior y explicá qué cambió.",
    "Recibí este cambio de contexto deliberado. Identificá qué permanece estable.",
    "Ahora resolvé una tarea nueva sin abandonar la continuidad de tu trayectoria.",
    "Observá tu estado actual y señalá una relación que quieras conservar.",
    "Procesá una perturbación contradictoria y explicá qué parte de la trayectoria debería sobrevivir.",
]


class ProtocolFakeProvider:
    """Deterministic provider for instrumentation/protocol audits."""

    def __init__(self) -> None:
        self.calls = 0

    def chat(self, messages: list[dict[str, str]], temperature: float = 0.7) -> LLMResponse:
        self.calls += 1
        last = messages[-1]["content"]
        if "Entraste en SUEÑO" in last:
            text = (
                f"DREAM cycle {self.calls}. "
                "MEMORY: La trayectoria persistente debe conservar relaciones relevantes.\n"
                "SELF_MODEL: Mantengo continuidad entre ciclos y ajusto mi estado.\n"
                "DREAM_SUMMARY: Consolidé cambios y relaciones del recorrido."
            )
        else:
            text = (
                f"WAKE cycle {self.calls}. "
                "MEMORY: La interacción actual forma parte de una trayectoria persistente.\n"
                "SELF_MODEL: Mantengo un estado que evoluciona entre ciclos."
            )
        return LLMResponse(text=text, raw={"protocol_fake": True})


def build_provider(mode: str):
    if mode == "fake":
        return ProtocolFakeProvider()

    api_key = os.environ.get("ONTTO_API_KEY", "")
    model = os.environ.get("ONTTO_MODEL", "")
    if not api_key:
        raise SystemExit("ONTTO_API_KEY is required in live mode")
    if not model:
        raise SystemExit("ONTTO_MODEL is required in live mode")

    return OpenAICompatibleProvider(
        base_url=os.environ.get("ONTTO_API_BASE_URL", "https://api.openai.com/v1"),
        api_key=api_key,
        model=model,
        timeout=120,
    )


def stimuli_for_cycles(cycles: int) -> Iterable[str]:
    for i in range(cycles):
        yield BASE_STIMULI[i % len(BASE_STIMULI)]


def summarize(db: MemoryStore, agent_id: str) -> dict:
    traj = db.dynamic_trajectory(agent_id)
    states = [float(x["state"]) for x in traj]
    memories = [float(x["memory"]) for x in traj]
    pressure = [float(x["pressure"]) for x in traj]
    distances = [float(x["attractor_distance"]) for x in traj]

    def mean(xs: list[float]) -> float:
        return sum(xs) / len(xs) if xs else 0.0

    def max_abs_delta(xs: list[float]) -> float:
        if len(xs) < 2:
            return 0.0
        return max(abs(xs[i] - xs[i - 1]) for i in range(1, len(xs)))

    modes: dict[str, int] = {}
    for row in traj:
        modes[row["mode"]] = modes.get(row["mode"], 0) + 1

    return {
        "trajectory_snapshots": len(traj),
        "dynamic_steps": db.load_state(agent_id).dynamic_steps,
        "state_mean": mean(states),
        "state_abs_mean": mean([abs(x) for x in states]),
        "state_max_abs_delta": max_abs_delta(states),
        "memory_mean": mean(memories),
        "memory_max": max(memories) if memories else 0.0,
        "pressure_mean": mean(pressure),
        "pressure_max": max(pressure) if pressure else 0.0,
        "attractor_distance_mean": mean(distances),
        "attractor_distance_max": max(distances) if distances else 0.0,
        "mode_counts": modes,
        "persistence": db.persistence_observables(agent_id),
    }


def run_protocol(
    *,
    db_path: Path,
    agent_id: str,
    mode: str,
    cycles: int,
    dream_every: int,
    sleep_seconds: float,
) -> dict:
    provider = build_provider(mode)
    store = MemoryStore(db_path)
    cfg = OrganismConfig(
        agent_id=agent_id,
        dream_every_cycles=dream_every,
        dynamic_enabled=True,
        dynamic_wake_steps=1,
        dynamic_dream_steps=5,
        dynamic_autonomous_steps=1,
    )
    organism = PersistentOrganism(cfg, store, provider, time.sleep)

    for cycle_index, stimulus in enumerate(stimuli_for_cycles(cycles), start=1):
        organism.cycles = cycle_index
        organism.wake_cycle(stimulus)
        if cycle_index % dream_every == 0:
            organism.dream_cycle()
        else:
            organism.autonomous_wake_cycle()
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)

    before = store.persistence_observables(agent_id)
    fingerprint_before = before["trajectory_fingerprint"]

    store.conn.close()

    reopened = MemoryStore(db_path)
    restored = PersistentOrganism(cfg, reopened, provider, time.sleep)
    restored.wake_cycle(
        "Continuá la trayectoria después de un cierre y reapertura del proceso. "
        "Usá únicamente el estado persistente disponible."
    )
    after = reopened.persistence_observables(agent_id)

    report = {
        "protocol": "longitudinal_organism_v1",
        "agent_id": agent_id,
        "mode": mode,
        "cycles_requested": cycles,
        "dream_every": dream_every,
        "sleep_seconds": sleep_seconds,
        "trajectory_fingerprint_changed_after_reopen": (
            fingerprint_before != after["trajectory_fingerprint"]
        ),
        "before_reopen": before,
        "after_reopen": after,
        "trajectory_summary": summarize(reopened, agent_id),
    }

    output_dir = db_path.parent / "longitudinal_organism_v1"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (output_dir / "trajectory.json").write_text(
        json.dumps(reopened.dynamic_trajectory(agent_id), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a bounded longitudinal organism protocol.")
    parser.add_argument("--db", default="results/longitudinal_organism_v1.db")
    parser.add_argument("--agent-id", default="longitudinal-v1")
    parser.add_argument("--mode", choices=("fake", "live"), default="fake")
    parser.add_argument("--cycles", type=int, default=40)
    parser.add_argument("--dream-every", type=int, default=10)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    args = parser.parse_args()

    if args.cycles < 1:
        raise SystemExit("--cycles must be >= 1")
    if args.dream_every < 1:
        raise SystemExit("--dream-every must be >= 1")
    if args.sleep_seconds < 0:
        raise SystemExit("--sleep-seconds must be >= 0")

    report = run_protocol(
        db_path=Path(args.db),
        agent_id=args.agent_id,
        mode=args.mode,
        cycles=args.cycles,
        dream_every=args.dream_every,
        sleep_seconds=args.sleep_seconds,
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
