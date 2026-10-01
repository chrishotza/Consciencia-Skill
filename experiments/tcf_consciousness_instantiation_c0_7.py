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
    self_prediction_gain,
    sign_p,
    train_policy,
    train_self_observer,
    warmup_context,
)
from experiments.tcf_consciousness_instantiation_c0 import choose_action


PROTOCOL_VERSION = "C0.7"
PERMUTATION_SEED = 97050


def permute_targets(observer: SelfObserver, seed: int) -> SelfObserver:
    payload = observer.to_dict()
    rng = np.random.default_rng(seed)
    targets = np.asarray(payload["targets"], dtype=float)
    permuted = rng.permutation(targets)
    payload["targets"] = permuted.tolist()
    return SelfObserver.from_dict(payload)


def run_episode(
    *,
    observer: SelfObserver,
    policy: SelfPolicy,
    seed: int,
) -> dict[str, float]:
    bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
    context = warmup_context(bridge, seed=seed + 1000)
    context, _, target_state = apply_single_impulse(context=context, sign=1.0)
    intervention_error = abs(context.state - target_state)

    gains = []
    actions = []
    states = [float(context.state)]

    for _ in range(RECOVERY_STEPS):
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
        actions.append(float(signal))
        states.append(float(context.state))

    return {
        "mean_gain": float(np.mean(gains)),
        "final_state_distance": float(abs(context.state)),
        "state_variance": float(np.var(np.asarray(states, dtype=float))),
        "mean_abs_action": float(np.mean(np.abs(np.asarray(actions, dtype=float)))),
        "action_switches": float(np.count_nonzero(np.diff(np.asarray(actions, dtype=float)))),
        "intervention_target_error": float(intervention_error),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=64)
    parser.add_argument("--train-episodes", type=int, default=64)
    parser.add_argument("--observer-samples", type=int, default=512)
    parser.add_argument("--out", default="results/tcf_consciousness_instantiation_c0_7")
    args = parser.parse_args()

    out = Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    full_observer = train_self_observer(seed=97001, samples=args.observer_samples)
    permuted_observer = permute_targets(full_observer, PERMUTATION_SEED)

    full_policy = train_policy(
        full_observer,
        seed=97002,
        episodes=args.train_episodes,
        recovery_steps=RECOVERY_STEPS,
    )
    permuted_policy = train_policy(
        permuted_observer,
        seed=97002,
        episodes=args.train_episodes,
        recovery_steps=RECOVERY_STEPS,
    )

    full_snapshot = json.loads(json.dumps(full_policy.to_dict()))
    permuted_snapshot = json.loads(json.dumps(permuted_policy.to_dict()))

    full_rows = []
    permuted_rows = []
    for episode in range(args.episodes):
        seed = 97010 + episode
        full_rows.append(
            run_episode(
                observer=full_observer,
                policy=SelfPolicy.from_dict(json.loads(json.dumps(full_snapshot))),
                seed=seed,
            )
        )
        permuted_rows.append(
            run_episode(
                observer=permuted_observer,
                policy=SelfPolicy.from_dict(json.loads(json.dumps(permuted_snapshot))),
                seed=seed,
            )
        )

    metric_names = (
        "mean_gain",
        "final_state_distance",
        "state_variance",
        "mean_abs_action",
        "action_switches",
        "intervention_target_error",
    )

    full = {
        name: np.asarray([row[name] for row in full_rows], dtype=float)
        for name in metric_names
    }
    permuted = {
        name: np.asarray([row[name] for row in permuted_rows], dtype=float)
        for name in metric_names
    }

    gain_delta = full["mean_gain"] - permuted["mean_gain"]
    distance_delta = permuted["final_state_distance"] - full["final_state_distance"]
    variance_delta = full["state_variance"] - permuted["state_variance"]
    action_delta = full["mean_abs_action"] - permuted["mean_abs_action"]

    summary = {
        "experiment": "tcf_consciousness_instantiation_c0_7",
        "protocol_version": PROTOCOL_VERSION,
        "question": (
            "Does the measured self-organizing behavior depend on the learned "
            "state-to-next-state mapping rather than only on model size and target distribution?"
        ),
        "control": "target_permutation_with_matched_retraining",
        "episodes": args.episodes,
        "train_episodes": args.train_episodes,
        "observer_samples": args.observer_samples,
        "same_observer_feature_memory": True,
        "same_target_multiset": True,
        "same_policy_training_budget": True,
        "semantic_input_during_probe": False,
        "external_retraining_during_probe": False,
        "phenomenal_consciousness_claimed": False,
        "primary_outputs": {
            "full_gain_minus_target_permuted_gain": {
                "mean": float(np.mean(gain_delta)),
                "p": float(sign_p(gain_delta, 97101)),
            },
            "target_permuted_distance_minus_full_distance": {
                "mean": float(np.mean(distance_delta)),
                "p": float(sign_p(distance_delta, 97102)),
            },
            "full_variance_minus_target_permuted_variance": {
                "mean": float(np.mean(variance_delta)),
                "p": float(sign_p(variance_delta, 97103)),
            },
            "full_mean_abs_action_minus_target_permuted": {
                "mean": float(np.mean(action_delta)),
                "p": float(sign_p(action_delta, 97104)),
            },
        },
        "full_summary": {
            name: float(values.mean()) for name, values in full.items()
        },
        "target_permuted_summary": {
            name: float(values.mean()) for name, values in permuted.items()
        },
        "intervention_target_error_max": float(
            max(
                full["intervention_target_error"].max(),
                permuted["intervention_target_error"].max(),
            )
        ),
        "interpretation_rule": (
            "A difference under target permutation indicates dependence on the "
            "specific learned transition mapping under this matched control. "
            "It does not by itself establish phenomenal consciousness."
        ),
    }

    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out / "full_observer_snapshot.json").write_text(
        json.dumps(full_observer.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out / "target_permuted_observer_snapshot.json").write_text(
        json.dumps(permuted_observer.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out / "full_policy_snapshot.json").write_text(
        json.dumps(full_snapshot, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out / "target_permuted_policy_snapshot.json").write_text(
        json.dumps(permuted_snapshot, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
