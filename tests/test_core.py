from skill_conscious import ConsciousRuntime


def test_state_survives_restart(tmp_path):
    path = tmp_path / "state.json"

    first = ConsciousRuntime("agent-1", path)
    first.integrate(
        {
            "response": "first",
            "self_model": {"focus": "continuity"},
            "memory": "The agent is building continuity.",
            "internal_state": {"pressure": 0.2},
            "intention": "preserve continuity",
        }
    )

    second = ConsciousRuntime("agent-1", path)
    assert second.state.revision == 1
    assert second.state.self_model["focus"] == "continuity"
    assert second.state.memories == ["The agent is building continuity."]
    assert second.state.self_state["pressure"] == 0.2
    assert second.state.intention == "preserve continuity"


def test_prepare_exposes_persistent_self(tmp_path):
    runtime = ConsciousRuntime("agent-2", tmp_path / "state.json")
    runtime.integrate(
        {
            "response": "ok",
            "self_model": {"mode": "learning"},
        }
    )

    prompt = runtime.prepare("continue the task")

    assert "agent-2" in prompt
    assert "learning" in prompt
    assert "continue the task" in prompt
