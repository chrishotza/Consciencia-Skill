from __future__ import annotations

import argparse
import json
import math
from dataclasses import replace
from pathlib import Path

import numpy as np

from src.ontto.bridge import DynamicStateBridge
from src.ontto.dynamics import Config, simulate
from src.ontto.interoception import InteroceptiveProbe
from src.ontto.interoception_controller import InteroceptiveController
from src.ontto.interoceptive_meta_observer import InteroceptiveMetaObserver

TRAIN_MAG = 0.50
OOD_FAMILIES = ("quadratic_action", "pressure_threshold", "state_coupled")
STEPS = 8
WARM = 24
TRAIN_EPISODES = 128
EVAL_EPISODES_PER_FAMILY = 32
META_WEIGHT = 1.5


def warm(seed: int):
    rng = np.random.default_rng(seed)
    run = simulate(
        rng.choice((-0.15, 0.0, 0.15), size=WARM + 2),
        Config(noise_std=0.01),
        seed=seed,
    )
    t = WARM + 1
    return (
        float(run["state"][t - 1]),
        float(run["state"][t]),
        float(run["memory"][t]),
        float(run["pressure"][t]),
        t,
    )


def sign_p(values):
    d = np.asarray(values, float)
    d = d[np.abs(d) > 1e-12]
    if not d.size:
        return 1.0
    k = int(np.sum(d > 0))
    n = len(d)
    upper = sum(math.comb(n, i) for i in range(k, n + 1)) / 2**n
    lower = sum(math.comb(n, i) for i in range(0, k + 1)) / 2**n
    return float(min(1.0, 2.0 * min(upper, lower)))


def hidden_world_step(
    world,
    previous,
    state,
    memory,
    pressure,
    action,
    step,
    family,
):
    snap = world.advance(
        previous_state=previous,
        state=state,
        memory=memory,
        pressure=pressure,
        signal=action,
        steps=1,
        step_index=step,
    )
    a = abs(float(action))
    p = max(0.0, float(pressure))
    s = float(state)

    if family == "linear_action_pressure":
        risk = 0.04 + 0.09 * a + 0.06 * p
        direction = 1.0 if action >= 0 else -1.0
    elif family == "quadratic_action":
        risk = 0.035 + 0.075 * (a**2) + 0.055 * p
        direction = 1.0 if action >= 0 else -1.0
    elif family == "pressure_threshold":
        risk = 0.025 + 0.03 * a + 0.10 * max(0.0, p - 0.18)
        direction = -1.0 if (p > 0.30 and action != 0) else 1.0
        if action < 0:
            direction *= -1.0
    elif family == "state_coupled":
        risk = 0.02 + 0.06 * a + 0.08 * abs(s) * a + 0.04 * p
        direction = 1.0 if (s >= 0.0 and action >= 0) or (s < 0.0 and action < 0) else -1.0
    else:
        raise ValueError(f"unknown disturbance family: {family}")

    shifted_state = float(snap.state + direction * risk)
    return replace(
        snap,
        state=shifted_state,
        pressure=float(snap.pressure + 0.50 * risk),
        attractor_distance=abs(shifted_state - float(world.cfg.attractor)),
    )


def probe_snapshot(snapshot):
    return InteroceptiveProbe().read(
        InteroceptiveController._state_from_snapshot(snapshot),
        memory_count=6,
    )


def train_meta(episodes: int):
    meta = InteroceptiveMetaObserver()
    for i in range(episodes):
        seed = 12100 + i
        previous, state, memory, pressure, step = warm(seed)
        model = DynamicStateBridge(Config(noise_std=0.01), seed=seed + 40000)
        world = DynamicStateBridge(Config(noise_std=0.01), seed=seed + 70000)
        rng = np.random.default_rng(seed + 90000)
        for _ in range(STEPS):
            current_snap = model.advance(
                previous_state=previous,
                state=state,
                memory=memory,
                pressure=pressure,
                signal=0.0,
                steps=1,
                step_index=step,
            )
            current = probe_snapshot(current_snap)
            action = float(rng.choice((-1.0, 0.0, 1.0)))

            predicted = model.advance(
                previous_state=previous,
                state=state,
                memory=memory,
                pressure=pressure,
                signal=action,
                steps=1,
                step_index=step,
            )
            predicted_op = probe_snapshot(predicted).operating_condition

            actual = hidden_world_step(
                world,
                previous,
                state,
                memory,
                pressure,
                action,
                step,
                "linear_action_pressure",
            )
            actual_op = probe_snapshot(actual).operating_condition

            meta.observe(
                snapshot=current,
                action=action,
                predicted_operating_condition=float(predicted_op),
                actual_operating_condition=float(actual_op),
            )
            previous, state, memory, pressure, step = (
                actual.previous_state,
                actual.state,
                actual.memory,
                actual.pressure,
                actual.steps,
            )
    return meta


def choose_action(meta, current, model, previous, state, memory, pressure, step, policy, rng):
    rows = []
    for action in (-1.0, 0.0, 1.0):
        predicted = model.advance(
            previous_state=previous,
            state=state,
            memory=memory,
            pressure=pressure,
            signal=action,
            steps=1,
            step_index=step,
        )
        predicted_op = float(probe_snapshot(predicted).operating_condition)

        if policy == "lesion":
            meta_error = 0.0
            utility = predicted_op
        elif policy in ("permuted", "meta"):
            meta_error = meta.predict_error(
                snapshot=current,
                action=action,
                predicted_operating_condition=predicted_op,
            )
            utility = predicted_op - META_WEIGHT * meta_error
        elif policy == "random":
            meta_error = 0.0
            utility = predicted_op
        else:
            raise ValueError(f"unknown policy: {policy}")

        rows.append((utility, action, predicted_op, meta_error))

    first = max(rows, key=lambda x: (x[2], -abs(x[1]), -x[1]))
    if policy == "random":
        chosen = rows[int(rng.integers(0, len(rows)))]
    else:
        chosen = max(rows, key=lambda x: (x[0], -abs(x[1]), -x[1]))
    return chosen, first


def evaluate(meta, seed, family, magnitude, policy):
    previous, state, memory, pressure, step = warm(seed)
    model = DynamicStateBridge(Config(noise_std=0.01), seed=seed + 40000)
    world = DynamicStateBridge(Config(noise_std=0.01), seed=seed + 70000)
    rng = np.random.default_rng(seed + 120000)
    baseline = state

    perturb = hidden_world_step(
        world,
        previous,
        state,
        memory,
        pressure,
        magnitude,
        step,
        family,
    )
    previous, state, memory, pressure, step = (
        perturb.previous_state,
        perturb.state,
        perturb.memory,
        perturb.pressure,
        perturb.steps,
    )

    actual_errors = []
    meta_prediction_errors = []
    shifts = 0

    active_meta = None
    if policy == "meta":
        active_meta = meta
    elif policy == "permuted":
        active_meta = meta.permuted(seed + 88000)

    for _ in range(STEPS):
        current = probe_snapshot(perturb)
        chosen, first = choose_action(
            active_meta,
            current,
            model,
            previous,
            state,
            memory,
            pressure,
            step,
            policy,
            rng,
        )

        if policy not in ("lesion", "random"):
            meta_prediction_errors.append(chosen[3])

        shifts += int(chosen[1] != first[1])

        actual = hidden_world_step(
            world,
            previous,
            state,
            memory,
            pressure,
            chosen[1],
            step,
            family,
        )
        actual_op = float(probe_snapshot(actual).operating_condition)
        actual_errors.append(abs(actual_op - chosen[2]))

        previous, state, memory, pressure, step = (
            actual.previous_state,
            actual.state,
            actual.memory,
            actual.pressure,
            actual.steps,
        )
        perturb = actual

    actual_errors = np.asarray(actual_errors, dtype=float)
    meta_prediction_errors = np.asarray(meta_prediction_errors, dtype=float)

    return {
        "seed": seed,
        "family": family,
        "magnitude": magnitude,
        "policy": policy,
        "mean_error": float(np.mean(actual_errors)),
        "mean_prediction_mae": (
            float(
                np.mean(
                    np.abs(
                        meta_prediction_errors
                        - actual_errors[-len(meta_prediction_errors):]
                    )
                )
            )
            if len(meta_prediction_errors)
            else 0.0
        ),
        "policy_shift_rate": float(shifts / STEPS),
        "recovery": float(
            1.0 / (1.0 + abs(state - baseline) + max(0.0, pressure))
        ),
    }


def paired(a, b, key):
    aa = {(r["family"], r["seed"]): r for r in a}
    bb = {(r["family"], r["seed"]): r for r in b}
    keys = sorted(set(aa) & set(bb))
    deltas = [aa[k][key] - bb[k][key] for k in keys]
    return float(np.mean(deltas)), sign_p(deltas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="results/i4_3/summary.json")
    ap.add_argument("--train-episodes", type=int, default=TRAIN_EPISODES)
    ap.add_argument(
        "--eval-episodes-per-family",
        type=int,
        default=EVAL_EPISODES_PER_FAMILY,
    )
    args = ap.parse_args()

    trained = train_meta(args.train_episodes)
    payload = trained.to_dict()
    restored = InteroceptiveMetaObserver.from_dict(payload)
    serialization_exact = payload == restored.to_dict()

    rows = {policy: [] for policy in ("meta", "lesion", "permuted", "random")}
    for family_index, family in enumerate(OOD_FAMILIES):
        for i in range(args.eval_episodes_per_family):
            seed = 13100 + family_index * 1000 + i
            magnitude = (0.35, 0.65, 0.90)[i % 3]
            for policy in rows:
                rows[policy].append(
                    evaluate(restored, seed, family, magnitude, policy)
                )

    contrasts = {}
    for control in ("lesion", "permuted", "random"):
        for metric in ("mean_error", "recovery"):
            mean, p = paired(rows["meta"], rows[control], metric)
            contrasts[f"META_minus_{control}_{metric}_aggregate"] = {
                "mean": mean,
                "p": p,
            }

    mean, p = paired(rows["meta"], rows["permuted"], "mean_prediction_mae")
    contrasts["META_minus_PERMUTED_prediction_MAE_aggregate"] = {
        "mean": mean,
        "p": p,
    }

    family_contrasts = {}
    for family in OOD_FAMILIES:
        family_contrasts[family] = {}
        for control in ("lesion", "permuted"):
            subset_meta = [r for r in rows["meta"] if r["family"] == family]
            subset_control = [r for r in rows[control] if r["family"] == family]
            for metric in ("mean_error", "recovery"):
                mean, p = paired(subset_meta, subset_control, metric)
                family_contrasts[family][f"META_minus_{control}_{metric}"] = {
                    "mean": mean,
                    "p": p,
                }

    report = {
        "protocol": "I4.3_structural_ood_metacognitive_generalization",
        "version": "0.1",
        "question": "Does a second-order reliability model trained on one hidden-disturbance structure remain useful when the disturbance structure changes without online retraining?",
        "train_family": "linear_action_pressure",
        "ood_families": list(OOD_FAMILIES),
        "train_episodes": args.train_episodes,
        "eval_episodes_per_family": args.eval_episodes_per_family,
        "train_magnitude": TRAIN_MAG,
        "ood_magnitudes": [0.35, 0.65, 0.90],
        "steps": STEPS,
        "meta_weight": META_WEIGHT,
        "primary_endpoint": "META_minus_LESION_mean_error_aggregate",
        "secondary_endpoints": [
            "META_minus_PERMUTED_mean_error_aggregate",
            "META_minus_RANDOM_mean_error_aggregate",
            "META_minus_LESION_recovery_aggregate",
            "META_minus_PERMUTED_prediction_MAE_aggregate",
            "family_specific_contrasts",
            "policy_shift_rate",
        ],
        "serialization_exact": serialization_exact,
        "meta_samples": len(restored.targets),
        "contrasts": contrasts,
        "family_contrasts": family_contrasts,
        "summary": {
            policy: {
                "mean_error": float(np.mean([r["mean_error"] for r in rows[policy]])),
                "recovery": float(np.mean([r["recovery"] for r in rows[policy]])),
                "mean_prediction_mae": float(
                    np.mean([r["mean_prediction_mae"] for r in rows[policy]])
                ),
                "policy_shift_rate": float(
                    np.mean([r["policy_shift_rate"] for r in rows[policy]])
                ),
            }
            for policy in rows
        },
        "interpretation_boundary": (
            "A positive result supports structural OOD generalization of a computational "
            "metacognitive reliability mechanism. It does not establish subjective experience."
        ),
        "no_online_updates": True,
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"contrasts": contrasts, "family_contrasts": family_contrasts}, indent=2))


if __name__ == "__main__":
    main()
