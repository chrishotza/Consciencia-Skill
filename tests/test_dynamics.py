import importlib.util
from pathlib import Path
import sys

_spec = importlib.util.spec_from_file_location("skill_conscious_dynamics", Path(__file__).parents[1] / "src" / "skill_conscious" / "dynamics.py")
_module = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _module
_spec.loader.exec_module(_module)
compare_dynamics = _module.compare_dynamics
measure_dynamics = _module.measure_dynamics


def _oscillation(length=128, phase=0.0):
    import math
    return [math.sin(2.0 * math.pi * index / 16.0 + phase) for index in range(length)]


def test_profile_is_deterministic_and_bounded():
    profile_a = measure_dynamics([_oscillation(), _oscillation()])
    profile_b = measure_dynamics([_oscillation(), _oscillation()])
    assert profile_a == profile_b
    assert 0.0 <= profile_a.lz_complexity <= 1.0
    assert 0.0 <= profile_a.pairwise_correlation <= 1.0
    assert profile_a.metastability >= 0.0
    assert profile_a.avalanche_count >= 0


def test_phase_shift_can_reduce_pairwise_correlation_without_changing_shape():
    aligned = measure_dynamics([_oscillation(), _oscillation()])
    shifted = measure_dynamics([_oscillation(), _oscillation(phase=1.2)])
    assert aligned.pairwise_correlation >= shifted.pairwise_correlation


def test_recurrent_signal_is_more_regular_than_deterministic_noise_like_sequence():
    regular = [_oscillation(256)]
    noisy = [[((index * 37) % 101) / 50.0 - 1.0 for index in range(256)]]
    regular_profile = measure_dynamics(regular)
    noisy_profile = measure_dynamics(noisy)
    assert regular_profile.lz_complexity <= noisy_profile.lz_complexity


def test_compare_dynamics_reports_directional_changes():
    baseline = measure_dynamics([_oscillation(), _oscillation()])
    current = measure_dynamics([_oscillation(), _oscillation(phase=1.2)])
    delta = compare_dynamics(baseline, current)
    assert "pairwise_correlation" in delta
    assert delta["pairwise_correlation"] <= 0.0
