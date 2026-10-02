from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from src.ontto.lattice import LatticeComputer, LatticeConfig


def _xor_accuracy(n_trials: int, width: int, seed: int) -> float:
    rng = np.random.default_rng(seed)
    lattice = LatticeComputer(LatticeConfig(size=max(8, width)), seed=seed)
    correct = 0
    total = 0

    for _ in range(n_trials):
        a = rng.integers(0, 2, size=width)
        b = rng.integers(0, 2, size=width)

        lattice.reset()
        lattice.encode_bits(a, row=0)
        lattice.encode_bits(b, row=1)
        lattice.local_boolean_gate(
            left_row=0,
            right_row=1,
            output_row=2,
            width=width,
            op="xor",
        )

        prediction = lattice.decode_bits(row=2, width=width)
        target = np.logical_xor(a, b).astype(int)
        correct += int(np.sum(prediction == target))
        total += width

    return float(correct / total)


def _dynamic_metrics(
    *,
    size: int,
    steps: int,
    coupling: float,
    n_trials: int,
    seed: int,
) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    retention = []
    coherence = []
    redundancy = []
    spread = []

    for i in range(n_trials):
        lattice = LatticeComputer(
            LatticeConfig(size=size, coupling=coupling),
            seed=seed + i,
        )
        pattern = rng.choice(
            [-1.0, 1.0],
            size=(size, size),
            p=[0.75, 0.25],
        )
        lattice.write(pattern)
        initial = lattice.state.copy()

        for _ in range(steps):
            lattice.step()

        corr = float(np.corrcoef(initial.ravel(), lattice.state.ravel())[0, 1])
        retention.append(corr if np.isfinite(corr) else 0.0)
        coherence.append(lattice.coherence())
        redundancy.append(lattice.redundancy())

        spread_metrics = lattice.perturbation_spread(
            row=size // 2,
            col=size // 2,
            amplitude=0.25,
            steps=5,
            threshold=1e-3,
        )
        spread.append(spread_metrics["affected_fraction"])

    return {
        "mean_retention": float(np.mean(retention)),
        "mean_coherence": float(np.mean(coherence)),
        "mean_redundancy": float(np.mean(redundancy)),
        "mean_local_perturbation_spread": float(np.mean(spread)),
    }


def _paired_delta(a: list[float], b: list[float]) -> dict[str, float]:
    delta = np.asarray(a, dtype=float) - np.asarray(b, dtype=float)
    return {
        "mean": float(np.mean(delta)),
        "std": float(np.std(delta)),
        "n": float(delta.size),
    }


def run(seed: int) -> dict[str, object]:
    size = 16
    width = 12
    trials = 64
    steps = 12

    xor_accuracy = _xor_accuracy(
        n_trials=trials,
        width=width,
        seed=seed,
    )

    full_spreads = []
    decoupled_spreads = []
    for i in range(trials):
        full = _dynamic_metrics(
            size=size,
            steps=steps,
            coupling=0.22,
            n_trials=1,
            seed=seed + i,
        )
        decoupled = _dynamic_metrics(
            size=size,
            steps=steps,
            coupling=0.0,
            n_trials=1,
            seed=seed + i,
        )
        full_spreads.append(full["mean_local_perturbation_spread"])
        decoupled_spreads.append(decoupled["mean_local_perturbation_spread"])

    spread_delta = _paired_delta(full_spreads, decoupled_spreads)

    lesion_effects = []
    for i in range(trials):
        rng = np.random.default_rng(seed + 1000 + i)
        lattice = LatticeComputer(
            LatticeConfig(size=size, coupling=0.22),
            seed=seed + 1000 + i,
        )
        pattern = rng.choice(
            [-1.0, 1.0],
            size=(size, size),
            p=[0.75, 0.25],
        )
        lattice.write(pattern)
        for _ in range(steps):
            lattice.step()

        before = lattice.state.copy()
        mask = np.zeros_like(lattice.state, dtype=bool)
        mask[6:10, 6:10] = True
        lattice.lesion(mask)
        lesion_effects.append(float(np.mean(np.abs(before - lattice.state))))

    full_metrics = _dynamic_metrics(
        size=size,
        steps=steps,
        coupling=0.22,
        n_trials=trials,
        seed=seed + 2000,
    )
    decoupled_metrics = _dynamic_metrics(
        size=size,
        steps=steps,
        coupling=0.0,
        n_trials=trials,
        seed=seed + 2000,
    )

    return {
        "protocol": "Lattice Computer v0",
        "source_basis": {
            "primary": "Grinberg-Zylberbaum, La Teoría Sintérgica, 1991, printed p. 86",
            "secondary": "Grinberg-Zylberbaum, Las Manifestaciones del Ser, pp. 54 and 67",
        },
        "parameters": {
            "size": size,
            "bit_width": width,
            "trials": trials,
            "steps": steps,
        },
        "results": {
            "xor_accuracy": xor_accuracy,
            "coupling_spread_delta_mean": spread_delta["mean"],
            "coupling_spread_delta_std": spread_delta["std"],
            "coupling_spread_n": int(spread_delta["n"]),
            "lesion_mean_absolute_effect": float(np.mean(lesion_effects)),
            "full_mean_retention": full_metrics["mean_retention"],
            "decoupled_mean_retention": decoupled_metrics["mean_retention"],
            "full_mean_coherence": full_metrics["mean_coherence"],
            "decoupled_mean_coherence": decoupled_metrics["mean_coherence"],
            "full_mean_redundancy": full_metrics["mean_redundancy"],
            "decoupled_mean_redundancy": decoupled_metrics["mean_redundancy"],
        },
        "interpretation_boundary": (
            "This protocol evaluates a distributed computational substrate "
            "inspired by the source material. It does not test subjective "
            "experience and does not validate the physical claims of Syntergic Theory."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20261002)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/lattice_v0/summary.json"),
    )
    args = parser.parse_args()

    result = run(args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
