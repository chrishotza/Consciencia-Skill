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

SEED = 20261021
REPLICATES = 24
WARMUP_CYCLES = 24
PERMUTATIONS = 20_000
LOCAL_PERMUTATION = (1, 0, 3, 4, 5, 6, 2)
METRICS = {
    "signed_auc_delta": "phase-local semantic-specificity gap in bridge ON-OFF signed AUC",
    "abs_auc_delta": "phase-local semantic-specificity gap in bridge ON-OFF absolute AUC",
    "future_action_change_delta": "phase-local semantic-specificity gap in bridge ON-OFF future-action change",
}


def permute_schedule_within_period(schedule: list[str]) -> tuple[list[str], list[list[int]]]:
    if len(schedule) != CYCLES:
        raise ValueError(f"schedule must have exactly {CYCLES} entries")
    if sorted(LOCAL_PERMUTATION) != list(range(PERIOD)):
        raise ValueError("LOCAL_PERMUTATION must be a permutation of one period")
    if any(LOCAL_PERMUTATION[i] == i for i in range(PERIOD)):
        raise AssertionError("LOCAL_PERMUTATION must be a derangement")

    permuted = [schedule[0]]
    source_indices_by_period: list[list[int]] = []
    for block_start in (1, 1 + PERIOD):
        block = schedule[block_start:block_start + PERIOD]
        if len(block) != PERIOD:
            raise ValueError("expected two complete seven-phase blocks after t0")
        indices = [block_start + index for index in LOCAL_PERMUTATION]
        permuted.extend(schedule[index] for index in indices)
        source_indices_by_period.append(indices)

    if sorted(permuted[1:]) != sorted(schedule[1:]):
        raise AssertionError("local semantic permutation must preserve the global multiset")

    for offset in (0, PERIOD):
        original = schedule[1 + offset:1 + offset + PERIOD]
        shuffled = permuted[1 + offset:1 + offset + PERIOD]
        if sorted(original) != sorted(shuffled):
            raise AssertionError("local permutation must preserve each period multiset")

    return permuted, source_indices_by_period


def pair_specificity(matched: dict[str, float], permuted: dict[str, float]) -> dict[str, float]:
    return {
        key: float(matched[key] - permuted[key])
        for key in METRICS
    }


def run(*, seed: int, replicates: int, warmup_cycles: int, permutations: int, out: Path) -> dict:
    if seed <= 0:
        raise ValueError("seed must be positive")
    if replicates != REPLICATES:
        raise ValueError(f"I5.21 replicates are frozen at {REPLICATES}")
    if warmup_cycles != WARMUP_CYCLES:
        raise ValueError(f"I5.21 warmup is frozen at {WARMUP_CYCLES}")
    if permutations != PERMUTATIONS:
        raise ValueError(f"I5.21 uses the frozen {PERMUTATIONS}-permutation analysis")

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
            permuted_schedule, source_indices_by_period = permute_schedule_within_period(schedule)

            matched_db = out / f"lag_{lag:+d}_matched_{rep}.db"
            permuted_db = out / f"lag_{lag:+d}_local_permuted_{rep}.db"
            off_db = out / f"lag_{lag:+d}_off_{rep}.db"
            shutil.copy2(base_db, matched_db)
            shutil.copy2(base_db, permuted_db)
            shutil.copy2(base_db, off_db)

            matched_rows = run_condition(matched_db, rep_seed, schedule, True, t0_action)
            permuted_rows = run_condition(
                permuted_db,
                rep_seed,
                permuted_schedule,
                True,
                t0_action,
            )
            off_rows = run_condition(off_db, rep_seed, schedule, False, t0_action)

            matched_db.unlink(missing_ok=True)
            permuted_db.unlink(missing_ok=True)
            off_db.unlink(missing_ok=True)

            matched_metrics = metrics(base_rows, matched_rows)
            permuted_metrics = metrics(base_rows, permuted_rows)
            off_metrics = metrics(base_rows, off_rows)

            matched_bridge = {
                "abs_auc_delta": float(matched_metrics["state_auc_abs"] - off_metrics["state_auc_abs"]),
                "signed_auc_delta": float(matched_metrics["state_auc_signed"] - off_metrics["state_auc_signed"]),
                "future_action_change_delta": float(
                    matched_metrics["future_action_change_rate"]
                    - off_metrics["future_action_change_rate"]
                ),
            }
            permuted_bridge = {
                "abs_auc_delta": float(permuted_metrics["state_auc_abs"] - off_metrics["state_auc_abs"]),
                "signed_auc_delta": float(permuted_metrics["state_auc_signed"] - off_metrics["state_auc_signed"]),
                "future_action_change_delta": float(
                    permuted_metrics["future_action_change_rate"]
                    - off_metrics["future_action_change_rate"]
                ),
            }

            row[f"lag_{lag:+d}"] = {
                "matched_on": matched_metrics,
                "phase_local_permuted_on": permuted_metrics,
                "off": off_metrics,
                "matched_bridge": matched_bridge,
                "phase_local_permuted_bridge": permuted_bridge,
                "phase_local_specificity_gap": pair_specificity(
                    matched_bridge,
                    permuted_bridge,
                ),
                "phase_local_permutation": {
                    "source_indices_by_period": source_indices_by_period,
                    "t0_preserved": (
                        float(matched_rows[0]["applied_signal"])
                        == float(permuted_rows[0]["applied_signal"])
                    ),
                    "semantic_multiset_preserved": sorted(
                        r["self_model"] for r in matched_rows[1:]
                    ) == sorted(
                        r["self_model"] for r in permuted_rows[1:]
                    ),
                    "period_block_multisets_preserved": all(
                        sorted(
                            matched_rows[1 + offset:1 + offset + PERIOD][i]["self_model"]
                            for i in range(PERIOD)
                        )
                        == sorted(
                            permuted_rows[1 + offset:1 + offset + PERIOD][i]["self_model"]
                            for i in range(PERIOD)
                        )
                        for offset in (0, PERIOD)
                    ),
                },
            }

        per_rep.append(row)
        base_db.unlink(missing_ok=True)

    matrices = {
        metric: np.asarray(
            [
                [
                    per_rep[rep][f"lag_{lag:+d}"]["phase_local_specificity_gap"][metric]
                    for lag in LAGS
                ]
                for rep in range(replicates)
            ],
            dtype=float,
        )
        for metric in METRICS
    }

    endpoints: dict[str, dict] = {}
    for index, metric in enumerate(METRICS):
        matrix = matrices[metric]
        endpoints[metric] = {
            "description": METRICS[metric],
            "shape": list(matrix.shape),
            "global_specificity_effect": aggregate_bridge_effect(
                matrix,
                seed=seed + 9100 + index,
                permutations=permutations,
            ),
            "phase_specificity_interaction": phase_interaction_permutation(
                matrix,
                seed=seed + 9200 + index,
                permutations=permutations,
            ),
            "max_t_multiplicity_control": max_t_adjusted_p(
                matrix,
                seed=seed + 9300 + index,
                permutations=permutations,
            ),
            "per_lag_specificity_sign_flip_p": {
                str(lag): sign_flip_signed(
                    matrix[:, i],
                    seed=seed + 9400 + index * 10 + i,
                    permutations=permutations,
                )
                for i, lag in enumerate(LAGS)
            },
        }

    t0_matches = []
    semantic_multiset_matches = []
    period_block_matches = []
    for rep in range(replicates):
        for lag in LAGS:
            control = per_rep[rep][f"lag_{lag:+d}"]["phase_local_permutation"]
            t0_matches.append(control["t0_preserved"])
            semantic_multiset_matches.append(control["semantic_multiset_preserved"])
            period_block_matches.append(control["period_block_multisets_preserved"])

    result = {
        "experiment": "i5_21_phase_local_semantic_permutation",
        "seed": seed,
        "replicates": replicates,
        "warmup_cycles": warmup_cycles,
        "cycles": CYCLES,
        "lags": list(LAGS),
        "period": PERIOD,
        "permutations": permutations,
        "local_permutation": list(LOCAL_PERMUTATION),
        "primary_question": (
            "Does semantic correspondence remain necessary when temporal scrambling "
            "is restricted within the local seven-phase cycle?"
        ),
        "control_invariant": {
            "t0_applied_action_match_rate": float(np.mean(t0_matches)),
            "semantic_multiset_preserved_rate": float(np.mean(semantic_multiset_matches)),
            "period_block_multiset_preserved_rate": float(np.mean(period_block_matches)),
        },
        "boundary": (
            "I5.21 separates phase-content correspondence from broader disruption "
            "of temporal order; it does not establish consciousness or subjective experience."
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
        default="results/i5_21_phase_local_semantic_permutation",
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
