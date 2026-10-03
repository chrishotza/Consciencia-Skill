from dataclasses import replace
from pathlib import Path

from skill_conscious import ConsciousHostLoop, ConsciousRuntime, ExperienceFieldProfile


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


def futures(now_offset: float = 0.0) -> list[dict]:
    return [
        {
            "id": "preserve",
            "signals": {"goal_fit": 0.49},
            "predicted_experience_field": profile(0.01).to_dict(),
        },
        {
            "id": "explore",
            "signals": {"goal_fit": 0.52},
            "predicted_experience_field": profile(0.35 if now_offset == 0.0 else 0.45).to_dict(),
        },
    ]


def test_host_loop_closes_dynamic_cycle_and_persists(tmp_path: Path):
    runtime = ConsciousRuntime(
        "host-dynamic",
        state_path=tmp_path / "runtime.json",
        dynamic_core_enabled=True,
        dynamic_core_state_path=tmp_path / "dynamic.json",
        dynamic_core_return_weight=0.50,
    )

    model_calls = []

    def model(prompt: str):
        model_calls.append(prompt)
        if len(model_calls) == 1:
            return {
                "response": "initial",
                "experience_field": profile().to_dict(),
                "experience_field_evidence_id": "host-observation-1",
                "candidate_futures": futures(),
            }
        return {
            "response": "evaluated consequence",
            "candidate_futures": futures(0.35),
            "self_evaluation": {
                "utility": 1.0,
                "credited_signal": "coherence",
            },
        }

    def execute_action(trajectory, snapshot):
        return {
            "world_change": "action executed",
            "experience_field": profile(0.35).to_dict(),
            "self_state": {"action_count": 1.0},
        }

    loop = ConsciousHostLoop(
        runtime,
        model=model,
        execute_action=execute_action,
    )
    result = loop.step("external situation")

    assert result["action_executed"] is True
    assert result["selected_trajectory"]["id"] == "preserve"
    assert result["next_trajectory"]["id"] == "preserve"
    assert result["consequence"]["experience_field"]["prediction_error"] > 0.0
    assert runtime.state.action_history[-1]["experience_dynamics"]["enabled"] is True
    assert runtime.state.self_model["experience_attractor_sequence"] > 0
    assert runtime.state.self_model["experience_field_sequence"] > 0

    restarted = ConsciousRuntime(
        "host-dynamic",
        state_path=tmp_path / "runtime.json",
        dynamic_core_enabled=True,
        dynamic_core_state_path=tmp_path / "dynamic.json",
        dynamic_core_return_weight=0.50,
    )
    selected_after_restart = restarted.select_trajectory(futures(0.35))
    assert selected_after_restart["id"] == "preserve"
