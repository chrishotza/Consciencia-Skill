from experiments.interoception_i2 import OOD_PERTURBATIONS, run_condition


def test_i2_condition_is_deterministic():
    a = run_condition(4201, 0.5, 'full')
    b = run_condition(4201, 0.5, 'full')
    assert a == b


def test_i2_control_modes_produce_valid_endpoints():
    for mode in ('full', 'none', 'shuffled', 'clamped', 'lesion', 'rescue'):
        row = run_condition(4202, OOD_PERTURBATIONS[0], mode)
        assert row['ood'] is True
        assert 0.0 < row['recovery_score'] <= 1.0
        assert 0.0 <= row['mean_operating_condition'] <= 1.0
