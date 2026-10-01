from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ontto.dynamics import Config as DynamicsConfig
from src.ontto.bridge import DynamicStateBridge
from src.ontto.self_policy import SelfPolicy

from experiments.tcf_consciousness_instantiation_c0 import (
    AUTONOMOUS_STEPS,
    DynamicContext,
    choose_action,
    roll_forward,
    sign_p,
    train_policy,
    train_self_observer,
    warmup_context,
)

PROTOCOL_VERSION = "C0.3"
EPISODES = 64
SHUFFLES = 8


def derangement(rng: np.random.Generator, size: int) -> np.ndarray:
    reference = np.arange(size)
    while True:
        permutation = rng.permutation(size)
        if not np.any(permutation == reference):
            return permutation


def collect_full_contexts(
    observer,
    policy: SelfPolicy,
    *,
    episodes: int,
) -> list[DynamicContext]:
    contexts: list[DynamicContext] = []
    for episode in range(episodes):
        seed = 90010 + episode
        bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
        context = warmup_context(bridge, seed=seed + 1000)
        context, _ = roll_forward(
            observer=observer,
            policy=policy,
            context=context,
            condition="full",
            bridge_seed=seed + 94000,
            steps=AUTONOMOUS_STEPS,
        )
        contexts.append(context)
    return contexts


def evaluate_information_matched_state_dependence(
    *,
    observer,
    policy: SelfPolicy,
    contexts: list[DynamicContext],
    shuffles: int,
) -> dict[str, float]:
    size = len(contexts)
    rng = np.random.default_rng(90303)
    own_gaps: list[float] = []
    null_gaps: list[float] = []
    mismatches: list[float] = []

    for episode, context in enumerate(contexts):
        actual_action = choose_action(
            policy,
            observer,
            context=context,
            state_blind=False,
            open_loop=False,
        )

        own_episode_gaps: list[float] = []
        null_episode_gaps: list[float] = []
        mismatch_count = 0

        for _ in range(shuffles):
            first_perm = derangement(rng, size)
            second_perm = derangement(rng, size)

            first_context = replace(
                context,
                state=float(contexts[int(first_perm[episode])].state),
            )
            second_context = replace(
                context,
                state=float(contexts[int(second_perm[episode])].state),
            )

            first_action = choose_action(
                policy,
                observer,
                context=first_context,
                state_blind=False,
                open_loop=False,
            )
            second_action = choose_action(
                policy,
                observer,
                context=second_context,
                state_blind=False,
                open_loop=False,
            )

            own_gap = abs(float(actual_action) - float(first_action))
            null_gap = abs(float(first_action) - float(second_action))

            own_episode_gaps.append(own_gap)
            null_episode_gaps.append(null_gap)
            mismatch_count += float(actual_action != first_action)

        own_gaps.append(float(np.mean(own_episode_gaps)))
        null_gaps.append(float(np.mean(null_episode_gaps)))
        mismatches.append(mismatch_count / shuffles)

    own = np.asarray(own_gaps, dtype=float)
    null = np.asarray(null_gaps, dtype=float)
    contrast = own - null

    return {
        "own_state_gap_mean": float(np.mean(own)),
        "matched_shuffle_gap_mean": float(np.mean(null)),
        "contrast_mean": float(np.mean(contrast)),
        "contrast_p": float(sign_p(contrast, 90403)),
        "actual_vs_shuffle_action_mismatch_rate": float(np.mean(mismatches)),
        "episodes": float(size),
        "shuffles_per_episode": float(shuffles),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodes", type=int, default=EPISODES)
    ap.add_argument("--train-episodes", type=int, default=64)
    ap.add_argument("--observer-samples", type=int, default=512)
    ap.add_argument(
        "--out",
        default="results/tcf_consciousness_instantiation_c0_3",
    )
    args = ap.parse_args()

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
    policy_for_probe = SelfPolicy.from_dict(json.loads(json.dumps(snapshot)))

    contexts = collect_full_contexts(
        observer,
        policy_for_probe,
        episodes=args.episodes,
    )
    result = evaluate_information_matched_state_dependence(
        observer=observer,
        policy=policy_for_probe,
        contexts=contexts,
        shuffles=args.shuffles if hasattr(args, "shuffles") else SHUFFLES,
    )

    summary = {
        "experiment": "tcf_consciousness_instantiation_c0_3",
        "protocol_version": PROTOCOL_VERSION,
        "episodes": args.episodes,
        "train_episodes": args.train_episodes,
        "observer_samples": args.observer_samples,
        "shuffles_per_episode": SHUFFLES,
        "control": "information_matched_state_shuffle",
        "primary_output": "own_state_gap_minus_matched_shuffle_gap",
        "semantic_input_during_probe": False,
        "external_retraining_during_probe": False,
        "policy_snapshot_shared_across_control": True,
        "phenomenal_consciousness_claimed": False,
        **result,
        "interpretation_rule": (
            "C0.3 asks whether action is more sensitive to the current own-state "
            "value than to shuffled states drawn from the same empirical state distribution; "
            "a positive contrast is evidence for state-specific causal dependence under this probe, "
            "not a demonstration of phenomenal consciousness."
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
