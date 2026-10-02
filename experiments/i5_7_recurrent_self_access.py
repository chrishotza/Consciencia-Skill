from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import numpy as np

from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.provider import LLMResponse
from src.ontto.storage import MemoryStore

CYCLES = 8
CANDIDATE_SIGNALS = (-1.0, 1.0)
EPS = 1e-12


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
        workspace_query_task_enabled=False,
    )
    organism = PersistentOrganism(cfg, store, FakeProvider(), lambda _: None)
    for i in range(cycles):
        organism.wake_cycle(f"calibration {i}")
        organism.autonomous_wake_cycle()
    store.conn.close()


def run_arm(
    db_path: Path,
    *,
    seed: int,
    condition: str,
    task_weight: float,
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
        workspace_selective_access_enabled=False,
        workspace_query_task_enabled=True,
        workspace_query_task_query_mode="full",
        workspace_query_task_attention_mode="full",
        workspace_query_task_bottleneck_enabled=True,
        workspace_query_task_lesion_target=False,
        workspace_query_task_weight=task_weight,
        workspace_query_task_threshold=0.20,
    )
    organism = PersistentOrganism(cfg, store, FakeProvider(), lambda _: None)

    rows: list[dict[str, object]] = []
    for cycle in range(cycles):
        if condition == "pulse_shuffled_query" and cycle == 0:
            organism.cfg.workspace_query_task_query_mode = "shuffled"
        elif condition == "pulse_zero_query" and cycle == 0:
            organism.cfg.workspace_query_task_query_mode = "zero"
        elif condition == "persistent_shuffled_query":
            organism.cfg.workspace_query_task_query_mode = "shuffled"
        else:
            organism.cfg.workspace_query_task_query_mode = "full"

        organism.autonomous_wake_cycle()
        state = store.load_state("receiver")
        event = store.recent_events("receiver", 1)[0]
        selection = event["payload"]["self_selection"]
        task = selection["persistent_query_task"]

        rows.append(
            {
                "cycle": cycle,
                "seed": seed,
                "condition": condition,
                "dynamic_state": float(state.dynamic_state),
                "dynamic_memory": float(state.dynamic_memory),
                "dynamic_pressure": float(state.dynamic_pressure),
                "self_prediction": float(state.self_prediction),
                "self_prediction_error": float(state.self_prediction_error),
                "chosen_signal": float(selection["chosen_signal"]),
                "target_module": int(task["target_module"]),
                "target_action": float(task["target_action"]),
                "query_module": int(task["query_module"]),
                "query_accuracy": float(task["query_accuracy"]),
                "predicted_action": float(task["predicted_action"]),
                "action_accuracy": float(task["action_accuracy"]),
                "attention_mass": float(task["attention_mass"]),
                "access_strength": float(task["access_strength"]),
            }
        )

    store.conn.close()
    return rows


def paired_metrics(condition_rows, full_rows, cycles: int) -> dict[str, object]:
    full_by_cycle = {int(r["cycle"]): r for r in full_rows}

    signed_state = np.asarray(
        [
            float(condition_rows[i]["dynamic_state"])
            - float(full_by_cycle[i]["dynamic_state"])
            for i in range(cycles)
        ],
        dtype=float,
    )
    abs_state = np.abs(signed_state)
    self_prediction_delta = np.abs(
        np.asarray(
            [
                float(condition_rows[i]["self_prediction"])
                - float(full_by_cycle[i]["self_prediction"])
                for i in range(cycles)
            ],
            dtype=float,
        )
    )
    action_change = np.asarray(
        [
            int(
                float(condition_rows[i]["chosen_signal"])
                != float(full_by_cycle[i]["chosen_signal"])
            )
            for i in range(cycles)
        ],
        dtype=int,
    )
    query_change = np.asarray(
        [
            int(
                int(condition_rows[i]["query_module"])
                != int(full_by_cycle[i]["query_module"])
            )
            for i in range(cycles)
        ],
        dtype=int,
    )
    target_change = np.asarray(
        [
            int(
                int(condition_rows[i]["target_module"])
                != int(full_by_cycle[i]["target_module"])
                or float(condition_rows[i]["target_action"])
                != float(full_by_cycle[i]["target_action"])
            )
            for i in range(cycles)
        ],
        dtype=int,
    )
    accuracy_delta = np.asarray(
        [
            float(condition_rows[i]["action_accuracy"])
            - float(full_by_cycle[i]["action_accuracy"])
            for i in range(cycles)
        ],
        dtype=float,
    )

    t1 = 1 if cycles > 1 else 0
    base = abs_state[t1]
    later_max = float(abs_state[t1:].max()) if cycles > 1 else 0.0
    amplification = float(later_max / base) if base > EPS else 0.0

    return {
        "state_signed_delta_t1": float(signed_state[t1]),
        "state_abs_delta_t1": float(abs_state[t1]),
        "state_abs_delta_max_later": later_max,
        "reentry_amplification": amplification,
        "reentry_persistence_cycles": int(np.count_nonzero(abs_state[t1:] > EPS)),
        "state_divergence_auc": float(np.trapezoid(abs_state, dx=1.0)),
        "self_prediction_delta_max": float(self_prediction_delta.max()),
        "action_change_count": int(action_change.sum()),
        "action_change_rate": float(action_change.mean()),
        "post_pulse_action_change_rate": float(action_change[t1:].mean()) if cycles > 1 else 0.0,
        "query_change_count": int(query_change.sum()),
        "query_change_rate": float(query_change.mean()),
        "post_pulse_query_change_rate": float(query_change[t1:].mean()) if cycles > 1 else 0.0,
        "target_change_count": int(target_change.sum()),
        "post_pulse_target_change_rate": float(target_change[t1:].mean()) if cycles > 1 else 0.0,
        "mean_action_accuracy_delta": float(accuracy_delta.mean()),
        "post_pulse_action_accuracy_delta": float(accuracy_delta[t1:].mean()) if cycles > 1 else 0.0,
        "state_signed_delta_series": signed_state.tolist(),
        "state_abs_delta_series": abs_state.tolist(),
        "action_change_series": action_change.tolist(),
        "query_change_series": query_change.tolist(),
        "target_change_series": target_change.tolist(),
    }


def run(seed, replicates, warmup_cycles, cycles, task_weight, out):
    out.mkdir(parents=True, exist_ok=True)
    conditions = (
        "full",
        "pulse_shuffled_query",
        "pulse_zero_query",
        "persistent_shuffled_query",
    )

    rows = []
    for replicate in range(replicates):
        rep_seed = seed + replicate
        base = out / f"base_{replicate}.db"
        warmup(base, rep_seed, warmup_cycles)

        for condition in conditions:
            db = out / f"{condition}_{replicate}.db"
            shutil.copy2(base, db)
            rows.extend(
                run_arm(
                    db,
                    seed=rep_seed,
                    condition=condition,
                    task_weight=task_weight,
                    cycles=cycles,
                )
            )
            db.unlink(missing_ok=True)

        base.unlink(missing_ok=True)

    grouped = {}
    for row in rows:
        grouped.setdefault(str(row["condition"]), []).append(row)

    summary = {
        "experiment": "i5_7_recurrent_self_access",
        "seed": seed,
        "replicates": replicates,
        "warmup_cycles": warmup_cycles,
        "cycles": cycles,
        "task_weight": task_weight,
        "candidate_signals": list(CANDIDATE_SIGNALS),
        "conditions": conditions,
        "boundary": (
            "Tests recurrent causal re-entry of task-level query + attention inside "
            "PersistentOrganism. It does not establish consciousness or subjective experience."
        ),
        "endpoints": {},
    }

    for idx, condition in enumerate(conditions):
        if condition == "full":
            continue

        metrics = []
        for replicate in range(replicates):
            rep_seed = seed + replicate
            cond_rows = [r for r in grouped[condition] if int(r["seed"]) == rep_seed]
            full_rows = [r for r in grouped["full"] if int(r["seed"]) == rep_seed]
            if len(cond_rows) != cycles or len(full_rows) != cycles:
                raise RuntimeError("paired cycle records are incomplete")
            cond_rows.sort(key=lambda r: int(r["cycle"]))
            full_rows.sort(key=lambda r: int(r["cycle"]))
            metrics.append(paired_metrics(cond_rows, full_rows, cycles))

        state_t1_signed = np.asarray(
            [m["state_signed_delta_t1"] for m in metrics], dtype=float
        )

        summary["endpoints"][condition] = {
            "state_signed_delta_t1_mean": float(state_t1_signed.mean()),
            "state_signed_delta_t1_p": sign_flip(
                state_t1_signed, seed + 100 + idx
            ),
            "state_abs_delta_t1_mean": float(
                np.mean([m["state_abs_delta_t1"] for m in metrics])
            ),
            "state_abs_delta_max_later_mean": float(
                np.mean([m["state_abs_delta_max_later"] for m in metrics])
            ),
            "reentry_amplification_mean": float(
                np.mean([m["reentry_amplification"] for m in metrics])
            ),
            "reentry_persistence_cycles_mean": float(
                np.mean([m["reentry_persistence_cycles"] for m in metrics])
            ),
            "state_divergence_auc_mean": float(
                np.mean([m["state_divergence_auc"] for m in metrics])
            ),
            "self_prediction_delta_max_mean": float(
                np.mean([m["self_prediction_delta_max"] for m in metrics])
            ),
            "post_pulse_action_change_rate_mean": float(
                np.mean([m["post_pulse_action_change_rate"] for m in metrics])
            ),
            "post_pulse_query_change_rate_mean": float(
                np.mean([m["post_pulse_query_change_rate"] for m in metrics])
            ),
            "post_pulse_target_change_rate_mean": float(
                np.mean([m["post_pulse_target_change_rate"] for m in metrics])
            ),
            "post_pulse_action_accuracy_delta_mean": float(
                np.mean([m["post_pulse_action_accuracy_delta"] for m in metrics])
            ),
            "per_replicate": metrics,
        }

    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out / "runs.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261007)
    ap.add_argument("--replicates", type=int, default=24)
    ap.add_argument("--warmup", type=int, default=24)
    ap.add_argument("--cycles", type=int, default=CYCLES)
    ap.add_argument("--task-weight", type=float, default=0.35)
    ap.add_argument("--out", default="results/i5_7_recurrent_self_access")
    args = ap.parse_args()

    print(
        json.dumps(
            run(
                args.seed,
                args.replicates,
                args.warmup,
                args.cycles,
                args.task_weight,
                Path(args.out),
            ),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
