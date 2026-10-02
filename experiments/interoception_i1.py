from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from src.ontto.dynamics import Config, simulate
from src.ontto.interoception import InteroceptiveProbe
from src.ontto.storage import OntologicalState

TRAIN_MAGNITUDES = (0.25, 0.50, 0.75)
OOD_MAGNITUDES = (0.35, 0.65, 0.90)
DEFAULT_TRAIN_EPISODES = 192
DEFAULT_TEST_EPISODES = 96
SNAPSHOT_INDEX = 40
RECOVERY_HORIZON = 8

def sign_test_pvalue(differences: np.ndarray) -> float:
    d = np.asarray(differences, dtype=float)
    d = d[np.abs(d) > 1e-12]
    if d.size == 0:
        return 1.0
    positives = int(np.sum(d > 0.0))
    n = int(d.size)
    prob = sum(math.comb(n, k) for k in range(positives, n + 1)) / (2.0**n)
    p = 2.0 * min(prob, 1.0 - prob + math.comb(n, positives) / (2.0**n))
    return float(min(1.0, p))

def ridge_fit(x: np.ndarray, y: np.ndarray, ridge: float = 1e-3) -> np.ndarray:
    x1 = np.column_stack([np.ones(len(x)), x])
    reg = ridge * np.eye(x1.shape[1])
    reg[0, 0] = ridge * 0.1
    return np.linalg.solve(x1.T @ x1 + reg, x1.T @ y)

def ridge_predict(beta: np.ndarray, x: np.ndarray) -> np.ndarray:
    return np.column_stack([np.ones(len(x)), x]) @ beta

def episode(seed: int, magnitude: float) -> tuple[np.ndarray, float]:
    rng = np.random.default_rng(seed)
    length = SNAPSHOT_INDEX + RECOVERY_HORIZON + 2
    inputs = np.zeros(length, dtype=float)
    warm_inputs = rng.choice((-0.15, 0.0, 0.15), size=SNAPSHOT_INDEX - 10)
    inputs[2:SNAPSHOT_INDEX - 8] = warm_inputs
    inputs[SNAPSHOT_INDEX] = float(magnitude) * (1.0 if seed % 2 == 0 else -1.0)
    run = simulate(inputs, Config(noise_std=0.01), seed=seed)
    t = SNAPSHOT_INDEX
    state = float(run['state'][t])
    previous = float(run['state'][t - 1])
    prediction_error = abs(state - previous)
    confidence = 1.0 / (1.0 + prediction_error)
    ont_state = OntologicalState(
        dynamic_state=state,
        dynamic_prev_state=previous,
        dynamic_memory=float(run['memory'][t]),
        dynamic_pressure=float(run['pressure'][t]),
        dynamic_attractor_distance=abs(state),
        dynamic_last_input=float(inputs[t]),
        self_prediction_error=prediction_error,
        self_prediction_confidence=confidence,
    )
    features = np.asarray(list(InteroceptiveProbe().describe(ont_state).values()), dtype=float)
    future_state = float(run['state'][t + RECOVERY_HORIZON])
    future_pressure = float(run['pressure'][t + RECOVERY_HORIZON])
    recovery = 1.0 / (1.0 + abs(future_state) + future_pressure)
    return features, float(recovery)

def make_dataset(seeds: list[int], magnitudes: tuple[float, ...]) -> tuple[np.ndarray, np.ndarray]:
    xs: list[np.ndarray] = []
    ys: list[float] = []
    for i, seed in enumerate(seeds):
        x, y = episode(seed, magnitudes[i % len(magnitudes)])
        xs.append(x)
        ys.append(y)
    return np.vstack(xs), np.asarray(ys, dtype=float)

def evaluate_model(beta: np.ndarray, x: np.ndarray, y: np.ndarray) -> dict[str, float]:
    pred = ridge_predict(beta, x)
    return {
        'mae': float(np.mean(np.abs(pred - y))),
        'rmse': float(np.sqrt(np.mean((pred - y) ** 2))),
    }

def main() -> None:
    parser = argparse.ArgumentParser(description='I1 interoceptive self-assessment experiment')
    parser.add_argument('--output', default='results/i1_interoception.json')
    parser.add_argument('--train-episodes', type=int, default=DEFAULT_TRAIN_EPISODES)
    parser.add_argument('--test-episodes', type=int, default=DEFAULT_TEST_EPISODES)
    args = parser.parse_args()
    train_seeds = list(range(1100, 1100 + args.train_episodes))
    id_seeds = list(range(2100, 2100 + args.test_episodes))
    ood_seeds = list(range(3100, 3100 + args.test_episodes))
    x_train, y_train = make_dataset(train_seeds, TRAIN_MAGNITUDES)
    x_id, y_id = make_dataset(id_seeds, TRAIN_MAGNITUDES)
    x_ood, y_ood = make_dataset(ood_seeds, OOD_MAGNITUDES)
    beta_full = ridge_fit(x_train, y_train)
    beta_raw = ridge_fit(x_train[:, [0]], y_train)
    rng = np.random.default_rng(7711)
    beta_permuted = ridge_fit(x_train, rng.permutation(y_train))
    constant = float(np.mean(y_train))
    full_id = evaluate_model(beta_full, x_id, y_id)
    full_ood = evaluate_model(beta_full, x_ood, y_ood)
    raw_id = evaluate_model(beta_raw, x_id[:, [0]], y_id)
    raw_ood = evaluate_model(beta_raw, x_ood[:, [0]], y_ood)
    perm_id = evaluate_model(beta_permuted, x_id, y_id)
    perm_ood = evaluate_model(beta_permuted, x_ood, y_ood)
    constant_id_mae = float(np.mean(np.abs(constant - y_id)))
    constant_ood_mae = float(np.mean(np.abs(constant - y_ood)))
    full_ood_errors = np.abs(ridge_predict(beta_full, x_ood) - y_ood)
    raw_ood_errors = np.abs(ridge_predict(beta_raw, x_ood[:, [0]]) - y_ood)
    perm_ood_errors = np.abs(ridge_predict(beta_permuted, x_ood) - y_ood)
    report = {
        'protocol': 'I1_interoceptive_self_assessment',
        'version': '0.1',
        'train_magnitudes': list(TRAIN_MAGNITUDES),
        'ood_magnitudes': list(OOD_MAGNITUDES),
        'snapshot_index': SNAPSHOT_INDEX,
        'recovery_horizon': RECOVERY_HORIZON,
        'train_episodes': args.train_episodes,
        'test_episodes_per_split': args.test_episodes,
        'semantic_input_during_probe': False,
        'models': {
            'interoceptive': {'in_domain': full_id, 'ood': full_ood},
            'raw_state': {'in_domain': raw_id, 'ood': raw_ood},
            'target_permuted': {'in_domain': perm_id, 'ood': perm_ood},
            'constant': {'in_domain_mae': constant_id_mae, 'ood_mae': constant_ood_mae},
        },
        'primary_contrasts': {
            'raw_minus_intero_mae_ood': float(raw_ood['mae'] - full_ood['mae']),
            'permuted_minus_intero_mae_ood': float(perm_ood['mae'] - full_ood['mae']),
            'constant_minus_intero_mae_ood': float(constant_ood_mae - full_ood['mae']),
            'paired_p_raw_ood': sign_test_pvalue(raw_ood_errors - full_ood_errors),
            'paired_p_permuted_ood': sign_test_pvalue(perm_ood_errors - full_ood_errors),
        },
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
