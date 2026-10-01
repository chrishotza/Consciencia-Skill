from __future__ import annotations

import argparse
import copy
import json
import shutil
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experiments.organism_dream_state_trace_v67 import (  # noqa: E402
    FRONTIER_MEMORIES,
    STABLE_MEMORIES,
    DreamTraceProvider,
    delete_semantic_surfaces,
)
from src.ontto.bridge import DynamicStateBridge  # noqa: E402
from src.ontto.dynamics import Config as DynamicsConfig  # noqa: E402
from src.ontto.organism import OrganismConfig, PersistentOrganism  # noqa: E402
from src.ontto.self_observer import SelfObserver  # noqa: E402
from src.ontto.storage import MemoryStore  # noqa: E402


CALIBRATION_SIGNALS = (-1.0, 1.0, 0.0, 1.0, -1.0, 0.0)


def paired_sign_p(values: list[float] | np.ndarray, seed: int) -> float:
    values = np.asarray(values, dtype=float)
    if not len(values):
        return 1.0
    observed = abs(float(values.mean()))
    rng = np.random.default_rng(seed)
    signs = rng.choice(np.asarray([-1.0, 1.0]), size=(20000, len(values)))
    null = np.abs((signs * values).mean(axis=1))
    return float((np.count_nonzero(null >= observed) + 1) / 20001)


def prepare_condition(path: Path, seed: int, condition: str, calibration_cycles: int):
    store = MemoryStore(path)
    cfg = OrganismConfig(
        agent_id="receiver",
        dynamic_seed=seed,
        dream_every_cycles=10_000,
        event_limit=16,
        self_observer_enabled=True,
        self_selection_enabled=False,
        semantic_dynamic_bridge_enabled=False,
        semantic_self_model_bridge_enabled=False,
        dream_semantic_bridge_enabled=True,
    )
    organism = PersistentOrganism(
        cfg,
        store,
        DreamTraceProvider(condition),
        lambda _: None,
    )

    for _ in range(calibration_cycles):
        signal = CALIBRATION_SIGNALS[organism.cycles % len(CALIBRATION_SIGNALS)]
        organism._advance_dynamic(signal, 1)
        organism.cycles += 1
        store.save_state("receiver", organism.state)

    frozen_observer = SelfObserver.from_dict(organism.self_observer.to_dict())

    memories = STABLE_MEMORIES if condition == "stable" else FRONTIER_MEMORIES
    for memory in memories:
        store.add_memory("receiver", memory, importance=0.65)

    organism.dream_cycle()
    store.conn.close()

    state = delete_semantic_surfaces(path)
    return frozen_observer, state


def self_model_action(observer: SelfObserver, state) -> tuple[float, float, float]:
    prediction = observer.predict(
        previous_state=state.dynamic_prev_state,
        state=state.dynamic_state,
        memory=0.0,
        pressure=0.0,
        last_input=0.0,
        attractor_distance=abs(state.dynamic_state),
        steps_delta=1,
    )
    predicted_change = prediction.predicted_state - state.dynamic_state
    action = float(np.clip(predicted_change, -1.0, 1.0))
    return float(prediction.predicted_state), float(predicted_change), action


def apply_action(state, action: float, seed: int) -> float:
    bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
    snap = bridge.advance(
        previous_state=state.dynamic_prev_state,
        state=state.dynamic_state,
        memory=0.0,
        pressure=0.0,
        signal=action,
        steps=1,
        step_index=state.dynamic_steps,
    )
    return float(snap.state)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--replicates", type=int, default=24)
    ap.add_argument("--calibration-cycles", type=int, default=48)
    ap.add_argument("--out", default="results/organism_self_model_action_v70")
    args = ap.parse_args()

    out = Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    action_deltas = []
    control_deltas = []
    predicted_deltas = []
    read_vs_clamped_deltas = []
    post_action_deltas = []
    swap_action_deltas = []
    observer_identical = []
    rows = []

    for replicate in range(args.replicates):
        seed = 9951 + replicate
        stable_db = out / f"stable_{replicate}.db"
        frontier_db = out / f"frontier_{replicate}.db"

        stable_observer, stable_state = prepare_condition(
            stable_db, seed, "stable", args.calibration_cycles
        )
        frontier_observer, frontier_state = prepare_condition(
            frontier_db, seed, "frontier", args.calibration_cycles
        )

        same_observer = json.dumps(
            stable_observer.to_dict(), sort_keys=True
        ) == json.dumps(frontier_observer.to_dict(), sort_keys=True)
        observer_identical.append(float(same_observer))

        stable_predicted, stable_change, stable_action = self_model_action(
            stable_observer, stable_state
        )
        frontier_predicted, frontier_change, frontier_action = self_model_action(
            frontier_observer, frontier_state
        )

        clamp_state = (stable_state.dynamic_state + frontier_state.dynamic_state) / 2.0
        stable_clamp = copy.deepcopy(stable_state)
        frontier_clamp = copy.deepcopy(frontier_state)
        stable_clamp.dynamic_state = clamp_state
        frontier_clamp.dynamic_state = clamp_state

        _, _, stable_control_action = self_model_action(
            stable_observer, stable_clamp
        )
        _, _, frontier_control_action = self_model_action(
            frontier_observer, frontier_clamp
        )

        stable_swap = copy.deepcopy(stable_state)
        stable_swap.dynamic_prev_state = frontier_state.dynamic_prev_state
        stable_swap.dynamic_state = frontier_state.dynamic_state
        frontier_swap = copy.deepcopy(frontier_state)
        frontier_swap.dynamic_prev_state = stable_state.dynamic_prev_state
        frontier_swap.dynamic_state = stable_state.dynamic_state

        _, _, stable_swap_action = self_model_action(stable_observer, stable_swap)
        _, _, frontier_swap_action = self_model_action(frontier_observer, frontier_swap)

        stable_post = apply_action(copy.deepcopy(stable_state), stable_action, seed)
        frontier_post = apply_action(copy.deepcopy(frontier_state), frontier_action, seed)
        stable_control_post = apply_action(
            copy.deepcopy(stable_state), stable_control_action, seed
        )
        frontier_control_post = apply_action(
            copy.deepcopy(frontier_state), frontier_control_action, seed
        )

        action_delta = abs(stable_action - frontier_action)
        control_delta = abs(stable_control_action - frontier_control_action)
        predicted_delta = abs(stable_predicted - frontier_predicted)
        read_vs_clamped = 0.5 * (
            abs(stable_action - stable_control_action)
            + abs(frontier_action - frontier_control_action)
        )
        post_delta = abs(stable_post - frontier_post)
        swap_delta = 0.5 * (
            abs(stable_swap_action - frontier_action)
            + abs(frontier_swap_action - stable_action)
        )

        action_deltas.append(action_delta)
        control_deltas.append(control_delta)
        predicted_deltas.append(predicted_delta)
        read_vs_clamped_deltas.append(read_vs_clamped)
        post_action_deltas.append(post_delta)
        swap_action_deltas.append(swap_delta)

        rows.append(
            {
                "replicate": replicate,
                "seed": seed,
                "observer_models_identical": bool(same_observer),
                "stable_state": float(stable_state.dynamic_state),
                "frontier_state": float(frontier_state.dynamic_state),
                "stable_predicted_state": stable_predicted,
                "frontier_predicted_state": frontier_predicted,
                "stable_action": stable_action,
                "frontier_action": frontier_action,
                "stable_control_action": stable_control_action,
                "frontier_control_action": frontier_control_action,
                "stable_swap_action": stable_swap_action,
                "frontier_swap_action": frontier_swap_action,
                "action_delta_abs": action_delta,
                "control_action_delta_abs": control_delta,
                "predicted_state_delta_abs": predicted_delta,
                "read_vs_clamped_action_delta": read_vs_clamped,
                "post_action_state_delta_abs": post_delta,
                "swap_action_error": swap_delta,
                "stable_post_state": stable_post,
                "frontier_post_state": frontier_post,
                "stable_control_post_state": stable_control_post,
                "frontier_control_post_state": frontier_control_post,
            }
        )

    action_arr = np.asarray(action_deltas, dtype=float)
    predicted_arr = np.asarray(predicted_deltas, dtype=float)
    read_clamped_arr = np.asarray(read_vs_clamped_deltas, dtype=float)
    swap_arr = np.asarray(swap_action_deltas, dtype=float)

    summary = {
        "experiment": "organism_self_model_action_v70",
        "replicates": args.replicates,
        "calibration_cycles": args.calibration_cycles,
        "semantic_ablation": True,
        "numeric_self_model_frozen_before_dream": True,
        "probe_text_input": False,
        "dream_state_action_delta_mean": float(np.mean(action_arr)),
        "dream_state_action_delta_p": paired_sign_p(action_arr, 70001),
        "predicted_state_delta_mean": float(np.mean(predicted_arr)),
        "predicted_state_delta_p": paired_sign_p(predicted_arr, 70002),
        "read_vs_clamped_action_delta_mean": float(np.mean(read_clamped_arr)),
        "read_vs_clamped_action_delta_p": paired_sign_p(
            read_clamped_arr, 70003
        ),
        "control_action_delta_mean": float(np.mean(control_deltas)),
        "swap_action_error_mean": float(np.mean(swap_arr)),
        "post_action_state_delta_abs_mean": float(np.mean(post_action_deltas)),
        "observer_models_identical_fraction": float(np.mean(observer_identical)),
        "all_memories_removed_before_probe": True,
        "self_model_text_cleared_before_probe": True,
        "numeric_self_model_frozen_before_dream": True,
        "semantic_text_input_during_probe": False,
    }

    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (out / "runs.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
