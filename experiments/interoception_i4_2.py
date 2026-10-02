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
from src.ontto.interoceptive_meta_observer import InteroceptiveMetaObserver
from src.ontto.interoception_controller import InteroceptiveController

TRAIN_MAG = 0.50
OOD_MAGS = (0.35, 0.65, 0.90)
STEPS = 8
RESCUE_AT = STEPS // 2
WARM = 24
TRAIN_EPISODES = 128
EVAL_EPISODES = 128


def warm(seed):
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


def hidden_world_step(world, previous, state, memory, pressure, action, step):
    snap = world.advance(
        previous_state=previous,
        state=state,
        memory=memory,
        pressure=pressure,
        signal=action,
        steps=1,
        step_index=step,
    )
    risk = 0.04 + 0.09 * abs(action) + 0.06 * max(0.0, float(pressure))
    direction = 1.0 if action >= 0 else -1.0
    shifted_state = float(snap.state + direction * risk)
    return replace(
        snap,
        state=shifted_state,
        pressure=float(snap.pressure + 0.50 * risk),
        attractor_distance=abs(shifted_state - float(world.cfg.attractor)),
    )


def train_meta(episodes):
    meta = InteroceptiveMetaObserver()
    probe = InteroceptiveProbe()

    for i in range(episodes):
        seed = 10100 + i
        previous, state, memory, pressure, step = warm(seed)
        model = DynamicStateBridge(Config(noise_std=0.01), seed=seed + 40000)
        world = DynamicStateBridge(Config(noise_std=0.01), seed=seed + 70000)
        rng = np.random.default_rng(seed + 90000)
        for _ in range(STEPS):
            current = probe.read(
                InteroceptiveController._state_from_snapshot(
                    model.advance(
                        previous_state=previous,
                        state=state,
                        memory=memory,
                        pressure=pressure,
                        signal=0.0,
                        steps=1,
                        step_index=step,
                    )
                ),
                memory_count=6,
            )
            action = float(rng.choice((-1.0, 0.0, 1.0)))
            pred = model.advance(
                previous_state=previous,
                state=state,
                memory=memory,
                pressure=pressure,
                signal=action,
                steps=1,
                step_index=step,
            )
            pred_op = probe.read(
                InteroceptiveController._state_from_snapshot(pred),
                memory_count=6,
            ).operating_condition

            actual = hidden_world_step(
                world,
                previous,
                state,
                memory,
                pressure,
                action,
                step,
            )
            actual_op = probe.read(
                InteroceptiveController._state_from_snapshot(actual),
                memory_count=6,
            ).operating_condition

            meta.observe(
                snapshot=current,
                action=action,
                predicted_operating_condition=float(pred_op),
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


def choose_action(
    meta,
    current,
    model,
    previous,
    state,
    memory,
    pressure,
    step,
    policy,
    rng,
):
    rows = []
    for action in (-1.0, 0.0, 1.0):
        pred = model.advance(
            previous_state=previous,
            state=state,
            memory=memory,
            pressure=pressure,
            signal=action,
            steps=1,
            step_index=step,
        )
        pred_op = float(
            InteroceptiveProbe().read(
                InteroceptiveController._state_from_snapshot(pred),
                memory_count=6,
            ).operating_condition
        )

        if meta is None:
            utility = pred_op
            meta_error = 0.0
        else:
            meta_error = meta.predict_error(
                snapshot=current,
                action=action,
                predicted_operating_condition=pred_op,
            )
            utility = pred_op - 1.5 * meta_error

        rows.append((utility, action, pred_op, meta_error))

    first = max(rows, key=lambda x: (x[2], -abs(x[1]), -x[1]))
    if policy == "lesion":
        chosen = first
    elif policy == "random":
        chosen = rows[int(rng.integers(0, len(rows)))]
    elif policy == "rescue":
        chosen = first
    else:
        chosen = max(rows, key=lambda x: (x[0], -abs(x[1]), -x[1]))

    return chosen, first


def evaluate(meta, seed, magnitude, policy):
    previous, state, memory, pressure, step = warm(seed)
    model = DynamicStateBridge(Config(noise_std=0.01), seed=seed + 40000)
    world = DynamicStateBridge(Config(noise_std=0.01), seed=seed + 70000)
    probe = InteroceptiveProbe()
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
    )
    previous, state, memory, pressure, step = (
        perturb.previous_state,
        perturb.state,
        perturb.memory,
        perturb.pressure,
        perturb.steps,
    )

    meta_errors = []
    actual_errors = []
    recoveries = []
    shifts = 0
    active_steps = 0
    pre_rescue = []
    post_rescue = []

    for i in range(STEPS):
        current = probe.read(
            InteroceptiveController._state_from_snapshot(perturb),
            memory_count=6,
        )

        active_meta = None
        if policy == "full":
            active_meta = meta
        elif policy == "permuted":
            active_meta = meta.permuted(seed + 88000)
        elif policy == "rescue" and i >= RESCUE_AT:
            active_meta = meta

        chosen, first = choose_action(
            active_meta,
            current,
            model,
            previous,
            state,
            memory,
            pressure,
            step,
            "meta" if active_meta is not None else "lesion",
            rng,
        )

        if active_meta is not None:
            active_steps += 1
            shifts += int(chosen[1] != first[1])
            meta_errors.append(chosen[3])

        actual = hidden_world_step(
            world,
            previous,
            state,
            memory,
            pressure,
            chosen[1],
            step,
        )
        actual_op = float(
            probe.read(
                InteroceptiveController._state_from_snapshot(actual),
                memory_count=6,
            ).operating_condition
        )
        actual_error = abs(actual_op - chosen[2])
        actual_errors.append(actual_error)

        previous, state, memory, pressure, step = (
            actual.previous_state,
            actual.state,
            actual.memory,
            actual.pressure,
            actual.steps,
        )
        perturb = actual
        rec = 1.0 / (
            1.0
            + abs(float(state) - float(baseline))
            + max(0.0, float(pressure))
        )
        recoveries.append(rec)

        if policy == "rescue":
            if i < RESCUE_AT:
                pre_rescue.append(rec)
            else:
                post_rescue.append(rec)

    return {
        "seed": seed,
        "magnitude": magnitude,
        "policy": policy,
        "mean_error": float(np.mean(actual_errors)),
        "mean_recovery": float(np.mean(recoveries)),
        "final_recovery": float(recoveries[-1]),
        "meta_mae": (
            float(
                np.mean(
                    np.abs(
                        np.asarray(meta_errors)
                        - np.asarray(actual_errors[-len(meta_errors):]),
                    )
                )
            )
            if meta_errors
            else 0.0
        ),
        "policy_shift_rate": float(shifts / active_steps) if active_steps else 0.0,
        "pre_rescue_recovery": float(np.mean(pre_rescue)) if pre_rescue else 0.0,
        "post_rescue_recovery": float(np.mean(post_rescue)) if post_rescue else 0.0,
    }


def paired(a, b, key):
    aa = {r["seed"]: r for r in a}
    bb = {r["seed"]: r for r in b}
    seeds = sorted(set(aa) & set(bb))
    d = [aa[s][key] - bb[s][key] for s in seeds]
    return float(np.mean(d)), sign_p(d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="results/i4_2_interoception.json")
    ap.add_argument("--train-episodes", type=int, default=TRAIN_EPISODES)
    ap.add_argument("--eval-episodes", type=int, default=EVAL_EPISODES)
    args = ap.parse_args()

    trained = train_meta(args.train_episodes)
    payload = trained.to_dict()
    restored = InteroceptiveMetaObserver.from_dict(payload)
    serialization_exact = payload == restored.to_dict()

    rows = {p: [] for p in ("full", "lesion", "permuted", "rescue")}
    for i in range(args.eval_episodes):
        seed = 11100 + i
        magnitude = OOD_MAGS[i % len(OOD_MAGS)]
        for p in rows:
            rows[p].append(evaluate(restored, seed, magnitude, p))

    contrasts = {}
    for control in ("lesion", "permuted"):
        for metric in ("mean_error", "mean_recovery"):
            mean, p = paired(rows["full"], rows[control], metric)
            contrasts[f"FULL_minus_{control}_{metric}"] = {"mean": mean, "p": p}

    mean, p = paired(rows["rescue"], rows["lesion"], "mean_recovery")
    contrasts["RESCUE_minus_LESION_mean_recovery"] = {"mean": mean, "p": p}

    report = {
        "protocol": "I4.2_persistent_metacognitive_lesion_rescue",
        "version": "0.1",
        "train_episodes": args.train_episodes,
        "eval_episodes": args.eval_episodes,
        "train_magnitude": TRAIN_MAG,
        "ood_magnitudes": list(OOD_MAGS),
        "steps": STEPS,
        "rescue_activation_step": RESCUE_AT,
        "serialization_exact": serialization_exact,
        "primary_endpoint": "mean_recovery",
        "secondary_endpoints": [
            "mean_error",
            "final_recovery",
            "meta_mae",
            "policy_shift_rate",
            "pre_rescue_recovery",
            "post_rescue_recovery",
        ],
        "meta_samples": len(restored.targets),
        "contrasts": contrasts,
        "summary": {
            p: {
                "mean_error": float(np.mean([r["mean_error"] for r in rows[p]])),
                "mean_recovery": float(np.mean([r["mean_recovery"] for r in rows[p]])),
                "final_recovery": float(np.mean([r["final_recovery"] for r in rows[p]])),
                "meta_mae": float(np.mean([r["meta_mae"] for r in rows[p]])),
                "policy_shift_rate": float(np.mean([r["policy_shift_rate"] for r in rows[p]])),
                "pre_rescue_recovery": float(np.mean([r["pre_rescue_recovery"] for r in rows[p]])),
                "post_rescue_recovery": float(np.mean([r["post_rescue_recovery"] for r in rows[p]])),
            }
            for p in rows
        },
        "rows": rows,
        "scientific_gate": {
            "interpretation": "persistent computational metacognitive regulation only; not a consciousness claim",
            "requires": [
                "exact serialize/restore equality",
                "paired held-out evaluation",
                "first-order lesion control",
                "target-permuted control",
                "rescue after second-order restoration",
                "no online meta updates during evaluation",
            ],
        },
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"contrasts": contrasts, "summary": report["summary"]}, indent=2))


if __name__ == "__main__":
    main()
