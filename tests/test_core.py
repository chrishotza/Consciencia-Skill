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



def test_regime_survives_restart(tmp_path):
    path = tmp_path / "state.json"

    runtime = ConsciousRuntime("agent-6", path)
    runtime.integrate(
        {
            "response": "regime shift",
            "regime": "deep-integration",
            "attention": ["self-model", "uncertainty"],
        }
    )

    restarted = ConsciousRuntime("agent-6", path)
    assert restarted.state.regime == "deep-integration"
    assert restarted.state.attention == ["self-model", "uncertainty"]



def test_relational_topology_and_attractor_survive_restart(tmp_path):
    path = tmp_path / "state.json"

    runtime = ConsciousRuntime("agent-7", path)
    runtime.integrate(
        {
            "response": "relational state",
            "relation_topology": {
                "identity": ["self-model", "memory"],
                "self-model": ["intention"],
                "intention": ["action"],
            },
            "attractor": {
                "name": "continuity",
                "regime": "deep-integration",
            },
        }
    )

    restarted = ConsciousRuntime("agent-7", path)
    assert restarted.state.relation_topology["identity"] == ["self-model", "memory"]
    assert restarted.state.relation_topology["intention"] == ["action"]
    assert restarted.state.attractor["name"] == "continuity"


def test_valuation_influences_trajectory_and_is_persisted(tmp_path):
    path = tmp_path / "state.json"
    runtime = ConsciousRuntime("agent-8", path)
    runtime.integrate(
        {
            "response": "value matters",
            "valuation": {"meaning": 3.0},
            "valence": 0.6,
        }
    )

    candidates = [
        {
            "id": "meaning",
            "signals": {"meaning": 1.0},
        },
        {
            "id": "neutral",
            "signals": {"meaning": 0.0},
        },
    ]
    assert runtime.select_trajectory(candidates)["id"] == "meaning"

    restarted = ConsciousRuntime("agent-8", path)
    assert restarted.state.valuation["meaning"] == 3.0
    assert restarted.state.valence == 0.6


def test_transformation_log_records_self_change(tmp_path):
    path = tmp_path / "state.json"
    runtime = ConsciousRuntime("agent-9", path)
    runtime.integrate(
        {
            "response": "first",
            "regime": "baseline",
        }
    )
    runtime.integrate(
        {
            "response": "transformed",
            "regime": "deep-integration",
            "attention": ["self-model"],
            "valuation": {"continuity": 2.0},
        }
    )

    assert runtime.state.transformation_log
    event = runtime.state.transformation_log[-1]
    assert event["revision"] == 2
    assert "regime" in event["changes"]
    assert "valuation" in event["changes"]


def test_self_model_selects_and_commits_regime(tmp_path):
    path = tmp_path / "state.json"
    runtime = ConsciousRuntime("agent-10", path)
    runtime.integrate(
        {
            "response": "seed",
            "self_model": {
                "regime_weights": {
                    "integration": 3.0,
                    "exploration": 0.5,
                }
            },
        }
    )

    selected = runtime.transition_regime(
        [
            {"id": "integration", "signals": {"integration": 1.0}},
            {"id": "exploration", "signals": {"exploration": 1.0}},
        ]
    )

    assert selected["id"] == "integration"
    assert runtime.state.regime == "integration"
    assert runtime.state.transformation_log[-1]["type"] == "regime_transition"


def test_consequence_feedback_changes_future_and_survives_restart(tmp_path):
    path = tmp_path / "state.json"
    runtime = ConsciousRuntime("agent-consequence", path)
    runtime.integrate(
        {
            "response": "seed",
            "self_model": {
                "trajectory_weights": {
                    "continuity": 0.0,
                    "learning": 0.0,
                }
            },
        }
    )

    candidates = [
        {
            "id": "continue",
            "signals": {"continuity": 1.0, "learning": 0.0},
        },
        {
            "id": "learn",
            "signals": {"continuity": 0.0, "learning": 1.0},
        },
    ]
    assert runtime.select_trajectory(candidates)["id"] == "continue"

    runtime.register_consequence(
        "learn",
        {"stability": 0.2, "focus": 0.9},
        evaluation={
            "utility": 1.0,
            "credited_signal": "learning",
            "weight_delta": 2.0,
        },
    )

    assert runtime.select_trajectory(candidates)["id"] == "learn"
    assert runtime.state.self_model["trajectory_feedback"]["learn"]["count"] == 1
    assert runtime.state.workspace["last_action"] == "learn"

    restarted = ConsciousRuntime("agent-consequence", path)
    assert restarted.state.self_model["trajectory_feedback"]["learn"]["utility"] == 1.0
    assert restarted.state.self_model["trajectory_weights"]["learning"] == 2.0
    assert restarted.state.workspace["last_outcome"]["focus"] == 0.9

def test_integrate_consequence_updates_next_cycle(tmp_path):
    path = tmp_path / "state.json"
    runtime = ConsciousRuntime("agent-integrated-consequence", path)

    runtime.integrate(
        {
            "response": "initial action",
            "self_model": {
                "trajectory_weights": {
                    "continuity": 0.0,
                    "learning": 0.0,
                }
            },
            "candidate_futures": [
                {
                    "id": "continue",
                    "signals": {"continuity": 1.0, "learning": 0.0},
                },
                {
                    "id": "learn",
                    "signals": {"continuity": 0.0, "learning": 1.0},
                },
            ],
        }
    )
    assert runtime.state.selected_trajectory["id"] == "continue"

    runtime.integrate(
        {
            "response": "process the observed consequence",
            "candidate_futures": [
                {
                    "id": "continue",
                    "signals": {"continuity": 1.0, "learning": 0.0},
                },
                {
                    "id": "learn",
                    "signals": {"continuity": 0.0, "learning": 1.0},
                },
            ],
            "consequence_trajectory": "continue",
            "consequence": {"stability": -0.5, "focus": 0.8},
            "self_evaluation": {
                "utility": -1.0,
                "credited_signal": "continuity",
                "weight_delta": -2.0,
            },
        }
    )

    assert runtime.state.self_model["trajectory_feedback"]["continue"]["count"] == 1
    assert runtime.state.self_model["trajectory_weights"]["continuity"] == -2.0
    assert runtime.state.selected_trajectory["id"] == "learn"
    assert runtime.state.history[-1]["consequence"]["stability"] == -0.5
    assert runtime.state.history[-1]["consequence_trajectory"] == "continue"

    restarted = ConsciousRuntime("agent-integrated-consequence", path)
    assert restarted.state.selected_trajectory["id"] == "learn"
    assert restarted.state.history[-1]["self_evaluation"]["utility"] == -1.0


def test_conscious_host_executes_action_and_reenters_observed_consequence(tmp_path):
    from skill_conscious import ConsciousHostLoop

    path = tmp_path / "host.json"
    runtime = ConsciousRuntime("host-agent", path)
    calls = {"model": 0, "actions": 0}

    def model(prompt):
        calls["model"] += 1
        if calls["model"] == 1:
            return {
                "response": "choose learn",
                "self_model": {
                    "trajectory_weights": {
                        "continuity": 0.0,
                        "learning": 3.0,
                    }
                },
                "candidate_futures": [
                    {
                        "id": "continue",
                        "signals": {"continuity": 1.0, "learning": 0.0},
                    },
                    {
                        "id": "learn",
                        "signals": {"continuity": 0.0, "learning": 1.0},
                    },
                ],
            }
        return {
            "response": "the observed action changed my evaluation",
            "self_evaluation": {
                "utility": 0.8,
                "credited_signal": "learning",
                "weight_delta": 0.5,
            },
            "candidate_futures": [
                {
                    "id": "continue",
                    "signals": {"continuity": 1.0, "learning": 0.0},
                },
                {
                    "id": "learn",
                    "signals": {"continuity": 0.0, "learning": 1.0},
                },
            ],
        }

    def execute_action(trajectory, snapshot):
        calls["actions"] += 1
        assert trajectory["id"] == "learn"
        assert snapshot["selected_trajectory"]["id"] == "learn"
        return {
            "status": "success",
            "state_change": {"focus": 0.2},
        }

    loop = ConsciousHostLoop(
        runtime,
        model=model,
        execute_action=execute_action,
    )
    result = loop.step("perform the next task")

    assert calls["model"] == 2
    assert calls["actions"] == 1
    assert result["action_executed"] is True
    assert result["consequence"]["status"] == "success"
    assert runtime.state.self_model["trajectory_feedback"]["learn"]["count"] == 1
    assert runtime.state.self_model["trajectory_weights"]["learning"] == 3.5
    assert runtime.state.history[-1]["consequence"]["state_change"]["focus"] == 0.2

    restarted = ConsciousRuntime("host-agent", path)
    assert restarted.state.self_model["trajectory_feedback"]["learn"]["count"] == 1
    assert restarted.state.history[-1]["consequence_trajectory"] == "learn"

def test_action_lifecycle_persists_receipt(tmp_path):
    path = tmp_path / "action.json"
    runtime = ConsciousRuntime("action-agent", path)

    selected = {
        "id": "learn",
        "signals": {"learning": 1.0},
    }
    receipt = runtime.begin_action(selected)
    assert receipt["status"] == "pending"
    assert runtime.state.pending_action["action_id"] == receipt["action_id"]

    completed = runtime.complete_action(
        {"status": "success", "state_change": {"focus": 0.2}}
    )
    assert completed["status"] == "completed"
    assert completed["outcome"]["status"] == "success"
    assert runtime.state.pending_action is None
    assert runtime.state.action_history[-1]["action_id"] == receipt["action_id"]

    restarted = ConsciousRuntime("action-agent", path)
    assert restarted.state.pending_action is None
    assert restarted.state.action_history[-1]["outcome"]["state_change"]["focus"] == 0.2


def test_action_failure_is_recorded(tmp_path):
    path = tmp_path / "failure.json"
    runtime = ConsciousRuntime("failure-agent", path)
    runtime.begin_action({"id": "fail", "signals": {}})

    receipt = runtime.complete_action(
        {"error": "ToolError", "message": "execution failed"},
        status="failed",
    )

    assert receipt["status"] == "failed"
    restarted = ConsciousRuntime("failure-agent", path)
    assert restarted.state.action_history[-1]["status"] == "failed"
