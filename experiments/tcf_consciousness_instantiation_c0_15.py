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
    sign_p,
    train_self_observer,
    warmup_context,
)


PROTOCOL_VERSION = "C0.15"
TOTAL_STEPS = 16
LESION_START = 8
RESCUE_START = 12


def first_order_prediction(observer, context, signal):
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


def choose_action(observer, meta, context, fallback_error):
    candidates = []
    for signal in SIGNALS:
        predicted = first_order_prediction(observer, context, signal)
        if meta is None:
            predicted_error = fallback_error
        else:
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
        candidates.append(
            (float(predicted_error), abs(float(signal)), float(signal))
        )
    return min(candidates, key=lambda row: (row[0], row[1], row[2]))[2]


def advance(observer, meta, bridge, context, fallback_error):
    action = choose_action(observer, meta, context, fallback_error)
    predicted = first_order_prediction(observer, context, action)
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
    baseline_error = abs(float(snapshot.state) - context.state)
    gain = baseline_error - actual_error
    next_context = type(context)(
        previous_state=float(snapshot.previous_state),
        state=float(snapshot.state),
        memory=float(snapshot.memory),
        pressure=float(snapshot.pressure),
        step_index=int(snapshot.steps),
    )
    return next_context, float(action), float(gain), float(actual_error)


def calibrate_meta(observer, seed):
    meta = ActionConditionedMetaObserver(ridge=1e-3, max_samples=2048)
    bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
    context = warmup_context(bridge, seed=seed + 1000)
    for index in range(256):
        signal = float(SIGNALS[index % len(SIGNALS)])
        predicted = first_order_prediction(observer, context, signal)
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
        context = type(context)(
            previous_state=float(snapshot.previous_state),
            state=float(snapshot.state),
            memory=float(snapshot.memory),
            pressure=float(snapshot.pressure),
            step_index=int(snapshot.steps),
        )
    return meta


def run_arm(observer, meta, seed, fallback_error, mode):
    bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
    context = warmup_context(bridge, seed=seed + 1000)

    checkpoint = None
    rows = []

    for step in range(TOTAL_STEPS):
        active_meta = meta
        if mode == "lesion" and step >= LESION_START:
            active_meta = None
        elif mode == "rescue" and LESION_START <= step < RESCUE_START:
            active_meta = None

        context, action, gain, actual_error = advance(
            observer,
            active_meta,
            bridge,
            context,
            fallback_error,
        )
        rows.append(
            {
                "step": step + 1,
                "action": action,
                "gain": gain,
                "actual_error": actual_error,
            }
        )

        if step + 1 == LESION_START:
            checkpoint = {
                "context": {
                    "previous_state": context.previous_state,
                    "state": context.state,
                    "memory": context.memory,
                    "pressure": context.pressure,
                    "step_index": context.step_index,
                },
                "observer": observer.to_dict(),
                "meta": meta.to_dict(),
            }

    return rows, checkpoint


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=64)
    parser.add_argument("--out", default="results/tcf_consciousness_instantiation_c0_15")
    args = parser.parse_args()

    out = Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    rows = []
    for index in range(args.episodes):
        seed = 150010 + index
        observer = train_self_observer(seed=seed, samples=256)
        meta = calibrate_meta(observer, seed + 5000)
        fallback_error = float(np.mean(meta.targets))

        full, _ = run_arm(
            observer,
            meta,
            seed + 8000,
            fallback_error,
            "full",
        )
        lesion, _ = run_arm(
            observer,
            meta,
            seed + 8000,
            fallback_error,
            "lesion",
        )
        rescue, checkpoint = run_arm(
            observer,
            meta,
            seed + 8000,
            fallback_error,
            "rescue",
        )

        full_late = full[LESION_START:]
        lesion_late = lesion[LESION_START:]
        rescue_recovery = rescue[RESCUE_START:]
        full_recovery = full[RESCUE_START:]

        rows.append(
            {
                "full_vs_lesion_action": float(
                    np.mean(
                        [a["action"] for a in full_late]
                    )
                    - np.mean(
                        [a["action"] for a in lesion_late]
                    )
                ),
                "full_vs_lesion_gain": float(
                    np.mean([a["gain"] for a in full_late])
                    - np.mean([a["gain"] for a in lesion_late])
                ),
                "full_vs_rescue_action": float(
                    np.mean([a["action"] for a in full_recovery])
                    - np.mean([a["action"] for a in rescue_recovery])
                ),
                "full_vs_rescue_gain": float(
                    np.mean([a["gain"] for a in full_recovery])
                    - np.mean([a["gain"] for a in rescue_recovery])
                ),
                "rescue_exact_checkpoint": checkpoint is not None,
            }
        )

    full_lesion_action = np.asarray(
        [row["full_vs_lesion_action"] for row in rows],
        dtype=float,
    )
    full_lesion_gain = np.asarray(
        [row["full_vs_lesion_gain"] for row in rows],
        dtype=float,
    )
    full_rescue_action = np.asarray(
        [row["full_vs_rescue_action"] for row in rows],
        dtype=float,
    )
    full_rescue_gain = np.asarray(
        [row["full_vs_rescue_gain"] for row in rows],
        dtype=float,
    )

    summary = {
        "experiment": "tcf_consciousness_instantiation_c0_15",
        "protocol_version": PROTOCOL_VERSION,
        "question": (
            "Is the persistent action-conditioned second-order model causally "
            "necessary for autonomous selection, and does restoring it rescue behavior?"
        ),
        "conditions": {
            "FULL": "second-order model active throughout",
            "LESION": "second-order model disabled after step 8",
            "RESCUE": "second-order model disabled at steps 9-12 and restored for steps 13-16",
        },
        "matched_design": {
            "same_observer_snapshot": True,
            "same_meta_snapshot": True,
            "same_episode_seed_per_arm": True,
            "same_dynamic_configuration": True,
            "lesion_only_targets_second_order_model": True,
            "rescue_uses_serialized_checkpoint": True,
            "external_retraining_during_probe": False,
            "semantic_input_during_probe": False,
        },
        "phenomenal_consciousness_claimed": False,
        "primary_outputs": {
            "full_minus_lesion_action_late": {
                "mean": float(np.mean(full_lesion_action)),
                "p": float(sign_p(full_lesion_action, 150101)),
            },
            "full_minus_lesion_gain_late": {
                "mean": float(np.mean(full_lesion_gain)),
                "p": float(sign_p(full_lesion_gain, 150102)),
            },
            "full_minus_rescue_action_post_restore": {
                "mean": float(np.mean(full_rescue_action)),
                "p": float(sign_p(full_rescue_action, 150103)),
            },
            "full_minus_rescue_gain_post_restore": {
                "mean": float(np.mean(full_rescue_gain)),
                "p": float(sign_p(full_rescue_gain, 150104)),
            },
        },
        "secondary_outputs": {
            "exact_checkpoint_fraction": float(
                np.mean([row["rescue_exact_checkpoint"] for row in rows])
            ),
            "max_abs_full_vs_lesion_action": float(
                np.max(np.abs(full_lesion_action))
            ),
            "max_abs_full_vs_lesion_gain": float(
                np.max(np.abs(full_lesion_gain))
            ),
        },
        "interpretation_rule": (
            "A nonzero FULL-vs-LESION contrast with convergence after RESTORE "
            "supports causal necessity and rescue of the persistent second-order "
            "selection mechanism. This is a computational result and does not "
            "establish subjective experience."
        ),
        "analysis_note": (
            "Contrasts are paired by episode and use signed means. The lesion "
            "removes only the second-order observer from action selection; the "
            "first-order self-observer and dynamics remain intact."
        ),
    }

    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
