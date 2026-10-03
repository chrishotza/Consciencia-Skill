from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

from skill_conscious import ConsciousRuntime


SEQUENCE = [
    {"stability": 0.2, "focus": 0.3},
    {"stability": 0.4, "focus": 0.5},
    {"stability": 0.7, "focus": 0.6},
    {"stability": 0.9, "focus": 0.8},
]


def state_hash(snapshot: dict) -> str:
    payload = json.dumps(snapshot, ensure_ascii=False, sort_keys=True).encode()
    return hashlib.sha256(payload).hexdigest()


def run_condition(name: str, root: Path) -> dict:
    runtime = ConsciousRuntime(name, root / f"{name}.json")
    initial_hash = state_hash(runtime.snapshot())
    selected = []
    dissonance = []
    revisions = []

    for index, state in enumerate(SEQUENCE):
        frame = {
            "response": f"cycle-{index}",
            "internal_state": state,
            "intention": "maintain coherent development",
            "candidate_futures": [
                {
                    "id": "preserve",
                    "signals": {
                        "continuity": 1.0,
                        "learning": 0.2,
                        "risk": 0.1,
                    },
                },
                {
                    "id": "learn",
                    "signals": {
                        "continuity": 0.5,
                        "learning": 1.0,
                        "risk": 0.2,
                    },
                },
            ],
        }

        if name in {"latent", "reconciled"}:
            frame["latent_patterns"] = {
                "stability-seeking": {
                    "activation": min(1.0, 0.2 + (0.2 * index)),
                    "evidence": ["repeated stability trajectory"],
                }
            }
            frame["self_model"] = {
                "expected_self_state": {
                    "stability": 0.8,
                    "focus": 0.7,
                },
                "trajectory_weights": {
                    "continuity": 2.0,
                    "learning": 0.8,
                },
                "self_model_learning_rate": 0.25,
            }

        runtime.integrate(frame)
        selected.append(runtime.state.selected_trajectory["id"])
        dissonance.append(runtime.state.self_dissonance)

        if name == "reconciled":
            result = runtime.reconcile_self_model()
            revisions.append(result)

    final_snapshot = runtime.snapshot()
    restarted = ConsciousRuntime(name, root / f"{name}.json")

    return {
        "condition": name,
        "initial_state_hash": initial_hash,
        "final_state_hash": state_hash(final_snapshot),
        "selected_trajectories": selected,
        "self_dissonance": dissonance,
        "self_model_revisions": revisions,
        "restart_identity": restarted.state.identity,
        "restart_revision": restarted.state.revision,
        "latent_pattern_keys": sorted(restarted.state.latent_patterns),
        "coherence": restarted.state.coherence,
        "transformations": len(restarted.state.transformation_log),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("experiment-results/latent-self-ablation.json"))
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        results = [
            run_condition("baseline", root),
            run_condition("explicit", root),
            run_condition("latent", root),
            run_condition("reconciled", root),
        ]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
