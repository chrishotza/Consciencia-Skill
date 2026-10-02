from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from experiments.i5_23_cyclic_shift_sweep import METRICS, SHIFTS
from experiments.i5_17_phase_resolved_bridge_mediation_map import LAGS

SEED = 20261024
PERMUTATIONS = 20_000


def interaction_statistic(matrix: np.ndarray) -> float:
    values = np.asarray(matrix, dtype=float)
    if values.ndim != 3:
        raise ValueError("matrix must have shape (replicate, shift, lag)")
    cell_means = values.mean(axis=0)
    row_means = cell_means.mean(axis=1, keepdims=True)
    col_means = cell_means.mean(axis=0, keepdims=True)
    grand_mean = float(cell_means.mean())
    interaction = cell_means - row_means - col_means + grand_mean
    return float(np.sum(interaction * interaction))


def interaction_permutation_test(
    matrix: np.ndarray,
    *,
    seed: int,
    permutations: int,
) -> dict:
    values = np.asarray(matrix, dtype=float)
    if values.ndim != 3:
        raise ValueError("matrix must have shape (replicate, shift, lag)")
    replicates, n_shifts, n_lags = values.shape
    if n_shifts != len(SHIFTS) or n_lags != len(LAGS):
        raise ValueError("matrix axes must match frozen I5.23 shift/lag dimensions")
    if replicates < 2:
        raise ValueError("at least two replicates are required")

    observed = interaction_statistic(values)
    rng = np.random.default_rng(seed)
    null = np.empty(permutations, dtype=float)

    for p in range(permutations):
        permuted = np.empty_like(values)
        for rep in range(replicates):
            row_perm = rng.permutation(n_shifts)
            col_perm = rng.permutation(n_lags)
            permuted[rep] = values[rep][row_perm][:, col_perm]
        null[p] = interaction_statistic(permuted)

    p_value = float((np.count_nonzero(null >= observed) + 1) / (permutations + 1))
    null_mean = float(null.mean())
    null_std = float(null.std(ddof=1)) if permutations > 1 else 0.0
    standardized = (
        float((observed - null_mean) / null_std)
        if null_std > 0
        else None
    )

    return {
        "observed_interaction_statistic": observed,
        "permutation_p": p_value,
        "null_mean": null_mean,
        "null_std": null_std,
        "standardized_excess": standardized,
        "permutations": permutations,
        "null": (
            "Within each replicate, shift and lag labels are independently "
            "permuted, preserving the replicate's full 6x6 value surface."
        ),
    }


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


def run(
    *,
    input_path: Path,
    permutations: int,
    seed: int,
    out: Path,
) -> dict:
    summary = json.loads(input_path.read_text(encoding="utf-8"))

    if summary.get("experiment") != "i5_23_cyclic_shift_sweep":
        raise ValueError("input must be the frozen I5.23 cyclic-shift sweep summary")
    if summary.get("shifts") != list(SHIFTS):
        raise ValueError("I5.23 shift set does not match the frozen protocol")
    if summary.get("lags") != list(LAGS):
        raise ValueError("I5.23 lag set does not match the frozen protocol")
    invariant = summary.get("control_invariant", {})
    required_invariants = (
        "t0_self_model_match",
        "t0_applied_action_match",
        "post_t0_semantic_content_multiset_preserved",
        "phase_label_sequence_preserved",
    )
    for key in required_invariants:
        if float(invariant.get(key, 0.0)) != 1.0:
            raise ValueError(f"I5.23 input invariant {key} is not 100%")

    endpoints: dict[str, dict] = {}
    raw_p = []

    for index, metric in enumerate(METRICS):
        matrix = extract_matrix(summary, metric)
        result = interaction_permutation_test(
            matrix,
            seed=seed + index,
            permutations=permutations,
        )
        endpoints[metric] = {
            "shape": list(matrix.shape),
            **result,
            "bonferroni_p_across_three_endpoints": float(
                min(1.0, result["permutation_p"] * len(METRICS))
            ),
        }
        raw_p.append(result["permutation_p"])

    result = {
        "experiment": "i5_24_global_shift_lag_interaction",
        "source_experiment": "i5_23_cyclic_shift_sweep",
        "source_summary": str(input_path),
        "source_seed": summary["seed"],
        "replicates": summary["replicates"],
        "shifts": list(SHIFTS),
        "lags": list(LAGS),
        "permutations": permutations,
        "new_trajectories_collected": False,
        "primary_question": (
            "Does the specificity surface contain a global shift×lag interaction "
            "beyond additive shift and lag main effects?"
        ),
        "multiplicity": {
            "endpoint_count": len(METRICS),
            "method": "Bonferroni across the three endpoint-specific global interaction tests",
        },
        "endpoints": endpoints,
        "boundary": (
            "I5.24 is a statistical follow-up on frozen I5.23 data. "
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
    parser.add_argument(
        "--input",
        default="results/i5_23_cyclic_shift_sweep/summary.json",
    )
    parser.add_argument("--permutations", type=int, default=PERMUTATIONS)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument(
        "--out",
        default="results/i5_24_global_shift_lag_interaction",
    )
    args = parser.parse_args()
    result = run(
        input_path=Path(args.input),
        permutations=args.permutations,
        seed=args.seed,
        out=Path(args.out),
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
