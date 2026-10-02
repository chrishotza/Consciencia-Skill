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
    SEMANTIC_TEXT,
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

SEED = 20261022
REPLICATES = 24
WARMUP_CYCLES = 24
PERMUTATIONS = 20_000
SHIFT = 1

METRICS = {
    "signed_auc_delta": "cyclic semantic phase-shift specificity gap in bridge ON-OFF signed AUC",
    "abs_auc_delta": "cyclic semantic phase-shift specificity gap in bridge ON-OFF absolute AUC",
    "future_action_change_delta": "cyclic semantic phase-shift specificity gap in bridge ON-OFF future-action change",
}


def shifted_schedule(lag: int, rotation: int, shift: int = SHIFT) -> list[str]:
    matched = build_schedule(lag, rotation)
    labels = list("ABCDEFG")
    semantic_shift = rotation + shift
    mapping = {
        label: SEMANTIC_TEXT[labels[(i + semantic_shift) % PERIOD]]
        for i, label in enumerate(labels)
    }
    shifted: list[str] = [matched[0]]
    for entry in matched[1:]:
        label, _ = entry.split(" — ", 1)
        shifted.append(f"{label} — {mapping[label]}")
    if shifted[0] != matched[0]:
        raise AssertionError("t0 must remain identical")
    if sorted(shifted[1:]) != sorted(matched[1:]):
        raise AssertionError("cyclic shift must preserve the post-t0 semantic multiset")
    return shifted


def pair_specificity(matched: dict[str, float], shifted: dict[str, float]) -> dict[str, float]:
    return {key: float(matched[key] - shifted[key]) for key in METRICS}


def run(*, seed: int, replicates: int, warmup_cycles: int, permutations: int, out: Path) -> dict:
    if seed <= 0:
        raise ValueError("seed must be positive")
    if replicates != REPLICATES:
        raise ValueError(f"I5.22 replicates are frozen at {REPLICATES}")
    if warmup_cycles != WARMUP_CYCLES:
        raise ValueError(f"I5.22 warmup is frozen at {WARMUP_CYCLES}")
    if permutations != PERMUTATIONS:
        raise ValueError(f"I5.22 uses the frozen {PERMUTATIONS}-permutation analysis")
    if SHIFT % PERIOD == 0:
        raise ValueError("SHIFT must break phase-to-content alignment")

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
        base_rows = run_condition(base_run_db, rep_seed, base_schedule, True, 0.0)
        t0_action = float(base_rows[0]["applied_signal"])
        base_run_db.unlink(missing_ok=True)

        row = {"replicate": rep, "semantic_rotation": rotation}

        for lag in LAGS:
            matched_schedule = build_schedule(lag, rotation)
            shifted = shifted_schedule(lag, rotation)

            matched_db = out / f"lag_{lag:+d}_matched_{rep}.db"
            shifted_db = out / f"lag_{lag:+d}_shifted_{rep}.db"
            off_db = out / f"lag_{lag:+d}_off_{rep}.db"
            shutil.copy2(base_db, matched_db)
            shutil.copy2(base_db, shifted_db)
            shutil.copy2(base_db, off_db)

            matched_rows = run_condition(matched_db, rep_seed, matched_schedule, True, t0_action)
            shifted_rows = run_condition(shifted_db, rep_seed, shifted, True, t0_action)
            off_rows = run_condition(off_db, rep_seed, matched_schedule, False, t0_action)

            matched_db.unlink(missing_ok=True)
            shifted_db.unlink(missing_ok=True)
            off_db.unlink(missing_ok=True)

            matched_metrics = metrics(base_rows, matched_rows)
            shifted_metrics = metrics(base_rows, shifted_rows)
            off_metrics = metrics(base_rows, off_rows)

            matched_bridge = {
                "abs_auc_delta": float(matched_metrics["state_auc_abs"] - off_metrics["state_auc_abs"]),
                "signed_auc_delta": float(matched_metrics["state_auc_signed"] - off_metrics["state_auc_signed"]),
                "future_action_change_delta": float(
                    matched_metrics["future_action_change_rate"] - off_metrics["future_action_change_rate"]
                ),
            }
            shifted_bridge = {
                "abs_auc_delta": float(shifted_metrics["state_auc_abs"] - off_metrics["state_auc_abs"]),
                "signed_auc_delta": float(shifted_metrics["state_auc_signed"] - off_metrics["state_auc_signed"]),
                "future_action_change_delta": float(
                    shifted_metrics["future_action_change_rate"] - off_metrics["future_action_change_rate"]
                ),
            }

            row[f"lag_{lag:+d}"] = {
                "matched_on": matched_metrics,
                "cyclic_shifted_on": shifted_metrics,
                "off": off_metrics,
                "matched_bridge": matched_bridge,
                "cyclic_shifted_bridge": shifted_bridge,
                "cyclic_shift_specificity_gap": pair_specificity(matched_bridge, shifted_bridge),
                "cyclic_shift_control": {
                    "shift": SHIFT,
                    "t0_self_model_match": matched_rows[0]["self_model"] == shifted_rows[0]["self_model"],
                    "t0_applied_action_match": float(matched_rows[0]["applied_signal"]) == float(shifted_rows[0]["applied_signal"]),
                    "post_t0_semantic_multiset_preserved": sorted(
                        r["self_model"] for r in matched_rows[1:]
                    ) == sorted(
                        r["self_model"] for r in shifted_rows[1:]
                    ),
                    "phase_label_sequence_preserved": [
                        r["self_model"].split(" — ", 1)[0] for r in matched_rows[1:]
                    ] == [
                        r["self_model"].split(" — ", 1)[0] for r in shifted_rows[1:]
                    ],
                },
            }

        per_rep.append(row)
        base_db.unlink(missing_ok=True)

    matrices = {
        metric: np.asarray(
            [
                [
                    per_rep[rep][f"lag_{lag:+d}"]["cyclic_shift_specificity_gap"][metric]
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
                matrix, seed=seed + 10100 + index, permutations=permutations
            ),
            "phase_specificity_interaction": phase_interaction_permutation(
                matrix, seed=seed + 10200 + index, permutations=permutations
            ),
            "max_t_multiplicity_control": max_t_adjusted_p(
                matrix, seed=seed + 10300 + index, permutations=permutations
            ),
            "per_lag_specificity_sign_flip_p": {
                str(lag): sign_flip_signed(
                    matrix[:, i],
                    seed=seed + 10400 + index * 10 + i,
                    permutations=permutations,
                )
                for i, lag in enumerate(LAGS)
            },
        }

    controls = [
        per_rep[rep][f"lag_{lag:+d}"]["cyclic_shift_control"]
        for rep in range(replicates)
        for lag in LAGS
    ]

    result = {
        "experiment": "i5_22_cyclic_semantic_phase_shift",
        "seed": seed,
        "replicates": replicates,
        "warmup_cycles": warmup_cycles,
        "cycles": CYCLES,
        "lags": list(LAGS),
        "period": PERIOD,
        "permutations": permutations,
        "shift": SHIFT,
        "primary_question": (
            "Does phase-content specificity remain when semantic transitions and phase-label "
            "sequence are preserved, but content is cyclically shifted relative to phase?"
        ),
        "control_invariant": {
            "t0_self_model_match_rate": float(np.mean([c["t0_self_model_match"] for c in controls])),
            "t0_applied_action_match_rate": float(np.mean([c["t0_applied_action_match"] for c in controls])),
            "post_t0_semantic_multiset_preserved_rate": float(
                np.mean([c["post_t0_semantic_multiset_preserved"] for c in controls])
            ),
            "phase_label_sequence_preserved_rate": float(
                np.mean([c["phase_label_sequence_preserved"] for c in controls])
            ),
        },
        "boundary": (
            "I5.22 isolates phase-content anchoring while preserving the temporal phase sequence "
            "and post-t0 semantic multiset; it does not establish consciousness or subjective experience."
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
    parser.add_argument("--out", default="results/i5_22_cyclic_semantic_phase_shift")
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
