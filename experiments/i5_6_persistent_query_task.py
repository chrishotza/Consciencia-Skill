from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import numpy as np

from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.provider import LLMResponse
from src.ontto.storage import MemoryStore


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


def sign_flip(values: np.ndarray, seed: int, permutations: int = 20000) -> float:
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
        dream_every_cycles=10000,
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
    query_mode: str,
    attention_mode: str,
    bottleneck_enabled: bool,
    lesion_target: bool,
    task_weight: float,
) -> dict[str, object]:
    store = MemoryStore(db_path)
    cfg = OrganismConfig(
        agent_id="receiver",
        dynamic_seed=seed,
        dream_every_cycles=10000,
        event_limit=0,
        self_observer_enabled=True,
        self_selection_enabled=True,
        self_selection_policy="self_model",
        self_selection_signals=(-1.0, 1.0),
        workspace_enabled=False,
        workspace_selective_access_enabled=False,
        workspace_query_task_enabled=True,
        workspace_query_task_query_mode=query_mode,
        workspace_query_task_attention_mode=attention_mode,
        workspace_query_task_bottleneck_enabled=bottleneck_enabled,
        workspace_query_task_lesion_target=lesion_target,
        workspace_query_task_weight=task_weight,
        workspace_query_task_threshold=0.20,
    )
    organism = PersistentOrganism(cfg, store, FakeProvider(), lambda _: None)
    organism.autonomous_wake_cycle()
    state = store.load_state("receiver")
    event = store.recent_events("receiver", 1)[0]
    selection = event["payload"]["self_selection"]
    task = selection["persistent_query_task"]
    chosen = float(selection["chosen_signal"])
    target_action = float(task["target_action"])
    row = {
        "chosen_signal": chosen,
        "target_action": target_action,
        "task_action_accuracy": float(chosen == target_action),
        "internal_prediction_accuracy": float(task["action_accuracy"]),
        "query_module": int(task["query_module"]),
        "target_module": int(task["target_module"]),
        "query_accuracy": float(task["query_accuracy"]),
        "attention_mass": float(task["attention_mass"]),
        "access_strength": float(task["access_strength"]),
        "persistence_snapshot": {
            "target_module": state.workspace_task_target_module,
            "target_action": state.workspace_task_target_action,
            "query_module": state.workspace_task_query_module,
            "predicted_action": state.workspace_task_predicted_action,
            "action_accuracy": state.workspace_task_action_accuracy,
            "attention_mass": state.workspace_task_attention_mass,
            "access_strength": state.workspace_task_access_strength,
            "steps": state.workspace_task_steps,
        },
    }
    store.conn.close()

    restored = MemoryStore(db_path)
    restored_state = restored.load_state("receiver")
    row["persistence_equal"] = row["persistence_snapshot"] == {
        "target_module": restored_state.workspace_task_target_module,
        "target_action": restored_state.workspace_task_target_action,
        "query_module": restored_state.workspace_task_query_module,
        "predicted_action": restored_state.workspace_task_predicted_action,
        "action_accuracy": restored_state.workspace_task_action_accuracy,
        "attention_mass": restored_state.workspace_task_attention_mass,
        "access_strength": restored_state.workspace_task_access_strength,
        "steps": restored_state.workspace_task_steps,
    }
    restored.conn.close()
    return row


def run(seed: int, replicates: int, warmup_cycles: int, task_weight: float, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    controls = {
        "full": ("full", "full", True, False),
        "shuffled_query": ("shuffled", "full", True, False),
        "zero_query": ("zero", "full", True, False),
        "random_query": ("random", "full", True, False),
        "shuffled_attention": ("full", "shuffled", True, False),
        "lesion_target": ("full", "full", True, True),
        "no_bottleneck": ("full", "full", False, False),
    }
    rows = []
    for rep in range(replicates):
        rep_seed = seed + rep
        base = out / f"base_{rep}.db"
        warmup(base, rep_seed, warmup_cycles)
        for name, (query_mode, attention_mode, bottleneck, lesion) in controls.items():
            db = out / f"{name}_{rep}.db"
            shutil.copy2(base, db)
            row = run_arm(
                db,
                seed=rep_seed,
                query_mode=query_mode,
                attention_mode=attention_mode,
                bottleneck_enabled=bottleneck,
                lesion_target=lesion,
                task_weight=task_weight,
            )
            rows.append({"replicate": rep, "seed": rep_seed, "control": name, **row})
            db.unlink(missing_ok=True)
        base.unlink(missing_ok=True)

    grouped = {}
    for row in rows:
        grouped.setdefault(row["control"], []).append(row)
    full = grouped["full"]

    endpoints = {
        "full_actual_action_accuracy": float(np.mean([r["task_action_accuracy"] for r in full])),
        "full_internal_prediction_accuracy": float(np.mean([r["internal_prediction_accuracy"] for r in full])),
        "full_query_accuracy": float(np.mean([r["query_accuracy"] for r in full])),
        "full_attention_mass_mean": float(np.mean([r["attention_mass"] for r in full])),
        "full_persistence_rate": float(np.mean([r["persistence_equal"] for r in full])),
    }

    for idx, name in enumerate(controls):
        if name == "full":
            continue
        paired = np.asarray(
            [
                full[i]["task_action_accuracy"] - grouped[name][i]["task_action_accuracy"]
                for i in range(replicates)
            ],
            dtype=float,
        )
        endpoints[f"full_minus_{name}_action_accuracy"] = float(paired.mean())
        endpoints[f"full_minus_{name}_action_accuracy_p"] = sign_flip(paired, seed + 101 + idx)

        endpoints[f"{name}_query_accuracy"] = float(
            np.mean([r["query_accuracy"] for r in grouped[name]])
        )
        endpoints[f"{name}_action_change_rate"] = float(
            np.mean(
                [
                    int(grouped[name][i]["chosen_signal"] != full[i]["chosen_signal"])
                    for i in range(replicates)
                ]
            )
        )

    summary = {
        "experiment": "i5_6_persistent_query_task",
        "seed": seed,
        "replicates": replicates,
        "warmup_cycles": warmup_cycles,
        "task_weight": task_weight,
        "controls": controls,
        "endpoints": endpoints,
        "boundary": "Task-level integration of state-dependent query + attention into PersistentOrganism. It tests causal action selection under an internally generated routing task, not consciousness.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out / "runs.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261006)
    ap.add_argument("--replicates", type=int, default=24)
    ap.add_argument("--warmup", type=int, default=24)
    ap.add_argument("--task-weight", type=float, default=0.35)
    ap.add_argument("--out", default="results/i5_6_persistent_query_task")
    args = ap.parse_args()
    print(
        json.dumps(
            run(
                args.seed,
                args.replicates,
                args.warmup,
                args.task_weight,
                Path(args.out),
            ),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
