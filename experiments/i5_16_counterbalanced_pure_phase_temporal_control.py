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

CYCLES = 15
LAGS = (-3, -2, -1, 1, 2, 3)
PERIOD = 7
PHASE_LABELS = tuple("ABCDEFG")
SEMANTIC_TEXT = {
    "A": "continuidad persistente.",
    "B": "expansión de trayectoria.",
    "C": "reorganización relacional.",
    "D": "integración contextual.",
    "E": "retención de identidad.",
    "F": "anticipación de transición.",
    "G": "cierre recurrente.",
}


def semantic_map(rotation: int) -> dict[str, str]:
    labels = list(PHASE_LABELS)
    shift = rotation % PERIOD
    return {
        label: SEMANTIC_TEXT[labels[(i + shift) % PERIOD]]
        for i, label in enumerate(labels)
    }


def build_schedule(lag: int, rotation: int = 0) -> list[str]:
    mapping = semantic_map(rotation)
    schedule: list[str] = []
    for cycle in range(CYCLES):
        phase_index = 0 if cycle == 0 else (cycle + lag) % PERIOD
        schedule.append(f"{PHASE_LABELS[phase_index]} — {mapping[PHASE_LABELS[phase_index]]}")
    return schedule


BASE_PHASE_SCHEDULE = [f"{label} — {SEMANTIC_TEXT[label]}" for label in PHASE_LABELS]
BASE_SCHEDULE = build_schedule(0, 0)
LAG_SCHEDULES = {
    lag: build_schedule(lag, 0) for lag in LAGS
}


class ScheduledSelfModelProvider:
    def __init__(self, schedule):
        self.schedule = list(schedule)
        if len(self.schedule) != CYCLES:
            raise ValueError(f"schedule must have exactly {CYCLES} entries")
        self.index = 0

    def chat(self, messages, temperature=0.7):
        idx = min(self.index, len(self.schedule) - 1)
        self_model = self.schedule[idx]
        self.index += 1
        return LLMResponse(
            text=(
                "Counterbalanced pure-phase temporal control.\n"
                "MEMORY: retain dynamic continuity.\n"
                f"SELF_MODEL: {self_model}"
            ),
            raw={"self_model": self_model, "schedule_index": idx},
        )


def sign_flip_signed(values: np.ndarray, seed: int, permutations: int = 20_000) -> float:
    values = np.asarray(values, dtype=float)
    if values.size == 0:
        return 1.0
    observed = abs(float(values.mean()))
    rng = np.random.default_rng(seed)
    signs = rng.choice((-1.0, 1.0), size=(permutations, values.size))
    null = np.abs((signs * values[None, :]).mean(axis=1))
    return float((np.count_nonzero(null >= observed) + 1) / (permutations + 1))


def make_cfg(seed: int, bridge_enabled: bool) -> OrganismConfig:
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


def warmup(db_path: Path, seed: int, cycles: int) -> None:
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
    db_path: Path,
    seed: int,
    schedule: list[str],
    bridge_enabled: bool,
    forced_t0_action: float,
) -> list[dict]:
    store = MemoryStore(db_path)
    organism = PersistentOrganism(
        make_cfg(seed, bridge_enabled),
        store,
        ScheduledSelfModelProvider(schedule),
        lambda _: None,
    )
    original = organism._advance_dynamic
    call_index = {"value": 0}
    applied: list[float] = []

    def tracked(self, signal, steps):
        idx = call_index["value"]
        cycle = idx // 2
        autonomous = (idx % 2) == 1
        action = (
            float(forced_t0_action)
            if autonomous and cycle == 0
            else float(signal)
        )
        if autonomous:
            applied.append(action)
        call_index["value"] += 1
        return original(action, steps)

    organism._advance_dynamic = MethodType(tracked, organism)

    rows: list[dict] = []
    for cycle in range(CYCLES):
        organism.wake_cycle("I5.16 counterbalanced pure-phase temporal control")
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


def metrics(base: list[dict], condition: list[dict]) -> dict:
    future = np.asarray(
        [
            float(base[i]["chosen_signal"]) != float(condition[i]["chosen_signal"])
            for i in range(1, CYCLES)
        ],
        dtype=float,
    )
    signed_state = np.asarray(
        [
            float(condition[i]["dynamic_state"]) - float(base[i]["dynamic_state"])
            for i in range(1, CYCLES)
        ],
        dtype=float,
    )
    return {
        "future_action_change_rate": float(np.mean(future)),
        "state_auc_abs": float(np.trapezoid(np.abs(signed_state), dx=1.0)),
        "state_auc_signed": float(np.trapezoid(signed_state, dx=1.0)),
        "final_state_delta_signed": float(signed_state[-1]),
        "t0_action_match": float(base[0]["applied_signal"]) == float(condition[0]["applied_signal"]),
        "model_distribution_match": sorted(r["self_model"] for r in base[1:]) == sorted(
            r["self_model"] for r in condition[1:]
        ),
    }


def run(seed: int, replicates: int, warmup_cycles: int, cycles: int, out: Path) -> dict:
    if cycles != CYCLES:
        raise ValueError(f"I5.16 uses the declared {CYCLES}-cycle horizon")
    out.mkdir(parents=True, exist_ok=True)

    per_rep: list[dict] = []
    bridge_rows = {lag: [] for lag in (-1, 1)}

    for rep in range(replicates):
        rep_seed = seed + rep
        rotation = rep % PERIOD
        base_schedule = build_schedule(0, rotation)
        base_db = out / f"base_{rep}.db"
        warmup(base_db, rep_seed, warmup_cycles)

        base_run_db = out / f"base_run_{rep}.db"
        shutil.copy2(base_db, base_run_db)
        base_rows = run_condition(base_run_db, rep_seed, base_schedule, True, 0.0)
        t0_action = float(base_rows[0]["applied_signal"])
        base_run_db.unlink(missing_ok=True)

        row = {
            "replicate": rep,
            "semantic_rotation": rotation,
        }

        for lag in LAGS:
            db = out / f"lag_{lag:+d}_{rep}.db"
            shutil.copy2(base_db, db)
            schedule = build_schedule(lag, rotation)
            rows = run_condition(db, rep_seed, schedule, True, t0_action)
            db.unlink(missing_ok=True)
            row[f"lag_{lag:+d}"] = metrics(base_rows, rows)

        for lag in (-1, 1):
            db = out / f"lag_{lag:+d}_off_{rep}.db"
            shutil.copy2(base_db, db)
            schedule = build_schedule(lag, rotation)
            rows = run_condition(db, rep_seed, schedule, False, t0_action)
            db.unlink(missing_ok=True)
            bridge_rows[lag].append(metrics(base_rows, rows))

        row["opposite_lag_signed_auc_difference"] = {
            str(k): float(
                row[f"lag_{k:+d}"]["state_auc_signed"]
                - row[f"lag_{-k:+d}"]["state_auc_signed"]
            )
            for k in (1, 2, 3)
        }
        row["opposite_lag_abs_auc_difference"] = {
            str(k): float(
                row[f"lag_{k:+d}"]["state_auc_abs"]
                - row[f"lag_{-k:+d}"]["state_auc_abs"]
            )
            for k in (1, 2, 3)
        }
        per_rep.append(row)
        base_db.unlink(missing_ok=True)

    endpoints: dict[str, dict] = {}
    for lag in LAGS:
        records = [row[f"lag_{lag:+d}"] for row in per_rep]
        signed_auc = np.asarray([r["state_auc_signed"] for r in records], dtype=float)
        final_delta = np.asarray([r["final_state_delta_signed"] for r in records], dtype=float)
        endpoints[str(lag)] = {
            "future_action_change_rate_mean": float(np.mean([r["future_action_change_rate"] for r in records])),
            "state_auc_abs_mean": float(np.mean([r["state_auc_abs"] for r in records])),
            "state_auc_signed_mean": float(np.mean(signed_auc)),
            "state_auc_signed_p": sign_flip_signed(signed_auc, seed + 100 + lag),
            "final_state_delta_signed_mean": float(np.mean(final_delta)),
            "final_state_delta_signed_p": sign_flip_signed(final_delta, seed + 200 + lag),
            "t0_action_match_rate": float(np.mean([r["t0_action_match"] for r in records])),
            "model_distribution_match_rate": float(np.mean([r["model_distribution_match"] for r in records])),
        }

    symmetry: dict[str, dict] = {}
    for k in (1, 2, 3):
        signed_delta = np.asarray(
            [row["opposite_lag_signed_auc_difference"][str(k)] for row in per_rep],
            dtype=float,
        )
        abs_delta = np.asarray(
            [row["opposite_lag_abs_auc_difference"][str(k)] for row in per_rep],
            dtype=float,
        )
        symmetry[str(k)] = {
            "plus_minus_signed_auc_difference_mean": float(np.mean(signed_delta)),
            "plus_minus_signed_auc_difference_p": sign_flip_signed(signed_delta, seed + 300 + k),
            "plus_minus_abs_auc_difference_mean": float(np.mean(abs_delta)),
            "plus_minus_abs_auc_difference_p": sign_flip_signed(abs_delta, seed + 400 + k),
        }

    bridge: dict[str, dict] = {}
    for lag in (-1, 1):
        on = [row[f"lag_{lag:+d}"]["state_auc_abs"] for row in per_rep]
        off = [m["state_auc_abs"] for m in bridge_rows[lag]]
        delta = np.asarray(on, dtype=float) - np.asarray(off, dtype=float)
        bridge[str(lag)] = {
            "on_auc_mean": float(np.mean(on)),
            "off_auc_mean": float(np.mean(off)),
            "on_minus_off_auc_mean": float(np.mean(delta)),
            "on_minus_off_auc_p": sign_flip_signed(delta, seed + 500 + lag),
        }

    result = {
        "experiment": "i5_16_counterbalanced_pure_phase_temporal_control",
        "seed": seed,
        "replicates": replicates,
        "warmup_cycles": warmup_cycles,
        "cycles": cycles,
        "lags": list(LAGS),
        "period": PERIOD,
        "phase_labels": list(PHASE_LABELS),
        "base_phase_schedule": list(PHASE_LABELS) * 2 + ["A"],
        "counterbalancing": "seven cyclic semantic-label rotations across replicates",
        "boundary": "Pure post-t0 phase shifts over a seven-state periodic sequence; does not establish consciousness.",
        "endpoints": endpoints,
        "symmetry": symmetry,
        "bridge": bridge,
        "per_replicate": per_rep,
    }
    (out / "summary.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261016)
    ap.add_argument("--replicates", type=int, default=24)
    ap.add_argument("--warmup", type=int, default=24)
    ap.add_argument("--cycles", type=int, default=CYCLES)
    ap.add_argument("--out", default="results/i5_16_counterbalanced_pure_phase_temporal_control")
    args = ap.parse_args()
    print(json.dumps(run(args.seed, args.replicates, args.warmup, args.cycles, Path(args.out)), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
