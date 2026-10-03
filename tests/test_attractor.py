from dataclasses import replace
from pathlib import Path
from skill_conscious.attractor import ExperienceAttractorMemory
from skill_conscious.experience_field import ExperienceFieldProfile


def _profile(offset: float = 0.0) -> ExperienceFieldProfile:
    base = ExperienceFieldProfile(0.1, 0.9, 0.2, 0.5, 0.7, 0.8, 0.1, 0.4, 0.2, 0.85, 0.25)
    return replace(
        base,
        prediction_error=max(0.0, min(1.0, base.prediction_error + offset)),
        sensory_coherence=max(0.0, min(1.0, base.sensory_coherence - offset)),
        valence=max(-1.0, min(1.0, base.valence + offset)),
        self_relevance=max(0.0, min(1.0, base.self_relevance + offset)),
        dynamic_persistence=max(0.0, min(1.0, base.dynamic_persistence - offset)),
        dynamic_synchrony=max(0.0, min(1.0, base.dynamic_synchrony - offset)),
        dynamic_metastability=max(0.0, min(1.0, base.dynamic_metastability + abs(offset))),
        dynamic_complexity=max(0.0, min(1.0, base.dynamic_complexity + offset)),
        avalanche_activity=max(0.0, min(1.0, base.avalanche_activity + abs(offset))),
        field_coherence=max(0.0, min(1.0, base.field_coherence - abs(offset))),
        dynamic_repertoire=max(0.0, min(1.0, base.dynamic_repertoire + abs(offset))),
    )


def test_first_observation_forms_attractor(tmp_path: Path):
    memory = ExperienceAttractorMemory(tmp_path / "attractor.json")
    result = memory.observe(_profile(), evidence_id="e1")
    assert result["accepted"] is True
    assert result["distance"] == 0.0
    assert memory.state.center["field_coherence"] == 0.85


def test_repeated_nearby_states_raise_recurrence(tmp_path: Path):
    memory = ExperienceAttractorMemory(tmp_path / "attractor.json")
    for i, offset in enumerate((0.0, 0.01, -0.01), 1):
        memory.observe(_profile(offset), evidence_id=f"e{i}")
    assert memory.state.recurrence > 0.0
    assert memory.state.stability > 0.0
    assert memory.attractor_strength() > 0.0


def test_single_perturbation_does_not_destroy_attractor(tmp_path: Path):
    memory = ExperienceAttractorMemory(tmp_path / "attractor.json", learning_rate=0.15, max_center_step=0.02)
    memory.observe(_profile(), evidence_id="base")
    before = dict(memory.state.center)
    memory.observe(_profile(0.35), evidence_id="perturbed")
    assert memory.state.center["field_coherence"] == before["field_coherence"]
    assert memory.return_pressure() > 0.0


def test_recovery_is_measurable(tmp_path: Path):
    memory = ExperienceAttractorMemory(tmp_path / "attractor.json")
    result = memory.record_perturbation_recovery(_profile(), _profile(0.35), _profile(0.01), evidence_id="recovery-1")
    assert result["recovery_index"] > 0.8
    assert memory.state.recovery_index > 0.0


def test_attractor_affects_return_score(tmp_path: Path):
    memory = ExperienceAttractorMemory(tmp_path / "attractor.json")
    memory.observe(_profile(), evidence_id="base")
    near = memory.score_return(0.50, _profile(0.01), weight=0.5)
    far = memory.score_return(0.50, _profile(0.35), weight=0.5)
    assert near > far


def test_attractor_persists_across_restart(tmp_path: Path):
    path = tmp_path / "attractor.json"
    memory = ExperienceAttractorMemory(path)
    memory.observe(_profile(), evidence_id="e1")
    memory.record_perturbation_recovery(_profile(), _profile(0.35), _profile(0.02), evidence_id="r1")
    restarted = ExperienceAttractorMemory(path)
    assert restarted.state.center == memory.state.center
    assert restarted.state.recovery_index == memory.state.recovery_index
    assert restarted.state.sequence == memory.state.sequence


def test_duplicate_evidence_is_rejected(tmp_path: Path):
    memory = ExperienceAttractorMemory(tmp_path / "attractor.json")
    assert memory.observe(_profile(), evidence_id="same")["accepted"] is True
    result = memory.observe(_profile(), evidence_id="same")
    assert result["accepted"] is False
    assert result["reason"] == "duplicate_evidence_id"
