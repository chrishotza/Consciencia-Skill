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
# CI validation marker for the research-lab execution path.
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


def make_cfg(seed: int, task_weight: float) -> OrganismConfig:
    return OrganismConfig(
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


def run_arm(
    db_path: Path,
    *,
    seed: int,
    condition: str,
    task_weight: float,
    cycles: int,
    replay_actions: list[float] | None = None,
) -> tuple[list[dict[str, object]], list[float]]:
    store = MemoryStore(db_path)
    organism = PersistentOrganism(
        make_cfg(seed, task_weight),
        store,
        FakeProvider(),
        lambda _: None,
    )

    original_advance = organism._advance_dynamic
    cycle_index = {"value": 0}
    applied_actions: list[float] = []

    if condition == "action_replay_full_query":
        if replay_actions is None or len(replay_actions) != cycles:
            raise ValueError("replay_actions must contain one action per cycle")

        def replay_advance(self, signal, steps):
            idx = cycle_index["value"]
            applied = float(replay_actions[idx])
            applied_actions.append(applied)
            cycle_index["value"] += 1
            return original_advance(applied, steps)

        organism._advance_dynamic = MethodType(replay_advance, organism)
    else:
        def tracked_advance(self, signal, steps):
            applied_actions.append(float(signal))
            cycle_index["value"] += 1
            return original_advance(signal, steps)

        organism._advance_dynamic = MethodType(tracked_advance, organism)

    rows: list[dict[str, object]] = []

    for cycle in range(cycles):
        if condition == "pulse_shuffled_query" and cycle == 0:
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
    return rows, applied_actions


def trajectory_metrics(pulse_rows, replay_rows, full_rows):
    cycles = len(pulse_rows)
    replay_by = {int(r["cycle"]): r for r in replay_rows}
    full_by = {int(r["cycle"]): r for r in full_rows}

    pulse_vs_replay = np.abs(
        np.asarray(
            [
                float(pulse_rows[i]["dynamic_state"])
                - float(replay_by[i]["dynamic_state"])
                for i in range(cycles)
            ],
            dtype=float,
        )
    )
    pulse_vs_full = np.abs(
        np.asarray(
            [
                float(pulse_rows[i]["dynamic_state"])
                - float(full_by[i]["dynamic_state"])
                for i in range(cycles)
            ],
            dtype=float,
        )
    )
    replay_vs_full = np.abs(
        np.asarray(
            [
                float(replay_by[i]["dynamic_state"])
                - float(full_by[i]["dynamic_state"])
                for i in range(cycles)
            ],
            dtype=float,
        )
    )
    applied_match = np.asarray(
        [
            float(pulse_rows[i]["applied_signal"])
            == float(replay_by[i]["applied_signal"])
            for i in range(cycles)
        ],
        dtype=int,
    )
    selected_vs_applied = np.asarray(
        [
            float(replay_by[i]["chosen_signal"])
            != float(replay_by[i]["applied_signal"])
            for i in range(cycles)
        ],
        dtype=int,
    )

    post = pulse_vs_replay[1:] if cycles > 1 else pulse_vs_replay

    return {
        "pulse_vs_replay_state_t1": float(pulse_vs_replay[1]) if cycles > 1 else float(pulse_vs_replay[0]),
        "pulse_vs_replay_auc_post": float(np.trapezoid(post, dx=1.0)),
        "pulse_vs_replay_max": float(pulse_vs_replay.max()),
        "pulse_vs_full_auc_post": float(np.trapezoid(pulse_vs_full[1:], dx=1.0)) if cycles > 1 else 0.0,
        "replay_vs_full_auc_post": float(np.trapezoid(replay_vs_full[1:], dx=1.0)) if cycles > 1 else 0.0,
        "applied_action_exact_match": bool(np.all(applied_match == 1)),
        "selected_vs_applied_rate_replay": float(selected_vs_applied.mean()),
        "pulse_vs_replay_series": pulse_vs_replay.tolist(),
        "pulse_vs_full_series": pulse_vs_full.tolist(),
        "replay_vs_full_series": replay_vs_full.tolist(),
    }


def run(seed, replicates, warmup_cycles, cycles, task_weight, out):
    out.mkdir(parents=True, exist_ok=True)
    rows_by_condition = {
        "full": [],
        "pulse_shuffled_query": [],
        "action_replay_full_query": [],
        "persistent_shuffled_query": [],
    }
    metrics = []

    for replicate in range(replicates):
        rep_seed = seed + replicate
        base = out / f"base_{replicate}.db"
        warmup(base, rep_seed, warmup_cycles)

        full_db = out / f"full_{replicate}.db"
        shutil.copy2(base, full_db)
        full_rows, _ = run_arm(
            full_db,
            seed=rep_seed,
            condition="full",
            task_weight=task_weight,
            cycles=cycles,
        )
        full_db.unlink(missing_ok=True)

        pulse_db = out / f"pulse_{replicate}.db"
        shutil.copy2(base, pulse_db)
        pulse_rows, pulse_actions = run_arm(
            pulse_db,
            seed=rep_seed,
            condition="pulse_shuffled_query",
            task_weight=task_weight,
            cycles=cycles,
        )
        pulse_db.unlink(missing_ok=True)

        replay_db = out / f"replay_{replicate}.db"
        shutil.copy2(base, replay_db)
        replay_rows, _ = run_arm(
            replay_db,
            seed=rep_seed,
            condition="action_replay_full_query",
            task_weight=task_weight,
            cycles=cycles,
            replay_actions=pulse_actions,
        )
        replay_db.unlink(missing_ok=True)

        persistent_db = out / f"persistent_{replicate}.db"
        shutil.copy2(base, persistent_db)
        persistent_rows, _ = run_arm(
            persistent_db,
            seed=rep_seed,
            condition="persistent_shuffled_query",
            task_weight=task_weight,
            cycles=cycles,
        )
        persistent_db.unlink(missing_ok=True)

        for condition, condition_rows in (
            ("full", full_rows),
            ("pulse_shuffled_query", pulse_rows),
            ("action_replay_full_query", replay_rows),
            ("persistent_shuffled_query", persistent_rows),
        ):
            rows_by_condition[condition].extend(
                [{**row, "replicate": replicate} for row in condition_rows]
            )

        metric = trajectory_metrics(pulse_rows, replay_rows, full_rows)
        metric["replicate"] = replicate
        metrics.append(metric)

        base.unlink(missing_ok=True)

    pulse_replay_t1 = np.asarray(
        [float(m["pulse_vs_replay_state_t1"]) for m in metrics], dtype=float
    )
    pulse_replay_auc = np.asarray(
        [float(m["pulse_vs_replay_auc_post"]) for m in metrics], dtype=float
    )

    summary = {
        "experiment": "i5_9_action_replay_sufficiency",
        "seed": seed,
        "replicates": replicates,
        "warmup_cycles": warmup_cycles,
        "cycles": cycles,
        "task_weight": task_weight,
        "conditions": [
            "full",
            "pulse_shuffled_query",
            "action_replay_full_query",
            "persistent_shuffled_query",
        ],
        "boundary": (
            "Tests whether the dynamic effect of a query perturbation can be reconstructed "
            "from the resulting applied action sequence. Does not establish consciousness."
        ),
        "endpoints": {
            "pulse_vs_replay_state_t1_mean": float(pulse_replay_t1.mean()),
            "pulse_vs_replay_state_t1_p": sign_flip(pulse_replay_t1, seed + 1),
            "pulse_vs_replay_auc_post_mean": float(pulse_replay_auc.mean()),
            "pulse_vs_replay_auc_post_p": sign_flip(pulse_replay_auc, seed + 2),
            "pulse_vs_replay_max_mean": float(
                np.mean([m["pulse_vs_replay_max"] for m in metrics])
            ),
            "pulse_vs_full_auc_post_mean": float(
                np.mean([m["pulse_vs_full_auc_post"] for m in metrics])
            ),
            "replay_vs_full_auc_post_mean": float(
                np.mean([m["replay_vs_full_auc_post"] for m in metrics])
            ),
            "applied_action_exact_match_rate": float(
                np.mean([m["applied_action_exact_match"] for m in metrics])
            ),
            "selected_vs_applied_rate_replay_mean": float(
                np.mean([m["selected_vs_applied_rate_replay"] for m in metrics])
            ),
        },
        "per_replicate": metrics,
    }

    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    all_rows = []
    for condition_rows in rows_by_condition.values():
        all_rows.extend(condition_rows)
    (out / "runs.json").write_text(
        json.dumps(all_rows, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261009)
    ap.add_argument("--replicates", type=int, default=24)
    ap.add_argument("--warmup", type=int, default=24)
    ap.add_argument("--cycles", type=int, default=CYCLES)
    ap.add_argument("--task-weight", type=float, default=0.35)
    ap.add_argument("--out", default="results/i5_9_action_replay_sufficiency")
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
