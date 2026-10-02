from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from src.ontto.causal_query_bottleneck import CausalQueryBottleneck
from src.ontto.workspace_query import QUERY_MODULES


def sign_flip(values: np.ndarray, seed: int, permutations: int = 20000) -> float:
    values = np.asarray(values, dtype=float)
    if values.size == 0:
        return 1.0
    observed = abs(float(values.mean()))
    rng = np.random.default_rng(seed)
    signs = rng.choice((-1.0, 1.0), size=(permutations, values.size))
    null = np.abs((signs * values[None, :]).mean(axis=1))
    return float((np.count_nonzero(null >= observed) + 1) / (permutations + 1))


def run(seed: int, episodes: int, threshold: float):
    model = CausalQueryBottleneck(threshold=threshold)
    rng = np.random.default_rng(seed)

    controls = {
        "full": ("full", "full", True),
        "shuffled_query": ("shuffled", "full", True),
        "zero_query": ("zero", "full", True),
        "random_query": ("random", "full", True),
        "shuffled_attention": ("full", "shuffled", True),
        "lesion_target": ("full", "full", True),
        "no_bottleneck": ("full", "full", False),
    }
    rows = []
    for episode in range(episodes):
        target_module = int(rng.choice(QUERY_MODULES))
        target_action = float(rng.choice((-1.0, 1.0)))
        episode_seed = int(seed + episode)
        for name, (query_mode, attention_mode, bottleneck) in controls.items():
            if name == "lesion_target":
                # Causal target lesion: overwrite the queried target after routing.
                result = model.decide(
                    target_module=target_module,
                    target_action=target_action,
                    seed=episode_seed,
                    query_mode=query_mode,
                    attention_mode=attention_mode,
                    bottleneck_enabled=bottleneck,
                )
                result = result.__class__(
                    **{
                        **result.__dict__,
                        "masked_score": 0.0,
                        "predicted_action": 0.0,
                    }
                )
            else:
                result = model.decide(
                    target_module=target_module,
                    target_action=target_action,
                    seed=episode_seed,
                    query_mode=query_mode,
                    attention_mode=attention_mode,
                    bottleneck_enabled=bottleneck,
                )
            rows.append(
                {
                    "episode": episode,
                    "seed": episode_seed,
                    "control": name,
                    "target_module": target_module,
                    "target_action": target_action,
                    "query_module": result.query_module,
                    "query_accuracy": result.query_accuracy,
                    "attention_mass": result.attention_mass,
                    "predicted_action": result.predicted_action,
                    "action_accuracy": float(result.predicted_action == target_action),
                    "masked_score": result.masked_score,
                    "attended_module": result.attended_module,
                }
            )

    by_name = {}
    for row in rows:
        by_name.setdefault(row["control"], []).append(row)
    full = by_name["full"]

    endpoints = {
        "full_action_accuracy": float(np.mean([r["action_accuracy"] for r in full])),
        "full_query_accuracy": float(np.mean([r["query_accuracy"] for r in full])),
        "full_attention_mass_mean": float(np.mean([r["attention_mass"] for r in full])),
    }

    for idx, name in enumerate(controls):
        if name == "full":
            continue
        paired = np.asarray(
            [full[i]["action_accuracy"] - by_name[name][i]["action_accuracy"] for i in range(episodes)],
            dtype=float,
        )
        endpoints[f"full_minus_{name}_accuracy"] = float(paired.mean())
        endpoints[f"full_minus_{name}_p"] = sign_flip(paired, seed + 100 + idx)

        query_paired = np.asarray(
            [full[i]["query_accuracy"] - by_name[name][i]["query_accuracy"] for i in range(episodes)],
            dtype=float,
        )
        endpoints[f"full_minus_{name}_query_accuracy"] = float(query_paired.mean())

    endpoints["full_action_accuracy_ciag"] = "paired sign-flip protocol; no independent CI claimed"

    return {
        "experiment": "i5_5_causal_query_bottleneck",
        "seed": seed,
        "episodes": episodes,
        "threshold": threshold,
        "query_modules": list(QUERY_MODULES),
        "controls": controls,
        "endpoints": endpoints,
        "boundary": "Combined state-dependent query + attention bottleneck mechanism test. It does not establish consciousness.",
    }, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261005)
    ap.add_argument("--episodes", type=int, default=512)
    ap.add_argument("--threshold", type=float, default=0.20)
    ap.add_argument("--out", default="results/i5_5_causal_query_bottleneck")
    args = ap.parse_args()
    summary, rows = run(args.seed, args.episodes, args.threshold)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out / "runs.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
