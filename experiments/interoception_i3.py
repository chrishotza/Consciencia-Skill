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

TRAIN_MAGNITUDE = 0.50
OOD_MAGNITUDES = (0.35, 0.65, 0.90)
EVENT_COUNT = 3
RECOVERY_STEPS = 8
WARMUP_STEPS = 24
DEFAULT_EPISODES = 96

def sign_test_pvalue(values: list[float] | np.ndarray) -> float:
    d = np.asarray(values, dtype=float)
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
    return (float(run['state'][t - 1]), float(run['state'][t]), float(run['memory'][t]), float(run['pressure'][t]), t)

def recovery_score(state: float, pressure: float, baseline: float) -> float:
    return 1.0 / (1.0 + abs(float(state) - float(baseline)) + max(0.0, float(pressure)))

def run_condition(seed: int, magnitude: float, mode: str) -> dict:
    previous, state, memory, pressure, step_index = warm_state(seed)
    bridge = DynamicStateBridge(Config(noise_std=0.01), seed=seed + 60000)
    controller = InteroceptiveController(InteroceptiveProbe(), memory_count=6)
    rng = np.random.default_rng(seed + 80000)
    event_scores: list[float] = []
    overshoots: list[float] = []
    operating_scores: list[float] = []
    baselines: list[float] = []

    for event_index in range(EVENT_COUNT):
        baseline = state
        baselines.append(float(baseline))
        sign = 1.0 if ((seed + event_index) % 2 == 0) else -1.0
        event_magnitude = magnitude if event_index == 0 else magnitude * (1.0 + 0.10 * event_index)
        perturb = bridge.advance(
            previous_state=previous, state=state, memory=memory, pressure=pressure,
            signal=sign * event_magnitude, steps=1, step_index=step_index
        )
        previous, state, memory, pressure, step_index = (
            perturb.previous_state, perturb.state, perturb.memory, perturb.pressure, perturb.steps
        )
        peak_abs = abs(state - baseline)
        for recovery_step in range(RECOVERY_STEPS):
            if mode == 'rescue':
                active_mode = 'lesion' if event_index == 0 and recovery_step < RECOVERY_STEPS // 2 else 'full'
            else:
                active_mode = mode

            if active_mode == 'none':
                action = float(rng.choice((-1.0, 0.0, 1.0)))
            else:
                candidates = controller.evaluate(
                    bridge, previous_state=previous, state=state, memory=memory,
                    pressure=pressure, signals=(-1.0, 0.0, 1.0), step_index=step_index,
                    mode=active_mode, shuffle_seed=seed + event_index * 1000 + recovery_step + 90000
                )
                action = float(controller.choose(candidates).signal)

            nxt = bridge.advance(
                previous_state=previous, state=state, memory=memory, pressure=pressure,
                signal=action, steps=1, step_index=step_index
            )
            previous, state, memory, pressure, step_index = (
                nxt.previous_state, nxt.state, nxt.memory, nxt.pressure, nxt.steps
            )
            peak_abs = max(peak_abs, abs(state - baseline))
            probe_state = controller._state_from_snapshot(nxt)
            operating_scores.append(float(controller.probe.read(probe_state, memory_count=6).operating_condition))

        event_scores.append(recovery_score(state, pressure, baseline))
        overshoots.append(float(peak_abs))

    return {
        'seed': int(seed),
        'mode': mode,
        'magnitude': float(magnitude),
        'ood': bool(magnitude in OOD_MAGNITUDES),
        'event_recovery_scores': event_scores,
        'event_overshoots': overshoots,
        'mean_recovery': float(np.mean(event_scores)),
        'final_recovery': float(event_scores[-1]),
        'mean_overshoot': float(np.mean(overshoots)),
        'max_overshoot': float(np.max(overshoots)),
        'mean_operating_condition': float(np.mean(operating_scores)),
        'baseline_states': baselines,
    }

def paired(rows_a: list[dict], rows_b: list[dict], key_fn) -> tuple[float, float]:
    a = {int(row['seed']): row for row in rows_a}
    b = {int(row['seed']): row for row in rows_b}
    seeds = sorted(set(a) & set(b))
    diffs = np.asarray([key_fn(a[s]) - key_fn(b[s]) for s in seeds], dtype=float)
    return float(np.mean(diffs)), sign_test_pvalue(diffs)

def main() -> None:
    parser = argparse.ArgumentParser(description='I3 repeated interoceptive perturbation/recovery')
    parser.add_argument('--output', default='results/i3_interoception.json')
    parser.add_argument('--episodes', type=int, default=DEFAULT_EPISODES)
    args = parser.parse_args()
    seeds = list(range(5200, 5200 + args.episodes))
    magnitudes = [TRAIN_MAGNITUDE if i % 2 == 0 else OOD_MAGNITUDES[i % len(OOD_MAGNITUDES)] for i in range(args.episodes)]
    modes = ('full', 'none', 'shuffled', 'clamped', 'lesion', 'rescue')
    rows = {mode: [] for mode in modes}
    for seed, magnitude in zip(seeds, magnitudes):
        for mode in modes:
            rows[mode].append(run_condition(seed, magnitude, mode))

    contrasts = {}
    for control in ('none', 'shuffled', 'clamped', 'lesion'):
        mean, p = paired(rows['full'], rows[control], lambda row: row['mean_recovery'])
        contrasts[f'FULL_minus_{control}_mean_recovery'] = {'mean': mean, 'p': p}
        mean_over, p_over = paired(rows['full'], rows[control], lambda row: -row['mean_overshoot'])
        contrasts[f'FULL_minus_{control}_reduced_overshoot'] = {'mean': mean_over, 'p': p_over}
    rescue_mean, rescue_p = paired(rows['rescue'], rows['lesion'], lambda row: row['mean_recovery'])
    contrasts['RESCUE_minus_LESION_mean_recovery'] = {'mean': rescue_mean, 'p': rescue_p}
    full_ood = [row for row in rows['full'] if row['ood']]
    none_ood = [row for row in rows['none'] if row['ood']]
    ood_mean, ood_p = paired(full_ood, none_ood, lambda row: row['mean_recovery'])
    contrasts['FULL_minus_NONE_ood_mean_recovery'] = {'mean': ood_mean, 'p': ood_p}

    report = {
        'protocol': 'I3_repeated_interoceptive_perturbation_recovery',
        'version': '0.1',
        'episodes': args.episodes,
        'event_count': EVENT_COUNT,
        'recovery_steps_per_event': RECOVERY_STEPS,
        'train_magnitude': TRAIN_MAGNITUDE,
        'ood_magnitudes': list(OOD_MAGNITUDES),
        'semantic_input_during_probe': False,
        'external_retraining_during_probe': False,
        'primary_endpoint': 'mean_recovery',
        'secondary_endpoints': ['final_recovery', 'mean_overshoot', 'max_overshoot', 'mean_operating_condition'],
        'contrasts': contrasts,
        'summary': {mode: {
            'mean_recovery': float(np.mean([r['mean_recovery'] for r in rows[mode]])),
            'final_recovery': float(np.mean([r['final_recovery'] for r in rows[mode]])),
            'mean_overshoot': float(np.mean([r['mean_overshoot'] for r in rows[mode]])),
        } for mode in modes},
        'rows': rows,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report['contrasts'], indent=2))

if __name__ == '__main__':
    main()
