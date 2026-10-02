from __future__ import annotations

import argparse
import json
from pathlib import Path

from experiments.i5_17_phase_resolved_bridge_mediation_map import run as run_i517
from experiments.i5_18_global_phase_bridge_interaction import analyze as analyze_i518

INDEPENDENT_SEED = 20261019
SOURCE_SEED = 20261017
REPLICATES = 24
WARMUP_CYCLES = 24
CYCLES = 15
PERMUTATIONS = 20_000


def validate_frozen_protocol(
    *,
    seed: int,
    replicates: int,
    warmup_cycles: int,
    cycles: int,
    permutations: int,
) -> None:
    if seed == SOURCE_SEED:
        raise ValueError("I5.19 requires an independent seed")
    if replicates != REPLICATES:
        raise ValueError(f"I5.19 replicates are frozen at {REPLICATES}")
    if warmup_cycles != WARMUP_CYCLES:
        raise ValueError(f"I5.19 warmup is frozen at {WARMUP_CYCLES}")
    if cycles != CYCLES:
        raise ValueError(f"I5.19 cycle horizon is frozen at {CYCLES}")
    if permutations != PERMUTATIONS:
        raise ValueError(f"I5.18 analysis is frozen at {PERMUTATIONS} permutations")


def assemble_summary(raw_summary: dict, analysis_summary: dict, seed: int) -> dict:
    return {
        "experiment": "i5_19_independent_bridge_replication",
        "seed": seed,
        "source_i5_17_seed": raw_summary["seed"],
        "source_i5_18_source_seed": analysis_summary["source_seed"],
        "replicates": raw_summary["replicates"],
        "warmup_cycles": raw_summary["warmup_cycles"],
        "cycles": raw_summary["cycles"],
        "lags": raw_summary["lags"],
        "permutations": analysis_summary["permutations"],
        "protocol_status": (
            "Independent-seed replication of the frozen I5.17 acquisition "
            "protocol followed by the frozen I5.18 global analysis; "
            "endpoints and multiplicity procedure unchanged."
        ),
        "new_trajectories_collected": True,
        "analysis_summary": analysis_summary["metrics"],
    }


def run_replication(
    *,
    seed: int,
    replicates: int,
    warmup_cycles: int,
    cycles: int,
    permutations: int,
    out: Path,
) -> dict:
    validate_frozen_protocol(
        seed=seed,
        replicates=replicates,
        warmup_cycles=warmup_cycles,
        cycles=cycles,
        permutations=permutations,
    )
    out.mkdir(parents=True, exist_ok=True)

    raw_out = out / "i5_17_replication"
    analysis_out = out / "i5_18_analysis"

    raw_summary = run_i517(
        seed=seed,
        replicates=replicates,
        warmup_cycles=warmup_cycles,
        cycles=cycles,
        out=raw_out,
    )
    analysis_summary = analyze_i518(
        raw_out / "summary.json",
        analysis_out,
        permutations=permutations,
    )
    result = assemble_summary(raw_summary, analysis_summary, seed)
    (out / "summary.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=INDEPENDENT_SEED)
    parser.add_argument("--replicates", type=int, default=REPLICATES)
    parser.add_argument("--warmup", type=int, default=WARMUP_CYCLES)
    parser.add_argument("--cycles", type=int, default=CYCLES)
    parser.add_argument("--permutations", type=int, default=PERMUTATIONS)
    parser.add_argument(
        "--out",
        default="results/i5_19_independent_bridge_replication",
    )
    args = parser.parse_args()

    result = run_replication(
        seed=args.seed,
        replicates=args.replicates,
        warmup_cycles=args.warmup,
        cycles=args.cycles,
        permutations=args.permutations,
        out=Path(args.out),
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
