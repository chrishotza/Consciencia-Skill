from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from types import MethodType

import numpy as np

from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.provider import LLMResponse
from src.ontto.storage import MemoryStore

CYCLES = 8
# CI validation marker for semantic correspondence specificity.
BASE_SELF_MODEL = "Mantengo una identidad persistente entre ciclos."


class QueryConditionedProvider:
    QUERY_RE = re.compile(r"query_module[^0-9-]*(-?\\d+)")

    def chat(self, messages, temperature=0.7):
        context = "\n".join(
            str(message.get("content", ""))
            for message in messages
            if isinstance(message, dict)
        )
        matches = self.QUERY_RE.findall(context)
        query_module = int(matches[-1]) if matches else -1

        if query_module < 0:
            self_model = BASE_SELF_MODEL
        elif query_module % 2 == 0:
            self_model = "Mantengo continuidad estable y conservo el recorrido persistente."
        else:
            self_model = "Cambio de régimen y abro una ruta futura completamente nueva."

        return LLMResponse(
            text=(
                "One-cycle correspondence probe.\n"
                "MEMORY: retain dynamic continuity.\n"
                f"SELF_MODEL: {self_model}"
            ),
            raw={"self_model": self_model, "query_module": query_module},
        )


class ScheduledSelfModelProvider:
    def __init__(self, schedule):
        self.schedule = list(schedule)
        self.index = 0

    def chat(self, messages, temperature=0.7):
        idx = min(self.index, len(self.schedule) - 1)
        self_model = self.schedule[idx]
        self.index += 1
        return LLMResponse(
            text=(
                "One-cycle correspondence replay.\n"
                "MEMORY: retain dynamic continuity.\n"
                f"SELF_MODEL: {self_model}"
            ),
            raw={"self_model": self_model, "scheduled": True},
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
    organism = PersistentOrganism(cfg, store, QueryConditionedProvider(), lambda _: None)
    for i in range(cycles):
        organism.wake_cycle(f"calibration {i}")
        organism.autonomous_wake_cycle()
    store.conn.close()


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


def run_pulse(db_path, seed, cycles):
    store = MemoryStore(db_path)
    organism = PersistentOrganism(make_cfg(seed, True), store, QueryConditionedProvider(), lambda _: None)
    original = organism._advance_dynamic
    call_index = {"value": 0}
    applied = []

    def tracked(self, signal, steps):
        idx = call_index["value"]
        if idx % 2 == 1:
            applied.append(float(signal))
        call_index["value"] += 1
        return original(signal, steps)

    organism._advance_dynamic = MethodType(tracked, organism)
    rows = []
    for cycle in range(cycles):
        organism.cfg.workspace_query_task_query_mode = "shuffled" if cycle == 0 else "full"
        organism.wake_cycle("I5.13 true correspondence probe")
        organism.autonomous_wake_cycle()
        state = store.load_state("receiver")
        event = store.recent_events("receiver", 1)[0]
        selection = event["payload"]["self_selection"]
        task = selection["persistent_query_task"]
        rows.append({
            "cycle": cycle,
            "dynamic_state": float(state.dynamic_state),
            "chosen_signal": float(selection["chosen_signal"]),
            "applied_signal": float(applied[-1]),
            "self_model": str(state.self_model),
            "query_module": int(task["query_module"]),
            "target_module": int(task["target_module"]),
        })
    store.conn.close()
    return rows, applied


def run_shifted(db_path, seed, cycles, schedule, bridge_enabled, t0_action):
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
        action = float(t0_action) if autonomous and cycle == 0 else float(signal)
        if autonomous:
            applied.append(action)
        call_index["value"] += 1
        return original(action, steps)

    organism._advance_dynamic = MethodType(tracked, organism)
    rows = []
    for cycle in range(cycles):
        organism.cfg.workspace_query_task_query_mode = "full"
        organism.wake_cycle("I5.13 one-cycle-shift control")
        organism.autonomous_wake_cycle()
        state = store.load_state("receiver")
        event = store.recent_events("receiver", 1)[0]
        selection = event["payload"]["self_selection"]
        task = selection["persistent_query_task"]
        rows.append({
            "cycle": cycle,
            "dynamic_state": float(state.dynamic_state),
            "chosen_signal": float(selection["chosen_signal"]),
            "applied_signal": float(applied[-1]),
            "self_model": str(state.self_model),
            "query_module": int(task["query_module"]),
            "target_module": int(task["target_module"]),
        })
    store.conn.close()
    return rows, applied


def metrics(pulse, shifted_on, shifted_off):
    cycles = len(pulse)
    shifted_by = {int(r["cycle"]): r for r in shifted_on}
    shifted_off_by = {int(r["cycle"]): r for r in shifted_off}
    action_change = np.asarray(
        [int(float(pulse[i]["chosen_signal"]) != float(shifted_by[i]["chosen_signal"])) for i in range(1, cycles)],
        dtype=int,
    )
    state_diff = np.abs(
        np.asarray(
            [float(pulse[i]["dynamic_state"]) - float(shifted_by[i]["dynamic_state"]) for i in range(cycles)],
            dtype=float,
        )
    )
    bridge_diff = np.abs(
        np.asarray(
            [float(shifted_by[i]["dynamic_state"]) - float(shifted_off_by[i]["dynamic_state"]) for i in range(cycles)],
            dtype=float,
        )
    )
    return {
        "future_action_change_rate": float(action_change.mean()),
        "state_auc_post": float(np.trapezoid(state_diff[1:], dx=1.0)),
        "bridge_on_off_auc_post": float(np.trapezoid(bridge_diff[1:], dx=1.0)),
        "t0_action_match": float(pulse[0]["applied_signal"]) == float(shifted_by[0]["applied_signal"]),
        "model_distribution_match": sorted(r["self_model"] for r in pulse[1:]) == sorted(r["self_model"] for r in shifted_on[1:]),
    }


def run(seed, replicates, warmup_cycles, cycles, out):
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for rep in range(replicates):
        rep_seed = seed + rep
        base = out / f"base_{rep}.db"
        warmup(base, rep_seed, warmup_cycles)

        pulse_db = out / f"pulse_{rep}.db"
        shutil.copy2(base, pulse_db)
        pulse_rows, pulse_actions = run_pulse(pulse_db, rep_seed, cycles)
        pulse_db.unlink(missing_ok=True)

        schedule = [row["self_model"] for row in pulse_rows]
        shifted_schedule = [schedule[0]] + schedule[2:] + [schedule[1]]

        on_db = out / f"shifted_on_{rep}.db"
        shutil.copy2(base, on_db)
        on_rows, _ = run_shifted(on_db, rep_seed, cycles, shifted_schedule, True, float(pulse_actions[0]))
        on_db.unlink(missing_ok=True)

        off_db = out / f"shifted_off_{rep}.db"
        shutil.copy2(base, off_db)
        off_rows, _ = run_shifted(off_db, rep_seed, cycles, shifted_schedule, False, float(pulse_actions[0]))
        off_db.unlink(missing_ok=True)

        rows.append(metrics(pulse_rows, on_rows, off_rows))
        base.unlink(missing_ok=True)

    action = np.asarray([m["future_action_change_rate"] for m in rows], dtype=float)
    state_auc = np.asarray([m["state_auc_post"] for m in rows], dtype=float)
    bridge_auc = np.asarray([m["bridge_on_off_auc_post"] for m in rows], dtype=float)

    return {
        "experiment": "i5_13_one_cycle_shift_semantic_correspondence_control",
        "seed": seed,
        "replicates": replicates,
        "warmup_cycles": warmup_cycles,
        "cycles": cycles,
        "boundary": "Tests temporal specificity of query-to-self-model correspondence. Does not establish consciousness.",
        "endpoints": {
            "future_action_change_rate_mean": float(action.mean()),
            "future_action_change_rate_p": sign_flip(action, seed + 1),
            "state_auc_post_mean": float(state_auc.mean()),
            "state_auc_post_p": sign_flip(state_auc, seed + 2),
            "bridge_on_off_auc_post_mean": float(bridge_auc.mean()),
            "bridge_on_off_auc_post_p": sign_flip(bridge_auc, seed + 3),
            "t0_action_match_rate": float(np.mean([m["t0_action_match"] for m in rows])),
            "model_distribution_match_rate": float(np.mean([m["model_distribution_match"] for m in rows])),
        },
        "per_replicate": rows,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261013)
    ap.add_argument("--replicates", type=int, default=24)
    ap.add_argument("--warmup", type=int, default=24)
    ap.add_argument("--cycles", type=int, default=CYCLES)
    ap.add_argument("--out", default="results/i5_13_one_cycle_shift_semantic_correspondence_control")
    args = ap.parse_args()
    print(json.dumps(run(args.seed, args.replicates, args.warmup, args.cycles, Path(args.out)), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
