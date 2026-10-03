from experiments.llm_longitudinal_benchmark import DeterministicProvider, benchmark_with_llm


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
