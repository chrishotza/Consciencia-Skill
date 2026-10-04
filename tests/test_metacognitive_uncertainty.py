from __future__ import annotations

from pathlib import Path

from skill_conscious import ConsciousRuntime


def _runtime(tmp_path: Path, expected_accuracy: float) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        "metacognitive-uncertainty",
        state_path=tmp_path / "runtime.json",
        metacognitive_uncertainty_weight=2.0,
    )
    runtime.state.self_model.update(
        {
            "metacognitive_prediction_expected_accuracy": expected_accuracy,
            "metacognitive_uncertainty": 1.0 - expected_accuracy,
        }
    )
    return runtime


def _candidates() -> list[dict]:
    return [
        {
            "id": "exploit",
            "signals": {"goal_fit": 1.0},
            "epistemic_value": 0.0,
        },
        {
            "id": "explore",
            "signals": {},
            "epistemic_value": 1.0,
        },
    ]


def test_metacognitive_uncertainty_changes_selection(tmp_path: Path):
    confident = _runtime(tmp_path / "confident", 0.9)
    uncertain = _runtime(tmp_path / "uncertain", 0.1)

    assert confident.select_trajectory(_candidates())["id"] == "exploit"
    selected = uncertain.select_trajectory(_candidates())
    assert selected["id"] == "explore"

    diagnostics = selected["metacognition"]["metacognitive_uncertainty"]
    assert diagnostics["uncertainty"] == 0.9
    assert diagnostics["contribution"] == 1.8


def test_metacognitive_uncertainty_is_reversible(tmp_path: Path):
    runtime = _runtime(tmp_path, 0.9)
    candidates = _candidates()

    baseline = runtime.select_trajectory(candidates)
    snapshot = runtime.snapshot_metacognitive_prediction()

    runtime.intervene_metacognitive_prediction_expected_accuracy(
        0.1,
        persist=False,
        intervention_id="uncertainty-intervention",
    )
    intervention = runtime.select_trajectory(candidates)

    runtime.restore_metacognitive_prediction(
        snapshot,
        persist=False,
        intervention_id="uncertainty-restoration",
    )
    restored = runtime.select_trajectory(candidates)

    assert baseline["id"] == "exploit"
    assert intervention["id"] == "explore"
    assert restored["id"] == "exploit"

    baseline_diag = baseline["metacognition"]["metacognitive_uncertainty"]
    intervention_diag = intervention["metacognition"]["metacognitive_uncertainty"]
    restored_diag = restored["metacognition"]["metacognitive_uncertainty"]

    assert baseline_diag["uncertainty"] == 0.1
    assert intervention_diag["uncertainty"] == 0.9
    assert restored_diag == baseline_diag


def test_metacognitive_uncertainty_persists_through_restart(tmp_path: Path):
    runtime = _runtime(tmp_path, 0.1)
    runtime.store.save(runtime.state)

    restarted = ConsciousRuntime(
        "metacognitive-uncertainty",
        state_path=tmp_path / "runtime.json",
        metacognitive_uncertainty_weight=2.0,
    )
    assert restarted.metacognitive_uncertainty() == 0.9

    selected = restarted.select_trajectory(_candidates())
    assert selected["id"] == "explore"


def test_model_cannot_forge_runtime_uncertainty(tmp_path: Path):
    runtime = _runtime(tmp_path, 0.9)
    before = runtime.metacognitive_uncertainty()

    runtime.integrate(
        {
            "response": "attempt uncertainty overwrite",
            "self_model": {"metacognitive_uncertainty": 1.0},
            "candidate_futures": _candidates(),
        }
    )

    assert runtime.metacognitive_uncertainty() == before == 0.1
    assert runtime.state.self_model["metacognitive_uncertainty"] == 0.1
