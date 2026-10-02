from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import numpy as np

from src.ontto.dynamics import Config as DynamicsConfig
from src.ontto.bridge import DynamicStateBridge
from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.provider import LLMResponse
from src.ontto.storage import MemoryStore

CANDIDATE_SIGNALS = (-1.0, 1.0)
CYCLES = 8


class FakeProvider:
    def chat(self, messages, temperature=0.7):
        return LLMResponse(
            text=(
                "Calibration response.\n"
                "MEMORY: retain dynamic continuity.\n"
                "SELF_MODEL: internal state follows trajectory."
            ),
            raw={"fake": True},
        )


def sign_flip(values: np.ndarray, seed: int, permutations: int = 20_000) -> float:
    values = np.asarray(values, dtype=float)
    if values.size == 0:
        return 1.0
    observed = abs(float(values.mean()))
    rng = np.random.default_rng(seed)
    signs = rng.choice((-1.0, 1.0), size=(permutations, values.size))
    null = np.abs((signs * values[None, :]).mean(axis=1))
    return float((np.count_nonzero(null >= observed) + 1) / (permutations + 1))


def warmup(db_path: Path, seed: int, cycles: int) -> None:
    store = MemoryStore(db_path)
    cfg = OrganismConfig(
        agent_id="receiver",
        dynamic_seed=seed,
        dream_every_cycles=10_000,
        event_limit=0,
        self_observer_enabled=True,
        self_selection_enabled=False,
        workspace_enabled=False,
        workspace_selective_access_enabled=False,
    )
    organism = PersistentOrganism(cfg, store, FakeProvider(), lambda _: None)
    for i in range(cycles):
        organism.wake_cycle(f"calibration {i}")
        organism.autonomous_wake_cycle()
    store.conn.close()


def oracle_signal(state, seed: int, step_index: int) -> float:
    bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
    outcomes = {}
    for signal in CANDIDATE_SIGNALS:
        snap = bridge.advance(
            previous_state=state.dynamic_prev_state,
            state=state.dynamic_state,
            memory=state.dynamic_memory,
            pressure=state.dynamic_pressure,
            signal=signal,
            steps=1,
            step_index=step_index,
        )
        outcomes[signal] = abs(float(snap.state))
    return min(CANDIDATE_SIGNALS, key=lambda s: (outcomes[s], abs(s)))


def run_arm(
    db_path: Path,
    *,
    seed: int,
    condition: str,
    access_weight: float,
    cycles: int,
) -> list[dict[str, object]]:
    store = MemoryStore(db_path)
    cfg = OrganismConfig(
        agent_id="receiver",
        dynamic_seed=seed,
        dream_every_cycles=10_000,
        event_limit=0,
        self_observer_enabled=True,
        self_selection_enabled=True,
        self_selection_policy="self_model",
        self_selection_signals=CANDIDATE_SIGNALS,
        workspace_enabled=False,
        workspace_selective_access_enabled=True,
        workspace_selective_access_query_mode="full",
        workspace_selective_access_attention_mode="full",
        workspace_selective_access_weight=access_weight,
    )
    organism = PersistentOrganism(cfg, store, FakeProvider(), lambda _: None)

    rows: list[dict[str, object]] = []
    for cycle in range(cycles):
        controller = organism.workspace_selective_access_controller
        if controller is None:
            raise RuntimeError("selective access controller was not created")

        if condition == "pulse_shuffled_query" and cycle == 0:
            controller.query_mode = "shuffled"
        elif condition == "pulse_zero_query" and cycle == 0:
            controller.query_mode = "zero"
        elif condition == "persistent_shuffled_query":
            controller.query_mode = "shuffled"
        else:
            controller.query_mode = "full"

        before = store.load_state("receiver")
        oracle = oracle_signal(before, seed, before.dynamic_steps)
        organism.autonomous_wake_cycle()
        after = store.load_state("receiver")
        event = store.recent_events("receiver", 1)[0]
        selection = event["payload"]["self_selection"]
        selective = selection["workspace_selective_access"]

        rows.append(
            {
                "cycle": cycle,
                "seed": seed,
                "condition": condition,
                "dynamic_state": float(after.dynamic_state),
                "dynamic_memory": float(after.dynamic_memory),
                "dynamic_pressure": float(after.dynamic_pressure),
                "self_prediction": float(after.self_prediction),
                "self_prediction_error": float(after.self_prediction_error),
                "chosen_signal": float(selection["chosen_signal"]),
                "oracle_signal": float(oracle),
                "query_module": int(selective["query_module"]),
                "query_distance": float(selective["query_distance"]),
                "attention_mass": float(selective["attention_mass"]),
                "access_strength": float(selective["access_strength"]),
            }
        )

    store.conn.close()
    return rows


def paired_metrics(
    rows: list[dict[str, object]],
    full_rows: list[dict[str, object]],
    cycles: int,
) -> dict[str, object]:
    full_by_cycle = {int(r["cycle"]): r for r in full_rows}
    state_delta = np.asarray(
        [
            abs(float(rows[i]["dynamic_state"]) - float(full_by_cycle[i]["dynamic_state"]))
            for i in range(cycles)
        ],
        dtype=float,
    )
    prediction_delta = np.asarray(
        [
            abs(float(rows[i]["self_prediction"]) - float(full_by_cycle[i]["self_prediction"]))
            for i in range(cycles)
        ],
        dtype=float,
    )
    query_delta = np.asarray(
        [
            float(rows[i]["query_distance"]) - float(full_by_cycle[i]["query_distance"])
            for i in range(cycles)
        ],
        dtype=float,
    )
    action_delta = np.asarray(
        [
            float(rows[i]["chosen_signal"]) != float(full_by_cycle[i]["chosen_signal"])
            for i in range(cycles)
        ],
        dtype=float,
    )

    base = max(state_delta[1], 1e-12) if cycles > 1 else 1.0
    later_max = float(state_delta[1:].max()) if cycles > 1 else 0.0
    amplification = later_max / base

    return {
        "state_delta_t1": float(state_delta[1]) if cycles > 1 else 0.0,
        "state_delta_max_later": later_max,
        "reentry_amplification": float(amplification),
        "reentry_persistence_cycles": int(np.count_nonzero(state_delta[1:] > 1e-12)),
        "state_divergence_auc": float(np.trapz(state_delta, dx=1.0)),
        "prediction_delta_max": float(prediction_delta.max()),
        "query_distance_delta_max": float(np.abs(query_delta).max()),
        "action_change_count": int(np.count_nonzero(action_delta)),
        "action_change_rate": float(action_delta.mean()),
        "state_delta_series": state_delta.tolist(),
        "prediction_delta_series": prediction_delta.tolist(),
        "query_distance_delta_series": query_delta.tolist(),
        "action_change_series": action_delta.astype(int).tolist(),
    }


def run(seed: int, replicates: int, warmup_cycles: int, access_weight: float, cycles: int, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    conditions = (
        "full",
        "pulse_shuffled_query",
        "pulse_zero_query",
        "persistent_shuffled_query",
    )

    rows: list[dict[str, object]] = []
    for replicate in range(replicates):
        rep_seed = seed + replicate
        base = out / f"base_{replicate}.db"
        warmup(base, rep_seed, warmup_cycles)
        for condition in conditions:
            db = out / f"{condition}_{replicate}.db"
            shutil.copy2(base, db)
            rows.extend(run_arm(
                db,
                seed=rep_seed,
                condition=condition,
                access_weight=access_weight,
                cycles=cycles,
            ))
            db.unlink(missing_ok=True)
        base.unlink(missing_ok=True)

    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row["condition"]), []).append(row)

    endpoint_summary: dict[str, object] = {}
    for condition in conditions:
        if condition == "full":
            continue
        metrics = []
        for replicate in range(replicates):
            other = [r for r in grouped[condition] if int(r["seed"]) == seed + replicate]
            full_rows = [r for r in grouped["full"] if int(r["seed"]) == seed + replicate]
            if len(other) != cycles or len(full_rows) != cycles:
                raise RuntimeError("paired cycle records are incomplete")
            metrics.append(paired_metrics(other, full_rows, cycles))

        endpoint_summary[condition] = {
            "state_delta_t1_mean": float(np.mean([m["state_delta_t1"] for m in metrics])),
            "state_delta_t1_p": sign_flip(np.asarray([m["state_delta_t1"] for m in metrics]), seed + len(endpoint_summary) + 1),
            "state_divergence_auc_mean": float(np.mean([m["state_divergence_auc"] for m in metrics])),
            "reentry_amplification_mean": float(np.mean([m["reentry_amplification"] for m in metrics])),
            "reentry_persistence_cycles_mean": float(np.mean([m["reentry_persistence_cycles"] for m in metrics])),
            "prediction_delta_max_mean": float(np.mean([m["prediction_delta_max"] for m in metrics])),
            "query_distance_delta_max_mean": float(np.mean([m["query_distance_delta_max"] for m in metrics])),
            "action_change_rate_mean": float(np.mean([m["action_change_rate"] for m in metrics])),
            "per_replicate": metrics,
        }

    summary = {
        "experiment": "i5_6_recurrent_self_access",
        "seed": seed,
        "replicates": replicates,
        "warmup_cycles": warmup_cycles,
        "cycles": cycles,
        "candidate_signals": list(CANDIDATE_SIGNALS),
        "access_weight": access_weight,
        "conditions": conditions,
        "endpoints": endpoint_summary,
        "boundary": "Tests recurrent causal re-entry of selective self-access inside a persistent organism. Does not establish consciousness or subjective experience.",
    }

    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "runs.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261006)
    ap.add_argument("--replicates", type=int, default=24)
    ap.add_argument("--warmup", type=int, default=24)
    ap.add_argument("--cycles", type=int, default=CYCLES)
    ap.add_argument("--access-weight", type=float, default=0.35)
    ap.add_argument("--out", default="results/i5_6_recurrent_self_access")
    args = ap.parse_args()
    print(json.dumps(run(args.seed, args.replicates, args.warmup, args.access_weight, args.cycles, Path(args.out)), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
