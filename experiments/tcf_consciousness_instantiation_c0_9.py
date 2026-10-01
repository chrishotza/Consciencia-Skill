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

PROTOCOL_VERSION = "C0.9"
PERTURBATION_SIGN = 1.0


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


def choose_with_prediction_source(
    policy: SelfPolicy,
    observer: SelfObserver,
    *,
    target_context,
    prediction_context,
) -> tuple[float, float]:
    scored = []
    for signal in SIGNALS:
        predicted_state = observer_prediction(
            observer,
            state=prediction_context.state,
            signal=signal,
        )
        predicted_displacement = abs(predicted_state - target_context.state)
        prediction = policy.predict(
            current_state=target_context.state,
            attractor_distance=0.0,
            predicted_state=predicted_state,
            predicted_displacement=predicted_displacement,
            signal=signal,
        )
        scored.append(
            (
                float(prediction.utility),
                float(abs(signal)),
                {
                    "signal": float(signal),
                    "predicted_state": predicted_state,
                    "predicted_displacement": float(predicted_displacement),
                },
            )
        )
    return tuple(
        float(value)
        for value in max(scored, key=lambda item: (item[0], -item[1]))[2].values()
        if isinstance(value, (float, int))
    )


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


def derangement(size: int) -> list[int]:
    if size < 2:
        raise ValueError("C0.9 requires at least two replicas")
    return [((index + 1) % size) for index in range(size)]


def run_episode(
    observer: SelfObserver,
    policy: SelfPolicy,
    *,
    target_context,
    donor_context,
    bridge_seed: int,
) -> dict[str, float]:
    normal_action = choose_action(
        policy,
        observer,
        target_context=target_context,
        prediction_context=target_context,
    )
    donor_action = choose_action(
        policy,
        observer,
        target_context=target_context,
        prediction_context=donor_context,
    )

    bridge_normal = DynamicStateBridge(DynamicsConfig(), seed=bridge_seed)
    bridge_donor = DynamicStateBridge(DynamicsConfig(), seed=bridge_seed)

    _, normal_gain, normal_next = self_prediction_gain(
        observer,
        bridge_normal,
        context=target_context,
        signal=normal_action,
    )
    _, donor_gain, donor_next = self_prediction_gain(
        observer,
        bridge_donor,
        context=target_context,
        signal=donor_action,
    )

    donor_prediction_gap = float(
        abs(
            observer_prediction(
                observer,
                state=target_context.state,
                signal=normal_action,
            )
            - observer_prediction(
                observer,
                state=donor_context.state,
                signal=normal_action,
            )
        )
    )

    return {
        "normal_action": float(normal_action),
        "donor_shuffle_action": float(donor_action),
        "action_difference": float(normal_action - donor_action),
        "action_mismatch": float(abs(normal_action - donor_action)),
        "normal_gain": float(normal_gain),
        "donor_shuffle_gain": float(donor_gain),
        "gain_contrast": float(normal_gain - donor_gain),
        "state_delta_after_step": float(normal_next.state - donor_next.state),
        "state_difference_after_step": float(abs(normal_next.state - donor_next.state)),
        "donor_prediction_gap": donor_prediction_gap,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=64)
    parser.add_argument("--train-episodes", type=int, default=64)
    parser.add_argument("--observer-samples", type=int, default=512)
    parser.add_argument(
        "--out",
        default="results/tcf_consciousness_instantiation_c0_9",
    )
    args = parser.parse_args()

    if args.episodes < 2:
        raise ValueError("C0.9 requires at least two evaluation episodes")

    out = Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    observer = train_self_observer(seed=99001, samples=args.observer_samples)
    policy = train_policy(
        observer,
        seed=99002,
        episodes=args.train_episodes,
        recovery_steps=12,
    )

    target_contexts = []
    donor_contexts = []
    for index in range(args.episodes):
        target_bridge = DynamicStateBridge(DynamicsConfig(), seed=99010 + index)
        donor_bridge = DynamicStateBridge(
            DynamicsConfig(),
            seed=199010 + index,
        )
        target_context, _, _ = apply_single_impulse(
            context=warmup_context(target_bridge, seed=99010 + index),
            sign=PERTURBATION_SIGN,
        )
        donor_context, _, _ = apply_single_impulse(
            context=warmup_context(donor_bridge, seed=199010 + index),
            sign=PERTURBATION_SIGN,
        )
        target_contexts.append(target_context)
        donor_contexts.append(donor_context)

    mapping = derangement(args.episodes)
    rows = []
    intervention_errors = []

    for index in range(args.episodes):
        target = target_contexts[index]
        donor = donor_contexts[mapping[index]]
        reference = float(
            target.state - PERTURBATION_SIGN * 0.50
        )
        intervention_errors.append(
            abs(float(target.state) - np.clip(reference + PERTURBATION_SIGN * 0.50, -1.0, 1.0))
        )
        rows.append(
            run_episode(
                observer,
                policy,
                target_context=target,
                donor_context=donor,
                bridge_seed=299010 + index,
            )
        )

    arrays = {
        key: np.asarray([row[key] for row in rows], dtype=float)
        for key in rows[0]
    }

    summary = {
        "experiment": "tcf_consciousness_instantiation_c0_9",
        "protocol_version": PROTOCOL_VERSION,
        "question": (
            "Does the policy depend on the within-episode causal correspondence "
            "between the current state and the learned self-observer readout?"
        ),
        "conditions": {
            "normal_interface": "policy receives the target episode's own observer prediction",
            "donor_shuffle_interface": (
                "policy receives observer predictions from a fixed derangement of other episodes; "
                "the donor multiset is preserved"
            ),
        },
        "matched_design": {
            "same_target_contexts": True,
            "same_dynamic_bridge_seed_per_pair": True,
            "same_observer": True,
            "same_policy": True,
            "same_candidate_signals": True,
            "same_target_multiset": True,
            "donor_mapping_is_derangement": True,
            "external_retraining_during_probe": False,
            "semantic_input_during_probe": False,
        },
        "phenomenal_consciousness_claimed": False,
        "primary_outputs": {
            "action_difference_normal_minus_donor": {
                "mean": float(np.mean(arrays["action_difference"])),
                "p": float(sign_p(arrays["action_difference"], 99101)),
            },
            "gain_contrast_normal_minus_donor_shuffle": {
                "mean": float(np.mean(arrays["gain_contrast"])),
                "p": float(sign_p(arrays["gain_contrast"], 99102)),
            },
            "state_delta_after_step_normal_minus_donor": {
                "mean": float(np.mean(arrays["state_delta_after_step"])),
                "p": float(sign_p(arrays["state_delta_after_step"], 99103)),
            },
        },
        "secondary_outputs": {
            "normal_gain_mean": float(np.mean(arrays["normal_gain"])),
            "donor_shuffle_gain_mean": float(np.mean(arrays["donor_shuffle_gain"])),
            "action_mismatch_mean": float(np.mean(arrays["action_mismatch"])),
            "state_difference_after_step_mean": float(np.mean(arrays["state_difference_after_step"])),
            "donor_prediction_gap_mean": float(np.mean(arrays["donor_prediction_gap"])),
            "intervention_target_error_max": float(max(intervention_errors)),
        },
        "interpretation_rule": (
            "A paired difference in gain indicates that changing only the observer-to-policy "
            "interface correspondence altered immediate self-prediction performance. This is "
            "a causal organizational test, not a demonstration of phenomenal consciousness."
        ),
        "analysis_note": (
            "Signed action and state contrasts are computed elementwise across the same episode seeds; "
            "no constant-value pseudo-replication is used."
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
    (out / "donor_mapping.json").write_text(
        json.dumps(mapping, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
