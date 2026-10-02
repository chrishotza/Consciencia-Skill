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


def test_present_integrates_self_and_world(tmp_path):
    runtime = ConsciousRuntime(
        "agent-3",
        tmp_path / "state.json",
    )
    runtime.integrate(
        {
            "response": "ok",
            "self_model": {"uncertainty": {"task": 0.4}},
            "internal_state": {"energy": 0.8},
            "intention": "understand",
            "attention": ["continuity", "self-state"],
            "memory": "The task requires continuity.",
        }
    )

    present = runtime.present("new external event")

    assert present["world_now"] == "new external event"
    assert present["self_now"]["energy"] == 0.8
    assert present["self_model"]["uncertainty"]["task"] == 0.4
    assert present["active_memory"] == ["The task requires continuity."]
    assert present["intention"] == "understand"
    assert present["attention"] == ["continuity", "self-state"]


def test_self_model_changes_trajectory_selection(tmp_path):
    runtime = ConsciousRuntime("agent-4", tmp_path / "state.json")
    runtime.integrate(
        {
            "response": "seed",
            "self_model": {
                "trajectory_weights": {
                    "continuity": 3.0,
                    "novelty": 0.0,
                }
            },
        }
    )

    candidates = [
        {
            "id": "continue",
            "intention": "preserve the current trajectory",
            "signals": {"continuity": 1.0, "novelty": 0.0},
        },
        {
            "id": "explore",
            "intention": "explore a new direction",
            "signals": {"continuity": 0.0, "novelty": 1.0},
        },
    ]

    selected = runtime.select_trajectory(candidates)
    assert selected["id"] == "continue"

    runtime.integrate(
        {
            "response": "the self-model changed",
            "self_model": {
                "trajectory_weights": {
                    "continuity": 0.0,
                    "novelty": 4.0,
                }
            },
        }
    )

    selected = runtime.select_trajectory(candidates)
    assert selected["id"] == "explore"


def test_selected_trajectory_survives_commit(tmp_path):
    runtime = ConsciousRuntime("agent-5", tmp_path / "state.json")
    runtime.integrate(
        {
            "response": "selected",
            "candidate_futures": [
                {
                    "id": "a",
                    "signals": {"continuity": 1.0},
                },
                {
                    "id": "b",
                    "signals": {"continuity": 0.0},
                },
            ],
            "self_model": {
                "trajectory_weights": {"continuity": 2.0},
            },
        }
    )

    selected = runtime.state.selected_trajectory
    assert selected is not None
    assert selected["id"] == "a"

    restarted = ConsciousRuntime("agent-5", tmp_path / "state.json")
    assert restarted.state.selected_trajectory["id"] == "a"
