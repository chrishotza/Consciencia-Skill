from __future__ import annotations

import json
import tempfile
from pathlib import Path

from skill_conscious import ConsciousRuntime, run_metacognitive_causal_probe


def run() -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="skill-conscious-meta-causal-") as directory:
        runtime = ConsciousRuntime(
            "metacognitive-causal-experiment",
            state_path=Path(directory) / "runtime.json",
        )
        runtime.state.valuation = {"goal_fit": 2.0}

        candidates = [
            {"id": "preserve", "signals": {"goal_fit": 0.8}},
            {"id": "explore", "signals": {"goal_fit": 0.4}},
        ]

        return run_metacognitive_causal_probe(
            runtime,
            candidates,
            intervention_valuation={"goal_fit": -2.0},
        ).to_dict()


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False, sort_keys=True))
