import numpy as np
import pytest

from experiments.i5_23_cyclic_shift_sweep import (
    CYCLES,LAGS,METRICS,PERIOD,PERMUTATIONS,REPLICATES,SHIFTS,WARMUP_CYCLES,
    build_schedule,pair_specificity,shift_profile_max_t,shifted_schedule,sweep_max_t_adjusted_p,
)

def test_protocol_constants():
    assert (REPLICATES,WARMUP_CYCLES,CYCLES,PERIOD,PERMUTATIONS)==(24,24,15,7,20000)
    assert SHIFTS==(-3,-2,-1,1,2,3)
    assert LAGS==(-3,-2,-1,1,2,3)
    assert set(METRICS)=={"signed_auc_delta","abs_auc_delta","future_action_change_delta"}

def test_all_shifts_preserve_invariants_and_break_alignment():
    matched=build_schedule(0,0)
    content=[x.split(" — ",1)[1] for x in matched[1:]]
    labels=[x.split(" — ",1)[0] for x in matched[1:]]
    for shift in SHIFTS:
        shifted=shifted_schedule(0,0,shift)
        assert shifted[0]==matched[0]
        assert [x.split(" — ",1)[0] for x in shifted[1:]]==labels
        assert sorted(x.split(" — ",1)[1] for x in shifted[1:])==sorted(content)
        assert [x.split(" — ",1)[1] for x in shifted[1:]]!=content

def test_pair_specificity():
    matched={"future_action_change_delta":0.5,"abs_auc_delta":2.0,"signed_auc_delta":-1.0}
    shifted={"future_action_change_delta":0.2,"abs_auc_delta":1.0,"signed_auc_delta":-0.25}
    got=pair_specificity(matched,shifted)
    assert got["future_action_change_delta"]==pytest.approx(0.3)
    assert got["abs_auc_delta"]==pytest.approx(1.0)
    assert got["signed_auc_delta"]==pytest.approx(-0.75)

def test_shift_profile_max_t():
    m=np.zeros((4,6,6))
    got=shift_profile_max_t(m,seed=7,permutations=200)
    assert len(got["observed_mean_by_shift"])==6
    assert len(got["max_t_adjusted_p_by_shift"])==6
    assert 0<=got["global_any_shift_p"]<=1

def test_sweep_max_t():
    m=np.zeros((4,6,6))
    got=sweep_max_t_adjusted_p(m,seed=11,permutations=200)
    assert got["shape"]==[6,6]
    assert 0<=got["global_any_shift_any_lag_p"]<=1
