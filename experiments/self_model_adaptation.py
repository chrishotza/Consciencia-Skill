"""Deterministic self-model adaptation probe."""

from pathlib import Path
from tempfile import TemporaryDirectory

from skill_conscious import ConsciousRuntime


def run() -> None:
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "self-model.json"
        runtime = ConsciousRuntime("self-model-probe", path)
        runtime.integrate(
            {
                "response": "initialize",
                "self_model": {
                    "expected_self_state": {"focus": 0.8},
                    "self_model_adaptation": {
                        "enabled": True,
                        "min_samples": 3,
                        "error_threshold": 0.25,
                        "confidence_threshold": 0.75,
                        "required_high_error": 3,
                        "learning_rate": 0.5,
                        "max_step": 0.1,
                        "cooldown": 2,
                        "bounds": {"focus": [0.0, 1.0]},
                    },
                },
            }
        )

        for index in range(1, 4):
            runtime.begin_action({"id": f"self-{index}", "signals": {}})
            receipt = runtime.complete_action(
                {
                    "status": "success",
                    "self_state": {"focus": 0.4},
                }
            )
            if index < 3:
                assert receipt["self_model_adaptation"]["updated"] is False
            else:
                assert receipt["self_model_adaptation"]["updated"] is True

        assert runtime.state.self_model["expected_self_state"]["focus"] == 0.7
        assert runtime.state.self_model["self_model_adaptation_history"][-1]["evidence"]["sample_count"] == 3

        restarted = ConsciousRuntime("self-model-probe", path)
        assert restarted.state.self_model["expected_self_state"]["focus"] == 0.7

        print("SELF-MODEL ADAPTATION: PASS")
        print("expected focus: 0.8 -> 0.7 after 3 host-observed self-state outcomes")


if __name__ == "__main__":
    run()
