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
CANDIDATE_SIGNALS = (-1.0, 1.0)

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
            route = "SEED"
        elif query_module % 2 == 0:
            self_model = SELF_MODEL_A
            route = "CONTINUE"
        else:
            self_model = SELF_MODEL_B
            route = "EXPLORE"

        return LLMResponse(
            text=(
                "Semantic future-selection probe.\n"
                "MEMORY: retain dynamic continuity.\n"
                f"SELF_MODEL: {self_model}"
            ),
            raw={
                "fake": True,
                "query_module": query_module,
                "route": route,
                "self_model": self_model,
            },
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
        self_selection_signals=CANDIDATE_SIGNALS,
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


def run_arm(
    db_path: Path,
    *,
    seed: int,
    condition: str,
    cycles: int,
    forced_t0_action: float | None = None,
) -> tuple[list[dict[str, object]], list[float]]:
    store = MemoryStore(db_path)
    organism = PersistentOrganism(
        make_cfg(seed, condition.endswith("BRIDGE_ON")),
        store,
        QueryConditionedProvider(),
        lambda _: None,
    )

    original_advance = organism._advance_dynamic
    call_index = {"value": 0}
    applied_actions: list[float] = []

    if condition == "ACTION_MATCH_FULL_QUERY_BRIDGE_ON" or condition == "ACTION_MATCH_FULL_QUERY_BRIDGE_OFF":
        if forced_t0_action is None:
            raise ValueError("forced_t0_action required for action-match arms")

        def clamped_first_advance(self, signal, steps):
            idx = call_index["value"]
            cycle = idx // 2
            is_autonomous = (idx % 2) == 1
            if is_autonomous and cycle == 0:
                action = float(forced_t0_action)
            else:
                action = float(signal)
            if is_autonomous:
                applied_actions.append(action)
            call_index["value"] += 1
            return original_advance(action, steps)

        organism._advance_dynamic = MethodType(clamped_first_advance, organism)
    else:
        def tracked_advance(self, signal, steps):
            idx = call_index["value"]
            is_autonomous = (idx % 2) == 1
            action = float(signal)
            if is_autonomous:
                applied_actions.append(action)
            call_index["value"] += 1
            return original_advance(action, steps)

        organism._advance_dynamic = MethodType(tracked_advance, organism)

    rows = []

    for cycle in range(cycles):
        if condition == "PULSE_SHUFFLED_QUERY_BRIDGE_ON" and cycle == 0:
            organism.cfg.workspace_query_task_query_mode = "shuffled"
        else:
            organism.cfg.workspace_query_task_query_mode = "full"

        organism.wake_cycle("I5.11 semantic future-selection probe")
        state_before = store.load_state("receiver")
        wake_event = store.recent_events("receiver", 1)[0]

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
                "dynamic_state_pre_action": float(state_before.dynamic_state),
                "dynamic_state": float(state.dynamic_state),
                "chosen_signal": float(selection["chosen_signal"]),
                "applied_signal": float(applied_actions[-1]),
                "self_model": str(state.self_model),
                "self_model_version": int(state.self_model_version),
                "query_module": int(task["query_module"]),
                "target_module": int(task["target_module"]),
                "query_accuracy": float(task["query_accuracy"]),
                "semantic_self_model_bridge": wake_event["payload"].get(
                    "semantic_self_model_bridge"
                ),
            }
        )

    store.conn.close()
    return rows, applied_actions


def metrics(pulse, action_match_on, action_match_off):
    cycles = len(pulse)
    on_by = {int(r["cycle"]): r for r in action_match_on}
    off_by = {int(r["cycle"]): r for r in action_match_off}

    state_div = np.abs(
        np.asarray(
            [
                float(pulse[i]["dynamic_state"]) - float(on_by[i]["dynamic_state"])
                for i in range(cycles)
            ],
            dtype=float,
        )
    )
    state_on_off = np.abs(
        np.asarray(
            [
                float(on_by[i]["dynamic_state"]) - float(off_by[i]["dynamic_state"])
                for i in range(cycles)
            ],
            dtype=float,
        )
    )
    future_action_change = np.asarray(
        [
            int(
                float(pulse[i]["chosen_signal"])
                != float(on_by[i]["chosen_signal"])
            )
            for i in range(1, cycles)
        ],
        dtype=int,
    )
    applied_t0_match = float(pulse[0]["applied_signal"]) == float(on_by[0]["applied_signal"])
    model_div = np.asarray(
        [
            int(str(pulse[i]["self_model"]) != str(on_by[i]["self_model"]))
            for i in range(1, cycles)
        ],
        dtype=int,
    )

    state_post = state_div[1:] if cycles > 1 else state_div
    on_off_post = state_on_off[1:] if cycles > 1 else state_on_off

    return {
        "future_action_change_rate": float(future_action_change.mean()),
        "future_action_change_count": int(future_action_change.sum()),
        "state_t1_delta": float(state_div[1]) if cycles > 1 else float(state_div[0]),
        "state_auc_post": float(np.trapezoid(state_post, dx=1.0)),
        "action_match_on_vs_off_auc_post": float(np.trapezoid(on_off_post, dx=1.0)),
        "applied_t0_match": bool(applied_t0_match),
        "self_model_divergence_rate_post": float(model_div.mean()),
        "state_series": state_div.tolist(),
    }


def run(seed, replicates, warmup_cycles, cycles, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    metrics_rows = []
    all_rows = []

    for replicate in range(replicates):
        rep_seed = seed + replicate
        base = out / f"base_{replicate}.db"
        warmup(base, rep_seed, warmup_cycles)

        pulse_db = out / f"pulse_{replicate}.db"
        shutil.copy2(base, pulse_db)
        pulse_rows, pulse_actions = run_arm(
            pulse_db,
            seed=rep_seed,
            condition="PULSE_SHUFFLED_QUERY_BRIDGE_ON",
            cycles=cycles,
        )
        pulse_db.unlink(missing_ok=True)

        action_on_db = out / f"action_on_{replicate}.db"
        shutil.copy2(base, action_on_db)
        action_on_rows, _ = run_arm(
            action_on_db,
            seed=rep_seed,
            condition="ACTION_MATCH_FULL_QUERY_BRIDGE_ON",
            cycles=cycles,
            forced_t0_action=pulse_actions[0],
        )
        action_on_db.unlink(missing_ok=True)

        action_off_db = out / f"action_off_{replicate}.db"
        shutil.copy2(base, action_off_db)
        action_off_rows, _ = run_arm(
            action_off_db,
            seed=rep_seed,
            condition="ACTION_MATCH_FULL_QUERY_BRIDGE_OFF",
            cycles=cycles,
            forced_t0_action=pulse_actions[0],
        )
        action_off_db.unlink(missing_ok=True)

        metric = metrics(pulse_rows, action_on_rows, action_off_rows)
        metric["replicate"] = replicate
        metrics_rows.append(metric)

        for condition, rows in (
            ("PULSE_SHUFFLED_QUERY_BRIDGE_ON", pulse_rows),
            ("ACTION_MATCH_FULL_QUERY_BRIDGE_ON", action_on_rows),
            ("ACTION_MATCH_FULL_QUERY_BRIDGE_OFF", action_off_rows),
        ):
            all_rows.extend(
                [{**row, "replicate": replicate, "condition": condition} for row in rows]
            )

        base.unlink(missing_ok=True)

    action_change = np.asarray(
        [m["future_action_change_rate"] for m in metrics_rows],
        dtype=float,
    )
    state_t1 = np.asarray(
        [m["state_t1_delta"] for m in metrics_rows],
        dtype=float,
    )
    state_auc = np.asarray(
        [m["state_auc_post"] for m in metrics_rows],
        dtype=float,
    )
    on_off_auc = np.asarray(
        [m["action_match_on_vs_off_auc_post"] for m in metrics_rows],
        dtype=float,
    )

    summary = {
        "experiment": "i5_11_semantic_reentry_trajectory_selection",
        "seed": seed,
        "replicates": replicates,
        "warmup_cycles": warmup_cycles,
        "cycles": cycles,
        "conditions": [
            "PULSE_SHUFFLED_QUERY_BRIDGE_ON",
            "ACTION_MATCH_FULL_QUERY_BRIDGE_ON",
            "ACTION_MATCH_FULL_QUERY_BRIDGE_OFF",
        ],
        "boundary": (
            "Tests whether semantic re-entry changes future trajectory selection after "
            "the first-cycle action is matched. Does not establish consciousness."
        ),
        "endpoints": {
            "future_action_change_rate_mean": float(action_change.mean()),
            "future_action_change_rate_p": sign_flip(action_change, seed + 1),
            "state_t1_delta_mean": float(state_t1.mean()),
            "state_t1_delta_p": sign_flip(state_t1, seed + 2),
            "state_auc_post_mean": float(state_auc.mean()),
            "state_auc_post_p": sign_flip(state_auc, seed + 3),
            "action_match_on_vs_off_auc_post_mean": float(on_off_auc.mean()),
            "action_match_on_vs_off_auc_post_p": sign_flip(on_off_auc, seed + 4),
            "t0_applied_action_match_rate": float(np.mean([m["applied_t0_match"] for m in metrics_rows])),
            "self_model_divergence_rate_post_mean": float(np.mean([m["self_model_divergence_rate_post"] for m in metrics_rows])),
        },
        "per_replicate": metrics_rows,
    }

    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out / "runs.json").write_text(
        json.dumps(all_rows, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20261011)
    parser.add_argument("--replicates", type=int, default=24)
    parser.add_argument("--warmup", type=int, default=24)
    parser.add_argument("--cycles", type=int, default=CYCLES)
    parser.add_argument("--out", default="results/i5_11_semantic_reentry_trajectory_selection")
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.seed,
                args.replicates,
                args.warmup,
                args.cycles,
                Path(args.out),
            ),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
