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
from src.ontto.meta_observer import MetaSelfObserver
from src.ontto.self_observer import SelfObserver

from experiments.organism_repeated_active_continuity_v78 import (
    SIGNALS,
    apply_single_impulse,
    self_prediction_gain,
    sign_p,
    train_self_observer,
    warmup_context,
)


PROTOCOL_VERSION = "C0.12"


def first_order_prediction(
    observer: SelfObserver,
    *,
    context,
    signal: float,
) -> float:
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


def meta_features(*, context, signal: float) -> np.ndarray:
    return MetaSelfObserver.features_for(
        previous_state=context.previous_state,
        state=context.state,
        memory=context.memory,
        pressure=context.pressure,
        last_input=signal,
        attractor_distance=abs(context.state),
        steps_delta=1,
    )


def train_meta_observer(
    observer: SelfObserver,
    *,
    seed: int,
    samples: int,
) -> MetaSelfObserver:
    meta = MetaSelfObserver(ridge=1e-3, max_samples=2048)
    rng = np.random.default_rng(seed)

    for index in range(samples):
        bridge = DynamicStateBridge(DynamicsConfig(), seed=seed + 10000 + index)
        context = warmup_context(
            bridge,
            seed=seed + 20000 + index,
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
        actual_error = abs(float(snapshot.state) - predicted)
        meta.observe(
            features=meta_features(context=context, signal=signal),
            prediction_error=actual_error,
        )
    return meta


def permute_targets(meta: MetaSelfObserver, seed: int) -> MetaSelfObserver:
    payload = {
        "ridge": meta.ridge,
        "max_samples": meta.max_samples,
        "features": [row.tolist() for row in meta.features],
        "targets": list(meta.targets),
    }
    rng = np.random.default_rng(seed)
    payload["targets"] = rng.permutation(
        np.asarray(payload["targets"], dtype=float)
    ).tolist()

    shuffled = MetaSelfObserver(
        ridge=float(payload["ridge"]),
        max_samples=int(payload["max_samples"]),
    )
    for features, target in zip(payload["features"], payload["targets"]):
        shuffled.observe(
            features=np.asarray(features, dtype=float),
            prediction_error=float(target),
        )
    return shuffled


def choose_action(
    observer: SelfObserver,
    meta: MetaSelfObserver | None,
    *,
    context,
    mode: str,
    constant_error: float,
) -> float:
    candidates = []
    for signal in SIGNALS:
        if mode == "meta":
            predicted_error = meta.predict_error(
                previous_state=context.previous_state,
                state=context.state,
                memory=context.memory,
                pressure=context.pressure,
                last_input=signal,
                attractor_distance=abs(context.state),
                steps_delta=1,
            )
        elif mode == "permuted":
            predicted_error = meta.predict_error(
                previous_state=context.previous_state,
                state=context.state,
                memory=context.memory,
                pressure=context.pressure,
                last_input=signal,
                attractor_distance=abs(context.state),
                steps_delta=1,
            )
        elif mode == "blind":
            predicted_error = constant_error
        else:
            raise ValueError(f"unknown mode: {mode}")
        candidates.append(
            (
                float(predicted_error),
                abs(float(signal)),
                float(signal),
            )
        )
    return min(candidates, key=lambda row: (row[0], row[1], row[2]))[2]


def evaluate(
    observer: SelfObserver,
    meta: MetaSelfObserver | None,
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
        _, gain, next_context = self_prediction_gain(
            observer,
            bridge,
            context=context,
            signal=action,
        )
        actual_error = abs(float(next_context.state) - predicted)
        if mode == "blind":
            meta_error = constant_error
        else:
            meta_error = meta.predict_error(
                previous_state=context.previous_state,
                state=context.state,
                memory=context.memory,
                pressure=context.pressure,
                last_input=action,
                attractor_distance=abs(context.state),
                steps_delta=1,
            )
        actions.append(action)
        gains.append(gain)
        predicted_errors.append(meta_error)
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
    parser.add_argument("--meta-samples", type=int, default=512)
    parser.add_argument(
        "--out",
        default="results/tcf_consciousness_instantiation_c0_12",
    )
    args = parser.parse_args()

    out = Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    observer = train_self_observer(
        seed=120001,
        samples=args.observer_samples,
    )
    meta = train_meta_observer(
        observer,
        seed=120002,
        samples=args.meta_samples,
    )
    permuted_meta = permute_targets(meta, seed=120003)

    contexts = []
    intervention_errors = []
    for index in range(args.episodes):
        seed = 120010 + index
        bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
        pre_event = warmup_context(bridge, seed=seed + 1000)
        context, _, target_state = apply_single_impulse(
            context=pre_event,
            sign=1.0,
        )
        intervention_errors.append(
            abs(float(context.state) - float(target_state))
        )
        contexts.append(context)

    seeds = [220010 + index for index in range(args.episodes)]
    blind_error = float(np.mean(meta.targets))

    true = evaluate(
        observer,
        meta,
        contexts=contexts,
        seeds=seeds,
        mode="meta",
        constant_error=blind_error,
    )
    permuted = evaluate(
        observer,
        permuted_meta,
        contexts=contexts,
        seeds=seeds,
        mode="permuted",
        constant_error=blind_error,
    )
    blind = evaluate(
        observer,
        None,
        contexts=contexts,
        seeds=seeds,
        mode="blind",
        constant_error=blind_error,
    )

    heldout_actual = []
    heldout_predicted = []
    heldout_baseline = []
    for index in range(args.episodes):
        bridge = DynamicStateBridge(
            DynamicsConfig(),
            seed=320010 + index,
        )
        context = warmup_context(
            bridge,
            seed=330010 + index,
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
            meta_pred = meta.predict_error(
                previous_state=context.previous_state,
                state=context.state,
                memory=context.memory,
                pressure=context.pressure,
                last_input=signal,
                attractor_distance=abs(context.state),
                steps_delta=1,
            )
            heldout_actual.append(actual)
            heldout_predicted.append(meta_pred)
            heldout_baseline.append(blind_error)

    heldout_actual = np.asarray(heldout_actual, dtype=float)
    heldout_predicted = np.asarray(heldout_predicted, dtype=float)
    heldout_baseline = np.asarray(heldout_baseline, dtype=float)

    summary = {
        "experiment": "tcf_consciousness_instantiation_c0_12",
        "protocol_version": PROTOCOL_VERSION,
        "question": (
            "Does a second-order self-observer, trained only on the first-order "
            "self-model's own prediction error, become causally specific to action selection?"
        ),
        "conditions": {
            "META_TRUE": "true first-order observer + true second-order error observer",
            "META_PERMUTED": "true first-order observer + target-permuted second-order observer",
            "META_BLIND": "true first-order observer + constant second-order error baseline",
        },
        "matched_design": {
            "same_first_order_observer": True,
            "same_episode_contexts": True,
            "same_candidate_signals": True,
            "same_dynamic_bridge_seeds": True,
            "same_training_budget": True,
            "same_target_multiset_for_meta_permutation": True,
            "external_retraining_during_probe": False,
            "semantic_input_during_probe": False,
        },
        "phenomenal_consciousness_claimed": False,
        "semantic_input_during_probe": False,
        "external_retraining_during_probe": False,
        "primary_outputs": {
            "meta_action_difference_true_minus_permuted": {
                "mean": float(np.mean(true["action"] - permuted["action"])),
                "p": float(sign_p(true["action"] - permuted["action"], 120101)),
            },
            "meta_gain_difference_true_minus_permuted": {
                "mean": float(np.mean(true["gain"] - permuted["gain"])),
                "p": float(sign_p(true["gain"] - permuted["gain"], 120102)),
            },
            "meta_action_difference_true_minus_blind": {
                "mean": float(np.mean(true["action"] - blind["action"])),
                "p": float(sign_p(true["action"] - blind["action"], 120103)),
            },
            "meta_gain_difference_true_minus_blind": {
                "mean": float(np.mean(true["gain"] - blind["gain"])),
                "p": float(sign_p(true["gain"] - blind["gain"], 120104)),
            },
            "meta_prediction_error_mae_advantage_over_constant": {
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
                        120105,
                    )
                ),
            },
        },
        "secondary_outputs": {
            "true_meta_gain_mean": float(np.mean(true["gain"])),
            "permuted_meta_gain_mean": float(np.mean(permuted["gain"])),
            "blind_meta_gain_mean": float(np.mean(blind["gain"])),
            "true_action_mismatch_vs_permuted": float(
                np.mean(np.abs(true["action"] - permuted["action"]))
            ),
            "true_action_mismatch_vs_blind": float(
                np.mean(np.abs(true["action"] - blind["action"]))
            ),
            "meta_heldout_mae": float(
                np.mean(np.abs(heldout_actual - heldout_predicted))
            ),
            "constant_heldout_mae": float(
                np.mean(np.abs(heldout_actual - heldout_baseline))
            ),
            "intervention_target_error_max": float(max(intervention_errors)),
        },
        "interpretation_rule": (
            "A separation specific to the true second-order model, together with "
            "held-out prediction of first-order model error, supports second-order "
            "self-monitoring in this computational system. It does not establish "
            "phenomenal consciousness."
        ),
        "analysis_note": (
            "All primary contrasts are signed, elementwise, and paired by episode. "
            "The held-out meta-prediction comparison is evaluated on unseen transition samples."
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
        json.dumps(
            {
                "ridge": meta.ridge,
                "max_samples": meta.max_samples,
                "features": [row.tolist() for row in meta.features],
                "targets": list(meta.targets),
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
