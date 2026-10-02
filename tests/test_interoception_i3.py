from experiments.interoception_i3 import OOD_MAGNITUDES, run_condition


def test_i3_is_deterministic():
    a = run_condition(5201, 0.50, 'full')
    b = run_condition(5201, 0.50, 'full')
    assert a == b


def test_i3_runs_three_events_and_reports_overshoot():
    row = run_condition(5202, OOD_MAGNITUDES[0], 'full')
    assert row['ood'] is True
    assert len(row['event_recovery_scores']) == 3
    assert len(row['event_overshoots']) == 3
    assert row['mean_recovery'] > 0.0
    assert row['mean_overshoot'] >= 0.0


def test_i3_all_control_modes_are_valid():
    for mode in ('full', 'none', 'shuffled', 'clamped', 'lesion', 'rescue'):
        row = run_condition(5203, 0.65, mode)
        assert len(row['event_recovery_scores']) == 3
        assert 0.0 < row['final_recovery'] <= 1.0
