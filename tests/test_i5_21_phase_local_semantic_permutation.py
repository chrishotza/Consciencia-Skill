import pytest

from experiments.i5_21_phase_local_semantic_permutation import (
    CYCLES,
    LOCAL_PERMUTATION,
    METRICS,
    PERIOD,
    PERMUTATIONS,
    REPLICATES,
    WARMUP_CYCLES,
    pair_specificity,
    permute_schedule_within_period,
)


def test_protocol_constants_are_frozen():
    assert REPLICATES == 24
    assert WARMUP_CYCLES == 24
    assert CYCLES == 15
    assert PERIOD == 7
    assert PERMUTATIONS == 20_000
    assert len(LOCAL_PERMUTATION) == PERIOD
    assert set(METRICS) == {
        "signed_auc_delta",
        "abs_auc_delta",
        "future_action_change_delta",
    }


def test_local_permutation_preserves_each_period_multiset_and_t0():
    schedule = [f"SELF_MODEL {i}" for i in range(CYCLES)]
    permuted, sources = permute_schedule_within_period(schedule)

    assert permuted[0] == schedule[0]
    assert len(sources) == 2
    assert all(len(block) == PERIOD for block in sources)
    for offset in (0, PERIOD):
        original = schedule[1 + offset:1 + offset + PERIOD]
        shuffled = permuted[1 + offset:1 + offset + PERIOD]
        assert sorted(original) == sorted(shuffled)
        assert all(
            shuffled[i] != original[i]
            for i in range(PERIOD)
        )


def test_pair_specificity_is_matched_minus_local_permuted():
    matched = {
        "future_action_change_delta": 0.5,
        "abs_auc_delta": 2.0,
        "signed_auc_delta": -1.0,
    }
    permuted = {
        "future_action_change_delta": 0.2,
        "abs_auc_delta": 1.0,
        "signed_auc_delta": -0.25,
    }
    result = pair_specificity(matched, permuted)

    assert result["future_action_change_delta"] == pytest.approx(0.3)
    assert result["abs_auc_delta"] == pytest.approx(1.0)
    assert result["signed_auc_delta"] == pytest.approx(-0.75)
