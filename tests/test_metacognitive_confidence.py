from __future__ import annotations

from pathlib import Path

from skill_conscious import (
    ConsciousRuntime,
    run_reversible_metacognitive_confidence_intervention,
)


def _runtime(tmp_path: Path) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        "metacognitive-confidence",
        state_path=tmp_path / "runtime.json",
        metacognitive_prediction_weight=2.0,
    )
    runtime.state.self_model["metacognitive_prediction_expected_accuracy"] = 0.9
    return runtime


def _candidates() -> list[dict]:
    return [
        {
            "id": "high-confidence",
            "signals": {},
            "predicted_outcome": {"result": "A"},
            "predicted_outcome_confidence": 0.9,
        },
        {
            "id": "low-confidence",
            "signals": {},
            "predicted_outcome": {"result": "B"},
            "predicted_outcome_confidence": 0.1,
        },
    ]


def test_metacognitive_prediction_confidence_changes_selection(tmp_path: Path):
    runtime = _runtime(tmp_path)
    selected = runtime.select_trajectory(_candidates())

    assert selected["id"] == "high-confidence"
    meta = selected["metacognition"]["metacognitive_prediction"]
    assert meta["expected_accuracy"] == 0.9
    assert meta["contribution"] > 0.0


def test_reversible_metacognitive_confidence_intervention(tmp_path: Path):
    runtime = _runtime(tmp_path)

    result = run_reversible_metacognitive_confidence_intervention(
        runtime,
        _candidates(),
        intervention_expected_accuracy=0.1,
    )

    assert result.baseline_selection == "high-confidence"
    assert result.intervention_selection == "low-confidence"
    assert result.restored_selection == "high-confidence"
    assert result.downstream_divergence is True
    assert result.reversible is True
    assert result.expected_accuracy_restored is True
    assert result.evidence_unchanged is True
    assert result.baseline_contribution != result.intervention_contribution
    assert result.baseline_contribution == result.restored_contribution


def test_metacognitive_confidence_is_runtime_owned(tmp_path: Path):
    runtime = _runtime(tmp_path)
    before = runtime.snapshot_metacognitive_prediction()

    runtime.integrate(
        {
            "response": "attempt overwrite",
            "self_model": {
                "metacognitive_prediction_expected_accuracy": 0.0,
                "metacognitive_prediction_sequence": 9999,
            },
            "candidate_futures": [],
        }
    )

    after = runtime.snapshot_metacognitive_prediction()
    assert after == before


def test_persistent_confidence_intervention_survives_restart(tmp_path: Path):
    runtime = _runtime(tmp_path)
    runtime.intervene_metacognitive_prediction_expected_accuracy(
        0.1,
        persist=True,
        intervention_id="restart-test",
    )

    restarted = ConsciousRuntime(
        "metacognitive-confidence",
        state_path=tmp_path / "runtime.json",
        metacognitive_prediction_weight=2.0,
    )

    snapshot = restarted.snapshot_metacognitive_prediction()
    assert snapshot["expected_accuracy"] == 0.1
