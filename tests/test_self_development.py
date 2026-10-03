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
                "homeostatic_adaptation": {
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
    assert event["evidence"]["evidence_ids"] == ["a1", "a2", "a3"]


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
    runtime.state.self_model["homeostatic_adaptation"]["max_step"] = 0.02

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
