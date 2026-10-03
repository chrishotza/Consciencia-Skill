"""Deterministic probe for evidence-driven homeostatic target adaptation."""

from pathlib import Path
from tempfile import TemporaryDirectory

from skill_conscious import ConsciousRuntime


def run() -> None:
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "probe.json"
        runtime = ConsciousRuntime("probe", path)
        runtime.integrate(
            {
                "response": "initialize",
                "self_model": {
                    "homeostatic_targets": {"energy": 0.8},
                    "homeostatic_adaptation": {
                        "enabled": True,
                        "min_samples": 3,
                        "error_threshold": 0.25,
                        "confidence_threshold": 0.75,
                        "required_high_error": 3,
                        "learning_rate": 0.5,
                        "max_step": 0.05,
                        "cooldown": 2,
                        "bounds": {"energy": [0.0, 1.0]},
                    },
                },
                "interoceptive_state": {"energy": 0.4},
            }
        )

        for index in range(1, 4):
            runtime.begin_action({"id": f"trial-{index}", "signals": {}})
            receipt = runtime.complete_action(
                {
                    "status": "success",
                    "interoceptive_state": {"energy": 0.4},
                }
            )
            if index < 3:
                assert receipt["target_adaptation"]["updated"] is False
            else:
                assert receipt["target_adaptation"]["updated"] is True

        assert runtime.state.self_model["homeostatic_targets"]["energy"] == 0.75
        assert runtime.state.self_model["homeostatic_adaptation_history"][-1]["target"] == "energy"
        assert runtime.state.self_model["homeostatic_adaptation_history"][-1]["evidence"]["sample_count"] == 3

        restarted = ConsciousRuntime("probe", path)
        assert restarted.state.self_model["homeostatic_targets"]["energy"] == 0.75

        print("SELF-DEVELOPMENT TARGET ADAPTATION: PASS")
        print("target energy: 0.8 -> 0.75 after 3 independent host observations")


if __name__ == "__main__":
    run()
