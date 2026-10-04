from __future__ import annotations

from pathlib import Path

from skill_conscious import ConsciousRuntime


def _runtime(tmp_path: Path, expected_accuracy: float) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        "metacognitive-plasticity",
        state_path=tmp_path / "runtime.json",
    )
    runtime.state.self_model.update(
        {
            "metacognitive_prediction_expected_accuracy": expected_accuracy,
            "trajectory_priority_adaptation": {
                "enabled": True,
                "min_samples": 1,
                "utility_threshold": 0.0,
                "learning_rate": 0.5,
                "max_step": 1.0,
                "cooldown": 0,
                "confidence_threshold": 0.0,
                "direction_consistency": 0.0,
                "bounds": {"continuity": [-3.0, 3.0]},
            },
            "trajectory_weights": {"continuity": 0.0},
        }
    )
    runtime.state.selected_trajectory = {
        "id": "continuity-action",
        "signals": {"continuity": 1.0},
        "predicted_outcome": {"result": "expected"},
        "predicted_outcome_confidence": 0.9,
    }
    return runtime


def _update(runtime: ConsciousRuntime) -> dict:
    result = runtime.register_consequence(
        "continuity-action",
        {"result": "observed"},
        evaluation={
            "credited_signal": "continuity",
            "utility": 1.0,
        },
    )
    return dict(result["priority_adaptation"]["update"])


def test_metacognitive_plasticity_scales_with_trust(tmp_path: Path):
    high = _runtime(tmp_path / "high", expected_accuracy=0.9)
    low = _runtime(tmp_path / "low", expected_accuracy=0.1)

    high_update = _update(high)
    low_update = _update(low)

    high_meta = high_update["metacognitive_plasticity"]
    low_meta = low_update["metacognitive_plasticity"]

    assert high_meta["factor"] == 1.32
    assert low_meta["factor"] == 0.68
    assert high_update["delta"] == 0.66
    assert low_update["delta"] == 0.34
    assert high_update["delta"] > low_update["delta"]


def test_metacognitive_plasticity_is_reversible(tmp_path: Path):
    runtime = _runtime(tmp_path, expected_accuracy=0.9)

    baseline = _update(runtime)
    baseline_factor = baseline["metacognitive_plasticity"]["factor"]

    snapshot = runtime.snapshot_metacognitive_prediction()
    runtime.intervene_metacognitive_prediction_expected_accuracy(
        0.1,
        persist=False,
        intervention_id="plasticity-intervention",
    )
    intervened = _update(runtime)

    runtime.restore_metacognitive_prediction(
        snapshot,
        persist=False,
        intervention_id="plasticity-restoration",
    )
    restored = _update(runtime)

    assert baseline_factor == restored["metacognitive_plasticity"]["factor"] == 1.32
    assert intervened["metacognitive_plasticity"]["factor"] == 0.68
    assert baseline["delta"] == restored["delta"] == 0.66
    assert intervened["delta"] == 0.34


def test_metacognitive_plasticity_persists_through_restart(tmp_path: Path):
    runtime = _runtime(tmp_path, expected_accuracy=0.1)
    runtime.store.save(runtime.state)

    restarted = ConsciousRuntime(
        "metacognitive-plasticity",
        state_path=tmp_path / "runtime.json",
    )
    restarted.state.selected_trajectory = dict(runtime.state.selected_trajectory or {})

    update = _update(restarted)

    assert update["metacognitive_plasticity"]["expected_accuracy"] == 0.1
    assert update["metacognitive_plasticity"]["factor"] == 0.68


def test_direct_weight_delta_is_also_metacognitively_scaled(tmp_path: Path):
    runtime = ConsciousRuntime(
        "metacognitive-plasticity-direct",
        state_path=tmp_path / "runtime.json",
    )
    runtime.state.self_model.update(
        {
            "metacognitive_prediction_expected_accuracy": 0.9,
            "trajectory_weights": {"continuity": 0.0},
        }
    )
    runtime.state.selected_trajectory = {
        "id": "continuity-action",
        "predicted_outcome_confidence": 0.9,
    }

    result = runtime.register_consequence(
        "continuity-action",
        {"result": "observed"},
        evaluation={
            "credited_signal": "continuity",
            "utility": 1.0,
            "weight_delta": 0.5,
        },
    )

    assert result["metacognitive_plasticity"]["factor"] == 1.32
    assert result["metacognitive_plasticity"]["base_delta"] == 0.5
    assert result["metacognitive_plasticity"]["effective_delta"] == 0.66
    assert runtime.state.self_model["trajectory_weights"]["continuity"] == 0.66
