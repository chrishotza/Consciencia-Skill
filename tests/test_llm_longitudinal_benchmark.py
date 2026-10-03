from experiments.llm_longitudinal_benchmark import (
    DeterministicProvider,
    benchmark_with_llm,
    run_causal_provider_ab,
)


def test_deterministic_llm_runs_all_longitudinal_conditions():
    report = benchmark_with_llm(
        DeterministicProvider(),
        cycles=8,
        restart_every=4,
    )

    assert report["protocol"] == "llm-longitudinal-v1"
    assert report["provider_boundary"] == "provider-neutral"
    assert report["not_a_phenomenal_consciousness_test"] is True
    assert len(report["conditions"]) == 5

    for result in report["conditions"]:
        assert len(result["selected_trajectories"]) == 8
        assert len(result["final_state_hash"]) == 64


def test_deterministic_llm_preserves_metacognitive_and_self_observation_layers():
    result = benchmark_with_llm(
        DeterministicProvider(),
        cycles=8,
        restart_every=4,
    )["conditions"][-1]

    assert result["prediction_samples"] == 8
    assert result["prediction_error_mean"] is not None
    assert result["self_observation_samples"] == 8


def test_causal_provider_ab_changes_downstream_selection_under_matched_conditions():
    report = run_causal_provider_ab(cycles=8)

    assert report["protocol"] == "llm-causal-ab-v1"
    assert report["same_initial_runtime"] is True
    assert report["same_candidate_field"] is True
    assert report["same_outcome_rule"] is True
    assert report["selection_diverged"] is True
    assert report["divergence_cycles"]

    continuity = report["branches"]["continuity_policy"]
    learning = report["branches"]["learning_policy"]

    assert continuity["selected_trajectories"] != learning["selected_trajectories"]
    assert continuity["final_state_hash"] != learning["final_state_hash"]
    assert continuity["final_trajectory_weights"]["continuity"] == 3.0
    assert learning["final_trajectory_weights"]["learning"] == 3.0


def test_causal_provider_ab_is_repeatable():
    first = run_causal_provider_ab(cycles=8)
    second = run_causal_provider_ab(cycles=8)

    assert first["branches"]["continuity_policy"]["selected_trajectories"] == (
        second["branches"]["continuity_policy"]["selected_trajectories"]
    )
    assert first["branches"]["learning_policy"]["selected_trajectories"] == (
        second["branches"]["learning_policy"]["selected_trajectories"]
    )
    assert first["branches"]["continuity_policy"]["final_state_hash"] == (
        second["branches"]["continuity_policy"]["final_state_hash"]
    )
    assert first["branches"]["learning_policy"]["final_state_hash"] == (
        second["branches"]["learning_policy"]["final_state_hash"]
    )
