from skill_conscious import ConsciousRuntime


def _complete_observed_action(runtime, value, label):
    runtime.begin_action({"id": label, "signals": {"continuity": 1.0}})
    return runtime.complete_action(
        {
            "status": "success",
            "interoceptive_state": {"energy": value},
        }
    )


def _configured_runtime(tmp_path):
    runtime = ConsciousRuntime("adaptive-agent", tmp_path / "state.json")
    runtime.integrate(
        {
            "response": "initialize adaptive target",
            "self_model": {
                "homeostatic_targets": {"energy": 0.8},
                "homeostatic_target_adaptation": {
                    "enabled": True,
                    "min_samples": 3,
                    "error_threshold": 0.25,
                    "confidence_threshold": 0.75,
                    "required_high_error": 3,
                    "learning_rate": 0.5,
                    "max_step": 0.05,
                    "cooldown": 2,
                    "bounds": {"energy": [0.0, 1.0]},
                },
            },
            "interoceptive_state": {"energy": 0.4},
        }
    )
    return runtime


def test_adaptive_target_requires_accumulated_evidence(tmp_path):
    runtime = _configured_runtime(tmp_path)

    _complete_observed_action(runtime, 0.4, "a1")
    _complete_observed_action(runtime, 0.4, "a2")
    assert runtime.state.self_model["homeostatic_targets"]["energy"] == 0.8

    receipt = _complete_observed_action(runtime, 0.4, "a3")

    assert receipt["target_adaptation"]["updated"] is True
    assert runtime.state.self_model["homeostatic_targets"]["energy"] == 0.75
    event = runtime.state.self_model["homeostatic_adaptation_history"][-1]
    assert event["target"] == "energy"
    assert event["cause"] == "accumulated_host_observation"
    assert event["evidence"]["sample_count"] == 3
    evidence_ids = event["evidence"]["evidence_ids"]
    assert len(evidence_ids) == 3
    assert all(evidence_ids)
    assert evidence_ids == [item["action_id"] for item in runtime.state.action_history[-3:]]


def test_adaptive_target_persists_across_restart(tmp_path):
    runtime = _configured_runtime(tmp_path)
    _complete_observed_action(runtime, 0.4, "a1")
    _complete_observed_action(runtime, 0.4, "a2")
    _complete_observed_action(runtime, 0.4, "a3")

    restarted = ConsciousRuntime("adaptive-agent", tmp_path / "state.json")

    assert restarted.state.self_model["homeostatic_targets"]["energy"] == 0.75
    assert restarted.state.self_model["homeostatic_adaptation_evidence"]["energy"]["last_update_sequence"] == 3
    assert restarted.state.self_model["homeostatic_adaptation_history"][-1]["after"] == 0.75


def test_adaptive_target_is_bounded_per_update(tmp_path):
    runtime = _configured_runtime(tmp_path)
    runtime.state.self_model["homeostatic_target_adaptation"]["max_step"] = 0.02

    for index in range(3):
        _complete_observed_action(runtime, 0.0, f"b{index + 1}")

    assert runtime.state.self_model["homeostatic_targets"]["energy"] == 0.78
    assert abs(runtime.state.self_model["homeostatic_adaptation_history"][-1]["delta"]) <= 0.02


def test_adaptive_target_abstains_without_interoceptive_observation(tmp_path):
    runtime = _configured_runtime(tmp_path)
    runtime.begin_action({"id": "no-observation", "signals": {}})
    receipt = runtime.complete_action({"status": "success"})

    assert receipt["target_adaptation"]["updated"] is False
    assert runtime.state.self_model["homeostatic_targets"]["energy"] == 0.8


def _configured_priority_runtime(tmp_path):
    runtime = ConsciousRuntime("priority-agent", tmp_path / "priority.json")
    runtime.integrate(
        {
            "response": "initialize priority adaptation",
            "self_model": {
                "trajectory_weights": {"learning": 0.0},
                "trajectory_priority_adaptation": {
                    "enabled": True,
                    "min_samples": 3,
                    "utility_threshold": 0.5,
                    "confidence_threshold": 0.75,
                    "learning_rate": 0.5,
                    "max_step": 0.25,
                    "cooldown": 2,
                    "bounds": {"learning": [-3.0, 3.0]},
                },
            },
        }
    )
    return runtime


def _record_priority_consequence(runtime, utility, label):
    runtime.begin_action({"id": label, "signals": {"learning": 1.0}})
    runtime.complete_action({"status": "success"})
    runtime.integrate(
        {
            "response": "evaluate observed consequence",
            "consequence_trajectory": "learn",
            "consequence": {"status": "success"},
            "self_evaluation": {
                "utility": utility,
                "credited_signal": "learning",
                "weight_delta": 99.0,
            },
        }
    )


def test_priority_adaptation_requires_accumulated_evidence(tmp_path):
    runtime = _configured_priority_runtime(tmp_path)

    _record_priority_consequence(runtime, 1.0, "p1")
    _record_priority_consequence(runtime, 1.0, "p2")
    assert runtime.state.self_model["trajectory_weights"]["learning"] == 0.0

    _record_priority_consequence(runtime, 1.0, "p3")

    assert runtime.state.self_model["trajectory_weights"]["learning"] == 0.25
    update = runtime.state.self_model["trajectory_priority_adaptation_history"][-1]
    assert update["cause"] == "accumulated_consequence_evaluation"
    assert update["ignored_direct_weight_delta"] == 99.0
    assert update["evidence"]["sample_count"] == 3


def test_priority_adaptation_persists_across_restart(tmp_path):
    runtime = _configured_priority_runtime(tmp_path)
    for index in range(3):
        _record_priority_consequence(runtime, 1.0, f"p{index + 1}")

    restarted = ConsciousRuntime("priority-agent", tmp_path / "priority.json")

    assert restarted.state.self_model["trajectory_weights"]["learning"] == 0.25
    assert restarted.state.self_model["trajectory_priority_adaptation_history"][-1]["after"] == 0.25


def test_adaptive_target_cannot_be_replaced_by_model_frame(tmp_path):
    runtime = _configured_runtime(tmp_path)

    runtime.integrate(
        {
            "response": "model proposes a new target",
            "self_model": {
                "homeostatic_targets": {"energy": 0.1},
            },
        }
    )

    assert runtime.state.self_model["homeostatic_targets"]["energy"] == 0.8


def test_runtime_owned_evidence_cannot_be_injected_by_model(tmp_path):
    runtime = _configured_runtime(tmp_path)

    runtime.integrate(
        {
            "response": "model proposes fake evidence",
            "self_model": {
                "homeostatic_adaptation_evidence": {
                    "energy": {
                        "sample_count": 999,
                        "mean_error": 1.0,
                    }
                },
            },
        }
    )

    assert "homeostatic_adaptation_evidence" not in runtime.state.self_model


