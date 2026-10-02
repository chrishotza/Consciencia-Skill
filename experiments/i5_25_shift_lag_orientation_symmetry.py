from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from experiments.i5_17_phase_resolved_bridge_mediation_map import LAGS
from experiments.i5_23_cyclic_shift_sweep import METRICS, SHIFTS

SEED = 20261025
PERMUTATIONS = 20_000


def extract_matrix(summary: dict, metric: str) -> np.ndarray:
    rows = summary["per_replicate"]
    return np.asarray(
        [
            [
                [
                    rows[rep][f"lag_{lag:+d}"][str(shift)]["specificity_gap"][metric]
                    for lag in LAGS
                ]
                for shift in SHIFTS
            ]
            for rep in range(len(rows))
        ],
        dtype=float,
    )


def sign_flip_mean_p(values: np.ndarray, seed: int, permutations: int) -> dict:
    values = np.asarray(values, dtype=float)
    if values.ndim != 1:
        raise ValueError("values must be one-dimensional")
    observed = float(values.mean())
    rng = np.random.default_rng(seed)
    signs = rng.choice((-1.0, 1.0), size=(permutations, values.size))
    null = (signs * values[None, :]).mean(axis=1)
    p = float((np.count_nonzero(np.abs(null) >= abs(observed)) + 1) / (permutations + 1))
    return {
        "observed_mean": observed,
        "permutation_p": p,
        "permutations": permutations,
    }


def max_t_pair_symmetry(matrix: np.ndarray, seed: int, permutations: int) -> dict:
    index = {shift: i for i, shift in enumerate(SHIFTS)}
    lag_index = {lag: i for i, lag in enumerate(LAGS)}
    pairs = []
    seen = set()

    for shift in SHIFTS:
        for lag in LAGS:
            key = (shift, lag)
            partner = (-shift, -lag)
            if key in seen or partner in seen:
                continue
            pairs.append((key, partner))
            seen.add(key)
            seen.add(partner)

    pair_values = []
    labels = []
    for (shift_a, lag_a), (shift_b, lag_b) in pairs:
        a = matrix[:, index[shift_a], lag_index[lag_a]]
        b = matrix[:, index[shift_b], lag_index[lag_b]]
        pair_values.append(a - b)
        labels.append(f"{shift_a}:{lag_a}__vs__{shift_b}:{lag_b}")

    pair_matrix = np.stack(pair_values, axis=1)
    observed = pair_matrix.mean(axis=0)

    rng = np.random.default_rng(seed)
    signs = rng.choice((-1.0, 1.0), size=(permutations, matrix.shape[0], 1))
    null_means = (signs * pair_matrix[None, ...]).mean(axis=1)
    max_null = np.max(np.abs(null_means), axis=1)

    adjusted = np.asarray(
        [
            (np.count_nonzero(max_null >= abs(value)) + 1) / (permutations + 1)
            for value in observed
        ],
        dtype=float,
    )

    global_p = float(
        (np.count_nonzero(max_null >= np.max(np.abs(observed))) + 1)
        / (permutations + 1)
    )

    return {
        "pair_count": len(labels),
        "pair_labels": labels,
        "observed_pair_means": observed.tolist(),
        "max_t_adjusted_p": adjusted.tolist(),
        "global_any_orientation_pair_p": global_p,
        "permutations": permutations,
    }


def compensatory_diagonal_contrast(matrix: np.ndarray, seed: int, permutations: int) -> dict:
    shift_index = {shift: i for i, shift in enumerate(SHIFTS)}
    lag_index = {lag: i for i, lag in enumerate(LAGS)}

    diagonal = np.stack(
        [matrix[:, shift_index[shift], lag_index[-shift]] for shift in SHIFTS],
        axis=1,
    )
    all_cells = matrix.reshape(matrix.shape[0], -1)
    diag_mean = diagonal.mean(axis=1)
    non_diag_values = []
    for sidx, shift in enumerate(SHIFTS):
        for lidx, lag in enumerate(LAGS):
            if lag != -shift:
                non_diag_values.append(matrix[:, sidx, lidx])
    non_diag_mean = np.stack(non_diag_values, axis=1).mean(axis=1)

    replicate_contrast = diag_mean - non_diag_mean
    out = sign_flip_mean_p(replicate_contrast, seed, permutations)
    out.update(
        {
            "diagonal_cell_count": len(SHIFTS),
            "off_diagonal_cell_count": len(SHIFTS) * (len(LAGS) - 1),
            "replicate_contrast_values": replicate_contrast.tolist(),
        }
    )
    return out


def run(input_path: Path, seed: int, permutations: int, out: Path) -> dict:
    summary = json.loads(input_path.read_text(encoding="utf-8"))
    if summary.get("experiment") != "i5_23_cyclic_shift_sweep":
        raise ValueError("input must be the frozen I5.23 summary")
    if summary.get("shifts") != list(SHIFTS) or summary.get("lags") != list(LAGS):
        raise ValueError("I5.23 shift/lag axes do not match the frozen protocol")

    invariants = summary.get("control_invariant", {})
    for key in (
        "t0_self_model_match",
        "t0_applied_action_match",
        "post_t0_semantic_content_multiset_preserved",
        "phase_label_sequence_preserved",
    ):
        if float(invariants.get(key, 0.0)) != 1.0:
            raise ValueError(f"frozen I5.23 invariant {key} is not 100%")

    endpoints = {}
    raw_ps = []

    for idx, metric in enumerate(METRICS):
        matrix = extract_matrix(summary, metric)
        orientation = max_t_pair_symmetry(matrix, seed + 100 + idx, permutations)
        diagonal = compensatory_diagonal_contrast(matrix, seed + 200 + idx, permutations)

        endpoints[metric] = {
            "shape": list(matrix.shape),
            "orientation_symmetry": orientation,
            "compensatory_diagonal_contrast": diagonal,
        }
        raw_ps.extend(
            [
                orientation["global_any_orientation_pair_p"],
                diagonal["permutation_p"],
            ]
        )

    adjusted_global = [min(1.0, p * len(raw_ps)) for p in raw_ps]

    result = {
        "experiment": "i5_25_shift_lag_orientation_symmetry",
        "source_experiment": "i5_23_cyclic_shift_sweep",
        "source_seed": summary["seed"],
        "replicates": summary["replicates"],
        "shifts": list(SHIFTS),
        "lags": list(LAGS),
        "permutations": permutations,
        "new_trajectories_collected": False,
        "primary_question": (
            "Is the I5.23 shift×lag structure asymmetric under simultaneous sign reversal, "
            "and is the compensatory lag=-shift diagonal enriched beyond the remaining cells?"
        ),
        "multiplicity": {
            "tests": 6,
            "method": "Bonferroni across orientation and diagonal tests for all three endpoints",
        },
        "endpoints": endpoints,
        "global_test_order": [
            "signed_auc_orientation",
            "signed_auc_diagonal",
            "abs_auc_orientation",
            "abs_auc_diagonal",
            "future_action orientation",
            "future_action diagonal",
        ],
        "bonferroni_adjusted_global_p": adjusted_global,
        "boundary": (
            "I5.25 is a frozen-data orientation/symmetry control on I5.23. "
            "It does not establish consciousness, subjective experience, or a unique mechanism."
        ),
    }

    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="results/i5_23_cyclic_shift_sweep/summary.json")
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--permutations", type=int, default=PERMUTATIONS)
    parser.add_argument("--out", default="results/i5_25_shift_lag_orientation_symmetry")
    args = parser.parse_args()
    result = run(Path(args.input), args.seed, args.permutations, Path(args.out))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
