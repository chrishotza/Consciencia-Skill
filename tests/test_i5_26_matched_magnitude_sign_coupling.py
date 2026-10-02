import numpy as np
import pytest

from experiments.i5_26_matched_magnitude_sign_coupling import (
    matched_magnitude_cells,
    max_t_across_magnitudes,
    sign_flip_p,
)


def test_matched_magnitude_contrast_from_synthetic_surface():
    matrix = np.zeros((4, 6, 6))
    matrix[:, 0, 5] = 2.0
    matrix[:, 5, 0] = 2.0
    matrix[:, 0, 0] = 0.0
    matrix[:, 5, 5] = 0.0

    opposite, same = matched_magnitude_cells(matrix, 3)
    assert opposite.mean() == pytest.approx(2.0)
    assert same.mean() == pytest.approx(0.0)


def test_sign_flip_p_is_deterministic():
    values = np.array([1.0, 1.0, 1.0, 1.0])
    a = sign_flip_p(values, seed=7, permutations=500)
    b = sign_flip_p(values, seed=7, permutations=500)
    assert a == b
    assert 0.0 <= a["permutation_p"] <= 1.0


def test_max_t_across_magnitudes_shape_and_bounds():
    contrasts = np.zeros((8, 3))
    result = max_t_across_magnitudes(contrasts, seed=9, permutations=300)
    assert len(result["observed_mean_by_magnitude"]) == 3
    assert len(result["max_t_adjusted_p_by_magnitude"]) == 3
    assert 0.0 <= result["global_any_magnitude_p"] <= 1.0
