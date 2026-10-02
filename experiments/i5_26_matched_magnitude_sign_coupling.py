from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from experiments.i5_17_phase_resolved_bridge_mediation_map import LAGS
from experiments.i5_23_cyclic_shift_sweep import METRICS, SHIFTS

SEED = 20261026
PERMUTATIONS = 20_000
MAGNITUDES = (1, 2, 3)


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


def sign_flip_p(values: np.ndarray, seed: int, permutations: int) -> dict:
    values = np.asarray(values, dtype=float)
    observed = float(values.mean())
    rng = np.random.default_rng(seed)
    signs = rng.choice((-1.0, 1.0), size=(permutations, values.size))
    null = (signs * values[None, :]).mean(axis=1)
    p = float(
        (np.count_nonzero(np.abs(null) >= abs(observed)) + 1)
        / (permutations + 1)
    )
    return {
        "observed_mean": observed,
        "permutation_p": p,
        "permutations": permutations,
    }


def matched_magnitude_cells(matrix: np.ndarray, magnitude: int) -> tuple[np.ndarray, np.ndarray]:
    shift_index = {shift: i for i, shift in enumerate(SHIFTS)}
    lag_index = {lag: i for i, lag in enumerate(LAGS)}

    opposite_sign = np.stack(
        [
            matrix[:, shift_index[-magnitude], lag_index[magnitude]],
            matrix[:, shift_index[magnitude], lag_index[-magnitude]],
        ],
        axis=1,
    ).mean(axis=1)

    same_sign = np.stack(
        [
            matrix[:, shift_index[-magnitude], lag_index[-magnitude]],
            matrix[:, shift_index[magnitude], lag_index[magnitude]],
        ],
        axis=1,
    ).mean(axis=1)

    return opposite_sign, same_sign


def max_t_across_magnitudes(
    contrasts: np.ndarray,
    seed: int,
    permutations: int,
) -> dict:
    values = np.asarray(contrasts, dtype=float)
    if values.ndim != 2 or values.shape[1] != len(MAGNITUDES):
        raise ValueError("contrasts must have shape (replicate, 3)")

    observed = values.mean(axis=0)
    rng = np.random.default_rng(seed)
    signs = rng.choice(
        (-1.0, 1.0),
        size=(permutations, values.shape[0], 1),
    )
    null = (signs * values[None, ...]).mean(axis=1)
    max_null = np.max(np.abs(null), axis=1)

    adjusted = np.asarray(
        [
            (np.count_nonzero(max_null >= abs(value)) + 1)
            / (permutations + 1)
            for value in observed
        ],
        dtype=float,
    )
    global_p = float(
        (np.count_nonzero(max_null >= np.max(np.abs(observed))) + 1)
        / (permutations + 1)
    )

    return {
        "observed_mean_by_magnitude": observed.tolist(),
        "max_t_adjusted_p_by_magnitude": adjusted.tolist(),
        "global_any_magnitude_p": global_p,
        "permutations": permutations,
    }


def run(input_path: Path, seed: int, permutations: int, out: Path) -> dict:
    summary = json.loads(input_path.read_text(encoding="utf-8"))

    if summary.get("experiment") != "i5_23_cyclic_shift_sweep":
        raise ValueError("input must be the frozen I5.23 summary")
    if summary.get("shifts") != list(SHIFTS) or summary.get("lags") != list(LAGS):
        raise ValueError("I5.23 axes do not match the frozen protocol")

    invariants = summary.get("control_invariant", {})
    for key in (
        "t0_self_model_match",
        "t0_applied_action_match",
        "post_t0_semantic_content_multiset_preserved",
        "phase_label_sequence_preserved",
    ):
        if float(invariants.get(key, 0.0)) != 1.0:
            raise ValueError(f"frozen invariant {key} is not 100%")

    endpoints = {}

    for index, metric in enumerate(METRICS):
        matrix = extract_matrix(summary, metric)
        contrasts = []
        by_magnitude = {}

        for magnitude in MAGNITUDES:
            opposite, same = matched_magnitude_cells(matrix, magnitude)
            contrast = opposite - same
            contrasts.append(contrast)
            by_magnitude[str(magnitude)] = {
                "opposite_sign_mean": float(opposite.mean()),
                "same_sign_mean": float(same.mean()),
                "contrast_mean": float(contrast.mean()),
                "sign_flip": sign_flip_p(
                    contrast,
                    seed + 1000 + index * 10 + magnitude,
                    permutations,
                ),
            }

        contrast_matrix = np.stack(contrasts, axis=1)

        endpoints[metric] = {
            "shape": list(matrix.shape),
            "by_magnitude": by_magnitude,
            "max_t_across_magnitudes": max_t_across_magnitudes(
                contrast_matrix,
                seed + 2000 + index,
                permutations,
            ),
            "global_p": sign_flip_p(
                contrast_matrix.mean(axis=1),
                seed + 3000 + index,
                permutations,
            ),
        }

    result = {
        "experiment": "i5_26_matched_magnitude_sign_coupling",
        "source_experiment": "i5_23_cyclic_shift_sweep",
        "source_seed": summary["seed"],
        "replicates": summary["replicates"],
        "magnitudes": list(MAGNITUDES),
        "permutations": permutations,
        "new_trajectories_collected": False,
        "primary_question": (
            "At matched absolute shift and lag magnitudes, does opposite-sign coupling "
            "(lag=-shift) differ from same-sign coupling (lag=shift)?"
        ),
        "boundary": (
            "I5.26 is a frozen-data matched-magnitude sign-coupling control. "
            "It does not establish consciousness, subjective experience, or a unique mechanism."
        ),
        "endpoints": endpoints,
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
    parser.add_argument("--out", default="results/i5_26_matched_magnitude_sign_coupling")
    args = parser.parse_args()
    result = run(Path(args.input), args.seed, args.permutations, Path(args.out))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
