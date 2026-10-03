from __future__ import annotations

import json
import tempfile
from pathlib import Path

from skill_conscious import ConsciousRuntime, run_reversible_self_observation_intervention


def run() -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="skill-conscious-self-observation-") as directory:
        runtime = ConsciousRuntime(
            "self-observation-experiment",
            state_path=Path(directory) / "runtime.json",
            self_observation_enabled=True,
            self_observation_weight=2.0,
        )
        runtime.state.self_state = {"focus": 0.8}
        runtime.observe_self(persist=True)

        baseline_expected = runtime.snapshot_self_observation()["expected"]
        inverted = {
            key: 1.0 - float(value)
            for key, value in baseline_expected.items()
        }

        candidates = [
            {
                "id": "continuity",
                "signals": {},
                "predicted_self_observation": dict(baseline_expected),
            },
            {
                "id": "divergence",
                "signals": {},
                "predicted_self_observation": dict(inverted),
            },
        ]

        return run_reversible_self_observation_intervention(
            runtime,
            candidates,
            intervention_expected=inverted,
        ).to_dict()


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False, sort_keys=True))
