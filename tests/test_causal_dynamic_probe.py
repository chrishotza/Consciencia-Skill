from dataclasses import replace
from pathlib import Path

from skill_conscious import ConsciousRuntime, ExperienceFieldProfile
from skill_conscious.causal_probe import run_reversible_intervention


def profile(offset: float = 0.0) -> ExperienceFieldProfile:
    base = ExperienceFieldProfile(
        0.10, 0.90, 0.20, 0.50, 0.70, 0.80,
        0.10, 0.40, 0.20, 0.85, 0.25,
    )
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


def build_runtime(tmp_path: Path) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        "causal-probe",
        state_path=tmp_path / "runtime.json",
        dynamic_core_enabled=True,
        dynamic_core_state_path=tmp_path / "dynamic.json",
        dynamic_core_return_weight=0.50,
    )
    baseline = profile()
    for token, observed in (
        ("observation-1", baseline),
        ("observation-2", profile(0.01)),
        ("observation-3", profile(-0.01)),
    ):
        runtime.observe_experience_field(
            observed,
            evidence_id=token,
            persist=False,
        )
    runtime.record_experience_recovery(
        baseline,
        profile(0.35),
        profile(0.01),
        evidence_id="recovery-1",
        persist=False,
    )
    runtime._restore_dynamic_core_state()
    return runtime


def candidates() -> list[dict]:
    return [
        {
            "id": "preserve",
            "signals": {"goal_fit": 0.49},
            "predicted_experience_field": profile(0.01).to_dict(),
        },
        {
            "id": "explore",
            "signals": {"goal_fit": 0.52},
            "predicted_experience_field": profile(0.35).to_dict(),
        },
    ]


def test_intervention_causes_divergence_then_reversal(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    baseline_center = dict(runtime.state.self_model["experience_attractor_center"])
    result = run_reversible_intervention(
        runtime,
        candidates(),
        intervention_center=profile(0.35).to_dict(),
    )

    assert result.baseline_selection == "preserve"
    assert result.intervention_selection == "explore"
    assert result.restored_selection == "preserve"
    assert result.downstream_divergence is True
    assert result.reversible is True
    assert result.evidence_unchanged is True
    assert runtime.state.self_model["experience_attractor_center"] == baseline_center


def test_intervention_does_not_create_learning_evidence(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    before = runtime.snapshot_experience_dynamics()

    run_reversible_intervention(
        runtime,
        candidates(),
        intervention_center=profile(0.35).to_dict(),
    )

    after = runtime.snapshot_experience_dynamics()
    assert before["attractor"]["evidence"] == after["attractor"]["evidence"]
    assert before["attractor"]["sequence"] == after["attractor"]["sequence"]
    assert before["reentry"]["sequence"] == after["reentry"]["sequence"]


def test_reversed_state_survives_restart(tmp_path: Path):
    runtime = build_runtime(tmp_path)
    run_reversible_intervention(
        runtime,
        candidates(),
        intervention_center=profile(0.35).to_dict(),
    )
    runtime.store.save(runtime.state)

    restarted = ConsciousRuntime(
        "causal-probe",
        state_path=tmp_path / "runtime.json",
        dynamic_core_enabled=True,
        dynamic_core_state_path=tmp_path / "dynamic.json",
        dynamic_core_return_weight=0.50,
    )
    assert restarted.select_trajectory(candidates())["id"] == "preserve"
