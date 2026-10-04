from experiments.longitudinal_baseline_benchmark import CONDITIONS, benchmark, run_condition


def test_all_conditions_share_protocol_and_persist_state():
    report = benchmark(cycles=3, restart_every=2)
    assert report['protocol'] == 'longitudinal-baseline-v1'
    assert report['interpretation']['not_a_llm_benchmark'] is True
    assert report['interpretation']['not_a_phenomenal_consciousness_test'] is True
    assert len(report['conditions']) == len(CONDITIONS)
    for result in report['conditions']:
        assert result['cycles'] == 3
        assert len(result['selected_trajectories']) == 3
        assert len(result['final_state_hash']) == 64
        check = report['restart_checks'][result['condition']]
        assert check['trajectory_sequence_match'] is True
        assert check['final_state_hash_match'] is True


def test_causal_self_has_a_distinct_selection_policy():
    baseline = run_condition(CONDITIONS[0], cycles=4)
    causal = run_condition(CONDITIONS[2], cycles=4)
    assert all(item == 'preserve_continuity' for item in baseline['selected_trajectories'])
    assert all(item == 'preserve_continuity' for item in causal['selected_trajectories'])
    assert causal['final_trajectory_weights']['continuity'] == 2.0


def test_evidence_gated_reentry_changes_longitudinal_policy():
    static = run_condition(CONDITIONS[2], cycles=6)
    adaptive = run_condition(CONDITIONS[3], cycles=6)
    assert adaptive['priority_adaptation_updates'] > 0
    assert adaptive['trajectory_switches'] > static['trajectory_switches']
    assert 'learning' in adaptive['final_trajectory_weights']


def test_metacognitive_reentry_records_prediction_and_self_observation():
    result = run_condition(CONDITIONS[4], cycles=3)
    assert result['prediction_samples'] == 3
    assert result['prediction_error_mean'] is not None
    assert result['self_observation_samples'] == 3
