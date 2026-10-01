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
from src.ontto.self_policy import SelfPolicy

from experiments.tcf_consciousness_instantiation_c0 import (
    AUTONOMOUS_STEPS,
    choose_action,
    sign_p,
    train_policy,
    train_self_observer,
    warmup_context,
)
from experiments.organism_repeated_active_continuity_v78 import self_prediction_gain


PROTOCOL_VERSION = "C0.5"
EPISODES = 64
SHUFFLES = 8


def derangement(rng: np.random.Generator, size: int) -> np.ndarray:
    reference = np.arange(size)
    while True:
        permutation = rng.permutation(size)
        if not np.any(permutation == reference):
            return permutation


def collect_contexts(observer, policy, episodes: int):
    contexts = []
    actions = []
    for episode in range(episodes):
        seed = 90010 + episode
        bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
        context = warmup_context(bridge, seed=seed + 1000)
        for _ in range(AUTONOMOUS_STEPS):
            signal = choose_action(
                policy,
                observer,
                context=context,
                state_blind=False,
                open_loop=False,
            )
            _, _, context = self_prediction_gain(
                observer, bridge, context=context, signal=signal
            )
        contexts.append(context)
        actions.append(
            float(
                choose_action(
                    policy,
                    observer,
                    context=context,
                    state_blind=False,
                    open_loop=False,
                )
            )
        )
    return contexts, np.asarray(actions, dtype=float)


def followup_action(observer, policy, context, signal, seed):
    bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
    _, _, next_context = self_prediction_gain(
        observer, bridge, context=context, signal=float(signal)
    )
    return float(
        choose_action(
            policy,
            observer,
            context=next_context,
            state_blind=False,
            open_loop=False,
        )
    )


def evaluate(observer, policy, contexts, actions, shuffles):
    rng = np.random.default_rng(90705)
    own_gaps = []
    matched_gaps = []

    for episode, context in enumerate(contexts):
        own_rows = []
        matched_rows = []
        for _ in range(shuffles):
            first = derangement(rng, len(contexts))
            second = derangement(rng, len(contexts))
            actual_signal = float(actions[episode])
            donor_one = float(actions[int(first[episode])])
            donor_two = float(actions[int(second[episode])])

            seed = 91000 + episode
            actual_followup = followup_action(
                observer, policy, context, actual_signal, seed
            )
            donor_one_followup = followup_action(
                observer, policy, context, donor_one, seed
            )
            donor_two_followup = followup_action(
                observer, policy, context, donor_two, seed
            )

            own_rows.append(
                abs(actual_followup - donor_one_followup)
            )
            matched_rows.append(
                abs(donor_one_followup - donor_two_followup)
            )

        own_gaps.append(float(np.mean(own_rows)))
        matched_gaps.append(float(np.mean(matched_rows)))

    own = np.asarray(own_gaps, dtype=float)
    matched = np.asarray(matched_gaps, dtype=float)
    contrast = own - matched
    return {
        "own_action_chain_gap_mean": float(np.mean(own)),
        "matched_action_chain_gap_mean": float(np.mean(matched)),
        "contrast_mean": float(np.mean(contrast)),
        "contrast_p": float(sign_p(contrast, 90805)),
        "episodes": len(contexts),
        "shuffles_per_episode": shuffles,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=EPISODES)
    parser.add_argument("--train-episodes", type=int, default=64)
    parser.add_argument("--observer-samples", type=int, default=512)
    parser.add_argument(
        "--out",
        default="results/tcf_consciousness_instantiation_c0_5",
    )
    args = parser.parse_args()

    out = Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    observer = train_self_observer(seed=90001, samples=args.observer_samples)
    policy = train_policy(
        observer,
        seed=90002,
        episodes=args.train_episodes,
        recovery_steps=12,
    )
    snapshot = json.loads(json.dumps(policy.to_dict()))
    probe = SelfPolicy.from_dict(json.loads(json.dumps(snapshot)))

    contexts, actions = collect_contexts(observer, probe, args.episodes)
    result = evaluate(
        observer, probe, contexts, actions, SHUFFLES
    )

    summary = {
        "experiment": "tcf_consciousness_instantiation_c0_5",
        "protocol_version": PROTOCOL_VERSION,
        "episodes": args.episodes,
        "train_episodes": args.train_episodes,
        "observer_samples": args.observer_samples,
        "shuffles_per_episode": SHUFFLES,
        "control": "information_matched_action_chain_shuffle",
        "primary_output": "own_action_chain_gap_minus_matched_action_chain_gap",
        "semantic_input_during_probe": False,
        "external_retraining_during_probe": False,
        "policy_snapshot_shared_across_control": True,
        "phenomenal_consciousness_claimed": False,
        **result,
        "interpretation_rule": (
            "C0.5 asks whether the action selected in the current self-state "
            "has more effect on the next selected action than matched donor "
            "actions drawn from the same empirical action distribution; this "
            "is an operational recurrence control, not a demonstration of "
            "phenomenal consciousness."
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
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
