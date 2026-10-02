import numpy as np
import pytest

from experiments.i5_18_global_phase_bridge_interaction import (
    LAGS,
    aggregate_bridge_effect,
    max_t_adjusted_p,
    phase_interaction_permutation,
)


def test_max_t_adjusted_p_is_deterministic():
    matrix = np.asarray(
        [
            [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0],
            [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0],
            [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0],
            [-2.0, -1.0, 0.0, 1.0, 2.0, 3.0],
        ],
        dtype=float,
    )
    a = max_t_adjusted_p(matrix, seed=123, permutations=1000)
    b = max_t_adjusted_p(matrix, seed=123, permutations=1000)
    assert a == b
    assert set(a["observed_mean"]) == {str(lag) for lag in LAGS}
    assert all(0.0 <= p <= 1.0 for p in a["max_t_adjusted_p"].values())


def test_phase_interaction_is_small_for_constant_phase_effect():
    matrix = np.ones((12, 6), dtype=float) * -0.5
    result = phase_interaction_permutation(matrix, seed=7, permutations=1000)
    assert result["observed_interaction_statistic"] == pytest.approx(0.0)
    assert result["permutation_p"] >= 0.5


def test_phase_interaction_detects_strong_phase_dependence():
    matrix = np.tile(np.asarray([0.0, 0.0, 0.0, 3.0, 3.0, 3.0]), (12, 1))
    result = phase_interaction_permutation(matrix, seed=9, permutations=2000)
    assert result["observed_interaction_statistic"] > 0.0
    assert result["permutation_p"] < 0.1


def test_global_bridge_effect_uses_replicate_level_sign_flip():
    matrix = np.ones((8, 6), dtype=float) * -1.0
    result = aggregate_bridge_effect(matrix, seed=11, permutations=1000)
    assert result["mean_across_lags"] == pytest.approx(-1.0)
    assert result["replicate_count"] == 8
    assert result["replicate_mean_sign_flip_p"] < 0.1
