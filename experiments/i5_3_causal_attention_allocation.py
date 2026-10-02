from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from src.ontto.attention_controller import ATTENTION_CODES, ATTENTION_MODULES, AttentionSchema


def sign_flip(values: np.ndarray, seed: int, permutations: int = 20000) -> float:
    values = np.asarray(values, dtype=float)
    observed = abs(float(values.mean()))
    rng = np.random.default_rng(seed)
    signs = rng.choice((-1.0, 1.0), size=(permutations, values.size))
    null = np.abs((signs * values[None, :]).mean(axis=1))
    return float((np.count_nonzero(null >= observed) + 1) / (permutations + 1))


def run(seed: int, episodes: int):
    rng = np.random.default_rng(seed)
    schema = AttentionSchema()
    full, shuffled, uniform, random, lesion, target_change = [], [], [], [], [], []

    for _ in range(episodes):
        target = int(rng.choice(ATTENTION_MODULES))
        cue = ATTENTION_CODES[target] + rng.normal(0.0, 0.08, size=2)

        a = schema.allocate(cue, mode="full")
        s = schema.allocate(cue, mode="shuffled")
        u = schema.allocate(cue, mode="uniform")
        r = schema.allocate(cue, mode="random", rng=rng)
        l = schema.allocate(cue, mode="lesion")

        full.append(schema.target_attention(a, target))
        shuffled.append(schema.target_attention(s, target))
        uniform.append(schema.target_attention(u, target))
        random.append(schema.target_attention(r, target))
        lesion.append(schema.target_attention(l, target))
        target_change.append(int(a.selected_index != s.selected_index))

    f, s, u, r, l = [np.asarray(x, dtype=float) for x in (full, shuffled, uniform, random, lesion)]
    tc = np.asarray(target_change, dtype=float)

    return {
        "experiment": "i5_3_causal_attention_allocation",
        "seed": seed,
        "episodes": episodes,
        "attention_modules": list(ATTENTION_MODULES),
        "endpoints": {
            "full_target_attention_mass": float(f.mean()),
            "full_minus_shuffled_target_mass": float((f - s).mean()),
            "full_minus_shuffled_p": sign_flip(f - s, seed + 1),
            "full_minus_uniform_target_mass": float((f - u).mean()),
            "full_minus_uniform_p": sign_flip(f - u, seed + 2),
            "full_minus_random_target_mass": float((f - r).mean()),
            "full_minus_random_p": sign_flip(f - r, seed + 3),
            "full_minus_lesion_target_mass": float((f - l).mean()),
            "full_minus_lesion_p": sign_flip(f - l, seed + 4),
            "attention_selection_change_rate": float(tc.mean()),
        },
        "boundary": "Standalone causal attention-allocation mechanism test. It does not establish consciousness.",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261003)
    ap.add_argument("--episodes", type=int, default=512)
    ap.add_argument("--out", default="results/i5_3_causal_attention_allocation")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    summary = run(args.seed, args.episodes)
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
