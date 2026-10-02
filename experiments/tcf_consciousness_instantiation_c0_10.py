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

from src.ontto.bridge import DynamicStateBridge
from src.ontto.dynamics import Config as DynamicsConfig
from src.ontto.self_observer import SelfObserver
from src.ontto.self_policy import SelfPolicy

from experiments.organism_repeated_active_continuity_v78 import (
    SIGNALS,
    apply_single_impulse,
    self_prediction_gain,
    sign_p,
    train_policy,
    train_self_observer,
    warmup_context,
)

PROTOCOL_VERSION = "C0.10"
PERTURBATION_SIGN = 1.0
PERTURBATION = 0.50


def observer_prediction(
    observer: SelfObserver,
    *,
    state: float,
    signal: float,
) -> float:
    prediction = observer.predict(
        previous_state=state,
        state=state,
        memory=0.0,
        pressure=0.0,
        last_input=signal,
        attractor_distance=abs(state),
        steps_delta=1,
    )
    return float(prediction.predicted_state)


def choose_action(
    policy: SelfPolicy,
    observer: SelfObserver,
    *,
    target_context,
    prediction_context,
) -> float:
    best = None
    for signal in SIGNALS:
        predicted_state = observer_prediction(
            observer,
            state=prediction_context.state,
            signal=signal,
        )
        predicted_displacement = abs(predicted_state - target_context.state)
        utility = policy.predict(
            current_state=target_context.state,
            attractor_distance=0.0,
            predicted_state=predicted_state,
            predicted_displacement=predicted_displacement,
            signal=signal,
        ).utility
        candidate = (float(utility), -abs(float(signal)), float(signal))
        if best is None or candidate > best:
            best = candidate
    assert best is not None
    return float(best[2])


def run_pair(
    observer: SelfObserver,
    policy: SelfPolicy,
    *,
    target_context,
    lag_context,
    bridge_seed: int,
) -> dict[str, float]:
    normal_action = choose_action(
        policy,
        observer,
        target_context=target_context,
        prediction_context=target_context,
    )
    lagged_action = choose_action(
        policy,
        observer,
        target_context=target_context,
        prediction_context=lag_context,
    )

    bridge_normal = DynamicStateBridge(DynamicsConfig(), seed=bridge_seed)
    bridge_lagged = DynamicStateBridge(DynamicsConfig(), seed=bridge_seed)

    _, normal_gain, normal_next = self_prediction_gain(
        observer,
        bridge_normal,
        context=target_context,
        signal=normal_action,
    )
    _, lagged_gain, lagged_next = self_prediction_gain(
        observer,
        bridge_lagged,
        context=target_context,
        signal=lagged_action,
    )

    normal_prediction = observer_prediction(
        observer,
        state=target_context.state,
        signal=normal_action,
    )
    lagged_prediction = observer_prediction(
        observer,
        state=lag_context.state,
        signal=normal_action,
    )

    return {
        "action_difference_normal_minus_lagged": float(
            normal_action - lagged_action
        ),
        "action_mismatch": float(abs(normal_action - lagged_action)),
        "gain_contrast_normal_minus_lagged": float(
            normal_gain - lagged_gain
        ),
        "normal_gain": float(normal_gain),
        "lagged_gain": float(lagged_gain),
        "state_delta_after_step_normal_minus_lagged": float(
            normal_next.state - lagged_next.state
        ),
        "state_difference_after_step": float(
            abs(normal_next.state - lagged_next.state)
        ),
        "interface_prediction_gap": float(
            abs(normal_prediction - lagged_prediction)
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=64)
    parser.add_argument("--train-episodes", type=int, default=64)
    parser.add_argument("--observer-samples", type=int, default=512)
    parser.add_argument(
        "--out",
        default="results/tcf_consciousness_instantiation_c0_10",
    )
    args = parser.parse_args()

    if args.episodes < 1:
        raise ValueError("C0.10 requires at least one evaluation episode")

    out = Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    observer = train_self_observer(seed=100001, samples=args.observer_samples)
    policy = train_policy(
        observer,
        seed=100002,
        episodes=args.train_episodes,
        recovery_steps=12,
    )

    rows = []
    intervention_errors = []

    for index in range(args.episodes):
        seed = 100010 + index
        bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
        pre_event = warmup_context(bridge, seed=seed + 1000)

        target_context, reference_state, target_state = apply_single_impulse(
            context=pre_event,
            sign=PERTURBATION_SIGN,
        )
        intervention_errors.append(
            abs(float(target_context.state) - float(target_state))
        )

        rows.append(
            run_pair(
                observer,
                policy,
                target_context=target_context,
                lag_context=pre_event,
                bridge_seed=100000 + index,
            )
        )

    arrays = {
        key: np.asarray([row[key] for row in rows], dtype=float)
        for key in rows[0]
    }

    summary = {
        "experiment": "tcf_consciousness_instantiation_c0_10",
        "protocol_version": PROTOCOL_VERSION,
        "question": (
            "Does the policy depend on the temporal alignment between the "
            "current post-intervention state and the self-observer readout?"
        ),
        "conditions": {
            "normal_interface": (
                "policy receives the observer prediction computed from the "
                "current post-intervention target state"
            ),
            "within_episode_lag": (
                "policy receives the observer prediction computed from the "
                "same episode's immediately pre-intervention state"
            ),
        },
        "matched_design": {
            "same_episode": True,
            "same_observer": True,
            "same_policy": True,
            "same_candidate_signals": True,
            "same_target_context_for_environment": True,
            "same_dynamic_bridge_seed_per_pair": True,
            "lag_is_within_episode": True,
            "external_retraining_during_probe": False,
            "semantic_input_during_probe": False,
        },
        "phenomenal_consciousness_claimed": False,
        "semantic_input_during_probe": False,
        "external_retraining_during_probe": False,
        "primary_outputs": {
            "action_difference_normal_minus_lagged": {
                "mean": float(np.mean(arrays["action_difference_normal_minus_lagged"])),
                "p": float(
                    sign_p(
                        arrays["action_difference_normal_minus_lagged"],
                        100101,
                    )
                ),
            },
            "gain_contrast_normal_minus_lagged": {
                "mean": float(np.mean(arrays["gain_contrast_normal_minus_lagged"])),
                "p": float(
                    sign_p(
                        arrays["gain_contrast_normal_minus_lagged"],
                        100102,
                    )
                ),
            },
            "state_delta_after_step_normal_minus_lagged": {
                "mean": float(
                    np.mean(
                        arrays["state_delta_after_step_normal_minus_lagged"]
                    )
                ),
                "p": float(
                    sign_p(
                        arrays["state_delta_after_step_normal_minus_lagged"],
                        100103,
                    )
                ),
            },
        },
        "secondary_outputs": {
            "normal_gain_mean": float(np.mean(arrays["normal_gain"])),
            "lagged_gain_mean": float(np.mean(arrays["lagged_gain"])),
            "action_mismatch_mean": float(
                np.mean(arrays["action_mismatch"])
            ),
            "state_difference_after_step_mean": float(
                np.mean(arrays["state_difference_after_step"])
            ),
            "interface_prediction_gap_mean": float(
                np.mean(arrays["interface_prediction_gap"])
            ),
            "intervention_target_error_max": float(
                max(intervention_errors)
            ),
        },
        "interpretation_rule": (
            "A paired difference after replacing only the observer readout "
            "with the same episode's pre-intervention readout would indicate "
            "sensitivity to temporal observer-policy alignment. This is a "
            "computational organizational result, not a demonstration of "
            "phenomenal consciousness."
        ),
        "analysis_note": (
            "All primary contrasts are signed, elementwise, and paired by "
            "episode seed. No constant-value pseudo-replication is used."
        ),
    }

    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out / "observer_snapshot.json").write_text(
        json.dumps(observer.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out / "policy_snapshot.json").write_text(
        json.dumps(policy.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
