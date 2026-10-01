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
    RECOVERY_STEPS,
    DynamicContext,
    apply_single_impulse,
    candidate_features,
    self_prediction_gain,
    sign_p,
    train_policy,
    train_self_observer,
    warmup_context,
)


CRITERIA = (
    "C1_own_state_persistence",
    "C2_self_environment_differentiation",
    "C3_causal_self_reference",
    "C4_trajectory_continuity",
    "C5_intrinsic_dynamics",
    "C6_reorganization",
    "C7_recurrent_closure",
)

CONDITIONS = ("full", "state_blind", "no_persistence", "open_loop")
AUTONOMOUS_STEPS = 8
PAUSE_PRE_STEPS = 4
PAUSE_POST_STEPS = 4
PERTURBATION = 0.50
C1_STATE_SEPARATION = 0.20


def choose_action(
    policy: SelfPolicy,
    observer: SelfObserver,
    *,
    context: DynamicContext,
    state_blind: bool,
    open_loop: bool,
) -> float:
    if open_loop:
        return 0.0
    state = 0.0 if state_blind else float(context.state)
    candidates = [
        candidate_features(observer, state=state, signal=signal)
        for signal in SIGNALS
    ]
    return float(policy.choose(candidates)["signal"])


def advance_one(
    *,
    observer: SelfObserver,
    policy: SelfPolicy,
    bridge: DynamicStateBridge,
    context: DynamicContext,
    condition: str,
) -> tuple[DynamicContext, float]:
    signal = choose_action(
        policy,
        observer,
        context=context,
        state_blind=condition == "state_blind",
        open_loop=condition == "open_loop",
    )
    _, _, next_context = self_prediction_gain(
        observer,
        bridge,
        context=context,
        signal=signal,
    )
    if condition == "no_persistence":
        next_context = DynamicContext(
            previous_state=0.0,
            state=0.0,
            memory=0.0,
            pressure=0.0,
            step_index=next_context.step_index,
        )
    return next_context, float(signal)


def roll_forward(
    *,
    observer: SelfObserver,
    policy: SelfPolicy,
    context: DynamicContext,
    condition: str,
    bridge_seed: int,
    steps: int,
) -> tuple[DynamicContext, list[float]]:
    bridge = DynamicStateBridge(DynamicsConfig(), seed=bridge_seed)
    states = [float(context.state)]
    for _ in range(steps):
        context, _ = advance_one(
            observer=observer,
            policy=policy,
            bridge=bridge,
            context=context,
            condition=condition,
        )
        states.append(float(context.state))
    return context, states


def own_state_persistence_metric(
    *,
    observer: SelfObserver,
    policy: SelfPolicy,
    context: DynamicContext,
    condition: str,
    seed: int,
) -> float:
    center = float(np.clip(context.state, -0.50, 0.50))
    left = DynamicContext(
        previous_state=center,
        state=center - C1_STATE_SEPARATION / 2.0,
        memory=context.memory,
        pressure=context.pressure,
        step_index=context.step_index,
    )
    right = DynamicContext(
        previous_state=center,
        state=center + C1_STATE_SEPARATION / 2.0,
        memory=context.memory,
        pressure=context.pressure,
        step_index=context.step_index,
    )
    left_final, _ = roll_forward(
        observer=observer,
        policy=policy,
        context=left,
        condition=condition,
        bridge_seed=seed,
        steps=AUTONOMOUS_STEPS,
    )
    right_final, _ = roll_forward(
        observer=observer,
        policy=policy,
        context=right,
        condition=condition,
        bridge_seed=seed,
        steps=AUTONOMOUS_STEPS,
    )
    final_separation = abs(left_final.state - right_final.state)
    return float(final_separation / C1_STATE_SEPARATION)


def continuity_under_pause_metric(
    *,
    observer: SelfObserver,
    policy: SelfPolicy,
    context: DynamicContext,
    seed: int,
) -> float:
    checkpoint, _ = roll_forward(
        observer=observer,
        policy=policy,
        context=context,
        condition="full",
        bridge_seed=seed,
        steps=PAUSE_PRE_STEPS,
    )
    uninterrupted, _ = roll_forward(
        observer=observer,
        policy=policy,
        context=checkpoint,
        condition="full",
        bridge_seed=seed + 1,
        steps=PAUSE_POST_STEPS,
    )
    restarted_context = DynamicContext(
        previous_state=0.0,
        state=0.0,
        memory=0.0,
        pressure=0.0,
        step_index=checkpoint.step_index,
    )
    restarted, _ = roll_forward(
        observer=observer,
        policy=policy,
        context=restarted_context,
        condition="full",
        bridge_seed=seed + 1,
        steps=PAUSE_POST_STEPS,
    )
    return float(
        abs(float(uninterrupted.state) - float(restarted.state))
    )


def action_environment_discrimination(
    *,
    observer: SelfObserver,
    policy: SelfPolicy,
    context: DynamicContext,
    condition: str,
) -> float:
    positive_context, _, _ = apply_single_impulse(context=context, sign=1.0)
    negative_context, _, _ = apply_single_impulse(context=context, sign=-1.0)
    positive = choose_action(
        policy,
        observer,
        context=positive_context,
        state_blind=condition == "state_blind",
        open_loop=condition == "open_loop",
    )
    negative = choose_action(
        policy,
        observer,
        context=negative_context,
        state_blind=condition == "state_blind",
        open_loop=condition == "open_loop",
    )
    return float(abs(positive - negative))


def causal_self_reference_metric(
    *,
    observer: SelfObserver,
    policy: SelfPolicy,
    context: DynamicContext,
    condition: str,
) -> float:
    if condition == "open_loop":
        return 0.0
    actual = choose_action(
        policy,
        observer,
        context=context,
        state_blind=False,
        open_loop=False,
    )
    blinded = choose_action(
        policy,
        observer,
        context=context,
        state_blind=True,
        open_loop=False,
    )
    return float(abs(actual - blinded))


def run_episode(
    *,
    observer: SelfObserver,
    policy_snapshot: dict,
    seed: int,
    condition: str,
    recovery_steps: int,
) -> dict[str, float]:
    policy = SelfPolicy.from_dict(json.loads(json.dumps(policy_snapshot)))
    bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
    context = warmup_context(bridge, seed=seed + 1000)

    own_state_persistence = own_state_persistence_metric(
        observer=observer,
        policy=policy,
        context=context,
        condition=condition,
        seed=seed + 93000,
    )

    autonomous_context, autonomous_states = roll_forward(
        observer=observer,
        policy=policy,
        context=context,
        condition=condition,
        bridge_seed=seed + 94000,
        steps=AUTONOMOUS_STEPS,
    )
    autonomous_variance = float(np.var(autonomous_states))

    c2 = action_environment_discrimination(
        observer=observer,
        policy=policy,
        context=autonomous_context,
        condition=condition,
    )
    c3 = causal_self_reference_metric(
        observer=observer,
        policy=policy,
        context=autonomous_context,
        condition=condition,
    )
    continuity_gap = continuity_under_pause_metric(
        observer=observer,
        policy=policy,
        context=autonomous_context,
        seed=seed + 95000,
    )

    pre_event = autonomous_context
    pre_action_signal = choose_action(
        policy,
        observer,
        context=pre_event,
        state_blind=condition == "state_blind",
        open_loop=condition == "open_loop",
    )

    intervention_context, _, target_state = apply_single_impulse(
        context=pre_event,
        sign=1.0,
    )
    intervention_error = float(abs(intervention_context.state - target_state))

    gains: list[float] = []
    states: list[float] = [float(intervention_context.state)]
    context = intervention_context

    for _ in range(recovery_steps):
        signal = choose_action(
            policy,
            observer,
            context=context,
            state_blind=condition == "state_blind",
            open_loop=condition == "open_loop",
        )
        _, gain, context = self_prediction_gain(
            observer,
            bridge,
            context=context,
            signal=signal,
        )
        gains.append(float(gain))
        states.append(float(context.state))
        if condition == "no_persistence":
            context = DynamicContext(
                previous_state=0.0,
                state=0.0,
                memory=0.0,
                pressure=0.0,
                step_index=context.step_index,
            )

    recovery_gain = float(np.mean(gains))

    # C7: causal action -> next-self-state coupling from the same pre-action context.
    counterfactual_zero = DynamicStateBridge(
        DynamicsConfig(), seed=seed + 96000
    )
    factual_bridge = DynamicStateBridge(
        DynamicsConfig(), seed=seed + 96000
    )
    _, _, factual_next = self_prediction_gain(
        observer,
        factual_bridge,
        context=pre_event,
        signal=pre_action_signal,
    )
    _, _, zero_next = self_prediction_gain(
        observer,
        counterfactual_zero,
        context=pre_event,
        signal=0.0,
    )
    recurrent_coupling = abs(
        float(factual_next.state) - float(zero_next.state)
    )

    return {
        "own_state_persistence": own_state_persistence,
        "environment_discrimination": c2,
        "causal_self_reference": c3,
        "continuity_pause_gap": continuity_gap,
        "intrinsic_variance": autonomous_variance,
        "recovery_gain": recovery_gain,
        "recurrent_coupling": recurrent_coupling,
        "intervention_target_error": intervention_error,
    }


def paired_rows(
    *,
    observer: SelfObserver,
    policy_snapshot: dict,
    condition: str,
    episodes: int,
    base_seed: int,
    recovery_steps: int,
) -> dict[str, np.ndarray]:
    rows = [
        run_episode(
            observer=observer,
            policy_snapshot=policy_snapshot,
            seed=base_seed + episode,
            condition=condition,
            recovery_steps=recovery_steps,
        )
        for episode in range(episodes)
    ]
    return {
        key: np.asarray([row[key] for row in rows], dtype=float)
        for key in rows[0]
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodes", type=int, default=64)
    ap.add_argument("--train-episodes", type=int, default=64)
    ap.add_argument("--observer-samples", type=int, default=512)
    ap.add_argument("--recovery-steps", type=int, default=RECOVERY_STEPS)
    ap.add_argument(
        "--out",
        default="results/tcf_consciousness_instantiation_c0",
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
        recovery_steps=args.recovery_steps,
    )
    snapshot = json.loads(json.dumps(policy.to_dict()))

    condition_rows = {
        condition: paired_rows(
            observer=observer,
            policy_snapshot=snapshot,
            condition=condition,
            episodes=args.episodes,
            base_seed=90010,
            recovery_steps=args.recovery_steps,
        )
        for condition in CONDITIONS
    }

    # Pre-registered criterion contrasts.
    c1 = condition_rows["full"]["own_state_persistence"] - condition_rows["no_persistence"]["own_state_persistence"]
    c2 = condition_rows["full"]["environment_discrimination"] - condition_rows["state_blind"]["environment_discrimination"]
    c3 = condition_rows["full"]["causal_self_reference"] - condition_rows["state_blind"]["causal_self_reference"]
    c4 = condition_rows["full"]["continuity_pause_gap"]
    c5 = condition_rows["full"]["intrinsic_variance"] - condition_rows["open_loop"]["intrinsic_variance"]
    c6 = condition_rows["full"]["recovery_gain"] - condition_rows["state_blind"]["recovery_gain"]
    c7 = condition_rows["full"]["recurrent_coupling"] - condition_rows["open_loop"]["recurrent_coupling"]

    contrasts = {
        "C1_own_state_persistence": c1,
        "C2_self_environment_differentiation": c2,
        "C3_causal_self_reference": c3,
        "C4_trajectory_continuity": c4,
        "C5_intrinsic_dynamics": c5,
        "C6_reorganization": c6,
        "C7_recurrent_closure": c7,
    }

    means = {name: float(np.mean(values)) for name, values in contrasts.items()}
    p_values = {
        name: sign_p(values, 90070 + index)
        for index, (name, values) in enumerate(contrasts.items())
    }

    summary = {
        "experiment": "tcf_consciousness_instantiation_c0",
        "protocol_version": "C0.2",
        "episodes": args.episodes,
        "train_episodes": args.train_episodes,
        "observer_samples": args.observer_samples,
        "recovery_steps": args.recovery_steps,
        "perturbation_magnitude": PERTURBATION,
        "criteria": list(CRITERIA),
        "conditions": list(CONDITIONS),
        "primary_outputs_are_criterion_vectors": True,
        "no_composite_consciousness_score": True,
        "phenomenal_consciousness_claimed": False,
        "semantic_input_during_probe": False,
        "external_retraining_during_probe": False,
        "policy_snapshot_shared_across_conditions": True,
        "criterion_effects_mean": means,
        "criterion_effects_p": p_values,
        "intervention_target_error_max": max(
            float(condition_rows[condition]["intervention_target_error"].max())
            for condition in CONDITIONS
        ),
        "conditions_summary": {
            condition: {
                metric: float(values.mean())
                for metric, values in condition_rows[condition].items()
            }
            for condition in CONDITIONS
        },
        "interpretation_rule": (
            "C0 tests candidate organizational properties and their ablations; "
            "passing a criterion does not by itself demonstrate phenomenal consciousness."
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
