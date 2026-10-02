import numpy as np
import pytest

from experiments.i5_25_shift_lag_orientation_symmetry import (
    compensatory_diagonal_contrast,
    max_t_pair_symmetry,
    sign_flip_mean_p,
)


def test_sign_flip_mean_is_deterministic():
    x = np.array([-1.0, 1.0, 1.0, -1.0])
    a = sign_flip_mean_p(x, seed=7, permutations=300)
    b = sign_flip_mean_p(x, seed=7, permutations=300)
    assert a == b


def test_orientation_pair_count_is_eighteen():
    matrix = np.zeros((8, 6, 6))
    result = max_t_pair_symmetry(matrix, seed=7, permutations=300)
    assert result["pair_count"] == 18
    assert len(result["pair_labels"]) == 18
    assert len(result["observed_pair_means"]) == 18
    assert len(result["max_t_adjusted_p"]) == 18


def test_diagonal_contrast_zero_for_constant_surface():
    matrix = np.ones((8, 6, 6))
    result = compensatory_diagonal_contrast(matrix, seed=7, permutations=300)
    assert result["observed_mean"] == pytest.approx(0.0)
    assert 0.0 <= result["permutation_p"] <= 1.0


def test_diagonal_contrast_detects_enrichment():
    matrix = np.zeros((12, 6, 6))
    for i in range(6):
        matrix[:, i, 5 - i] = 2.0
    result = compensatory_diagonal_contrast(matrix, seed=7, permutations=300)
    assert result["observed_mean"] > 0.0
    assert result["permutation_p"] < 0.1
