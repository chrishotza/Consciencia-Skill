from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from types import MethodType

import numpy as np

from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.provider import LLMResponse
from src.ontto.storage import MemoryStore

CYCLES = 8
CANDIDATE_SIGNALS = (-1.0, 1.0)


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
    full_reference_action: float | None = None,
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

    original_advance = organism._advance_dynamic
    cycle_index = {"value": 0}
    applied_actions: list[float] = []

    if condition in {"full_action_clamp", "pulse_shuffled_query_action_clamp"}:
        if full_reference_action is None:
            raise ValueError("full_reference_action is required for action-clamp arms")

        def clamped_advance(self, signal, steps):
            applied = float(full_reference_action) if cycle_index["value"] == 0 else float(signal)
            applied_actions.append(applied)
            cycle_index["value"] += 1
            return original_advance(applied, steps)

        organism._advance_dynamic = MethodType(clamped_advance, organism)
    else:
        def tracked_advance(self, signal, steps):
            applied_actions.append(float(signal))
            cycle_index["value"] += 1
            return original_advance(signal, steps)

        organism._advance_dynamic = MethodType(tracked_advance, organism)

    rows: list[dict[str, object]] = []

    for cycle in range(cycles):
        if condition in {"pulse_shuffled_query", "pulse_shuffled_query_action_clamp"} and cycle == 0:
            organism.cfg.workspace_query_task_query_mode = "shuffled"
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
                "applied_signal": float(applied_actions[-1]),
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


def metric_against_full(
    rows: list[dict[str, object]],
    full_rows: list[dict[str, object]],
) -> dict[str, object]:
    full_by_cycle = {int(r["cycle"]): r for r in full_rows}
    cycles = len(full_rows)

    abs_state = np.abs(
        np.asarray(
            [
                float(rows[i]["dynamic_state"]) - float(full_by_cycle[i]["dynamic_state"])
                for i in range(cycles)
            ],
            dtype=float,
        )
    )
    selected_change = np.asarray(
        [
            int(float(rows[i]["chosen_signal"]) != float(full_by_cycle[i]["chosen_signal"]))
            for i in range(cycles)
        ],
        dtype=int,
    )
    applied_change = np.asarray(
        [
            int(float(rows[i]["applied_signal"]) != float(full_by_cycle[i]["applied_signal"]))
            for i in range(cycles)
        ],
        dtype=int,
    )
    query_change = np.asarray(
        [
            int(int(rows[i]["query_module"]) != int(full_by_cycle[i]["query_module"]))
            for i in range(cycles)
        ],
        dtype=int,
    )
    target_change = np.asarray(
        [
            int(
                int(rows[i]["target_module"]) != int(full_by_cycle[i]["target_module"])
                or float(rows[i]["target_action"]) != float(full_by_cycle[i]["target_action"])
            )
            for i in range(cycles)
        ],
        dtype=int,
    )

    post = abs_state[1:] if cycles > 1 else abs_state
    return {
        "state_abs_delta_t1": float(abs_state[1]) if cycles > 1 else float(abs_state[0]),
        "state_divergence_auc_post": float(np.trapezoid(post, dx=1.0)),
        "state_abs_max_post": float(post.max()) if post.size else 0.0,
        "selected_action_change_rate_post": float(selected_change[1:].mean()) if cycles > 1 else float(selected_change.mean()),
        "applied_action_change_rate_post": float(applied_change[1:].mean()) if cycles > 1 else float(applied_change.mean()),
        "query_change_rate_post": float(query_change[1:].mean()) if cycles > 1 else float(query_change.mean()),
        "target_change_rate_post": float(target_change[1:].mean()) if cycles > 1 else float(target_change.mean()),
        "state_abs_series": abs_state.tolist(),
    }


def run(seed: int, replicates: int, warmup_cycles: int, cycles: int, task_weight: float, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    conditions = (
        "full",
        "full_action_clamp",
        "pulse_shuffled_query",
        "pulse_shuffled_query_action_clamp",
        "persistent_shuffled_query",
    )

    rows: list[dict[str, object]] = []

    for replicate in range(replicates):
        rep_seed = seed + replicate
        base = out / f"base_{replicate}.db"
        warmup(base, rep_seed, warmup_cycles)

        full_db = out / f"full_{replicate}.db"
        shutil.copy2(base, full_db)
        full_rows = run_arm(
            full_db,
            seed=rep_seed,
            condition="full",
            task_weight=task_weight,
            cycles=cycles,
        )
        full_reference_action = float(full_rows[0]["chosen_signal"])
        full_db.unlink(missing_ok=True)

        for condition in conditions[1:]:
            db = out / f"{condition}_{replicate}.db"
            shutil.copy2(base, db)
            rows.extend(
                [
                    {**row, "replicate": replicate}
                    for row in run_arm(
                        db,
                        seed=rep_seed,
                        condition=condition,
                        task_weight=task_weight,
                        cycles=cycles,
                        full_reference_action=full_reference_action,
                    )
                ]
            )
            db.unlink(missing_ok=True)

        rows.extend([{**row, "replicate": replicate} for row in full_rows])
        base.unlink(missing_ok=True)

    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row["condition"]), []).append(row)

    metric_cache: dict[tuple[str, int], dict[str, object]] = {}
    for condition in conditions:
        for replicate in range(replicates):
            rep_rows = sorted(
                [r for r in grouped[condition] if int(r["replicate"]) == replicate],
                key=lambda r: int(r["cycle"]),
            )
            ref_rows = sorted(
                [r for r in grouped["full"] if int(r["replicate"]) == replicate],
                key=lambda r: int(r["cycle"]),
            )
            metric_cache[(condition, replicate)] = metric_against_full(rep_rows, ref_rows)

    full_clamp_t1 = np.asarray(
        [
            metric_cache[("full_action_clamp", rep)]["state_abs_delta_t1"]
            for rep in range(replicates)
        ],
        dtype=float,
    )
    pulse_minus_clamp_t1 = np.asarray(
        [
            metric_cache[("pulse_shuffled_query", rep)]["state_abs_delta_t1"]
            - metric_cache[("pulse_shuffled_query_action_clamp", rep)]["state_abs_delta_t1"]
            for rep in range(replicates)
        ],
        dtype=float,
    )
    pulse_minus_clamp_auc = np.asarray(
        [
            metric_cache[("pulse_shuffled_query", rep)]["state_divergence_auc_post"]
            - metric_cache[("pulse_shuffled_query_action_clamp", rep)]["state_divergence_auc_post"]
            for rep in range(replicates)
        ],
        dtype=float,
    )

    summary = {
        "experiment": "i5_8_action_clamp_reentry",
        "seed": seed,
        "replicates": replicates,
        "warmup_cycles": warmup_cycles,
        "cycles": cycles,
        "task_weight": task_weight,
        "conditions": conditions,
        "boundary": (
            "Tests whether query perturbation reaches later organism state through "
            "the query -> action -> state pathway. Does not establish consciousness."
        ),
        "endpoints": {
            "full_action_clamp_state_t1_mean": float(full_clamp_t1.mean()),
            "full_action_clamp_state_t1_p": sign_flip(full_clamp_t1, seed + 1),
            "pulse_minus_clamp_state_t1_mean": float(pulse_minus_clamp_t1.mean()),
            "pulse_minus_clamp_state_t1_p": sign_flip(pulse_minus_clamp_t1, seed + 2),
            "pulse_minus_clamp_auc_mean": float(pulse_minus_clamp_auc.mean()),
            "pulse_minus_clamp_auc_p": sign_flip(pulse_minus_clamp_auc, seed + 3),
            "pulse_state_t1_mean": float(
                np.mean(
                    [
                        metric_cache[("pulse_shuffled_query", rep)]["state_abs_delta_t1"]
                        for rep in range(replicates)
                    ]
                )
            ),
            "pulse_clamp_state_t1_mean": float(
                np.mean(
                    [
                        metric_cache[("pulse_shuffled_query_action_clamp", rep)]["state_abs_delta_t1"]
                        for rep in range(replicates)
                    ]
                )
            ),
            "pulse_post_action_change_rate": float(
                np.mean(
                    [
                        metric_cache[("pulse_shuffled_query", rep)]["selected_action_change_rate_post"]
                        for rep in range(replicates)
                    ]
                )
            ),
            "pulse_clamp_post_selected_action_change_rate": float(
                np.mean(
                    [
                        metric_cache[("pulse_shuffled_query_action_clamp", rep)]["selected_action_change_rate_post"]
                        for rep in range(replicates)
                    ]
                )
            ),
            "pulse_clamp_post_applied_action_change_rate": float(
                np.mean(
                    [
                        metric_cache[("pulse_shuffled_query_action_clamp", rep)]["applied_action_change_rate_post"]
                        for rep in range(replicates)
                    ]
                )
            ),
            "pulse_post_query_change_rate": float(
                np.mean(
                    [
                        metric_cache[("pulse_shuffled_query", rep)]["query_change_rate_post"]
                        for rep in range(replicates)
                    ]
                )
            ),
            "pulse_clamp_post_query_change_rate": float(
                np.mean(
                    [
                        metric_cache[("pulse_shuffled_query_action_clamp", rep)]["query_change_rate_post"]
                        for rep in range(replicates)
                    ]
                )
            ),
            "pulse_post_target_change_rate": float(
                np.mean(
                    [
                        metric_cache[("pulse_shuffled_query", rep)]["target_change_rate_post"]
                        for rep in range(replicates)
                    ]
                )
            ),
            "pulse_clamp_post_target_change_rate": float(
                np.mean(
                    [
                        metric_cache[("pulse_shuffled_query_action_clamp", rep)]["target_change_rate_post"]
                        for rep in range(replicates)
                    ]
                )
            ),
        },
        "per_replicate": {
            condition: {
                str(rep): metric_cache[(condition, rep)]
                for rep in range(replicates)
            }
            for condition in conditions
        },
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
    ap.add_argument("--seed", type=int, default=20261008)
    ap.add_argument("--replicates", type=int, default=24)
    ap.add_argument("--warmup", type=int, default=24)
    ap.add_argument("--cycles", type=int, default=CYCLES)
    ap.add_argument("--task-weight", type=float, default=0.35)
    ap.add_argument("--out", default="results/i5_8_action_clamp_reentry")
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
