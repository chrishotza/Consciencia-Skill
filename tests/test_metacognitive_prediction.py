from __future__ import annotations

from pathlib import Path

from skill_conscious import ConsciousRuntime


def _run_predicted_action(
    runtime: ConsciousRuntime,
    *,
    predicted: str,
    observed: str,
) -> dict[str, object]:
    runtime.integrate(
        {
            "response": "cycle",
            "candidate_futures": [
                {
                    "id": "act",
                    "signals": {},
                    "predicted_outcome": {
                        "observed_change": predicted,
                    },
                }
            ],
        }
    )
    selected = runtime.state.selected_trajectory
    assert selected is not None
    runtime.begin_action(selected)
    return runtime.complete_action(
        {"observed_change": observed},
        persist=True,
    )


def test_metacognitive_prediction_is_closed_against_authoritative_outcome(
    tmp_path: Path,
):
    runtime = ConsciousRuntime(
        "prediction-error",
        state_path=tmp_path / "runtime.json",
    )

    receipt = _run_predicted_action(
        runtime,
        predicted="expected",
        observed="unexpected",
    )

    trace = runtime.state.self_model["metacognitive_trace"]
    prediction = receipt["metacognitive_prediction"]

    assert trace["predicted_outcome"] == {
        "observed_change": "expected",
    }
    assert trace["outcome"]["observed_change"] == "unexpected"
    assert prediction["available"] is True
    assert prediction["error"] == 1.0
    assert prediction["accuracy"] == 0.0
    assert trace["prediction_error"] == 1.0
    assert trace["prediction_accuracy"] == 0.0


def test_metacognitive_prediction_can_include_state_transition(
    tmp_path: Path,
):
    runtime = ConsciousRuntime(
        "prediction-transition",
        state_path=tmp_path / "runtime.json",
    )

    runtime.integrate(
        {
            "response": "cycle",
            "candidate_futures": [
                {
                    "id": "act",
                    "signals": {},
                    "predicted_outcome": {"status": "ok"},
                    "predicted_state_delta": {
                        "pending_action": {
                            "before": None,
                            "after": "not-authoritative",
                        }
                    },
                }
            ],
        }
    )
    selected = runtime.state.selected_trajectory
    assert selected is not None

    runtime.begin_action(selected)
    receipt = runtime.complete_action({"status": "ok"})

    prediction = receipt["metacognitive_prediction"]
    diagnostics = prediction["diagnostics"]

    assert prediction["available"] is True
    assert diagnostics["outcome"]["accuracy"] == 1.0
    assert diagnostics["state_delta"]["accuracy"] == 0.0
    assert prediction["error"] == 0.5


def test_repeated_prediction_errors_update_expected_accuracy(
    tmp_path: Path,
):
    runtime = ConsciousRuntime(
        "prediction-adaptation",
        state_path=tmp_path / "runtime.json",
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

    _run_predicted_action(
        runtime,
        predicted="expected",
        observed="wrong",
    )
    first_expected = runtime.state.self_model[
        "metacognitive_prediction_expected_accuracy"
    ]
    assert first_expected == 0.5

    _run_predicted_action(
        runtime,
        predicted="expected",
        observed="wrong",
    )
    second_expected = runtime.state.self_model[
        "metacognitive_prediction_expected_accuracy"
    ]

    assert second_expected == 0.25
    assert runtime.state.self_model["metacognitive_prediction_sequence"] == 2
    assert runtime.state.self_model["metacognitive_prediction_history"]


def test_prediction_runtime_fields_cannot_be_forged_by_model_frame(
    tmp_path: Path,
):
    runtime = ConsciousRuntime(
        "prediction-owned",
        state_path=tmp_path / "runtime.json",
    )
    _run_predicted_action(
        runtime,
        predicted="expected",
        observed="wrong",
    )

    before = runtime.snapshot_metacognitive_prediction()

    runtime.integrate(
        {
            "response": "attempt overwrite",
            "self_model": {
                "metacognitive_prediction_error": 0.0,
                "metacognitive_prediction_accuracy": 1.0,
                "metacognitive_prediction_expected_accuracy": 1.0,
                "metacognitive_prediction_sequence": 9999,
                "metacognitive_prediction_history": [],
            },
        }
    )

    after = runtime.snapshot_metacognitive_prediction()
    assert after == before


def test_prediction_error_survives_restart(tmp_path: Path):
    state_path = tmp_path / "runtime.json"
    runtime = ConsciousRuntime(
        "prediction-restart",
        state_path=state_path,
    )
    _run_predicted_action(
        runtime,
        predicted="expected",
        observed="wrong",
    )

    before = runtime.snapshot_metacognition_prediction()
    restarted = ConsciousRuntime(
        "prediction-restart",
        state_path=state_path,
    )

    assert restarted.snapshot_metacognition_prediction() == before
