from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from src.ontto.bridge import DynamicStateBridge
from src.ontto.dynamics import Config, simulate
from src.ontto.interoception import InteroceptiveProbe
from src.ontto.interoception_controller import InteroceptiveController

TRAIN_PERTURBATIONS = (0.25, 0.50, 0.75)
OOD_PERTURBATIONS = (0.35, 0.65, 0.90)
DEFAULT_EPISODES = 96
RECOVERY_HORIZON = 12
WARMUP_STEPS = 24

def sign_test_pvalue(differences: np.ndarray) -> float:
    d = np.asarray(differences, dtype=float)
    d = d[np.abs(d) > 1e-12]
    if d.size == 0:
        return 1.0
    positives = int(np.sum(d > 0.0))
    n = int(d.size)
    prob = sum(math.comb(n, k) for k in range(positives, n + 1)) / (2.0 ** n)
    return float(min(1.0, 2.0 * min(prob, 1.0 - prob + math.comb(n, positives) / (2.0 ** n))))

def warm_state(seed: int) -> tuple[float, float, float, float, int]:
    rng = np.random.default_rng(seed)
    inputs = rng.choice((-0.15, 0.0, 0.15), size=WARMUP_STEPS + 2)
    run = simulate(inputs, Config(noise_std=0.01), seed=seed)
    t = WARMUP_STEPS + 1
    return (
        float(run['state'][t - 1]),
        float(run['state'][t]),
        float(run['memory'][t]),
        float(run['pressure'][t]),
        t,
    )

def recovery_endpoint(state: float, pressure: float, baseline: float) -> float:
    return 1.0 / (1.0 + abs(float(state) - float(baseline)) + max(0.0, float(pressure)))

def run_condition(seed: int, magnitude: float, mode: str) -> dict[str, float | int | str]:
    previous, state, memory, pressure, step_index = warm_state(seed)
    baseline = state
    controller = InteroceptiveController(InteroceptiveProbe(), memory_count=6)
    bridge = DynamicStateBridge(Config(noise_std=0.01), seed=seed + 50000)
    perturbation_signal = magnitude if seed % 2 == 0 else -magnitude
    perturbed = bridge.advance(
        previous_state=previous, state=state, memory=memory, pressure=pressure,
        signal=perturbation_signal, steps=1, step_index=step_index,
    )
    previous, state, memory, pressure, step_index = (
        perturbed.previous_state, perturbed.state, perturbed.memory,
        perturbed.pressure, perturbed.steps,
    )
    pressure_trace = [pressure]
    operating_trace = []

    rng = np.random.default_rng(seed + 90000)
    for recovery_step in range(RECOVERY_HORIZON):
        if mode == 'rescue':
            active_mode = 'lesion' if recovery_step < RECOVERY_HORIZON // 2 else 'full'
        else:
            active_mode = mode

        if active_mode == 'none':
            chosen_signal = float(rng.choice((-1.0, 0.0, 1.0)))
        else:
            candidates = controller.evaluate(
                bridge, previous_state=previous, state=state, memory=memory,
                pressure=pressure, step_index=step_index, mode=active_mode,
                shuffle_seed=seed + recovery_step + 120000,
            )
            chosen_signal = float(controller.choose(candidates).signal)

        nxt = bridge.advance(
            previous_state=previous, state=state, memory=memory, pressure=pressure,
            signal=chosen_signal, steps=1, step_index=step_index,
        )
        previous, state, memory, pressure, step_index = (
            nxt.previous_state, nxt.state, nxt.memory, nxt.pressure, nxt.steps,
        )
        probe_state = controller._state_from_snapshot(nxt)
        operating = controller.probe.read(probe_state, memory_count=6).operating_condition
        operating_trace.append(float(operating))
        pressure_trace.append(float(pressure))

    return {
        'seed': int(seed),
        'magnitude': float(magnitude),
        'mode': mode,
        'ood': bool(magnitude in OOD_PERTURBATIONS),
        'final_state': float(state),
        'baseline_state': float(baseline),
        'final_pressure': float(pressure),
        'recovery_score': recovery_endpoint(state, pressure, baseline),
        'mean_pressure': float(np.mean(pressure_trace)),
        'mean_operating_condition': float(np.mean(operating_trace)),
        'final_operating_condition': float(operating_trace[-1]),
    }

def paired_difference(rows_a: list[dict], rows_b: list[dict], key: str) -> tuple[float, float]:
    by_seed_a = {int(row['seed']): row for row in rows_a}
    by_seed_b = {int(row['seed']): row for row in rows_b}
    common = sorted(set(by_seed_a) & set(by_seed_b))
    diff = np.asarray([float(by_seed_a[s][key]) - float(by_seed_b[s][key]) for s in common], dtype=float)
    return float(np.mean(diff)), sign_test_pvalue(diff)

def main() -> None:
    parser = argparse.ArgumentParser(description='I2 interoceptive regulation experiment')
    parser.add_argument('--output', default='results/i2_interoception.json')
    parser.add_argument('--episodes', type=int, default=DEFAULT_EPISODES)
    args = parser.parse_args()

    seeds = list(range(4200, 4200 + args.episodes))
    magnitudes = [TRAIN_PERTURBATIONS[i % len(TRAIN_PERTURBATIONS)] if i % 2 == 0 else OOD_PERTURBATIONS[i % len(OOD_PERTURBATIONS)] for i in range(args.episodes)]
    modes = ('full', 'none', 'shuffled', 'clamped', 'lesion', 'rescue')
    rows = {mode: [] for mode in modes}
    for seed, magnitude in zip(seeds, magnitudes):
        for mode in modes:
            rows[mode].append(run_condition(seed, magnitude, mode))

    contrasts = {}
    for control in ('none', 'shuffled', 'clamped', 'lesion'):
        mean, p = paired_difference(rows['full'], rows[control], 'recovery_score')
        contrasts[f'FULL_minus_{control}_recovery'] = {'mean': mean, 'p': p}
    rescue_all, rescue_p = paired_difference(rows['rescue'], rows['lesion'], 'recovery_score')
    contrasts['RESCUE_minus_LESION_recovery'] = {'mean': rescue_all, 'p': rescue_p}
    full_rows_ood = [r for r in rows['full'] if r['ood']]
    none_rows_ood = [r for r in rows['none'] if r['ood']]
    contrasts['FULL_minus_NONE_ood_recovery'] = dict(zip(('mean', 'p'), paired_difference(full_rows_ood, none_rows_ood, 'recovery_score')))

    report = {
        'protocol': 'I2_interoceptive_regulation',
        'version': '0.1',
        'episodes': args.episodes,
        'recovery_horizon': RECOVERY_HORIZON,
        'warmup_steps': WARMUP_STEPS,
        'train_perturbations': list(TRAIN_PERTURBATIONS),
        'ood_perturbations': list(OOD_PERTURBATIONS),
        'semantic_input_during_probe': False,
        'external_retraining_during_probe': False,
        'primary_endpoint': 'recovery_score',
        'contrasts': contrasts,
        'summary': {mode: {
            'mean_recovery_score': float(np.mean([r['recovery_score'] for r in rows[mode]])),
            'mean_pressure': float(np.mean([r['mean_pressure'] for r in rows[mode]])),
            'mean_operating_condition': float(np.mean([r['mean_operating_condition'] for r in rows[mode]])),
        } for mode in modes},
        'rows': rows,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report['contrasts'], indent=2))

if __name__ == '__main__':
    main()
