from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import numpy as np

from experiments.i5_17_phase_resolved_bridge_mediation_map import (
    CYCLES,
    LAGS,
    PERIOD,
    build_schedule,
    metrics,
    run_condition,
    sign_flip_signed,
    warmup,
)
from experiments.i5_18_global_phase_bridge_interaction import (
    aggregate_bridge_effect,
    max_t_adjusted_p,
    phase_interaction_permutation,
)

SEED = 20261020
REPLICATES = 24
WARMUP_CYCLES = 24
PERMUTATIONS = 20_000

METRICS = {
    "signed_auc_delta": "semantic-specificity gap in bridge ON-OFF signed AUC",
    "abs_auc_delta": "semantic-specificity gap in bridge ON-OFF absolute AUC",
    "future_action_change_delta": "semantic-specificity gap in bridge ON-OFF future-action change",
}


def permute_schedule(schedule: list[str]) -> tuple[list[str], list[int]]:
    if len(schedule) != CYCLES:
        raise ValueError(f"schedule must have exactly {CYCLES} entries")

    tail = list(range(1, len(schedule)))
    permutation = list(reversed(tail))
    if any(permutation[i] == tail[i] for i in range(len(tail))):
        raise AssertionError("semantic permutation must be a derangement")

    permuted = [schedule[0]] + [schedule[index] for index in permutation]
    if sorted(permuted[1:]) != sorted(schedule[1:]):
        raise AssertionError("semantic permutation must preserve the information multiset")
    return permuted, permutation


def pair_specificity(
    matched: dict[str, float],
    permuted: dict[str, float],
) -> dict[str, float]:
    return {
        key: float(matched[key] - permuted[key])
        for key in METRICS
    }


def run(
    *,
    seed: int,
    replicates: int,
    warmup_cycles: int,
    permutations: int,
    out: Path,
) -> dict:
    if seed <= 0:
        raise ValueError("seed must be positive")
    if replicates != REPLICATES:
        raise ValueError(f"I5.20 replicates are frozen at {REPLICATES}")
    if warmup_cycles != WARMUP_CYCLES:
        raise ValueError(f"I5.20 warmup is frozen at {WARMUP_CYCLES}")
    if permutations != PERMUTATIONS:
        raise ValueError(f"I5.20 uses the frozen {PERMUTATIONS}-permutation analysis")
    out.mkdir(parents=True, exist_ok=True)

    per_rep: list[dict] = []

    for rep in range(replicates):
        rep_seed = seed + rep
        rotation = rep % PERIOD
        base_schedule = build_schedule(0, rotation)

        base_db = out / f"base_{rep}.db"
        warmup(base_db, rep_seed, warmup_cycles)

        base_run_db = out / f"base_run_{rep}.db"
        shutil.copy2(base_db, base_run_db)
        base_rows = run_condition(
            base_run_db,
            rep_seed,
            base_schedule,
            True,
            0.0,
        )
        t0_action = float(base_rows[0]["applied_signal"])
        base_run_db.unlink(missing_ok=True)

        row = {
            "replicate": rep,
            "semantic_rotation": rotation,
        }

        for lag in LAGS:
            schedule = build_schedule(lag, rotation)
            permuted_schedule, permutation = permute_schedule(schedule)

            matched_db = out / f"lag_{lag:+d}_matched_{rep}.db"
            permuted_db = out / f"lag_{lag:+d}_permuted_{rep}.db"
            off_db = out / f"lag_{lag:+d}_off_{rep}.db"
            shutil.copy2(base_db, matched_db)
            shutil.copy2(base_db, permuted_db)
            shutil.copy2(base_db, off_db)

            matched_rows = run_condition(
                matched_db,
                rep_seed,
                schedule,
                True,
                t0_action,
            )
            permuted_rows = run_condition(
                permuted_db,
                rep_seed,
                permuted_schedule,
                True,
                t0_action,
            )
            off_rows = run_condition(
                off_db,
                rep_seed,
                schedule,
                False,
                t0_action,
            )

            matched_db.unlink(missing_ok=True)
            permuted_db.unlink(missing_ok=True)
            off_db.unlink(missing_ok=True)

            matched_metrics = metrics(base_rows, matched_rows)
            permuted_metrics = metrics(base_rows, permuted_rows)
            off_metrics = metrics(base_rows, off_rows)

            matched_bridge = {
                "abs_auc_delta": float(
                    matched_metrics["state_auc_abs"] - off_metrics["state_auc_abs"]
                ),
                "signed_auc_delta": float(
                    matched_metrics["state_auc_signed"]
                    - off_metrics["state_auc_signed"]
                ),
                "future_action_change_delta": float(
                    matched_metrics["future_action_change_rate"]
                    - off_metrics["future_action_change_rate"]
                ),
            }
            permuted_bridge = {
                "abs_auc_delta": float(
                    permuted_metrics["state_auc_abs"] - off_metrics["state_auc_abs"]
                ),
                "signed_auc_delta": float(
                    permuted_metrics["state_auc_signed"]
                    - off_metrics["state_auc_signed"]
                ),
                "future_action_change_delta": float(
                    permuted_metrics["future_action_change_rate"]
                    - off_metrics["future_action_change_rate"]
                ),
            }

            semantic_gap = {
                key: float(matched_bridge[key] - permuted_bridge[key])
                for key in METRICS
            }

            row[f"lag_{lag:+d}"] = {
                "matched_on": matched_metrics,
                "permuted_on": permuted_metrics,
                "off": off_metrics,
                "matched_bridge": matched_bridge,
                "permuted_bridge": permuted_bridge,
                "semantic_specificity_gap": semantic_gap,
                "semantic_permutation": {
                    "permutation_indices_after_t0": permutation,
                    "t0_preserved": (
                        float(matched_rows[0]["applied_signal"])
                        == float(permuted_rows[0]["applied_signal"])
                    ),
                    "semantic_multiset_preserved": sorted(
                        r["self_model"] for r in matched_rows[1:]
                    )
                    == sorted(r["self_model"] for r in permuted_rows[1:]),
                },
            }

        per_rep.append(row)
        base_db.unlink(missing_ok=True)

    matrices: dict[str, np.ndarray] = {}
    for metric in METRICS:
        matrices[metric] = np.asarray(
            [
                [
                    per_rep[rep][f"lag_{lag:+d}"]["semantic_specificity_gap"][metric]
                    for lag in LAGS
                ]
                for rep in range(replicates)
            ],
            dtype=float,
        )

    endpoints: dict[str, dict] = {}
    for index, metric in enumerate(METRICS):
        matrix = matrices[metric]
        endpoints[metric] = {
            "description": METRICS[metric],
            "shape": list(matrix.shape),
            "global_specificity_effect": aggregate_bridge_effect(
                matrix,
                seed=seed + 8100 + index,
                permutations=permutations,
            ),
            "phase_specificity_interaction": phase_interaction_permutation(
                matrix,
                seed=seed + 8200 + index,
                permutations=permutations,
            ),
            "max_t_multiplicity_control": max_t_adjusted_p(
                matrix,
                seed=seed + 8300 + index,
                permutations=permutations,
            ),
            "per_lag_specificity_sign_flip_p": {
                str(lag): sign_flip_signed(
                    matrix[:, i],
                    seed=seed + 8400 + index * 10 + i,
                    permutations=permutations,
                )
                for i, lag in enumerate(LAGS)
            },
        }

    t0_match_rates = []
    multiset_match_rates = []
    for rep in range(replicates):
        for lag in LAGS:
            control = per_rep[rep][f"lag_{lag:+d}"]["semantic_permutation"]
            t0_match_rates.append(control["t0_preserved"])
            multiset_match_rates.append(control["semantic_multiset_preserved"])

    result = {
        "experiment": "i5_20_semantic_permutation_specificity",
        "seed": seed,
        "replicates": replicates,
        "warmup_cycles": warmup_cycles,
        "cycles": CYCLES,
        "lags": list(LAGS),
        "period": PERIOD,
        "permutations": permutations,
        "counterbalancing": (
            "seven cyclic semantic-label rotations across replicates, "
            "with a fixed within-run temporal derangement after t0"
        ),
        "primary_question": (
            "Does the replicated bridge ON-OFF effect depend on the temporal "
            "correspondence of semantic self-model content rather than bridge activation alone?"
        ),
        "control_invariant": {
            "t0_applied_action_match_rate": float(np.mean(t0_match_rates)),
            "semantic_multiset_preserved_rate": float(np.mean(multiset_match_rates)),
            "note": (
                "The permuted condition uses exactly the same SELF_MODEL strings "
                "as the matched condition after t0, but in a different temporal order."
            ),
        },
        "boundary": (
            "I5.20 is a semantic-correspondence specificity control. "
            "It does not establish consciousness or subjective experience."
        ),
        "endpoints": endpoints,
        "per_replicate": per_rep,
    }
    (out / "summary.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--replicates", type=int, default=REPLICATES)
    parser.add_argument("--warmup", type=int, default=WARMUP_CYCLES)
    parser.add_argument("--permutations", type=int, default=PERMUTATIONS)
    parser.add_argument(
        "--out",
        default="results/i5_20_semantic_permutation_specificity",
    )
    args = parser.parse_args()

    result = run(
        seed=args.seed,
        replicates=args.replicates,
        warmup_cycles=args.warmup,
        permutations=args.permutations,
        out=Path(args.out),
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
