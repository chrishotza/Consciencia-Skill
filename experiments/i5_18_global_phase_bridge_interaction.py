from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

LAGS = (-3, -2, -1, 1, 2, 3)
PERMUTATIONS = 20_000
METRICS = {
    "signed_auc_delta": "bridge ON - OFF signed state AUC",
    "abs_auc_delta": "bridge ON - OFF absolute state AUC",
    "future_action_change_delta": "bridge ON - OFF future-action change rate",
}


def load_matrix(summary_path: Path, metric: str) -> np.ndarray:
    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    rows = payload.get("per_replicate", [])
    if not rows:
        raise ValueError("I5.17 summary contains no per_replicate rows")
    matrix = np.asarray(
        [
            [float(row[f"lag_{lag:+d}_bridge"][metric]) for lag in LAGS]
            for row in rows
        ],
        dtype=float,
    )
    if matrix.ndim != 2 or matrix.shape[1] != len(LAGS):
        raise ValueError(f"expected matrix with {len(LAGS)} lag columns")
    return matrix


def max_t_adjusted_p(
    matrix: np.ndarray,
    seed: int,
    permutations: int = PERMUTATIONS,
) -> dict:
    observed_means = matrix.mean(axis=0)
    observed_abs = np.abs(observed_means)
    rng = np.random.default_rng(seed)
    signs = rng.choice(
        (-1.0, 1.0),
        size=(permutations, matrix.shape[0], 1),
    )
    null_means = (signs * matrix[None, :, :]).mean(axis=1)
    max_abs = np.max(np.abs(null_means), axis=1)
    adjusted = {
        str(lag): float(
            (np.count_nonzero(max_abs >= observed_abs[i]) + 1)
            / (permutations + 1)
        )
        for i, lag in enumerate(LAGS)
    }
    return {
        "observed_mean": {
            str(lag): float(observed_means[i])
            for i, lag in enumerate(LAGS)
        },
        "uncorrected_two_sided_sign_flip_p": {
            str(lag): float(
                (
                    np.count_nonzero(
                        np.abs(null_means[:, i]) >= observed_abs[i]
                    )
                    + 1
                )
                / (permutations + 1)
            )
            for i, lag in enumerate(LAGS)
        },
        "max_t_adjusted_p": adjusted,
        "global_any_lag_p": float(
            (np.count_nonzero(max_abs >= np.max(observed_abs)) + 1)
            / (permutations + 1)
        ),
        "permutations": permutations,
    }


def phase_interaction_permutation(
    matrix: np.ndarray,
    seed: int,
    permutations: int = PERMUTATIONS,
) -> dict:
    observed_means = matrix.mean(axis=0)
    grand_mean = float(observed_means.mean())
    observed_stat = float(np.sum((observed_means - grand_mean) ** 2))

    rng = np.random.default_rng(seed)
    keys = rng.random((permutations, matrix.shape[0], matrix.shape[1]))
    permutations_idx = np.argsort(keys, axis=2)
    expanded = np.broadcast_to(matrix, (permutations, *matrix.shape))
    permuted = np.take_along_axis(expanded, permutations_idx, axis=2)
    permuted_means = permuted.mean(axis=1)
    permuted_grand = permuted_means.mean(axis=1)
    null_stat = np.sum(
        (permuted_means - permuted_grand[:, None]) ** 2,
        axis=1,
    )
    p = float(
        (np.count_nonzero(null_stat >= observed_stat) + 1)
        / (permutations + 1)
    )

    return {
        "lag_means": {
            str(lag): float(observed_means[i])
            for i, lag in enumerate(LAGS)
        },
        "grand_mean": grand_mean,
        "observed_interaction_statistic": observed_stat,
        "permutation_p": p,
        "permutations": permutations,
        "null": (
            "lag labels are permuted independently within each replicate; "
            "the bridge ON/OFF pairing is retained."
        ),
    }


def aggregate_bridge_effect(matrix: np.ndarray, seed: int, permutations: int) -> dict:
    replicate_means = matrix.mean(axis=1)
    observed = float(replicate_means.mean())
    rng = np.random.default_rng(seed)
    signs = rng.choice((-1.0, 1.0), size=(permutations, matrix.shape[0]))
    null = np.abs((signs * replicate_means[None, :]).mean(axis=1))
    p = float((np.count_nonzero(null >= abs(observed)) + 1) / (permutations + 1))
    return {
        "mean_across_lags": observed,
        "replicate_mean_sign_flip_p": p,
        "replicate_count": int(matrix.shape[0]),
        "permutations": permutations,
    }


def analyze(summary_path: Path, out: Path, permutations: int = PERMUTATIONS) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    source = json.loads(summary_path.read_text(encoding="utf-8"))
    if source.get("experiment") != "i5_17_phase_resolved_bridge_mediation_map":
        raise ValueError("input must be an I5.17 summary")

    results: dict[str, dict] = {}
    for index, metric in enumerate(METRICS):
        matrix = load_matrix(summary_path, metric)
        results[metric] = {
            "description": METRICS[metric],
            "shape": list(matrix.shape),
            "max_t_multiplicity_control": max_t_adjusted_p(
                matrix,
                seed=int(source["seed"]) + 7100 + index,
                permutations=permutations,
            ),
            "global_phase_interaction": phase_interaction_permutation(
                matrix,
                seed=int(source["seed"]) + 7200 + index,
                permutations=permutations,
            ),
            "global_bridge_effect": aggregate_bridge_effect(
                matrix,
                seed=int(source["seed"]) + 7300 + index,
                permutations=permutations,
            ),
        }

    result = {
        "experiment": "i5_18_global_phase_bridge_interaction",
        "source_experiment": source["experiment"],
        "source_seed": source["seed"],
        "source_replicates": source["replicates"],
        "source_cycles": source["cycles"],
        "lags": list(LAGS),
        "permutations": permutations,
        "data_status": "frozen I5.17 per-replicate bridge deltas; no new experimental trajectories collected",
        "primary_question": (
            "Does the bridge ON-OFF effect vary by temporal phase, "
            "after a global interaction test and multiplicity-controlled lag contrasts?"
        ),
        "analysis_boundary": (
            "Statistical follow-up of I5.17. Per-lag p-values from I5.17 are not "
            "reinterpreted as globally significant; I5.18 supplies the planned "
            "global phase-interaction and max-T correction."
        ),
        "metrics": results,
    }
    (out / "summary.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--input",
        default="results/i5_17_phase_resolved_bridge_mediation_map/summary.json",
    )
    ap.add_argument(
        "--out",
        default="results/i5_18_global_phase_bridge_interaction",
    )
    ap.add_argument("--permutations", type=int, default=PERMUTATIONS)
    args = ap.parse_args()

    result = analyze(
        Path(args.input),
        Path(args.out),
        args.permutations,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
