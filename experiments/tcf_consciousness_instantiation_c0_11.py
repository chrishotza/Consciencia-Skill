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


PROTOCOL_VERSION = "C0.11"


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
    context,
) -> float:
    best = None
    for signal in SIGNALS:
        predicted_state = observer_prediction(
            observer,
            state=context.state,
            signal=signal,
        )
        predicted_displacement = abs(predicted_state - context.state)
        utility = policy.predict(
            current_state=context.state,
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


def counterfactual_action(factual_action: float) -> float:
    alternatives = [signal for signal in SIGNALS if signal != factual_action]
    if factual_action != 0.0:
        preferred = -factual_action
        if preferred in alternatives:
            return float(preferred)
    return float(alternatives[0])


def run_pair(
    observer: SelfObserver,
    policy: SelfPolicy,
    *,
    context,
    bridge_seed: int,
) -> dict[str, float]:
    factual_action = choose_action(policy, observer, context=context)
    forced_action = counterfactual_action(factual_action)

    factual_bridge = DynamicStateBridge(DynamicsConfig(), seed=bridge_seed)
    forced_bridge = DynamicStateBridge(DynamicsConfig(), seed=bridge_seed)

    _, factual_gain, factual_next = self_prediction_gain(
        observer,
        factual_bridge,
        context=context,
        signal=factual_action,
    )
    _, forced_gain, forced_next = self_prediction_gain(
        observer,
        forced_bridge,
        context=context,
        signal=forced_action,
    )

    factual_second_action = choose_action(
        policy,
        observer,
        context=factual_next,
    )
    forced_second_action = choose_action(
        policy,
        observer,
        context=forced_next,
    )

    return {
        "factual_first_action": float(factual_action),
        "forced_first_action": float(forced_action),
        "first_action_difference": float(
            factual_action - forced_action
        ),
        "factual_gain": float(factual_gain),
        "forced_gain": float(forced_gain),
        "gain_difference": float(factual_gain - forced_gain),
        "factual_next_action": float(factual_second_action),
        "forced_next_action": float(forced_second_action),
        "next_action_difference": float(
            factual_second_action - forced_second_action
        ),
        "next_action_mismatch": float(
            abs(factual_second_action - forced_second_action)
        ),
        "next_state_difference": float(
            factual_next.state - forced_next.state
        ),
        "next_state_abs_difference": float(
            abs(factual_next.state - forced_next.state)
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=64)
    parser.add_argument("--train-episodes", type=int, default=64)
    parser.add_argument("--observer-samples", type=int, default=512)
    parser.add_argument(
        "--out",
        default="results/tcf_consciousness_instantiation_c0_11",
    )
    args = parser.parse_args()

    out = Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    observer = train_self_observer(seed=110001, samples=args.observer_samples)
    policy = train_policy(
        observer,
        seed=110002,
        episodes=args.train_episodes,
        recovery_steps=12,
    )

    rows = []
    intervention_errors = []

    for index in range(args.episodes):
        seed = 110010 + index
        bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
        pre_event = warmup_context(bridge, seed=seed + 1000)
        target_context, _, target_state = apply_single_impulse(
            context=pre_event,
            sign=1.0,
        )
        intervention_errors.append(
            abs(float(target_context.state) - float(target_state))
        )
        rows.append(
            run_pair(
                observer,
                policy,
                context=target_context,
                bridge_seed=210000 + index,
            )
        )

    arrays = {
        key: np.asarray([row[key] for row in rows], dtype=float)
        for key in rows[0]
    }

    summary = {
        "experiment": "tcf_consciousness_instantiation_c0_11",
        "protocol_version": PROTOCOL_VERSION,
        "question": (
            "Does an externally intervened action alter the next self-state "
            "and thereby the next policy action when the observer and policy "
            "remain fixed?"
        ),
        "conditions": {
            "factual": "the trained policy chooses the first action",
            "forced_counterfactual": (
                "the first action is replaced after the policy choice by a "
                "different candidate signal; the observer and policy are unchanged"
            ),
        },
        "matched_design": {
            "same_episode_context": True,
            "same_observer": True,
            "same_policy": True,
            "same_initial_target_state": True,
            "same_dynamic_seed_per_pair": True,
            "same_candidate_signal_set": True,
            "action_intervention_only": True,
            "observer_and_policy_lesion": False,
            "external_retraining_during_probe": False,
            "semantic_input_during_probe": False,
        },
        "phenomenal_consciousness_claimed": False,
        "primary_outputs": {
            "next_action_difference_factual_minus_forced": {
                "mean": float(np.mean(arrays["next_action_difference"])),
                "p": float(
                    sign_p(
                        arrays["next_action_difference"],
                        110101,
                    )
                ),
            },
            "next_state_difference_factual_minus_forced": {
                "mean": float(np.mean(arrays["next_state_difference"])),
                "p": float(
                    sign_p(
                        arrays["next_state_difference"],
                        110102,
                    )
                ),
            },
            "gain_difference_factual_minus_forced": {
                "mean": float(np.mean(arrays["gain_difference"])),
                "p": float(
                    sign_p(
                        arrays["gain_difference"],
                        110103,
                    )
                ),
            },
        },
        "secondary_outputs": {
            "first_action_difference_mean": float(
                np.mean(arrays["first_action_difference"])
            ),
            "next_action_mismatch_mean": float(
                np.mean(arrays["next_action_mismatch"])
            ),
            "next_state_abs_difference_mean": float(
                np.mean(arrays["next_state_abs_difference"])
            ),
            "factual_gain_mean": float(
                np.mean(arrays["factual_gain"])
            ),
            "forced_gain_mean": float(
                np.mean(arrays["forced_gain"])
            ),
            "intervention_target_error_max": float(
                max(intervention_errors)
            ),
        },
        "causal_chain": (
            "first-action intervention -> changed internal state -> "
            "same observer/policy readout -> second action"
        ),
        "interpretation_rule": (
            "A paired difference in second action after intervening only on "
            "the first action supports causal mediation through the organism's "
            "internal dynamics under this protocol. It is not evidence of "
            "phenomenal consciousness."
        ),
        "analysis_note": (
            "All primary contrasts are signed, elementwise, and paired by "
            "episode. No constant-value pseudo-replication is used."
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
