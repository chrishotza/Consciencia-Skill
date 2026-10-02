import numpy as np
import pytest

from experiments.i5_24_global_shift_lag_interaction import (
    interaction_permutation_test,
    interaction_statistic,
)


def test_additive_surface_has_zero_interaction():
    shifts = np.arange(6, dtype=float)[:, None]
    lags = np.arange(6, dtype=float)[None, :]
    cell = shifts + 10.0 * lags
    matrix = np.stack([cell + i for i in range(6)], axis=0)

    assert interaction_statistic(matrix) == pytest.approx(0.0)


def test_checkerboard_surface_has_positive_interaction():
    cell = np.array(
        [
            [1, -1, 1, -1, 1, -1],
            [-1, 1, -1, 1, -1, 1],
            [1, -1, 1, -1, 1, -1],
            [-1, 1, -1, 1, -1, 1],
            [1, -1, 1, -1, 1, -1],
            [-1, 1, -1, 1, -1, 1],
        ],
        dtype=float,
    )
    matrix = np.stack([cell * (1.0 + 0.1 * i) for i in range(24)], axis=0)

    result = interaction_permutation_test(matrix, seed=7, permutations=500)
    assert result["observed_interaction_statistic"] > 0.0
    assert 0.0 <= result["permutation_p"] <= 1.0


def test_interaction_permutation_is_deterministic():
    rng = np.random.default_rng(3)
    matrix = rng.normal(size=(8, 6, 6))

    a = interaction_permutation_test(matrix, seed=11, permutations=300)
    b = interaction_permutation_test(matrix, seed=11, permutations=300)

    assert a == b
