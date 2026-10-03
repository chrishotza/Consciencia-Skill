from __future__ import annotations

from pathlib import Path

from skill_conscious import ConsciousRuntime, run_reversible_self_observation_intervention


def test_self_observation_persists_and_tracks_meta_error(tmp_path: Path):
    runtime = ConsciousRuntime(
        "self-observe",
        state_path=tmp_path / "runtime.json",
        self_observation_enabled=True,
    )
    runtime.state.self_state = {"focus": 0.2}
    first = runtime.observe_self(persist=True)
    assert first["sequence"] == 1
    assert first["error"] == 0.0

    runtime.state.self_state = {"focus": 0.9}
    second = runtime.observe_self(persist=True)

    assert second["sequence"] == 2
    assert second["error"] > 0.0
    assert runtime.state.self_model["self_observation_sequence"] == 2


def test_predicted_self_observation_changes_selection(tmp_path: Path):
    runtime = ConsciousRuntime(
        "self-observe-select",
        state_path=tmp_path / "runtime.json",
        self_observation_enabled=True,
        self_observation_weight=2.0,
    )
    runtime.observe_self(persist=True)
    expected = runtime.snapshot_self_observation()["expected"]

    candidates = [
        {"id": "match", "signals": {}, "predicted_self_observation": expected},
        {
            "id": "mismatch",
            "signals": {},
            "predicted_self_observation": {
                key: 1.0 - float(value) for key, value in expected.items()
            },
        },
    ]

    selected = runtime.select_trajectory(candidates)
    assert selected["id"] == "match"
    assert selected["self_observation"]["fit"] > 0.9


def test_reversible_self_observation_intervention(tmp_path: Path):
    runtime = ConsciousRuntime(
        "self-observe-causal",
        state_path=tmp_path / "runtime.json",
        self_observation_enabled=True,
        self_observation_weight=2.0,
    )
    runtime.observe_self(persist=True)
    expected = runtime.snapshot_self_observation()["expected"]
    inverted = {
        key: 1.0 - float(value)
        for key, value in expected.items()
    }

    candidates = [
        {"id": "match", "signals": {}, "predicted_self_observation": expected},
        {"id": "inverse", "signals": {}, "predicted_self_observation": inverted},
    ]

    result = run_reversible_self_observation_intervention(
        runtime,
        candidates,
        intervention_expected=inverted,
    )

    assert result.baseline_selection == "match"
    assert result.intervention_selection == "inverse"
    assert result.restored_selection == "match"
    assert result.downstream_divergence is True
    assert result.reversible is True
    assert result.expected_observation_restored is True
    assert result.evidence_unchanged is True


def test_self_observation_restores_across_restart(tmp_path: Path):
    state_path = tmp_path / "runtime.json"
    runtime = ConsciousRuntime(
        "self-observe-restart",
        state_path=state_path,
        self_observation_enabled=True,
    )
    runtime.observe_self(persist=True)
    snapshot = runtime.snapshot_self_observation()
    runtime.intervene_self_observation_expected(
        {"coherence": 0.0},
        persist=True,
    )
    runtime.restore_self_observation(snapshot, persist=True)

    restarted = ConsciousRuntime(
        "self-observe-restart",
        state_path=state_path,
        self_observation_enabled=True,
    )
    assert restarted.snapshot_self_observation()["expected"] == snapshot["expected"]


def test_model_frame_cannot_overwrite_runtime_self_observation(tmp_path: Path):
    runtime = ConsciousRuntime(
        "self-observe-owned",
        state_path=tmp_path / "runtime.json",
        self_observation_enabled=True,
    )
    runtime.observe_self(persist=True)
    before = runtime.snapshot_self_observation()["expected"]

    runtime.integrate(
        {
            "response": "state update",
            "self_model": {
                "self_observation_expected": {
                    "coherence": 0.0,
                    "homeostatic_fit": 0.0,
                },
                "self_observation_sequence": 9999,
            },
        }
    )

    after = runtime.snapshot_self_observation()["expected"]
    assert after == before
