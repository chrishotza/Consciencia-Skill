import numpy as np

from experiments.i5_20_semantic_permutation_specificity import (
    CYCLES,
    METRICS,
    PERMUTATIONS,
    REPLICATES,
    WARMUP_CYCLES,
    pair_specificity,
    permute_schedule,
)


def test_protocol_constants_are_frozen():
    assert REPLICATES == 24
    assert WARMUP_CYCLES == 24
    assert CYCLES == 15
    assert PERMUTATIONS == 20_000
    assert set(METRICS) == {
        "signed_auc_delta",
        "abs_auc_delta",
        "future_action_change_delta",
    }


def test_semantic_permutation_preserves_multiset_and_changes_order():
    schedule = [f"SELF_MODEL {i}" for i in range(CYCLES)]
    permuted, permutation = permute_schedule(schedule)

    assert permutation != list(range(1, CYCLES))
    assert permuted[0] == schedule[0]
    assert sorted(permuted[1:]) == sorted(schedule[1:])
    assert all(permuted[i] != schedule[i] for i in range(1, CYCLES))


def test_pair_specificity_is_matched_minus_permuted():
    base = [
        {
            "future_action_change_rate": 0.0,
            "state_auc_abs": 0.0,
            "state_auc_signed": 0.0,
        }
    ]
    matched = [
        {
            "future_action_change_rate": 0.5,
            "state_auc_abs": 2.0,
            "state_auc_signed": -1.0,
        }
    ]
    permuted = [
        {
            "future_action_change_rate": 0.2,
            "state_auc_abs": 1.0,
            "state_auc_signed": -0.25,
        }
    ]
    result = pair_specificity(base, matched, permuted)

    assert result["future_action_change_delta"] == 0.3
    assert result["abs_auc_delta"] == 1.0
    assert result["signed_auc_delta"] == -0.75


def test_permutation_specificity_is_zero_when_conditions_match():
    base = [
        {
            "future_action_change_rate": 0.0,
            "state_auc_abs": 0.0,
            "state_auc_signed": 0.0,
        }
    ]
    rows = [
        {
            "future_action_change_rate": 0.3,
            "state_auc_abs": 1.0,
            "state_auc_signed": -0.5,
        }
    ]
    result = pair_specificity(base, rows, rows)

    assert np.allclose(
        [result["future_action_change_delta"]],
        [0.0],
    )
