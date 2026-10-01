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
    RECOVERY_STEPS,
    SIGNALS,
    apply_single_impulse,
    candidate_features,
    self_prediction_gain,
    sign_p,
    train_policy,
    train_self_observer,
    warmup_context,
)
from experiments.tcf_consciousness_instantiation_c0 import choose_action


PROTOCOL_VERSION = "C0.6"
LESION_STEPS = 6


def clone_observer(observer: SelfObserver) -> SelfObserver:
    return SelfObserver.from_dict(json.loads(json.dumps(observer.to_dict())))


def clone_policy(policy: SelfPolicy) -> SelfPolicy:
    return SelfPolicy.from_dict(json.loads(json.dumps(policy.to_dict())))


def lesion_observer(observer: SelfObserver) -> SelfObserver:
    lesioned = clone_observer(observer)
    lesioned.reset()
    return lesioned


def lesion_policy(policy: SelfPolicy) -> SelfPolicy:
    lesioned = clone_policy(policy)
    lesioned.features.clear()
    lesioned.targets.clear()
    return lesioned


def run_recovery(
    *,
    observer: SelfObserver,
    policy: SelfPolicy,
    context,
    bridge_seed: int,
    steps: int,
) -> dict[str, float]:
    bridge = DynamicStateBridge(DynamicsConfig(), seed=bridge_seed)
    gains: list[float] = []
    states = [float(context.state)]
    actions: list[float] = []

    for _ in range(steps):
        signal = choose_action(
            policy,
            observer,
            context=context,
            state_blind=False,
            open_loop=False,
        )
        _, gain, context = self_prediction_gain(
            observer,
            bridge,
            context=context,
            signal=signal,
        )
        actions.append(float(signal))
        gains.append(float(gain))
        states.append(float(context.state))

    return {
        "mean_gain": float(np.mean(gains)),
        "final_state_distance": float(abs(states[-1])),
        "state_variance": float(np.var(np.asarray(states, dtype=float))),
        "mean_abs_action": float(np.mean(np.abs(np.asarray(actions, dtype=float)))),
    }


def run_rescue(
    *,
    observer_full: SelfObserver,
    policy_full: SelfPolicy,
    observer_lesioned: SelfObserver,
    policy_lesioned: SelfPolicy,
    context,
    bridge_seed: int,
    lesion_kind: str,
) -> dict[str, float]:
    bridge = DynamicStateBridge(DynamicsConfig(), seed=bridge_seed)
    gains: list[float] = []
    states = [float(context.state)]

    for step in range(RECOVERY_STEPS):
        if step < LESION_STEPS:
            observer = observer_lesioned if lesion_kind == "observer" else observer_full
            policy = policy_lesioned if lesion_kind == "policy" else policy_full
        else:
            observer = observer_full
            policy = policy_full

        signal = choose_action(
            policy,
            observer,
            context=context,
            state_blind=False,
            open_loop=False,
        )
        _, gain, context = self_prediction_gain(
            observer,
            bridge,
            context=context,
            signal=signal,
        )
        gains.append(float(gain))
        states.append(float(context.state))

    return {
        "early_gain": float(np.mean(gains[:LESION_STEPS])),
        "late_gain": float(np.mean(gains[LESION_STEPS:])),
        "late_lift_vs_lesion": 0.0,
        "final_state_distance": float(abs(states[-1])),
        "state_variance": float(np.var(np.asarray(states, dtype=float))),
    }


def episode(
    *,
    observer: SelfObserver,
    policy: SelfPolicy,
    seed: int,
) -> dict[str, float]:
    warm_bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
    context = warmup_context(warm_bridge, seed=seed + 1000)

    intervention_context, _, target_state = apply_single_impulse(
        context=context,
        sign=1.0,
    )
    intervention_error = float(
        abs(intervention_context.state - target_state)
    )

    obs_lesion = lesion_observer(observer)
    pol_lesion = lesion_policy(policy)
    both_obs = obs_lesion
    both_pol = pol_lesion

    full = run_recovery(
        observer=observer,
        policy=policy,
        context=intervention_context,
        bridge_seed=seed + 2000,
        steps=RECOVERY_STEPS,
    )
    observer_only = run_recovery(
        observer=obs_lesion,
        policy=clone_policy(policy),
        context=intervention_context,
        bridge_seed=seed + 2000,
        steps=RECOVERY_STEPS,
    )
    policy_only = run_recovery(
        observer=clone_observer(observer),
        policy=pol_lesion,
        context=intervention_context,
        bridge_seed=seed + 2000,
        steps=RECOVERY_STEPS,
    )
    both = run_recovery(
        observer=both_obs,
        policy=both_pol,
        context=intervention_context,
        bridge_seed=seed + 2000,
        steps=RECOVERY_STEPS,
    )

    observer_rescue = run_rescue(
        observer_full=observer,
        policy_full=policy,
        observer_lesioned=obs_lesion,
        policy_lesioned=clone_policy(policy),
        context=intervention_context,
        bridge_seed=seed + 2000,
        lesion_kind="observer",
    )
    policy_rescue = run_rescue(
        observer_full=observer,
        policy_full=policy,
        observer_lesioned=clone_observer(observer),
        policy_lesioned=pol_lesion,
        context=intervention_context,
        bridge_seed=seed + 2000,
        lesion_kind="policy",
    )

    return {
        "full_gain": full["mean_gain"],
        "observer_lesion_gain": observer_only["mean_gain"],
        "policy_lesion_gain": policy_only["mean_gain"],
        "both_lesion_gain": both["mean_gain"],
        "full_final_distance": full["final_state_distance"],
        "observer_lesion_final_distance": observer_only["final_state_distance"],
        "policy_lesion_final_distance": policy_only["final_state_distance"],
        "both_lesion_final_distance": both["final_state_distance"],
        "observer_rescue_late_gain": observer_rescue["late_gain"],
        "policy_rescue_late_gain": policy_rescue["late_gain"],
        "observer_lesion_late_gain": observer_rescue["early_gain"],
        "policy_lesion_late_gain": policy_rescue["early_gain"],
        "intervention_target_error": intervention_error,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=64)
    parser.add_argument("--train-episodes", type=int, default=64)
    parser.add_argument("--observer-samples", type=int, default=512)
    parser.add_argument("--out", default="results/tcf_consciousness_instantiation_c0_6")
    args = parser.parse_args()

    out = Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    observer = train_self_observer(seed=96001, samples=args.observer_samples)
    policy = train_policy(
        observer,
        seed=96002,
        episodes=args.train_episodes,
        recovery_steps=RECOVERY_STEPS,
    )
    snapshot = json.loads(json.dumps(policy.to_dict()))

    rows = [
        episode(
            observer=SelfObserver.from_dict(json.loads(json.dumps(observer.to_dict()))),
            policy=SelfPolicy.from_dict(json.loads(json.dumps(snapshot))),
            seed=96010 + index,
        )
        for index in range(args.episodes)
    ]

    arrays = {
        key: np.asarray([row[key] for row in rows], dtype=float)
        for key in rows[0]
    }

    observer_necessity = arrays["full_gain"] - arrays["observer_lesion_gain"]
    policy_necessity = arrays["full_gain"] - arrays["policy_lesion_gain"]
    both_necessity = arrays["full_gain"] - arrays["both_lesion_gain"]

    observer_distance = (
        arrays["observer_lesion_final_distance"] - arrays["full_final_distance"]
    )
    policy_distance = (
        arrays["policy_lesion_final_distance"] - arrays["full_final_distance"]
    )

    observer_rescue_lift = (
        arrays["observer_rescue_late_gain"] - arrays["observer_lesion_late_gain"]
    )
    policy_rescue_lift = (
        arrays["policy_rescue_late_gain"] - arrays["policy_lesion_late_gain"]
    )

    summary = {
        "experiment": "tcf_consciousness_instantiation_c0_6",
        "protocol_version": PROTOCOL_VERSION,
        "episodes": args.episodes,
        "train_episodes": args.train_episodes,
        "observer_samples": args.observer_samples,
        "lesion_steps": LESION_STEPS,
        "recovery_steps": RECOVERY_STEPS,
        "conditions": [
            "full",
            "observer_lesion",
            "policy_lesion",
            "both_lesion",
            "observer_rescue",
            "policy_rescue",
        ],
        "primary_outputs": [
            "observer_necessity_gain_delta",
            "policy_necessity_gain_delta",
            "both_lesion_gain_delta",
            "observer_rescue_lift",
            "policy_rescue_lift",
            "final_state_distance_effects",
        ],
        "observer_necessity_gain_delta": {
            "mean": float(np.mean(observer_necessity)),
            "p": float(sign_p(observer_necessity, 96101)),
        },
        "policy_necessity_gain_delta": {
            "mean": float(np.mean(policy_necessity)),
            "p": float(sign_p(policy_necessity, 96102)),
        },
        "both_lesion_gain_delta": {
            "mean": float(np.mean(both_necessity)),
            "p": float(sign_p(both_necessity, 96103)),
        },
        "observer_distance_delta": {
            "mean": float(np.mean(observer_distance)),
            "p": float(sign_p(observer_distance, 96104)),
        },
        "policy_distance_delta": {
            "mean": float(np.mean(policy_distance)),
            "p": float(sign_p(policy_distance, 96105)),
        },
        "observer_rescue_lift": {
            "mean": float(np.mean(observer_rescue_lift)),
            "p": float(sign_p(observer_rescue_lift, 96106)),
        },
        "policy_rescue_lift": {
            "mean": float(np.mean(policy_rescue_lift)),
            "p": float(sign_p(policy_rescue_lift, 96107)),
        },
        "intervention_target_error_max": float(
            np.max(arrays["intervention_target_error"])
        ),
        "semantic_input_during_probe": False,
        "external_retraining_during_probe": False,
        "same_trained_snapshot_across_lesions": True,
        "phenomenal_consciousness_claimed": False,
        "interpretation_rule": (
            "C0.6 tests causal necessity of the trained self-observer and "
            "self-policy by lesioning them after a common training phase and "
            "measuring rescue after restoration. A causal lesion effect is "
            "an organizational result, not evidence by itself of phenomenal consciousness."
        ),
    }

    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out / "policy_snapshot.json").write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out / "observer_snapshot.json").write_text(
        json.dumps(observer.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
