from pathlib import Path

from skill_conscious import ConsciousRuntime


def test_self_model_change_is_causal_within_same_integrate_cycle(tmp_path: Path) -> None:
    runtime = ConsciousRuntime("agent", tmp_path / "state.json")

    runtime.integrate(
        {
            "response": "cycle",
            "self_model": {
                "trajectory_weights": {
                    "goal_fit": 10.0,
                }
            },
            "candidate_futures": [
                {
                    "id": "goal",
                    "signals": {"goal_fit": 1.0, "learning": 0.0},
                },
                {
                    "id": "learn",
                    "signals": {"goal_fit": 0.0, "learning": 1.0},
                },
            ],
        }
    )

    assert runtime.state.selected_trajectory["id"] == "goal"


def test_reconcile_self_model_reduces_expected_state_dissonance(tmp_path: Path) -> None:
    path = tmp_path / "state.json"
    runtime = ConsciousRuntime("agent", path)

    runtime.state.self_state = {"stability": 0.2}
    runtime.state.self_model = {
        "expected_self_state": {"stability": 1.0},
        "self_model_learning_rate": 0.25,
    }

    before = runtime.calculate_self_dissonance()
    result = runtime.reconcile_self_model()

    assert before == 0.8
    assert result["changed"] is True
    assert result["after"] < before
    assert runtime.state.self_model["expected_self_state"]["stability"] == 0.8
    assert runtime.state.transformation_log[-1]["type"] == "self_model_reconciliation"
