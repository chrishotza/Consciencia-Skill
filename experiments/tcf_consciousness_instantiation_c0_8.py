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
    apply_single_impulse,
    self_prediction_gain,
    sign_p,
    train_policy,
    train_self_observer,
    warmup_context,
)
from experiments.tcf_consciousness_instantiation_c0 import choose_action

PROTOCOL_VERSION = "C0.8"


def permute_targets(observer: SelfObserver, seed: int) -> SelfObserver:
    payload = observer.to_dict()
    rng = np.random.default_rng(seed)
    targets = np.asarray(payload["targets"], dtype=float)
    payload["targets"] = rng.permutation(targets).tolist()
    return SelfObserver.from_dict(payload)


def run_episode(observer: SelfObserver, policy: SelfPolicy, seed: int) -> dict[str, float]:
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


def paired_condition(observer: SelfObserver, policy: SelfPolicy, seeds: list[int]):
    names = (
        "mean_gain",
        "final_state_distance",
        "state_variance",
        "mean_abs_action",
        "action_switches",
        "intervention_target_error",
    )
    rows = [run_episode(observer, policy, seed) for seed in seeds]
    return {name: np.asarray([row[name] for row in rows], dtype=float) for name in names}


def delta(a, b):
    return a - b


def stat(values, seed):
    return {"mean": float(np.mean(values)), "p": float(sign_p(values, seed))}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=64)
    parser.add_argument("--train-episodes", type=int, default=64)
    parser.add_argument("--observer-samples", type=int, default=512)
    parser.add_argument("--out", default="results/tcf_consciousness_instantiation_c0_8")
    args = parser.parse_args()

    out = Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    true_observer = train_self_observer(seed=98001, samples=args.observer_samples)
    permuted_observer = permute_targets(true_observer, seed=98050)

    true_policy = train_policy(
        true_observer,
        seed=98002,
        episodes=args.train_episodes,
        recovery_steps=RECOVERY_STEPS,
    )
    permuted_policy = train_policy(
        permuted_observer,
        seed=98002,
        episodes=args.train_episodes,
        recovery_steps=RECOVERY_STEPS,
    )

    seeds = [98010 + i for i in range(args.episodes)]
    tt = paired_condition(true_observer, true_policy, seeds)
    tp = paired_condition(true_observer, permuted_policy, seeds)
    pt = paired_condition(permuted_observer, true_policy, seeds)
    pp = paired_condition(permuted_observer, permuted_policy, seeds)

    observer_effect = delta(tt["mean_gain"], pt["mean_gain"])
    policy_effect = delta(tt["mean_gain"], tp["mean_gain"])
    interaction = (
        tt["mean_gain"] - tp["mean_gain"] - pt["mean_gain"] + pp["mean_gain"]
    )

    variance_observer = delta(tt["state_variance"], pt["state_variance"])
    variance_policy = delta(tt["state_variance"], tp["state_variance"])
    variance_interaction = (
        tt["state_variance"] - tp["state_variance"] - pt["state_variance"] + pp["state_variance"]
    )

    distance_observer = delta(pt["final_state_distance"], tt["final_state_distance"])
    distance_policy = delta(tp["final_state_distance"], tt["final_state_distance"])
    distance_interaction = (
        tt["final_state_distance"]
        - tp["final_state_distance"]
        - pt["final_state_distance"]
        + pp["final_state_distance"]
    )

    summary = {
        "experiment": "tcf_consciousness_instantiation_c0_8",
        "protocol_version": PROTOCOL_VERSION,
        "question": (
            "Does measured self-organizing behavior depend separately on the "
            "learned observer, the learned policy, and their matched coupling?"
        ),
        "conditions": {
            "TT": "true observer + true policy",
            "TP": "true observer + target-permuted policy",
            "PT": "target-permuted observer + true policy",
            "PP": "target-permuted observer + target-permuted policy",
        },
        "matched_design": {
            "same_episode_seeds": True,
            "same_dynamic_perturbations": True,
            "same_observer_feature_memory": True,
            "same_target_multiset": True,
            "same_training_budget": True,
            "same_policy_training_seed": True,
        },
        "semantic_input_during_probe": False,
        "external_retraining_during_probe": False,
        "phenomenal_consciousness_claimed": False,
        "primary_outputs": {
            "observer_effect_gain": stat(observer_effect, 98101),
            "policy_effect_gain": stat(policy_effect, 98102),
            "observer_policy_interaction_gain": stat(interaction, 98103),
            "observer_effect_variance": stat(variance_observer, 98104),
            "policy_effect_variance": stat(variance_policy, 98105),
            "observer_policy_interaction_variance": stat(variance_interaction, 98106),
            "observer_effect_final_distance": stat(distance_observer, 98107),
            "policy_effect_final_distance": stat(distance_policy, 98108),
            "observer_policy_interaction_final_distance": stat(distance_interaction, 98109),
        },
        "condition_summary": {
            key: {
                name: float(values.mean()) for name, values in cond.items()
            }
            for key, cond in {
                "TT": tt,
                "TP": tp,
                "PT": pt,
                "PP": pp,
            }.items()
        },
        "intervention_target_error_max": max(
            float(tt["intervention_target_error"].max()),
            float(tp["intervention_target_error"].max()),
            float(pt["intervention_target_error"].max()),
            float(pp["intervention_target_error"].max()),
        ),
        "interaction_statistic": {
            "paired_by_episode_seed": True,
            "contrast": "TT - TP - PT + PP",
        },
        "interpretation_rule": (
            "TT/TP and TT/PT contrasts probe component-specific dependence; "
            "the crossed four-condition interaction probes whether the effect "
            "depends on the matched observer-policy pairing. These are causal "
            "organizational tests, not demonstrations of phenomenal consciousness."
        ),
    }

    snapshots = {
        "true_observer_snapshot.json": true_observer.to_dict(),
        "target_permuted_observer_snapshot.json": permuted_observer.to_dict(),
        "true_policy_snapshot.json": true_policy.to_dict(),
        "target_permuted_policy_snapshot.json": permuted_policy.to_dict(),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    for filename, payload in snapshots.items():
        (out / filename).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
