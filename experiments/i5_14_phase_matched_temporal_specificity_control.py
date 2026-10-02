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
BASE_SCHEDULE = [
    "A — continuidad persistente.",
    "B — expansión de trayectoria.",
    "C — reorganización relacional.",
    "A — continuidad persistente.",
    "B — expansión de trayectoria.",
    "C — reorganización relacional.",
    "A — continuidad persistente.",
    "B — expansión de trayectoria.",
]

SHIFT_PLUS = [BASE_SCHEDULE[0], *BASE_SCHEDULE[2:], BASE_SCHEDULE[1]]
SHIFT_MINUS = [BASE_SCHEDULE[0], BASE_SCHEDULE[7], *BASE_SCHEDULE[1:7]]


class ScheduledSelfModelProvider:
    def __init__(self, schedule):
        self.schedule = list(schedule)
        if len(self.schedule) != CYCLES:
            raise ValueError("schedule must have exactly 8 entries")
        self.index = 0

    def chat(self, messages, temperature=0.7):
        idx = min(self.index, len(self.schedule) - 1)
        self_model = self.schedule[idx]
        self.index += 1
        return LLMResponse(
            text=(
                "Phase-matched temporal control.\n"
                "MEMORY: retain dynamic continuity.\n"
                f"SELF_MODEL: {self_model}"
            ),
            raw={"self_model": self_model, "schedule_index": idx},
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


def make_cfg(seed, bridge_enabled):
    return OrganismConfig(
        agent_id="receiver",
        dynamic_seed=seed,
        dream_every_cycles=10_000,
        event_limit=12,
        self_observer_enabled=True,
        self_selection_enabled=True,
        self_selection_policy="self_model",
        self_selection_signals=(-1.0, 1.0),
        semantic_dynamic_bridge_enabled=False,
        semantic_self_model_bridge_enabled=bridge_enabled,
        semantic_self_model_scale=1.0,
        semantic_self_model_importance=0.65,
        workspace_query_task_enabled=True,
        workspace_query_task_query_mode="full",
        workspace_query_task_attention_mode="full",
        workspace_query_task_weight=0.35,
        workspace_query_task_threshold=0.20,
        workspace_query_task_bottleneck_enabled=True,
        workspace_query_task_lesion_target=False,
    )


def warmup(db_path, seed, cycles):
    store = MemoryStore(db_path)
    cfg = OrganismConfig(
        agent_id="receiver",
        dynamic_seed=seed,
        dream_every_cycles=10_000,
        event_limit=12,
        self_observer_enabled=True,
        self_selection_enabled=False,
        semantic_dynamic_bridge_enabled=False,
        semantic_self_model_bridge_enabled=False,
        workspace_query_task_enabled=False,
    )
    organism = PersistentOrganism(
        cfg,
        store,
        ScheduledSelfModelProvider(BASE_SCHEDULE),
        lambda _: None,
    )
    for i in range(cycles):
        organism.wake_cycle(f"calibration {i}")
        organism.autonomous_wake_cycle()
    store.conn.close()


def run_condition(
    db_path,
    seed,
    schedule,
    bridge_enabled,
    forced_t0_action=None,
):
    store = MemoryStore(db_path)
    organism = PersistentOrganism(
        make_cfg(seed, bridge_enabled),
        store,
        ScheduledSelfModelProvider(schedule),
        lambda _: None,
    )
    original = organism._advance_dynamic
    call_index = {"value": 0}
    applied = []

    def tracked(self, signal, steps):
        idx = call_index["value"]
        cycle = idx // 2
        autonomous = (idx % 2) == 1
        action = (
            float(forced_t0_action)
            if autonomous and cycle == 0 and forced_t0_action is not None
            else float(signal)
        )
        if autonomous:
            applied.append(action)
        call_index["value"] += 1
        return original(action, steps)

    organism._advance_dynamic = MethodType(tracked, organism)

    rows = []
    for cycle in range(CYCLES):
        organism.wake_cycle("I5.14 phase-matched temporal control")
        organism.autonomous_wake_cycle()
        state = store.load_state("receiver")
        event = store.recent_events("receiver", 1)[0]
        selection = event["payload"]["self_selection"]
        rows.append(
            {
                "cycle": cycle,
                "dynamic_state": float(state.dynamic_state),
                "chosen_signal": float(selection["chosen_signal"]),
                "applied_signal": float(applied[-1]),
                "self_model": str(state.self_model),
            }
        )

    store.conn.close()
    return rows


def paired_metrics(base, plus, minus, plus_off):
    base_by = {int(r["cycle"]): r for r in base}
    plus_by = {int(r["cycle"]): r for r in plus}
    minus_by = {int(r["cycle"]): r for r in minus}
    off_by = {int(r["cycle"]): r for r in plus_off}

    def action_change(other):
        return float(
            np.mean(
                [
                    int(float(base_by[i]["chosen_signal"]) != float(other[i]["chosen_signal"]))
                    for i in range(1, CYCLES)
                ]
            )
        )

    def auc_state(other):
        values = np.abs(
            np.asarray(
                [
                    float(base_by[i]["dynamic_state"]) - float(other[i]["dynamic_state"])
                    for i in range(1, CYCLES)
                ],
                dtype=float,
            )
        )
        return float(np.trapezoid(values, dx=1.0))

    def auc_between(left, right):
        values = np.abs(
            np.asarray(
                [
                    float(left[i]["dynamic_state"]) - float(right[i]["dynamic_state"])
                    for i in range(1, CYCLES)
                ],
                dtype=float,
            )
        )
        return float(np.trapezoid(values, dx=1.0))

    return {
        "future_action_change_plus": action_change(plus_by),
        "future_action_change_minus": action_change(minus_by),
        "state_auc_base_plus": auc_state(plus_by),
        "state_auc_base_minus": auc_state(minus_by),
        "state_auc_plus_minus": auc_between(plus_by, minus_by),
        "bridge_on_off_auc": auc_between(plus_by, off_by),
        "t0_action_match_plus": float(base[0]["applied_signal"]) == float(plus[0]["applied_signal"]),
        "t0_action_match_minus": float(base[0]["applied_signal"]) == float(minus[0]["applied_signal"]),
        "model_distribution_match_plus": sorted(r["self_model"] for r in base[1:]) == sorted(r["self_model"] for r in plus[1:]),
        "model_distribution_match_minus": sorted(r["self_model"] for r in base[1:]) == sorted(r["self_model"] for r in minus[1:]),
        "model_distribution_match_plus_off": sorted(r["self_model"] for r in plus[1:]) == sorted(r["self_model"] for r in plus_off[1:]),
    }


def run(seed, replicates, warmup_cycles, cycles, out):
    if cycles != CYCLES:
        raise ValueError("I5.14 is declared for an 8-cycle horizon")

    out.mkdir(parents=True, exist_ok=True)
    rows = []

    for rep in range(replicates):
        rep_seed = seed + rep
        base_db = out / f"base_{rep}.db"
        warmup(base_db, rep_seed, warmup_cycles)

        base_run_db = out / f"base_run_{rep}.db"
        shutil.copy2(base_db, base_run_db)
        base_rows = run_condition(base_run_db, rep_seed, BASE_SCHEDULE, True)
        t0_action = float(base_rows[0]["applied_signal"])
        base_run_db.unlink(missing_ok=True)

        plus_db = out / f"plus_{rep}.db"
        shutil.copy2(base_db, plus_db)
        plus_rows = run_condition(plus_db, rep_seed, SHIFT_PLUS, True, t0_action)
        plus_db.unlink(missing_ok=True)

        minus_db = out / f"minus_{rep}.db"
        shutil.copy2(base_db, minus_db)
        minus_rows = run_condition(minus_db, rep_seed, SHIFT_MINUS, True, t0_action)
        minus_db.unlink(missing_ok=True)

        off_db = out / f"plus_off_{rep}.db"
        shutil.copy2(base_db, off_db)
        plus_off_rows = run_condition(off_db, rep_seed, SHIFT_PLUS, False, t0_action)
        off_db.unlink(missing_ok=True)

        rows.append(paired_metrics(base_rows, plus_rows, minus_rows, plus_off_rows))
        base_db.unlink(missing_ok=True)

    metrics = {
        name: np.asarray([row[name] for row in rows], dtype=float)
        for name in (
            "future_action_change_plus",
            "future_action_change_minus",
            "state_auc_base_plus",
            "state_auc_base_minus",
            "state_auc_plus_minus",
            "bridge_on_off_auc",
        )
    }

    result = {
        "experiment": "i5_14_phase_matched_temporal_specificity_control",
        "seed": seed,
        "replicates": replicates,
        "warmup_cycles": warmup_cycles,
        "cycles": cycles,
        "boundary": "Tests phase-matched temporal specificity under an explicit semantic sequence. Does not establish consciousness.",
        "schedules": {
            "base": BASE_SCHEDULE,
            "shift_plus_1": SHIFT_PLUS,
            "shift_minus_1": SHIFT_MINUS,
        },
        "endpoints": {
            "future_action_change_plus_mean": float(metrics["future_action_change_plus"].mean()),
            "future_action_change_plus_p": sign_flip(metrics["future_action_change_plus"], seed + 1),
            "future_action_change_minus_mean": float(metrics["future_action_change_minus"].mean()),
            "future_action_change_minus_p": sign_flip(metrics["future_action_change_minus"], seed + 2),
            "state_auc_base_plus_mean": float(metrics["state_auc_base_plus"].mean()),
            "state_auc_base_plus_p": sign_flip(metrics["state_auc_base_plus"], seed + 3),
            "state_auc_base_minus_mean": float(metrics["state_auc_base_minus"].mean()),
            "state_auc_base_minus_p": sign_flip(metrics["state_auc_base_minus"], seed + 4),
            "state_auc_plus_minus_mean": float(metrics["state_auc_plus_minus"].mean()),
            "state_auc_plus_minus_p": sign_flip(metrics["state_auc_plus_minus"], seed + 5),
            "bridge_on_off_auc_mean": float(metrics["bridge_on_off_auc"].mean()),
            "bridge_on_off_auc_p": sign_flip(metrics["bridge_on_off_auc"], seed + 6),
            "t0_action_match_plus_rate": float(np.mean([row["t0_action_match_plus"] for row in rows])),
            "t0_action_match_minus_rate": float(np.mean([row["t0_action_match_minus"] for row in rows])),
            "model_distribution_match_plus_rate": float(np.mean([row["model_distribution_match_plus"] for row in rows])),
            "model_distribution_match_minus_rate": float(np.mean([row["model_distribution_match_minus"] for row in rows])),
            "model_distribution_match_plus_off_rate": float(np.mean([row["model_distribution_match_plus_off"] for row in rows])),
        },
        "per_replicate": rows,
    }
    (out / "summary.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261014)
    ap.add_argument("--replicates", type=int, default=24)
    ap.add_argument("--warmup", type=int, default=24)
    ap.add_argument("--cycles", type=int, default=CYCLES)
    ap.add_argument("--out", default="results/i5_14_phase_matched_temporal_specificity_control")
    args = ap.parse_args()
    print(
        json.dumps(
            run(args.seed, args.replicates, args.warmup, args.cycles, Path(args.out)),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
