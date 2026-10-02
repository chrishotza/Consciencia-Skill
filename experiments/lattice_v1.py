from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
from src.ontto.lattice import LatticeComputer, LatticeConfig

def _pattern(rng, roi):
    return rng.choice([-1.0, 1.0], size=(roi, roi), p=[0.75, 0.25])

def _write_roi(lattice, pattern, top, left):
    field = np.zeros_like(lattice.state)
    h, w = pattern.shape
    field[top:top+h, left:left+w] = pattern
    lattice.write(field)

def _score(lattice, pattern, top, left):
    h, w = pattern.shape
    observed = lattice.state[top:top+h, left:left+w]
    a = observed.ravel() - float(np.mean(observed))
    b = pattern.ravel() - float(np.mean(pattern))
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    return 0.0 if denom < 1e-12 else float(np.clip(np.dot(a, b) / denom, -1.0, 1.0))

def _run_trace(*, size, coupling, noise_std, pattern, seed, delays, perturb_at, perturb_amplitude):
    roi = pattern.shape[0]
    top = (size - roi) // 2
    left = (size - roi) // 2
    lattice = LatticeComputer(LatticeConfig(size=size, coupling=coupling, noise_std=noise_std), seed=seed)
    _write_roi(lattice, pattern, top, left)
    scores = {"0": _score(lattice, pattern, top, left)}
    perturb_cell = (max(0, top - 1), left + roi // 2)
    for step in range(1, max(delays) + 1):
        if perturb_at is not None and step == perturb_at:
            r, c = perturb_cell
            lattice.state[r, c] += perturb_amplitude
        lattice.step()
        if step in delays:
            scores[str(step)] = _score(lattice, pattern, top, left)
    return {"scores": scores, "final_summary": lattice.summary()}

def _paired_stats(a, b):
    delta = np.asarray(a) - np.asarray(b)
    return {"mean_delta": float(np.mean(delta)), "sd_delta": float(np.std(delta, ddof=1)), "n": int(delta.size)}

def run(seed):
    size, roi, trials, noise_std = 16, 7, 128, 0.01
    delays = [0, 1, 2, 4, 8, 16]
    perturb_at, perturb_amplitude = 4, 0.50
    coupled, decoupled = 0.22, 0.0
    buckets = {k: {d: [] for d in delays} for k in ["cc", "cp", "dc", "dp"]}
    for i in range(trials):
        trial_seed = seed + i
        pattern = _pattern(np.random.default_rng(trial_seed), roi)
        arms = [
            ("cc", coupled, None),
            ("cp", coupled, perturb_at),
            ("dc", decoupled, None),
            ("dp", decoupled, perturb_at),
        ]
        for key, coupling, perturb in arms:
            result = _run_trace(size=size, coupling=coupling, noise_std=noise_std, pattern=pattern, seed=trial_seed, delays=delays, perturb_at=perturb, perturb_amplitude=perturb_amplitude)
            for d in delays:
                buckets[key][d].append(result["scores"][str(d)])
    retention, perturbation_loss, coupling_delta = {}, {}, {}
    for d in delays:
        c = np.asarray(buckets["cc"][d], dtype=float)
        cp = np.asarray(buckets["cp"][d], dtype=float)
        dc = np.asarray(buckets["dc"][d], dtype=float)
        retention[str(d)] = {"coupled_mean": float(np.mean(c)), "coupled_sd": float(np.std(c, ddof=1)), "decoupled_mean": float(np.mean(dc)), "decoupled_sd": float(np.std(dc, ddof=1))}
        perturbation_loss[str(d)] = _paired_stats(c, cp)
        coupling_delta[str(d)] = _paired_stats(c, dc)
    x = np.asarray(delays, dtype=float)
    y = np.asarray([retention[str(d)]["coupled_mean"] for d in delays], dtype=float)
    auc = float(np.trapezoid(y, x) / (x[-1] - x[0]))
    return {"protocol":"Lattice Computer v1 — temporal trace retention under perturbation","parameters":{"size":size,"roi":roi,"trials":trials,"noise_std":noise_std,"delays":delays,"perturb_at":perturb_at,"perturb_amplitude":perturb_amplitude,"coupling":coupled,"decoupled_coupling_control":decoupled},"endpoints":{"primary_retention_delay_8":retention["8"]["coupled_mean"],"primary_retention_auc":auc,"secondary_perturbation_loss_delay_8":perturbation_loss["8"],"secondary_coupling_delta_delay_8":coupling_delta["8"]},"retention_curve":retention,"perturbation_loss_curve":perturbation_loss,"coupling_delta_curve":coupling_delta,"interpretation_boundary":"This protocol tests temporal trace retention in the implemented distributed substrate. It does not demonstrate consciousness, subjective experience, or the physical validity of Syntergic Theory."}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20261002)
    parser.add_argument("--output", type=Path, default=Path("results/lattice_v1/summary.json"))
    args = parser.parse_args()
    result = run(args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()