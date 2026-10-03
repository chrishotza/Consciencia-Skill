from __future__ import annotations

import json
import tempfile
from pathlib import Path

from skill_conscious import ConsciousRuntime


def run() -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="skill-conscious-meta-trace-") as directory:
        runtime = ConsciousRuntime("metacognitive-trace", state_path=Path(directory) / "runtime.json")
        runtime.integrate(
            {
                "response": "cycle",
                "candidate_futures": [
                    {"id": "preserve", "signals": {"goal_fit": 0.8, "continuity": 0.7}},
                    {"id": "explore", "signals": {"goal_fit": 0.5, "continuity": 0.6}},
                ],
            }
        )
        selected = runtime.state.selected_trajectory
        action = runtime.begin_action(selected or {})
        outcome = {"observed_change": "controlled"}
        receipt = runtime.complete_action(outcome)
        return {
            "trace": runtime.state.self_model.get("metacognitive_trace", {}),
            "action_receipt": receipt,
        }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False, sort_keys=True))
