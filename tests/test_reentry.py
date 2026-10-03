from pathlib import Path
from skill_conscious.experience_field import build_experience_field
from skill_conscious.reentry import ExperienceFieldReentry


def _field(vision: float, flip: bool = False):
    base = [
        [0.2 * i + 0.03 * ((i % 2) - 0.5) for i in range(64)],
        [0.2 * i + 0.02 * ((i % 3) - 1.0) for i in range(64)],
        [0.2 * i - 0.02 * ((i % 4) - 1.5) for i in range(64)],
    ]
    if flip:
        base = [[v * (-1 if i % 2 else 1) for i, v in enumerate(ch)] for ch in base]
    return build_experience_field({"vision": vision}, {"vision": 0.0}, base, affective_weights={"vision": -1.0}, self_relevance_weights={"vision": 1.0})[0]


def test_reentry_persists_field_and_expectation(tmp_path: Path):
    path = tmp_path / "experience.json"
    memory = ExperienceFieldReentry(path)
    first = _field(0.4)
    memory.observe(first, evidence_id="e1", regime="baseline")
    restarted = ExperienceFieldReentry(path)
    assert restarted.state.sequence == 1
    assert restarted.state.previous_profile == first.to_dict()
    assert restarted.state.expected_profile["prediction_error"] == 0.4


def test_reentry_deduplicates_host_evidence(tmp_path: Path):
    memory = ExperienceFieldReentry(tmp_path / "experience.json")
    profile = _field(1.0)
    assert memory.observe(profile, evidence_id="same")["accepted"] is True
    duplicate = memory.observe(profile, evidence_id="same")
    assert duplicate["accepted"] is False
    assert duplicate["reason"] == "duplicate_evidence_id"


def test_regime_preference_requires_accumulated_utility(tmp_path: Path):
    memory = ExperienceFieldReentry(tmp_path / "experience.json")
    for index in range(2):
        assert memory.record_consequence("exploration", 1.0, evidence_id=f"u{index}")["updated"] is False
    result = memory.record_consequence("exploration", 1.0, evidence_id="u3")
    assert result["updated"] is True
    assert memory.state.regime_preferences["exploration"] == 0.25


def test_reentry_changes_next_policy_score(tmp_path: Path):
    memory = ExperienceFieldReentry(tmp_path / "experience.json")
    profile = _field(1.0, flip=True)
    before = memory.score_regime(0.5, "exploration", field=profile)
    for token in ("a1", "a2", "a3"):
        memory.record_consequence("exploration", 1.0, evidence_id=token)
    assert memory.score_regime(0.5, "exploration", field=profile) > before


def test_reversal_uses_hysteresis(tmp_path: Path):
    memory = ExperienceFieldReentry(tmp_path / "experience.json", reversal_error_multiplier=1.2, reversal_sample_multiplier=2.0)
    for index in range(3):
        memory.record_consequence("baseline", 1.0, evidence_id=f"p{index}")
    assert memory.state.regime_preferences["baseline"] == 0.25
    for index in range(5):
        assert memory.record_consequence("baseline", -1.0, evidence_id=f"n{index}")["updated"] is False
    result = memory.record_consequence("baseline", -1.0, evidence_id="n5")
    assert result["updated"] is True
    assert result["reversal"] is True
    assert memory.state.regime_preferences["baseline"] == 0.0


def test_model_frame_cannot_inject_runtime_owned_field(tmp_path: Path):
    memory = ExperienceFieldReentry(tmp_path / "experience.json")
    cleaned = memory.sanitized_model_frame({"response": "ok", "self_model": {"experience_field_state": {"prediction_error": 999.0}, "user_value": 1.0}})
    assert "experience_field_state" not in cleaned["self_model"]
    assert cleaned["self_model"]["user_value"] == 1.0
