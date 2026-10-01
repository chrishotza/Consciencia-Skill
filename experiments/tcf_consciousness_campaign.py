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

from src.ontto.bridge import DynamicStateBridge
from src.ontto.dynamics import Config as DynamicsConfig
from src.ontto.self_policy import SelfPolicy

from experiments.tcf_consciousness_instantiation_c0 import (
    CONDITIONS,
    DynamicContext,
    run_episode,
    sign_p,
    train_policy,
    train_self_observer,
)
from experiments.organism_repeated_active_continuity_v78 import (
    self_prediction_gain,
    warmup_context,
)
from experiments.tcf_consciousness_instantiation_c0 import choose_action

AUTONOMOUS_STEPS = 8


PROTOCOL_VERSION = "C0-CAMPAIGN-1.0"
DEFAULT_EPISODES = 64
SHUFFLES = 8


def campaign_seed(group: str, replicate: int) -> int:
    index = int(group[1:])
    return 100000 + index * 1000 + replicate * 100


def derive_seed_map(base_seed: int) -> dict[str, int]:
    return {
        "observer": base_seed + 1,
        "policy": base_seed + 2,
        "trajectory": base_seed + 10000,
        "control": base_seed + 20000,
        "statistics": base_seed + 30000,
    }


def train_snapshot(seed_map: dict[str, int], train_episodes: int, observer_samples: int):
    observer = train_self_observer(
        seed=seed_map["observer"],
        samples=observer_samples,
    )
    policy = train_policy(
        observer,
        seed=seed_map["policy"],
        episodes=train_episodes,
        recovery_steps=12,
    )
    snapshot = json.loads(json.dumps(policy.to_dict()))
    return observer, snapshot


def run_condition_rows(
    observer,
    snapshot: dict,
    *,
    condition: str,
    episodes: int,
    base_seed: int,
) -> list[dict[str, float]]:
    return [
        run_episode(
            observer=observer,
            policy_snapshot=snapshot,
            seed=base_seed + episode,
            condition=condition,
            recovery_steps=12,
        )
        for episode in range(episodes)
    ]


def paired_metric(full_rows, control_rows, key: str):
    return np.asarray(
        [float(a[key]) - float(b[key]) for a, b in zip(full_rows, control_rows)],
        dtype=float,
    )


def derangement(rng: np.random.Generator, size: int) -> np.ndarray:
    reference = np.arange(size)
    while True:
        permutation = rng.permutation(size)
        if not np.any(permutation == reference):
            return permutation


def collect_full_trajectories(observer, policy: SelfPolicy, *, episodes: int, base_seed: int):
    rows = []
    for episode in range(episodes):
        seed = base_seed + episode
        bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
        context = warmup_context(bridge, seed=seed + 1000)
        initial = context
        states = [float(context.state)]
        actions = []

        for _ in range(AUTONOMOUS_STEPS):
            signal = choose_action(
                policy,
                observer,
                context=context,
                state_blind=False,
                open_loop=False,
            )
            _, _, context = self_prediction_gain(
                observer,
                bridge,
                context=context,
                signal=signal,
            )
            actions.append(float(signal))
            states.append(float(context.state))

        rows.append(
            {
                "initial": initial,
                "final": context,
                "actions": np.asarray(actions, dtype=float),
                "states": np.asarray(states, dtype=float),
            }
        )
    return rows


def c3_information_matched(observer, policy, trajectories, *, rng_seed: int):
    size = len(trajectories)
    rng = np.random.default_rng(rng_seed)
    final_contexts = [row["final"] for row in trajectories]
    own = []
    null = []

    for episode, context in enumerate(final_contexts):
        own_rows = []
        null_rows = []
        actual = choose_action(
            policy,
            observer,
            context=context,
            state_blind=False,
            open_loop=False,
        )
        for _ in range(SHUFFLES):
            first = derangement(rng, size)
            second = derangement(rng, size)
            first_context = replace(
                context,
                state=float(final_contexts[int(first[episode])].state),
            )
            second_context = replace(
                context,
                state=float(final_contexts[int(second[episode])].state),
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
            own_rows.append(abs(float(actual) - float(first_action)))
            null_rows.append(abs(float(first_action) - float(second_action)))

        own.append(float(np.mean(own_rows)))
        null.append(float(np.mean(null_rows)))

    own = np.asarray(own, dtype=float)
    null = np.asarray(null, dtype=float)
    contrast = own - null
    return {
        "effect": float(np.mean(contrast)),
        "p": float(sign_p(contrast, rng_seed + 1)),
        "own_gap_mean": float(np.mean(own)),
        "matched_gap_mean": float(np.mean(null)),
    }


def replay_variance(observer, *, initial: DynamicContext, actions: np.ndarray, seed: int) -> float:
    bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
    context = initial
    states = [float(context.state)]
    for signal in actions:
        _, _, context = self_prediction_gain(
            observer,
            bridge,
            context=context,
            signal=float(signal),
        )
        states.append(float(context.state))
    return float(np.var(np.asarray(states, dtype=float)))


def c5_action_replay(observer, trajectories, *, rng_seed: int):
    size = len(trajectories)
    rng = np.random.default_rng(rng_seed)
    full = []
    replay = []

    for episode, row in enumerate(trajectories):
        full.append(float(np.var(row["states"])))
        replay_rows = []
        for _ in range(SHUFFLES):
            donor = derangement(rng, size)
            replay_rows.append(
                replay_variance(
                    observer,
                    initial=row["initial"],
                    actions=trajectories[int(donor[episode])]["actions"],
                    seed=rng_seed + 1000 + episode,
                )
            )
        replay.append(float(np.mean(replay_rows)))

    full = np.asarray(full, dtype=float)
    replay = np.asarray(replay, dtype=float)
    contrast = full - replay
    return {
        "effect": float(np.mean(contrast)),
        "p": float(sign_p(contrast, rng_seed + 1)),
        "full_variance_mean": float(np.mean(full)),
        "replay_variance_mean": float(np.mean(replay)),
    }


def followup_action(observer, policy, context, signal: float, *, seed: int) -> float:
    bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
    _, _, next_context = self_prediction_gain(
        observer,
        bridge,
        context=context,
        signal=float(signal),
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


def c7_action_chain(observer, policy, trajectories, *, rng_seed: int):
    size = len(trajectories)
    rng = np.random.default_rng(rng_seed)
    actions = np.asarray(
        [
            choose_action(
                policy,
                observer,
                context=row["final"],
                state_blind=False,
                open_loop=False,
            )
            for row in trajectories
        ],
        dtype=float,
    )

    own = []
    null = []
    for episode, row in enumerate(trajectories):
        own_rows = []
        null_rows = []
        for _ in range(SHUFFLES):
            first = derangement(rng, size)
            second = derangement(rng, size)
            actual = float(actions[episode])
            donor_one = float(actions[int(first[episode])])
            donor_two = float(actions[int(second[episode])])
            seed = rng_seed + 2000 + episode

            actual_followup = followup_action(
                observer, policy, row["final"], actual, seed=seed
            )
            donor_one_followup = followup_action(
                observer, policy, row["final"], donor_one, seed=seed
            )
            donor_two_followup = followup_action(
                observer, policy, row["final"], donor_two, seed=seed
            )

            own_rows.append(abs(actual_followup - donor_one_followup))
            null_rows.append(abs(donor_one_followup - donor_two_followup))

        own.append(float(np.mean(own_rows)))
        null.append(float(np.mean(null_rows)))

    own = np.asarray(own, dtype=float)
    null = np.asarray(null, dtype=float)
    contrast = own - null
    return {
        "effect": float(np.mean(contrast)),
        "p": float(sign_p(contrast, rng_seed + 1)),
        "own_chain_gap_mean": float(np.mean(own)),
        "matched_chain_gap_mean": float(np.mean(null)),
    }


def run_group(
    group: str,
    replicate: int,
    *,
    episodes: int,
    train_episodes: int,
    observer_samples: int,
    out: Path,
):
    base_seed = campaign_seed(group, replicate)
    seed_map = derive_seed_map(base_seed)
    observer, snapshot = train_snapshot(
        seed_map,
        train_episodes=train_episodes,
        observer_samples=observer_samples,
    )
    policy = SelfPolicy.from_dict(json.loads(json.dumps(snapshot)))

    result = {
        "criterion": None,
        "control": None,
        "metric": None,
        "seed_base": base_seed,
        "seed_map": seed_map,
    }

    if group in {"G1", "G2", "G3", "G8"}:
        trajectories = collect_full_trajectories(
            observer,
            policy,
            episodes=episodes,
            base_seed=seed_map["trajectory"],
        )

    if group == "G1":
        result["criterion"] = "C3_causal_self_reference"
        result["control"] = "information_matched_state_shuffle"
        result["metric"] = c3_information_matched(
            observer,
            policy,
            trajectories,
            rng_seed=seed_map["control"],
        )

    elif group == "G2":
        result["criterion"] = "C5_intrinsic_dynamics"
        result["control"] = "information_matched_action_replay"
        result["metric"] = c5_action_replay(
            observer,
            trajectories,
            rng_seed=seed_map["control"],
        )

    elif group == "G3":
        result["criterion"] = "C7_recurrent_closure"
        result["control"] = "information_matched_action_chain_shuffle"
        result["metric"] = c7_action_chain(
            observer,
            policy,
            trajectories,
            rng_seed=seed_map["control"],
        )

    elif group in {"G4", "G5", "G6", "G7"}:
        full_rows = run_condition_rows(
            observer,
            snapshot,
            condition="full",
            episodes=episodes,
            base_seed=seed_map["trajectory"],
        )
        if group == "G4":
            control = "no_persistence"
            criterion = "C4_trajectory_continuity"
            key = "continuity_pause_gap"
        elif group == "G5":
            control = "no_persistence"
            criterion = "C1_own_state_persistence"
            key = "own_state_persistence"
        elif group == "G6":
            control = "state_blind"
            criterion = "C2_self_environment_differentiation"
            key = "environment_discrimination"
        else:
            control = "state_blind"
            criterion = "C6_reorganization"
            key = "recovery_gain"

        control_rows = run_condition_rows(
            observer,
            snapshot,
            condition=control,
            episodes=episodes,
            base_seed=seed_map["trajectory"],
        )
        values = paired_metric(full_rows, control_rows, key)
        result["criterion"] = criterion
        result["control"] = control
        result["metric"] = {
            "effect": float(np.mean(values)),
            "p": float(sign_p(values, seed_map["statistics"])),
        }

    elif group == "G8":
        row_sets = {
            condition: run_condition_rows(
                observer,
                snapshot,
                condition=condition,
                episodes=episodes,
                base_seed=seed_map["trajectory"],
            )
            for condition in CONDITIONS
        }

        c1 = paired_metric(
            row_sets["full"],
            row_sets["no_persistence"],
            "own_state_persistence",
        )
        c2 = paired_metric(
            row_sets["full"],
            row_sets["state_blind"],
            "environment_discrimination",
        )
        c4 = paired_metric(
            row_sets["full"],
            row_sets["no_persistence"],
            "continuity_pause_gap",
        )
        c6 = paired_metric(
            row_sets["full"],
            row_sets["state_blind"],
            "recovery_gain",
        )

        result["criterion"] = "C0_battery"
        result["control"] = "strong_controls_C3_C5_C7"
        result["metric"] = {
            "C1": {"effect": float(np.mean(c1)), "p": float(sign_p(c1, seed_map["statistics"] + 1))},
            "C2": {"effect": float(np.mean(c2)), "p": float(sign_p(c2, seed_map["statistics"] + 2))},
            "C3": c3_information_matched(
                observer, policy, trajectories, rng_seed=seed_map["control"] + 10
            ),
            "C4": {"effect": float(np.mean(c4)), "p": float(sign_p(c4, seed_map["statistics"] + 4))},
            "C5": c5_action_replay(
                observer, trajectories, rng_seed=seed_map["control"] + 20
            ),
            "C6": {"effect": float(np.mean(c6)), "p": float(sign_p(c6, seed_map["statistics"] + 6))},
            "C7": c7_action_chain(
                observer, policy, trajectories, rng_seed=seed_map["control"] + 30
            ),
        }

    else:
        raise ValueError(f"unknown campaign group: {group}")

    summary = {
        "experiment": "tcf_consciousness_campaign",
        "protocol_version": PROTOCOL_VERSION,
        "group": group,
        "replicate": replicate,
        "episodes": episodes,
        "train_episodes": train_episodes,
        "observer_samples": observer_samples,
        "semantic_input_during_probe": False,
        "external_retraining_during_probe": False,
        "policy_snapshot_shared_across_conditions": True,
        "phenomenal_consciousness_claimed": False,
        "result": result,
    }

    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out / "policy_snapshot.json").write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out / "campaign_slot.json").write_text(
        json.dumps(
            {
                "group": group,
                "replicate": replicate,
                "seed_base": base_seed,
                "seed_map": seed_map,
                "protocol_version": PROTOCOL_VERSION,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--group", required=True, choices=[f"G{i}" for i in range(1, 9)])
    parser.add_argument("--replicate", type=int, required=True, choices=[1, 2, 3, 4])
    parser.add_argument("--episodes", type=int, default=DEFAULT_EPISODES)
    parser.add_argument("--train-episodes", type=int, default=64)
    parser.add_argument("--observer-samples", type=int, default=512)
    parser.add_argument("--out", default="results/tcf_campaign")
    args = parser.parse_args()

    group_out = Path(args.out) / f"{args.group}_R{args.replicate}"
    shutil.rmtree(group_out, ignore_errors=True)
    run_group(
        args.group,
        args.replicate,
        episodes=args.episodes,
        train_episodes=args.train_episodes,
        observer_samples=args.observer_samples,
        out=group_out,
    )


if __name__ == "__main__":
    main()
