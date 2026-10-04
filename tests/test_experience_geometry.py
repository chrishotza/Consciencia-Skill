from __future__ import annotations

from pathlib import Path

from skill_conscious import (
    ConsciousRuntime,
    ExperienceState,
    build_experience_state,
    changed_dimensions,
    experience_distance,
)


def _snapshot(**overrides):
    state = {
        "valence": 0.0,
        "coherence": 1.0,
        "self_dissonance": 0.0,
        "salience": {"focus": 0.5},
        "self_model": {
            "metacognitive_prediction_expected_accuracy": 0.9,
            "metacognitive_prediction_error": 0.1,
            "self_observation_error": 0.0,
            "experience_field_state": {
                "self_relevance": 0.2,
                "field_coherence": 0.8,
                "dynamic_synchrony": 0.7,
                "dynamic_metastability": 0.3,
                "dynamic_complexity": 0.4,
                "dynamic_repertoire": 0.35,
            },
        },
    }
    state.update(overrides)
    return state


def test_experience_state_is_bounded_and_deterministic():
    state = build_experience_state(_snapshot())
    assert state == build_experience_state(_snapshot())
    assert set(state.features) >= {
        "valence",
        "coherence",
        "metacognitive_uncertainty",
        "dynamic_repertoire",
    }
    assert all(0.0 <= value <= 1.0 for value in state.features.values())


def test_experience_distance_is_zero_for_identical_states():
    state = build_experience_state(_snapshot())
    assert experience_distance(state, state) == 0.0


def test_experience_distance_is_symmetric_and_localizes_change():
    left = build_experience_state(_snapshot())
    right = build_experience_state(
        _snapshot(
            valence=1.0,
            self_model={
                **_snapshot()["self_model"],
                "metacognitive_prediction_expected_accuracy": 0.1,
            },
        )
    )

    assert experience_distance(left, right) == experience_distance(right, left)
    changed = changed_dimensions(left, right, threshold=0.1)
    assert "valence" in changed
    assert "metacognitive_uncertainty" in changed


def test_runtime_persists_experience_geometry_transition(tmp_path: Path):
    runtime = ConsciousRuntime(
        "experience-geometry",
        state_path=tmp_path / "runtime.json",
    )

    runtime.integrate(
        {
            "response": "record a measurable integrated state",
            "valence": 0.75,
            "self_state": {"focus": 1.0},
            "candidate_futures": [
                {
                    "id": "observe",
                    "signals": {"goal_fit": 1.0},
                }
            ],
        }
    )

    snapshot = runtime.snapshot_experience_geometry()
    assert len(snapshot["history"]) == 1
    transition = snapshot["history"][0]
    assert 0.0 <= transition["distance"] <= 1.0
    assert transition["current"]["features"]["valence"] > 0.5

    restarted = ConsciousRuntime(
        "experience-geometry",
        state_path=tmp_path / "runtime.json",
    )
    restarted_snapshot = restarted.snapshot_experience_geometry()
    assert restarted_snapshot["current"] == snapshot["current"]
    assert restarted_snapshot["history"] == snapshot["history"]


def test_llm_cannot_directly_write_experience_geometry(tmp_path: Path):
    runtime = ConsciousRuntime(
        "experience-geometry-owned",
        state_path=tmp_path / "runtime.json",
    )
    before = runtime.snapshot_experience_geometry()

    runtime.integrate(
        {
            "response": "attempt forged geometry",
            "self_model": {
                "experience_geometry_current": {"features": {"valence": 1.0}},
                "experience_geometry_history": [{"forged": True}],
            },
            "candidate_futures": [
                {
                    "id": "observe",
                    "signals": {"goal_fit": 1.0},
                }
            ],
        }
    )

    after = runtime.snapshot_experience_geometry()
    assert after["current"] != {"features": {"valence": 1.0}}
    assert not any(
        item.get("forged") is True
        for item in after["history"]
        if isinstance(item, dict)
    )
    assert after["current"]["features"]["valence"] == build_experience_state(
        runtime.snapshot()
    ).features["valence"]
    assert before["history"] == []
