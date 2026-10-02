from __future__ import annotations

import argparse
import json
import random
import re
import shutil
from pathlib import Path
from types import MethodType

import numpy as np

from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.provider import LLMResponse
from src.ontto.storage import MemoryStore

CYCLES = 8

BASE_SELF_MODEL = "Mantengo una identidad persistente entre ciclos."
SELF_MODEL_A = "Mantengo continuidad estable y conservo el recorrido persistente."
SELF_MODEL_B = "Cambio de régimen y abro una ruta futura completamente nueva."
QUERY_RE = re.compile(r"query_module[^0-9-]*(-?\d+)")


class QueryConditionedProvider:
    def chat(self, messages, temperature=0.7):
        context = "\n".join(
            str(message.get("content", ""))
            for message in messages
            if isinstance(message, dict)
        )
        matches = QUERY_RE.findall(context)
        query_module = int(matches[-1]) if matches else -1
        if query_module < 0:
            self_model = BASE_SELF_MODEL
        elif query_module % 2 == 0:
            self_model = SELF_MODEL_A
        else:
            self_model = SELF_MODEL_B
        return LLMResponse(
            text=(
                "Information-matched semantic control.\n"
                "MEMORY: retain dynamic continuity.\n"
                f"SELF_MODEL: {self_model}"
            ),
            raw={"query_module": query_module, "self_model": self_model},
        )


class ScheduledSelfModelProvider:
    def __init__(self, schedule: list[str]):
        self.schedule = list(schedule)
        self.index = 0

    def chat(self, messages, temperature=0.7):
        if self.index < len(self.schedule):
            self_model = self.schedule[self.index]
        else:
            self_model = self.schedule[-1]
        self.index += 1
        return LLMResponse(
            text=(
                "Information-matched semantic replay.\n"
                "MEMORY: retain dynamic continuity.\n"
                f"SELF_MODEL: {self_model}"
            ),
            raw={"scheduled": True, "self_model": self_model},
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


def run_pulse(db_path: Path, seed: int, cycles: int):
    store = MemoryStore(db_path)
    organism = PersistentOrganism(
        make_cfg(seed, True),
        store,
        QueryConditionedProvider(),
        lambda _: None,
    )
    original_advance = organism._advance_dynamic
    call_index = {"value": 0}
    applied_actions = []

    def tracked(self, signal, steps):
        idx = call_index["value"]
        if idx % 2 == 1:
            applied_actions.append(float(signal))
        call_index["value"] += 1
        return original_advance(signal, steps)

    organism._advance_dynamic = MethodType(tracked, organism)
    rows = []

    for cycle in range(cycles):
        organism.cfg.workspace_query_task_query_mode = "shuffled" if cycle == 0 else "full"
        organism.wake_cycle("I5.12 pulse")
        organism.autonomous_wake_cycle()
        state = store.load_state("receiver")
        event = store.recent_events("receiver", 1)[0]
        task = event["payload"]["self_selection"]["persistent_query_task"]
        rows.append({
            "cycle": cycle,
            "dynamic_state": float(state.dynamic_state),
            "chosen_signal": float(event["payload"]["self_selection"]["chosen_signal"]),
            "applied_signal": float(applied_actions[-1]),
            "self_model": str(state.self_model),
            "query_module": int(task["query_module"]),
            "target_module": int(task["target_module"]),
        })

    store.conn.close()
    return rows, applied_actions


def run_matched(
    db_path: Path,
    seed: int,
    cycles: int,
    schedule: list[str],
    bridge_enabled: bool,
    t0_action: float,
):
    store = MemoryStore(db_path)
    organism = PersistentOrganism(
        make_cfg(seed, bridge_enabled),
        store,
        ScheduledSelfModelProvider(schedule),
        lambda _: None,
    )
    original_advance = organism._advance_dynamic
    call_index = {"value": 0}
    applied_actions = []

    def tracked(self, signal, steps):
        idx = call_index["value"]
        cycle = idx // 2
        autonomous = (idx % 2) == 1
        action = float(t0_action) if autonomous and cycle == 0 else float(signal)
        if autonomous:
            applied_actions.append(action)
        call_index["value"] += 1
        return original_advance(action, steps)

    organism._advance_dynamic = MethodType(tracked, organism)
    rows = []

    for cycle in range(cycles):
        organism.cfg.workspace_query_task_query_mode = "full"
        organism.wake_cycle("I5.12 matched self-model control")
        organism.autonomous_wake_cycle()
        state = store.load_state("receiver")
        event = store.recent_events("receiver", 1)[0]
        task = event["payload"]["self_selection"]["persistent_query_task"]
        rows.append({
            "cycle": cycle,
            "dynamic_state": float(state.dynamic_state),
            "chosen_signal": float(event["payload"]["self_selection"]["chosen_signal"]),
            "applied_signal": float(applied_actions[-1]),
            "self_model": str(state.self_model),
            "query_module": int(task["query_module"]),
            "target_module": int(task["target_module"]),
        })

    store.conn.close()
    return rows, applied_actions


def metrics(pulse, matched_on, matched_off):
    cycles = len(pulse)
    on_by = {int(r["cycle"]): r for r in matched_on}
    off_by = {int(r["cycle"]): r for r in matched_off}

    future_action_change = np.asarray([
        int(float(pulse[i]["chosen_signal"]) != float(on_by[i]["chosen_signal"]))
        for i in range(1, cycles)
    ], dtype=int)
    state_diff = np.abs(np.asarray([
        float(pulse[i]["dynamic_state"]) - float(on_by[i]["dynamic_state"])
        for i in range(cycles)
    ], dtype=float))
    bridge_diff = np.abs(np.asarray([
        float(on_by[i]["dynamic_state"]) - float(off_by[i]["dynamic_state"])
        for i in range(cycles)
    ], dtype=float))
    t0_match = float(pulse[0]["applied_signal"]) == float(on_by[0]["applied_signal"])
    model_distribution_match = sorted(
        str(r["self_model"]) for r in pulse[1:]
    ) == sorted(
        str(r["self_model"]) for r in matched_on[1:]
    )

    return {
        "future_action_change_rate": float(future_action_change.mean()),
        "state_auc_post": float(np.trapezoid(state_diff[1:], dx=1.0)),
        "bridge_on_off_auc_post": float(np.trapezoid(bridge_diff[1:], dx=1.0)),
        "t0_action_match": bool(t0_match),
        "model_distribution_match": bool(model_distribution_match),
    }


def run(seed, replicates, warmup_cycles, cycles, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    metrics_rows = []
    all_rows = []

    for rep in range(replicates):
        rep_seed = seed + rep
        base = out / f"base_{rep}.db"
        warmup(base, rep_seed, warmup_cycles)

        pulse_db = out / f"pulse_{rep}.db"
        shutil.copy2(base, pulse_db)
        pulse_rows, pulse_actions = run_pulse(pulse_db, rep_seed, cycles)
        pulse_db.unlink(missing_ok=True)

        schedule = [r["self_model"] for r in pulse_rows]
        later = schedule[1:]
        rng = random.Random(rep_seed + 12000)
        shuffled = later[:]
        rng.shuffle(shuffled)
        matched_schedule = [schedule[0]] + shuffled

        matched_on_db = out / f"matched_on_{rep}.db"
        shutil.copy2(base, matched_on_db)
        matched_on_rows, _ = run_matched(
            matched_on_db,
            rep_seed,
            cycles,
            matched_schedule,
            True,
            float(pulse_actions[0]),
        )
        matched_on_db.unlink(missing_ok=True)

        matched_off_db = out / f"matched_off_{rep}.db"
        shutil.copy2(base, matched_off_db)
        matched_off_rows, _ = run_matched(
            matched_off_db,
            rep_seed,
            cycles,
            matched_schedule,
            False,
            float(pulse_actions[0]),
        )
        matched_off_db.unlink(missing_ok=True)

        metric = metrics(pulse_rows, matched_on_rows, matched_off_rows)
        metric["replicate"] = rep
        metrics_rows.append(metric)

        for name, rows in (
            ("PULSE_SHUFFLED_QUERY_BRIDGE_ON", pulse_rows),
            ("INFORMATION_MATCHED_SELF_MODEL_BRIDGE_ON", matched_on_rows),
            ("INFORMATION_MATCHED_SELF_MODEL_BRIDGE_OFF", matched_off_rows),
        ):
            all_rows.extend([{**row, "replicate": rep, "condition": name} for row in rows])

        base.unlink(missing_ok=True)

    action = np.asarray([m["future_action_change_rate"] for m in metrics_rows], dtype=float)
    state_auc = np.asarray([m["state_auc_post"] for m in metrics_rows], dtype=float)
    bridge_auc = np.asarray([m["bridge_on_off_auc_post"] for m in metrics_rows], dtype=float)

    summary = {
        "experiment": "i5_12_information_matched_self_model_control",
        "seed": seed,
        "replicates": replicates,
        "warmup_cycles": warmup_cycles,
        "cycles": cycles,
        "boundary": (
            "Tests specificity of query-to-self-model correspondence while preserving "
            "self-model content distribution. Does not establish consciousness."
        ),
        "endpoints": {
            "future_action_change_rate_mean": float(action.mean()),
            "future_action_change_rate_p": sign_flip(action, seed + 1),
            "state_auc_post_mean": float(state_auc.mean()),
            "state_auc_post_p": sign_flip(state_auc, seed + 2),
            "bridge_on_off_auc_post_mean": float(bridge_auc.mean()),
            "bridge_on_off_auc_post_p": sign_flip(bridge_auc, seed + 3),
            "t0_action_match_rate": float(np.mean([m["t0_action_match"] for m in metrics_rows])),
            "model_distribution_match_rate": float(np.mean([m["model_distribution_match"] for m in metrics_rows])),
        },
        "per_replicate": metrics_rows,
    }

    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "runs.json").write_text(json.dumps(all_rows, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261012)
    ap.add_argument("--replicates", type=int, default=24)
    ap.add_argument("--warmup", type=int, default=24)
    ap.add_argument("--cycles", type=int, default=CYCLES)
    ap.add_argument("--out", default="results/i5_12_information_matched_self_model_control")
    args = ap.parse_args()
    print(json.dumps(run(args.seed, args.replicates, args.warmup, args.cycles, Path(args.out)), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
