from pathlib import Path

from skill_conscious import ConsciousRuntime, ExperienceFieldProfile


def profile(offset: float = 0.0) -> ExperienceFieldProfile:
    base = ExperienceFieldProfile(
        0.10, 0.90, 0.20, 0.50, 0.70, 0.80,
        0.10, 0.40, 0.20, 0.85, 0.25,
    )
    from dataclasses import replace

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


def seed_dynamic_runtime(runtime: ConsciousRuntime) -> None:
    baseline = profile()
    runtime.observe_experience_field(
        baseline,
        evidence_id="native-observation",
        persist=False,
    )
    runtime.record_experience_recovery(
        baseline,
        profile(0.35),
        profile(0.01),
        evidence_id="native-recovery",
        persist=False,
    )
    runtime._restore_dynamic_core_state()


def test_dynamic_core_is_opt_in_and_changes_selection(tmp_path: Path):
    disabled = ConsciousRuntime(
        "disabled",
        state_path=tmp_path / "disabled.json",
        dynamic_core_enabled=False,
    )
    enabled = ConsciousRuntime(
        "enabled",
        state_path=tmp_path / "enabled.json",
        dynamic_core_enabled=True,
        dynamic_core_state_path=tmp_path / "enabled.dynamic.json",
        dynamic_core_return_weight=0.50,
    )

    assert disabled.select_trajectory(candidates())["id"] == "explore"

    seed_dynamic_runtime(enabled)
    selected = enabled.select_trajectory(candidates())
    assert selected["id"] == "preserve"
    assert "predicted_experience_field" in selected


def test_native_dynamic_state_is_restart_persistent(tmp_path: Path):
    state_path = tmp_path / "runtime.json"
    dynamic_path = tmp_path / "runtime.dynamic.json"

    runtime = ConsciousRuntime(
        "native",
        state_path=state_path,
        dynamic_core_enabled=True,
        dynamic_core_state_path=dynamic_path,
        dynamic_core_return_weight=0.50,
    )
    seed_dynamic_runtime(runtime)

    frame = {
        "response": "dynamic selection",
        "experience_field": profile().to_dict(),
        "experience_field_evidence_id": "integrated-cycle-1",
        "candidate_futures": candidates(),
    }
    runtime.integrate(frame)
    first = runtime.state.selected_trajectory
    assert first is not None
    assert first["id"] == "preserve"

    restarted = ConsciousRuntime(
        "native",
        state_path=state_path,
        dynamic_core_enabled=True,
        dynamic_core_state_path=dynamic_path,
        dynamic_core_return_weight=0.50,
    )
    second = restarted.select_trajectory(candidates())

    assert second["id"] == "preserve"
    assert restarted.state.self_model["experience_attractor_sequence"] > 0
    assert restarted.state.self_model["experience_field_sequence"] > 0


def test_model_cannot_overwrite_native_dynamic_state(tmp_path: Path):
    runtime = ConsciousRuntime(
        "protected",
        state_path=tmp_path / "runtime.json",
        dynamic_core_enabled=True,
        dynamic_core_state_path=tmp_path / "dynamic.json",
    )
    seed_dynamic_runtime(runtime)

    frame = {
        "response": "attempted overwrite",
        "self_model": {
            "experience_attractor_strength": 999.0,
            "experience_field_sequence": 999,
            "ordinary": "accepted",
        },
    }
    runtime.integrate(frame)

    assert runtime.state.self_model["experience_attractor_strength"] < 1.0
    assert runtime.state.self_model["experience_field_sequence"] < 999
    assert runtime.state.self_model["ordinary"] == "accepted"


def test_action_boundary_can_reenter_experience_field(tmp_path: Path):
    runtime = ConsciousRuntime(
        "action-boundary",
        state_path=tmp_path / "runtime.json",
        dynamic_core_enabled=True,
        dynamic_core_state_path=tmp_path / "dynamic.json",
    )
    runtime.integrate({
        "response": "prepare action",
        "candidate_futures": [
            {
                "id": "preserve",
                "signals": {"goal_fit": 1.0},
                "predicted_experience_field": profile().to_dict(),
            }
        ],
        "experience_field": profile().to_dict(),
        "experience_field_evidence_id": "pre-action",
    })
    runtime.begin_action(runtime.state.selected_trajectory)
    receipt = runtime.complete_action({
        "experience_field": profile(0.01).to_dict(),
    })

    assert receipt["experience_dynamics"]["enabled"] is True
    assert runtime.state.self_model["experience_field_sequence"] > 0
