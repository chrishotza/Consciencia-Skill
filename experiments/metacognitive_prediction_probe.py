from __future__ import annotations

import json
from tempfile import TemporaryDirectory
from pathlib import Path

from skill_conscious import ConsciousRuntime


def main() -> None:
    with TemporaryDirectory() as tmp:
        runtime = ConsciousRuntime(
            "metacognitive-prediction-probe",
            state_path=Path(tmp) / "runtime.json",
        )
        runtime.state.self_model["metacognitive_prediction_adaptation"] = {
            "enabled": True,
            "initial_expected_accuracy": 0.5,
            "min_samples": 2,
            "error_threshold": 0.1,
            "confidence_threshold": 0.5,
            "learning_rate": 0.5,
            "max_step": 1.0,
            "cooldown": 0,
            "direction_consistency": 0.5,
        }

        for observed in ("unexpected", "unexpected"):
            runtime.integrate(
                {
                    "response": "probe",
                    "candidate_futures": [
                        {
                            "id": "act",
                            "signals": {},
                            "predicted_outcome": {
                                "observed_change": "expected",
                            },
                        }
                    ],
                }
            )
            selected = runtime.state.selected_trajectory
            assert selected is not None
            runtime.begin_action(selected)
            receipt = runtime.complete_action(
                {"observed_change": observed}
            )
            print(json.dumps(receipt["metacognitive_prediction"], indent=2))

        print(
            json.dumps(
                runtime.snapshot_metacognitive_prediction(),
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
