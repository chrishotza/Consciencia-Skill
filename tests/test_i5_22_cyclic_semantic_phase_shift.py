import pytest

from experiments.i5_22_cyclic_semantic_phase_shift import (
    CYCLES,
    METRICS,
    PERIOD,
    PERMUTATIONS,
    REPLICATES,
    SHIFT,
    WARMUP_CYCLES,
    pair_specificity,
    shifted_schedule,
)


def test_protocol_constants_are_frozen():
    assert REPLICATES == 24
    assert WARMUP_CYCLES == 24
    assert CYCLES == 15
    assert PERIOD == 7
    assert PERMUTATIONS == 20_000
    assert SHIFT == 1
    assert set(METRICS) == {
        "signed_auc_delta",
        "abs_auc_delta",
        "future_action_change_delta",
    }


def test_cyclic_shift_preserves_t0_multiset_and_phase_sequence():
    matched = shifted_schedule(0, 0)
    shifted = shifted_schedule(0, 0)

    assert matched[0] == shifted[0]
    labels = [row.split(" — ", 1)[0] for row in shifted]
    assert labels[0] == "A"
    assert labels[1:] == list("BCDEFGABCDEFG")


def test_pair_specificity_is_matched_minus_shifted():
    matched = {
        "future_action_change_delta": 0.5,
        "abs_auc_delta": 2.0,
        "signed_auc_delta": -1.0,
    }
    shifted = {
        "future_action_change_delta": 0.2,
        "abs_auc_delta": 1.0,
        "signed_auc_delta": -0.25,
    }
    result = pair_specificity(matched, shifted)

    assert result["future_action_change_delta"] == pytest.approx(0.3)
    assert result["abs_auc_delta"] == pytest.approx(1.0)
    assert result["signed_auc_delta"] == pytest.approx(-0.75)
