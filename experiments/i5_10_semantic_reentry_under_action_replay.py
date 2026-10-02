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
# CI validation marker for semantic re-entry research execution.
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
                "Semantic self-model re-entry probe.\n"
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
    replay_actions: list[float] | None = None,
) -> tuple[list[dict[str, object]], list[float]]:
    store = MemoryStore(db_path)
    organism = PersistentOrganism(
        make_cfg(seed, condition.endswith("BRIDGE_ON")),
        store,
        QueryConditionedProvider(),
        lambda _: None,
    )

    original_advance = organism._advance_dynamic
    index = {"value": 0}
    applied_actions: list[float] = []

    if "ACTION_REPLAY" in condition:
        if replay_actions is None or len(replay_actions) != cycles:
            raise ValueError("replay_actions required for replay conditions")

        def replay_advance(self, signal, steps):
            action = float(replay_actions[index["value"]])
            applied_actions.append(action)
            index["value"] += 1
            return original_advance(action, steps)

        organism._advance_dynamic = MethodType(replay_advance, organism)
    else:
        def tracked_advance(self, signal, steps):
            action = float(signal)
            applied_actions.append(action)
            index["value"] += 1
            return original_advance(action, steps)

        organism._advance_dynamic = MethodType(tracked_advance, organism)

    rows: list[dict[str, object]] = []

    for cycle in range(cycles):
        if condition == "PULSE_SHUFFLED_QUERY_BRIDGE_ON" and cycle == 0:
            organism.cfg.workspace_query_task_query_mode = "shuffled"
        else:
            organism.cfg.workspace_query_task_query_mode = "full"

        organism.wake_cycle("I5.10 semantic re-entry probe")

        state_before_action = store.load_state("receiver")
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
                "dynamic_state_pre_action": float(state_before_action.dynamic_state),
                "dynamic_state": float(state.dynamic_state),
                "dynamic_memory": float(state.dynamic_memory),
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


def metrics(pulse, replay_on, replay_off):
    cycles = len(pulse)
    on_by = {int(r["cycle"]): r for r in replay_on}
    off_by = {int(r["cycle"]): r for r in replay_off}

    state_pulse_replay = np.abs(
        np.asarray(
            [
                float(pulse[i]["dynamic_state"])
                - float(on_by[i]["dynamic_state"])
                for i in range(cycles)
            ],
            dtype=float,
        )
    )
    state_on_off = np.abs(
        np.asarray(
            [
                float(on_by[i]["dynamic_state"])
                - float(off_by[i]["dynamic_state"])
                for i in range(cycles)
            ],
            dtype=float,
        )
    )
    model_divergence = np.asarray(
        [
            int(str(pulse[i]["self_model"]) != str(on_by[i]["self_model"]))
            for i in range(cycles)
        ],
        dtype=int,
    )
    version_delta = np.abs(
        np.asarray(
            [
                int(pulse[i]["self_model_version"])
                - int(on_by[i]["self_model_version"])
                for i in range(cycles)
            ],
            dtype=float,
        )
    )
    applied_match = np.asarray(
        [
            float(pulse[i]["applied_signal"]) == float(on_by[i]["applied_signal"])
            for i in range(cycles)
        ],
        dtype=int,
    )

    post_model = model_divergence[1:] if cycles > 1 else model_divergence
    post_state = state_pulse_replay[1:] if cycles > 1 else state_pulse_replay
    on_off_post = state_on_off[1:] if cycles > 1 else state_on_off

    return {
        "self_model_divergence_rate_post": float(post_model.mean()),
        "self_model_version_delta_max": float(version_delta.max()),
        "pulse_vs_replay_state_t1": float(state_pulse_replay[1]) if cycles > 1 else float(state_pulse_replay[0]),
        "pulse_vs_replay_state_auc_post": float(np.trapezoid(post_state, dx=1.0)),
        "replay_on_vs_off_state_auc_post": float(np.trapezoid(on_off_post, dx=1.0)),
        "applied_action_exact_match": bool(np.all(applied_match == 1)),
        "pulse_models": [r["self_model"] for r in pulse],
        "replay_models": [r["self_model"] for r in replay_on],
    }


def run(seed, replicates, warmup_cycles, cycles, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    all_metrics = []
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

        replay_on_db = out / f"replay_on_{replicate}.db"
        shutil.copy2(base, replay_on_db)
        replay_on_rows, _ = run_arm(
            replay_on_db,
            seed=rep_seed,
            condition="ACTION_REPLAY_FULL_QUERY_BRIDGE_ON",
            cycles=cycles,
            replay_actions=pulse_actions,
        )
        replay_on_db.unlink(missing_ok=True)

        replay_off_db = out / f"replay_off_{replicate}.db"
        shutil.copy2(base, replay_off_db)
        replay_off_rows, _ = run_arm(
            replay_off_db,
            seed=rep_seed,
            condition="ACTION_REPLAY_FULL_QUERY_BRIDGE_OFF",
            cycles=cycles,
            replay_actions=pulse_actions,
        )
        replay_off_db.unlink(missing_ok=True)

        metric = metrics(pulse_rows, replay_on_rows, replay_off_rows)
        metric["replicate"] = replicate
        all_metrics.append(metric)

        for condition, rows in (
            ("PULSE_SHUFFLED_QUERY_BRIDGE_ON", pulse_rows),
            ("ACTION_REPLAY_FULL_QUERY_BRIDGE_ON", replay_on_rows),
            ("ACTION_REPLAY_FULL_QUERY_BRIDGE_OFF", replay_off_rows),
        ):
            all_rows.extend([{**row, "replicate": replicate, "condition": condition} for row in rows])

        base.unlink(missing_ok=True)

    state_t1 = np.asarray([m["pulse_vs_replay_state_t1"] for m in all_metrics], dtype=float)
    state_auc = np.asarray([m["pulse_vs_replay_state_auc_post"] for m in all_metrics], dtype=float)
    on_off_auc = np.asarray([m["replay_on_vs_off_state_auc_post"] for m in all_metrics], dtype=float)

    summary = {
        "experiment": "i5_10_semantic_reentry_under_action_replay",
        "seed": seed,
        "replicates": replicates,
        "warmup_cycles": warmup_cycles,
        "cycles": cycles,
        "conditions": [
            "PULSE_SHUFFLED_QUERY_BRIDGE_ON",
            "ACTION_REPLAY_FULL_QUERY_BRIDGE_ON",
            "ACTION_REPLAY_FULL_QUERY_BRIDGE_OFF",
        ],
        "boundary": (
            "Tests whether query differences can create semantic self-model differences under "
            "matched action trajectories, and whether the semantic self-model bridge re-enters dynamics."
        ),
        "endpoints": {
            "self_model_divergence_rate_post_mean": float(np.mean([m["self_model_divergence_rate_post"] for m in all_metrics])),
            "pulse_vs_replay_state_t1_mean": float(state_t1.mean()),
            "pulse_vs_replay_state_t1_p": sign_flip(state_t1, seed + 1),
            "pulse_vs_replay_state_auc_post_mean": float(state_auc.mean()),
            "pulse_vs_replay_state_auc_post_p": sign_flip(state_auc, seed + 2),
            "replay_on_vs_off_state_auc_post_mean": float(on_off_auc.mean()),
            "replay_on_vs_off_state_auc_post_p": sign_flip(on_off_auc, seed + 3),
            "applied_action_exact_match_rate": float(np.mean([m["applied_action_exact_match"] for m in all_metrics])),
            "self_model_version_delta_max_mean": float(np.mean([m["self_model_version_delta_max"] for m in all_metrics])),
        },
        "per_replicate": all_metrics,
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
    parser.add_argument("--seed", type=int, default=20261010)
    parser.add_argument("--replicates", type=int, default=24)
    parser.add_argument("--warmup", type=int, default=24)
    parser.add_argument("--cycles", type=int, default=CYCLES)
    parser.add_argument("--out", default="results/i5_10_semantic_reentry_under_action_replay")
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                seed=args.seed,
                replicates=args.replicates,
                warmup_cycles=args.warmup,
                cycles=args.cycles,
                out=Path(args.out),
            ),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
