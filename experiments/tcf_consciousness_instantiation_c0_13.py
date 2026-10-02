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

from src.ontto.action_conditioned_meta_observer import ActionConditionedMetaObserver
from src.ontto.bridge import DynamicStateBridge
from src.ontto.dynamics import Config as DynamicsConfig
from src.ontto.self_observer import SelfObserver

from experiments.organism_repeated_active_continuity_v78 import (
    SIGNALS,
    apply_single_impulse,
    sign_p,
    train_self_observer,
    warmup_context,
)


PROTOCOL_VERSION = "C0.13"


def first_order_prediction(observer: SelfObserver, *, context, signal: float) -> float:
    return float(
        observer.predict(
            previous_state=context.state,
            state=context.state,
            memory=context.memory,
            pressure=context.pressure,
            last_input=signal,
            attractor_distance=abs(context.state),
            steps_delta=1,
        ).predicted_state
    )


def meta_features(observer: SelfObserver, *, context, signal: float) -> np.ndarray:
    predicted_state = first_order_prediction(
        observer,
        context=context,
        signal=signal,
    )
    return ActionConditionedMetaObserver.features_for(
        previous_state=context.previous_state,
        state=context.state,
        memory=context.memory,
        pressure=context.pressure,
        last_input=signal,
        attractor_distance=abs(context.state),
        steps_delta=1,
        predicted_state=predicted_state,
        predicted_displacement=abs(predicted_state - context.state),
    )


def train_meta(
    observer: SelfObserver,
    *,
    seed: int,
    samples: int,
) -> ActionConditionedMetaObserver:
    meta = ActionConditionedMetaObserver(ridge=1e-3, max_samples=2048)
    rng = np.random.default_rng(seed)
    for index in range(samples):
        bridge = DynamicStateBridge(
            DynamicsConfig(),
            seed=seed + index,
        )
        context = warmup_context(
            bridge,
            seed=seed + 10_000 + index,
        )
        signal = float(rng.choice(SIGNALS))
        predicted = first_order_prediction(
            observer,
            context=context,
            signal=signal,
        )
        snapshot = bridge.advance(
            previous_state=context.previous_state,
            state=context.state,
            memory=context.memory,
            pressure=context.pressure,
            signal=signal,
            steps=1,
            step_index=context.step_index,
        )
        meta.observe(
            features=ActionConditionedMetaObserver.features_for(
                previous_state=context.previous_state,
                state=context.state,
                memory=context.memory,
                pressure=context.pressure,
                last_input=signal,
                attractor_distance=abs(context.state),
                steps_delta=1,
                predicted_state=predicted,
                predicted_displacement=abs(predicted - context.state),
            ),
            prediction_error=abs(float(snapshot.state) - predicted),
        )
    return meta


def permute_targets(
    meta: ActionConditionedMetaObserver,
    *,
    seed: int,
) -> ActionConditionedMetaObserver:
    payload = meta.to_dict()
    rng = np.random.default_rng(seed)
    payload["targets"] = rng.permutation(
        np.asarray(payload["targets"], dtype=float)
    ).tolist()
    return ActionConditionedMetaObserver.from_dict(payload)


def choose_action(
    observer: SelfObserver,
    meta: ActionConditionedMetaObserver | None,
    *,
    context,
    mode: str,
    constant_error: float,
) -> float:
    candidates = []
    for signal in SIGNALS:
        predicted = first_order_prediction(
            observer,
            context=context,
            signal=signal,
        )
        if mode == "true" or mode == "permuted":
            predicted_error = meta.predict_error(
                previous_state=context.previous_state,
                state=context.state,
                memory=context.memory,
                pressure=context.pressure,
                last_input=signal,
                attractor_distance=abs(context.state),
                steps_delta=1,
                predicted_state=predicted,
                predicted_displacement=abs(predicted - context.state),
            )
        elif mode == "blind":
            predicted_error = constant_error
        else:
            raise ValueError(f"unknown mode: {mode}")
        candidates.append(
            (float(predicted_error), abs(float(signal)), float(signal))
        )
    return min(candidates, key=lambda row: (row[0], row[1], row[2]))[2]


def evaluate(
    observer: SelfObserver,
    meta: ActionConditionedMetaObserver | None,
    *,
    contexts,
    seeds,
    mode: str,
    constant_error: float,
) -> dict[str, np.ndarray]:
    actions = []
    gains = []
    predicted_errors = []
    actual_errors = []

    for context, seed in zip(contexts, seeds):
        bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
        action = choose_action(
            observer,
            meta,
            context=context,
            mode=mode,
            constant_error=constant_error,
        )
        predicted = first_order_prediction(
            observer,
            context=context,
            signal=action,
        )
        snapshot = bridge.advance(
            previous_state=context.previous_state,
            state=context.state,
            memory=context.memory,
            pressure=context.pressure,
            signal=action,
            steps=1,
            step_index=context.step_index,
        )
        actual_error = abs(float(snapshot.state) - predicted)
        if mode == "blind":
            predicted_error = constant_error
        else:
            predicted_error = meta.predict_error(
                previous_state=context.previous_state,
                state=context.state,
                memory=context.memory,
                pressure=context.pressure,
                last_input=action,
                attractor_distance=abs(context.state),
                steps_delta=1,
                predicted_state=predicted,
                predicted_displacement=abs(predicted - context.state),
            )
        actions.append(action)
        gains.append(
            float(
                abs(float(snapshot.state) - context.state)
                - actual_error
            )
        )
        predicted_errors.append(predicted_error)
        actual_errors.append(actual_error)

    return {
        "action": np.asarray(actions, dtype=float),
        "gain": np.asarray(gains, dtype=float),
        "predicted_error": np.asarray(predicted_errors, dtype=float),
        "actual_error": np.asarray(actual_errors, dtype=float),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=64)
    parser.add_argument("--observer-samples", type=int, default=512)
    parser.add_argument("--meta-samples", type=int, default=1024)
    parser.add_argument(
        "--out",
        default="results/tcf_consciousness_instantiation_c0_13",
    )
    args = parser.parse_args()

    out = Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    observer = train_self_observer(seed=130001, samples=args.observer_samples)
    meta = train_meta(
        observer,
        seed=130002,
        samples=args.meta_samples,
    )
    permuted = permute_targets(meta, seed=130003)

    contexts = []
    intervention_errors = []
    for index in range(args.episodes):
        seed = 130010 + index
        bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
        context, _, target_state = apply_single_impulse(
            context=warmup_context(bridge, seed=seed + 1000),
            sign=1.0,
        )
        contexts.append(context)
        intervention_errors.append(
            abs(float(context.state) - float(target_state))
        )

    seeds = [230010 + index for index in range(args.episodes)]
    blind_error = float(np.mean(meta.targets))

    true = evaluate(
        observer, meta, contexts=contexts, seeds=seeds,
        mode="true", constant_error=blind_error,
    )
    perm = evaluate(
        observer, permuted, contexts=contexts, seeds=seeds,
        mode="permuted", constant_error=blind_error,
    )
    blind = evaluate(
        observer, None, contexts=contexts, seeds=seeds,
        mode="blind", constant_error=blind_error,
    )

    heldout_actual = []
    heldout_predicted = []
    heldout_baseline = []
    for index in range(args.episodes):
        bridge = DynamicStateBridge(DynamicsConfig(), seed=330010 + index)
        context = warmup_context(
            bridge,
            seed=340010 + index,
        )
        for signal in SIGNALS:
            predicted = first_order_prediction(
                observer,
                context=context,
                signal=signal,
            )
            snapshot = bridge.advance(
                previous_state=context.previous_state,
                state=context.state,
                memory=context.memory,
                pressure=context.pressure,
                signal=signal,
                steps=1,
                step_index=context.step_index,
            )
            actual = abs(float(snapshot.state) - predicted)
            meta_prediction = meta.predict_error(
                previous_state=context.previous_state,
                state=context.state,
                memory=context.memory,
                pressure=context.pressure,
                last_input=signal,
                attractor_distance=abs(context.state),
                steps_delta=1,
                predicted_state=predicted,
                predicted_displacement=abs(predicted - context.state),
            )
            heldout_actual.append(actual)
            heldout_predicted.append(meta_prediction)
            heldout_baseline.append(blind_error)

    heldout_actual = np.asarray(heldout_actual, dtype=float)
    heldout_predicted = np.asarray(heldout_predicted, dtype=float)
    heldout_baseline = np.asarray(heldout_baseline, dtype=float)

    summary = {
        "experiment": "tcf_consciousness_instantiation_c0_13",
        "protocol_version": PROTOCOL_VERSION,
        "question": (
            "Does an action-conditioned second-order self-model become "
            "causally specific to selecting actions?"
        ),
        "conditions": {
            "META_TRUE": "action-conditioned second-order observer",
            "META_PERMUTED": "same features with permuted targets",
            "META_BLIND": "constant second-order error baseline",
        },
        "matched_design": {
            "same_first_order_observer": True,
            "same_episode_contexts": True,
            "same_candidate_signals": True,
            "same_dynamic_bridge_seeds": True,
            "same_meta_training_budget": True,
            "same_target_multiset_for_meta_permutation": True,
            "external_retraining_during_probe": False,
            "semantic_input_during_probe": False,
        },
        "phenomenal_consciousness_claimed": False,
        "semantic_input_during_probe": False,
        "external_retraining_during_probe": False,
        "primary_outputs": {
            "true_vs_permuted_action": {
                "mean": float(np.mean(true["action"] - perm["action"])),
                "p": float(sign_p(true["action"] - perm["action"], 130101)),
            },
            "true_vs_permuted_gain": {
                "mean": float(np.mean(true["gain"] - perm["gain"])),
                "p": float(sign_p(true["gain"] - perm["gain"], 130102)),
            },
            "true_vs_blind_action": {
                "mean": float(np.mean(true["action"] - blind["action"])),
                "p": float(sign_p(true["action"] - blind["action"], 130103)),
            },
            "true_vs_blind_gain": {
                "mean": float(np.mean(true["gain"] - blind["gain"])),
                "p": float(sign_p(true["gain"] - blind["gain"], 130104)),
            },
            "heldout_meta_mae_advantage": {
                "mean": float(
                    np.mean(
                        np.abs(heldout_actual - heldout_baseline)
                        - np.abs(heldout_actual - heldout_predicted)
                    )
                ),
                "p": float(
                    sign_p(
                        np.abs(heldout_actual - heldout_baseline)
                        - np.abs(heldout_actual - heldout_predicted),
                        130105,
                    )
                ),
            },
        },
        "secondary_outputs": {
            "true_gain_mean": float(np.mean(true["gain"])),
            "permuted_gain_mean": float(np.mean(perm["gain"])),
            "blind_gain_mean": float(np.mean(blind["gain"])),
            "true_action_mismatch_vs_permuted": float(
                np.mean(np.abs(true["action"] - perm["action"]))
            ),
            "true_action_mismatch_vs_blind": float(
                np.mean(np.abs(true["action"] - blind["action"]))
            ),
            "heldout_meta_mae": float(
                np.mean(np.abs(heldout_actual - heldout_predicted))
            ),
            "heldout_constant_mae": float(
                np.mean(np.abs(heldout_actual - heldout_baseline))
            ),
            "intervention_target_error_max": float(max(intervention_errors)),
        },
        "interpretation_rule": (
            "A true-vs-permuted separation would indicate causal specificity "
            "of the action-conditioned second-order mapping. This is a "
            "computational organizational result, not a demonstration of "
            "phenomenal consciousness."
        ),
        "analysis_note": (
            "All primary contrasts are signed, elementwise, and paired by episode. "
            "Held-out MAE uses unseen transition samples."
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
    (out / "meta_observer_snapshot.json").write_text(
        json.dumps(meta.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
