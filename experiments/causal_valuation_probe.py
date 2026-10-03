from __future__ import annotations

import json
import tempfile
from pathlib import Path

from skill_conscious import ConsciousRuntime, run_reversible_valuation_intervention


def run() -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="skill-conscious-valuation-") as directory:
        runtime = ConsciousRuntime(
            "causal-valuation-experiment",
            state_path=Path(directory) / "runtime.json",
        )
        runtime.state.valuation = {"goal_fit": 1.0}
        runtime.store.save(runtime.state)

        candidates = [
            {
                "id": "preserve_continuity",
                "signals": {"goal_fit": 0.80, "continuity": 0.75},
            },
            {
                "id": "explore",
                "signals": {"goal_fit": 0.70, "learning": 0.80},
            },
        ]

        return run_reversible_valuation_intervention(
            runtime,
            candidates,
            intervention_valuation={"goal_fit": -1.0},
        ).to_dict()


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False, sort_keys=True))
