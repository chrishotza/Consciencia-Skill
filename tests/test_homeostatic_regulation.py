from skill_conscious import ConsciousRuntime


def test_homeostatic_error_and_fit_are_derived_from_persistent_targets(tmp_path):
    runtime = ConsciousRuntime("homeostatic-agent", tmp_path / "state.json")
    runtime.integrate(
        {
            "response": "observe internal condition",
            "self_model": {
                "homeostatic_targets": {
                    "energy": 0.9,
                    "thermal_load": 0.1,
                }
            },
            "interoceptive_state": {
                "energy": 0.5,
                "thermal_load": 0.2,
            },
        }
    )

    assert runtime.calculate_homeostatic_error() == 0.25
    assert runtime.homeostatic_fit() == 0.75
    assert runtime.state.affective_state["homeostatic_error"] == 0.25
    assert runtime.state.affective_state["homeostatic_fit"] == 0.75

    restarted = ConsciousRuntime("homeostatic-agent", tmp_path / "state.json")
    assert restarted.homeostatic_fit() == 0.75
    assert restarted.state.self_model["homeostatic_targets"]["energy"] == 0.9


def test_homeostatic_signal_can_outweigh_external_goal(tmp_path):
    runtime = ConsciousRuntime("homeostatic-select", tmp_path / "state.json")
    runtime.integrate(
        {
            "response": "configure self relevance",
            "self_model": {
                "trajectory_weights": {
                    "goal_fit": 1.0,
                    "homeostatic_fit": 3.0,
                },
                "homeostatic_targets": {"energy": 0.8},
            },
            "interoceptive_state": {"energy": 0.6},
        }
    )

    selected = runtime.select_trajectory(
        [
            {
                "id": "external-goal",
                "signals": {
                    "goal_fit": 1.0,
                    "homeostatic_fit": 0.2,
                },
            },
            {
                "id": "internal-stability",
                "signals": {
                    "goal_fit": 0.0,
                    "homeostatic_fit": 0.9,
                },
            },
        ]
    )

    assert selected["id"] == "internal-stability"


def test_predicted_internal_state_changes_future_score(tmp_path):
    runtime = ConsciousRuntime("homeostatic-prediction", tmp_path / "state.json")
    runtime.integrate(
        {
            "response": "set internal target",
            "self_model": {
                "homeostatic_targets": {"energy": 0.8},
                "trajectory_weights": {"homeostatic_fit": 2.0},
            },
            "interoceptive_state": {"energy": 0.2},
        }
    )

    depleted = {
        "id": "depleted",
        "predicted_interoceptive_state": {"energy": 0.1},
        "signals": {},
    }
    restored = {
        "id": "restored",
        "predicted_interoceptive_state": {"energy": 0.8},
        "signals": {},
    }

    assert runtime.select_trajectory([depleted, restored])["id"] == "restored"


def test_observed_embodied_outcome_updates_state_and_homeostasis(tmp_path):
    path = tmp_path / "outcome.json"
    runtime = ConsciousRuntime("embodied-outcome", path)
    runtime.integrate(
        {
            "response": "prepare action",
            "self_model": {
                "homeostatic_targets": {"energy": 0.8},
            },
            "interoceptive_state": {"energy": 0.2},
        }
    )

    before = runtime.homeostatic_fit()
    runtime.begin_action({"id": "recover", "signals": {"homeostatic_fit": 0.9}})
    receipt = runtime.complete_action(
        {
            "status": "success",
            "interoceptive_state": {"energy": 0.75},
            "affective_state": {"valence": 0.4},
            "temporal_state": {"dt": 0.5},
        }
    )

    assert before == 0.4
    assert runtime.homeostatic_fit() == 0.95
    assert receipt["homeostatic_delta"] == 0.55
    assert runtime.state.interoceptive_state["energy"] == 0.75
    assert runtime.state.affective_state["valence"] == 0.4
    assert runtime.state.affective_state["homeostatic_fit"] == 0.95
    assert runtime.state.temporal_state["dt"] == 0.5

    restarted = ConsciousRuntime("embodied-outcome", path)
    assert restarted.homeostatic_fit() == 0.95
    assert restarted.state.action_history[-1]["observed_layers"]["interoceptive_state"]["energy"] == 0.75


def test_generated_candidates_include_internal_regulation_option(tmp_path):
    runtime = ConsciousRuntime("homeostatic-candidates", tmp_path / "state.json")
    runtime.integrate(
        {
            "response": "internal pressure is present",
            "self_model": {"homeostatic_targets": {"energy": 0.9}},
            "interoceptive_state": {"energy": 0.2},
        }
    )

    candidates = runtime.generate_candidate_futures()
    assert any(item["id"] == "restore_homeostasis" for item in candidates)
