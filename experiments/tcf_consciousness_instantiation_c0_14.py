from __future__ import annotations

import argparse
import hashlib
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
    train_self_observer,
    warmup_context,
)


PROTOCOL_VERSION = "C0.14"
STEPS = 16
RESTART_AT = 8


def prediction(observer: SelfObserver, context, signal: float) -> float:
    return float(
        observer.predict(
            previous_state=context.previous_state,
            state=context.state,
            memory=context.memory,
            pressure=context.pressure,
            last_input=signal,
            attractor_distance=abs(context.state),
            steps_delta=1,
        ).predicted_state
    )


def meta_predicted_error(
    observer: SelfObserver,
    meta: ActionConditionedMetaObserver,
    context,
    signal: float,
) -> float:
    predicted = prediction(observer, context, signal)
    return float(
        meta.predict_error(
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
    )


def choose_action(
    observer: SelfObserver,
    meta: ActionConditionedMetaObserver,
    context,
) -> float:
    candidates = [
        (
            meta_predicted_error(observer, meta, context, signal),
            abs(float(signal)),
            float(signal),
        )
        for signal in SIGNALS
    ]
    return min(candidates, key=lambda row: (row[0], row[1], row[2]))[2]


def advance(
    observer: SelfObserver,
    meta: ActionConditionedMetaObserver,
    bridge: DynamicStateBridge,
    context,
) -> tuple[object, float, float]:
    action = choose_action(observer, meta, context)
    predicted = prediction(observer, context, action)
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
    baseline_error = abs(float(snapshot.state) - float(context.state))
    gain = baseline_error - actual_error

    features = np.asarray(
        [
            1.0,
            float(context.previous_state),
            float(context.state),
            float(context.memory),
            float(context.pressure),
            float(action),
            float(abs(context.state)),
            1.0,
            float(predicted),
            float(abs(predicted - context.state)),
            float(action) * float(predicted),
            float(action) * float(abs(predicted - context.state)),
        ],
        dtype=float,
    )
    observer.observe(
        features=SelfObserver.features_for(
            previous_state=context.previous_state,
            state=context.state,
            memory=context.memory,
            pressure=context.pressure,
            last_input=action,
            attractor_distance=abs(context.state),
            steps_delta=1,
        ),
        actual_state=float(snapshot.state),
    )
    meta.observe(
        features=features,
        prediction_error=actual_error,
    )

    next_context = type(context)(
        previous_state=float(snapshot.previous_state),
        state=float(snapshot.state),
        memory=float(snapshot.memory),
        pressure=float(snapshot.pressure),
        step_index=int(snapshot.steps),
    )
    return next_context, float(action), float(gain)


def model_digest(observer: SelfObserver, meta: ActionConditionedMetaObserver) -> str:
    payload = json.dumps(
        {
            "observer": observer.to_dict(),
            "meta": meta.to_dict(),
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def run_continuous(
    observer: SelfObserver,
    meta: ActionConditionedMetaObserver,
    seed: int,
) -> dict:
    bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
    context = warmup_context(bridge, seed=seed + 1000)
    actions = []
    gains = []
    digests = []

    for _ in range(STEPS):
        context, action, gain = advance(observer, meta, bridge, context)
        actions.append(action)
        gains.append(gain)
        digests.append(model_digest(observer, meta))

    return {
        "actions": np.asarray(actions, dtype=float),
        "gains": np.asarray(gains, dtype=float),
        "digests": digests,
        "final_context": context,
    }


def run_restart(
    observer: SelfObserver,
    meta: ActionConditionedMetaObserver,
    seed: int,
) -> dict:
    bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
    context = warmup_context(bridge, seed=seed + 1000)

    actions = []
    gains = []
    digests = []

    for _ in range(RESTART_AT):
        context, action, gain = advance(observer, meta, bridge, context)
        actions.append(action)
        gains.append(gain)
        digests.append(model_digest(observer, meta))

    serialized = {
        "observer": observer.to_dict(),
        "meta": meta.to_dict(),
        "context": {
            "previous_state": context.previous_state,
            "state": context.state,
            "memory": context.memory,
            "pressure": context.pressure,
            "step_index": context.step_index,
        },
    }

    restored_observer = SelfObserver.from_dict(serialized["observer"])
    restored_meta = ActionConditionedMetaObserver.from_dict(
        serialized["meta"]
    )
    restored_context = type(context)(**serialized["context"])
    bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)

    restart_digest = model_digest(restored_observer, restored_meta)
    post_restart_actions = []
    post_restart_gains = []
    for _ in range(STEPS - RESTART_AT):
        restored_context, action, gain = advance(
            restored_observer,
            restored_meta,
            bridge,
            restored_context,
        )
        post_restart_actions.append(action)
        post_restart_gains.append(gain)

    return {
        "pre_restart_actions": np.asarray(actions, dtype=float),
        "pre_restart_gains": np.asarray(gains, dtype=float),
        "pre_restart_digests": digests,
        "restart_digest": restart_digest,
        "post_restart_actions": np.asarray(post_restart_actions, dtype=float),
        "post_restart_gains": np.asarray(post_restart_gains, dtype=float),
        "final_context": restored_context,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=64)
    parser.add_argument("--out", default="results/tcf_consciousness_instantiation_c0_14")
    args = parser.parse_args()

    out = Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    rows = []
    for index in range(args.episodes):
        seed = 140010 + index
        observer_a = train_self_observer(seed=seed, samples=256)
        meta_a = ActionConditionedMetaObserver(ridge=1e-3, max_samples=2048)

        # Calibrate the action-conditioned meta-model with the same
        # deterministic rollout used by both arms before the persistence test.
        bridge = DynamicStateBridge(DynamicsConfig(), seed=seed + 5000)
        context = warmup_context(bridge, seed=seed + 6000)
        for step in range(256):
            signal = float(SIGNALS[step % len(SIGNALS)])
            predicted = prediction(observer_a, context, signal)
            snapshot = bridge.advance(
                previous_state=context.previous_state,
                state=context.state,
                memory=context.memory,
                pressure=context.pressure,
                signal=signal,
                steps=1,
                step_index=context.step_index,
            )
            meta_a.observe(
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
            context = type(context)(
                previous_state=float(snapshot.previous_state),
                state=float(snapshot.state),
                memory=float(snapshot.memory),
                pressure=float(snapshot.pressure),
                step_index=int(snapshot.steps),
            )

        continuous = run_continuous(
            SelfObserver.from_dict(observer_a.to_dict()),
            ActionConditionedMetaObserver.from_dict(meta_a.to_dict()),
            seed=seed + 8000,
        )
        restart = run_restart(
            SelfObserver.from_dict(observer_a.to_dict()),
            ActionConditionedMetaObserver.from_dict(meta_a.to_dict()),
            seed=seed + 8000,
        )

        continuous_post = continuous["actions"][RESTART_AT:]
        continuous_post_gains = continuous["gains"][RESTART_AT:]
        restart_post = restart["post_restart_actions"]
        restart_post_gains = restart["post_restart_gains"]

        rows.append(
            {
                "action_mismatch_after_restart": float(
                    np.mean(np.abs(continuous_post - restart_post))
                ),
                "gain_mismatch_after_restart": float(
                    np.mean(np.abs(continuous_post_gains - restart_post_gains))
                ),
                "restart_digest_matches_checkpoint": (
                    restart["restart_digest"]
                    == restart["pre_restart_digests"][-1]
                ),
                "post_restart_gain_mean": float(np.mean(restart_post_gains)),
            }
        )

    action_mismatch = np.asarray(
        [row["action_mismatch_after_restart"] for row in rows],
        dtype=float,
    )
    gain_mismatch = np.asarray(
        [row["gain_mismatch_after_restart"] for row in rows],
        dtype=float,
    )

    summary = {
        "experiment": "tcf_consciousness_instantiation_c0_14",
        "protocol_version": PROTOCOL_VERSION,
        "question": (
            "Does the action-conditioned second-order self-model survive "
            "a serialization/restart boundary and continue guiding autonomous selection?"
        ),
        "matched_design": {
            "same_training_snapshot": True,
            "same_dynamic_seed_before_restart": True,
            "same_steps_before_restart": True,
            "same_serialized_observer_and_meta_model": True,
            "no_semantic_input_during_probe": True,
            "no_external_retraining_during_probe": True,
        },
        "phenomenal_consciousness_claimed": False,
        "primary_outputs": {
            "action_mismatch_after_restart": {
                "mean": float(np.mean(action_mismatch)),
                "p": float(sign_p(action_mismatch, 140101)),
            },
            "gain_mismatch_after_restart": {
                "mean": float(np.mean(gain_mismatch)),
                "p": float(sign_p(gain_mismatch, 140102)),
            },
        },
        "secondary_outputs": {
            "exact_restart_checkpoint_fraction": float(
                np.mean(
                    [
                        row["restart_digest_matches_checkpoint"]
                        for row in rows
                    ]
                )
            ),
            "post_restart_gain_mean": float(
                np.mean([row["post_restart_gain_mean"] for row in rows])
            ),
            "max_action_mismatch": float(np.max(action_mismatch)),
            "max_gain_mismatch": float(np.max(gain_mismatch)),
        },
        "interpretation_rule": (
            "Near-zero mismatch with exact model-digest recovery supports "
            "persistence of the second-order self-monitoring machinery across restart. "
            "This is a computational persistence result, not a demonstration of consciousness."
        ),
        "analysis_note": (
            "Continuous and restart arms share the same initial model and dynamics. "
            "The restart arm serializes and reloads both the first-order and action-conditioned "
            "second-order observers before continuing autonomous selection."
        ),
    }

    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
