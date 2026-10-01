from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ontto.dynamics import Config as DynamicsConfig
from src.ontto.self_observer import SelfObserver
from src.ontto.self_policy import SelfPolicy

from experiments.organism_repeated_active_continuity_v78 import (
    RECOVERY_STEPS,
    apply_single_impulse,
    choose_learned_policy,
    schedule_signs,
    self_prediction_gain,
    sign_p,
    train_policy,
    train_self_observer,
    warmup_context,
)


STAGE_SCHEDULE = "triple_alternating"
STAGES = ("base", "shift_a", "shift_b", "base_return")


def shift_a_config() -> DynamicsConfig:
    return DynamicsConfig(
        relaxation=0.18,
        pressure_gain=0.95,
        cross_gain=1.25,
    )


def shift_b_config() -> DynamicsConfig:
    return DynamicsConfig(
        relaxation=0.50,
        pressure_gain=0.35,
        cross_gain=0.45,
    )


def stage_config(stage: str) -> DynamicsConfig:
    if stage in ("base", "base_return"):
        return DynamicsConfig()
    if stage == "shift_a":
        return shift_a_config()
    if stage == "shift_b":
        return shift_b_config()
    raise ValueError(f"unknown stage: {stage}")


def run_stage(
    *,
    policy: SelfPolicy,
    observer: SelfObserver,
    bridge_seed: int,
    context,
    stage: str,
    online_update: bool,
    recovery_steps: int,
) -> tuple[dict[str, object], object]:
    cfg = stage_config(stage)
    from src.ontto.bridge import DynamicStateBridge

    bridge = DynamicStateBridge(cfg, seed=bridge_seed)
    bridge_rng_context = context
    signs = schedule_signs(STAGE_SCHEDULE, seed=bridge_seed + 2000)

    event_gains: list[float] = []
    intervention_errors: list[float] = []
    first_actions: list[float] = []

    for sign in signs:
        bridge_rng_context, reference_state, target_state = apply_single_impulse(
            context=bridge_rng_context,
            sign=sign,
        )
        intervention_errors.append(
            float(abs(bridge_rng_context.state - target_state))
        )

        gains: list[float] = []
        first_action: float | None = None

        for _ in range(recovery_steps):
            signal = choose_learned_policy(
                policy,
                observer,
                state=bridge_rng_context.state,
                state_blind=False,
            )
            if first_action is None:
                first_action = float(signal)

            features, gain, next_context = self_prediction_gain(
                observer,
                bridge,
                context=bridge_rng_context,
                signal=signal,
            )

            if online_update:
                policy.observe(
                    SelfPolicy.features_for(
                        current_state=features["current_state"],
                        attractor_distance=features["attractor_distance"],
                        predicted_state=features["predicted_state"],
                        predicted_displacement=features["predicted_displacement"],
                        signal=features["signal"],
                    ),
                    gain,
                )

            bridge_rng_context = next_context
            gains.append(float(gain))

        event_gains.append(float(np.mean(gains)))
        first_actions.append(float(first_action))

    return (
        {
            "stage": stage,
            "event_1_gain": event_gains[0],
            "event_2_gain": event_gains[1],
            "event_3_gain": event_gains[2],
            "stage_gain": float(np.mean(event_gains)),
            "intervention_target_error_max": float(max(intervention_errors)),
            "first_actions": first_actions,
        },
        bridge_rng_context,
    )


def run_episode(
    *,
    observer: SelfObserver,
    policy_snapshot: dict,
    seed: int,
    online_update: bool,
    recovery_steps: int,
) -> dict[str, object]:
    from src.ontto.bridge import DynamicStateBridge

    base_bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
    context = warmup_context(base_bridge, seed=seed + 1000)
    policy = SelfPolicy.from_dict(json.loads(json.dumps(policy_snapshot)))

    stages = {}
    for index, stage in enumerate(STAGES):
        result, context = run_stage(
            policy=policy,
            observer=observer,
            bridge_seed=seed + 10000 + index * 1000,
            context=context,
            stage=stage,
            online_update=online_update,
            recovery_steps=recovery_steps,
        )
        stages[stage] = result

    return stages


def paired_stage_metrics(
    *,
    observer: SelfObserver,
    policy_snapshot: dict,
    episodes: int,
    base_seed: int,
    recovery_steps: int,
) -> dict[str, dict[str, np.ndarray]]:
    frozen_rows = []
    adaptive_rows = []

    for episode in range(episodes):
        seed = base_seed + episode
        frozen_rows.append(
            run_episode(
                observer=observer,
                policy_snapshot=policy_snapshot,
                seed=seed,
                online_update=False,
                recovery_steps=recovery_steps,
            )
        )
        adaptive_rows.append(
            run_episode(
                observer=observer,
                policy_snapshot=policy_snapshot,
                seed=seed,
                online_update=True,
                recovery_steps=recovery_steps,
            )
        )

    grouped = {}
    for stage in STAGES:
        grouped[stage] = {}
        for metric in (
            "event_1_gain",
            "event_2_gain",
            "event_3_gain",
            "stage_gain",
            "intervention_target_error_max",
        ):
            grouped[stage][f"frozen_{metric}"] = np.asarray(
                [float(row[stage][metric]) for row in frozen_rows],
                dtype=float,
            )
            grouped[stage][f"adaptive_{metric}"] = np.asarray(
                [float(row[stage][metric]) for row in adaptive_rows],
                dtype=float,
            )
    return grouped


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodes-per-condition", type=int, default=64)
    ap.add_argument("--train-episodes", type=int, default=64)
    ap.add_argument("--observer-samples", type=int, default=512)
    ap.add_argument("--recovery-steps", type=int, default=RECOVERY_STEPS)
    ap.add_argument(
        "--out",
        default="results/organism_reversible_regime_adaptation_v80",
    )
    args = ap.parse_args()

    out = Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    observer = train_self_observer(seed=80001, samples=args.observer_samples)
    initial_policy = train_policy(
        observer,
        seed=80002,
        episodes=args.train_episodes,
        recovery_steps=args.recovery_steps,
    )
    snapshot = json.loads(json.dumps(initial_policy.to_dict()))

    (out / "initial_policy.json").write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    grouped = paired_stage_metrics(
        observer=observer,
        policy_snapshot=snapshot,
        episodes=args.episodes_per_condition,
        base_seed=80010,
        recovery_steps=args.recovery_steps,
    )

    final_adaptive = grouped["base_return"]["adaptive_event_3_gain"]
    final_frozen = grouped["base_return"]["frozen_event_3_gain"]

    shift_a_adaptive = grouped["shift_a"]["adaptive_event_3_gain"]
    shift_a_frozen = grouped["shift_a"]["frozen_event_3_gain"]
    shift_b_adaptive = grouped["shift_b"]["adaptive_event_3_gain"]
    shift_b_frozen = grouped["shift_b"]["frozen_event_3_gain"]

    return_recovery_difference = float(
        np.mean(final_adaptive - final_frozen)
    )
    shift_a_difference = float(
        np.mean(shift_a_adaptive - shift_a_frozen)
    )
    shift_b_difference = float(
        np.mean(shift_b_adaptive - shift_b_frozen)
    )

    summary = {
        "experiment": "organism_reversible_regime_adaptation_v80",
        "episodes_per_condition": args.episodes_per_condition,
        "train_episodes": args.train_episodes,
        "observer_samples": args.observer_samples,
        "recovery_steps": args.recovery_steps,
        "training_schedule": "single_impulse",
        "evaluation_schedule": STAGE_SCHEDULE,
        "stages": list(STAGES),
        "policy_snapshot_shared_between_frozen_and_adaptive": True,
        "online_updates_use_only_observed_self_prediction_gain": True,
        "external_retraining_during_probe": False,
        "semantic_input_during_probe": False,
        "reversible_nonstationary_protocol": True,
        "primary_endpoint": "base_return_event_3_adaptive_minus_frozen",
        "base_return_event_3_adaptation_lift": return_recovery_difference,
        "base_return_event_3_adaptation_p": sign_p(
            final_adaptive - final_frozen,
            80071,
        ),
        "shift_a_event_3_adaptation_lift": shift_a_difference,
        "shift_a_event_3_adaptation_p": sign_p(
            shift_a_adaptive - shift_a_frozen,
            80072,
        ),
        "shift_b_event_3_adaptation_lift": shift_b_difference,
        "shift_b_event_3_adaptation_p": sign_p(
            shift_b_adaptive - shift_b_frozen,
            80073,
        ),
        "base_return_adaptive_event_3_minus_event_1": float(
            np.mean(
                grouped["base_return"]["adaptive_event_3_gain"]
                - grouped["base_return"]["adaptive_event_1_gain"]
            )
        ),
        "base_return_frozen_event_3_minus_event_1": float(
            np.mean(
                grouped["base_return"]["frozen_event_3_gain"]
                - grouped["base_return"]["frozen_event_1_gain"]
            )
        ),
        "differential_return_recovery": float(
            np.mean(
                (grouped["base_return"]["adaptive_event_3_gain"]
                 - grouped["base_return"]["adaptive_event_1_gain"])
                - (
                    grouped["base_return"]["frozen_event_3_gain"]
                    - grouped["base_return"]["frozen_event_1_gain"]
                )
            )
        ),
        "max_intervention_target_error": max(
            float(grouped[stage]["adaptive_intervention_target_error_max"].max())
            for stage in STAGES
        ),
        "conditions": {
            stage: {
                "frozen_event_1": float(
                    grouped[stage]["frozen_event_1_gain"].mean()
                ),
                "frozen_event_2": float(
                    grouped[stage]["frozen_event_2_gain"].mean()
                ),
                "frozen_event_3": float(
                    grouped[stage]["frozen_event_3_gain"].mean()
                ),
                "adaptive_event_1": float(
                    grouped[stage]["adaptive_event_1_gain"].mean()
                ),
                "adaptive_event_2": float(
                    grouped[stage]["adaptive_event_2_gain"].mean()
                ),
                "adaptive_event_3": float(
                    grouped[stage]["adaptive_event_3_gain"].mean()
                ),
                "adaptive_minus_frozen_event_3": float(
                    np.mean(
                        grouped[stage]["adaptive_event_3_gain"]
                        - grouped[stage]["frozen_event_3_gain"]
                    )
                ),
                "intervention_target_error_max": float(
                    grouped[stage]["adaptive_intervention_target_error_max"].max()
                ),
            }
            for stage in STAGES
        },
    }

    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
