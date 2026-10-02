import numpy as np

from experiments.i6_1_causal_self_model_loop import (
    SIGNALS,
    run_replicate,
    sign_flip_test,
)


def test_protocol_signals_are_frozen():
    assert SIGNALS == (-1.0, 0.0, 1.0)


def test_sign_flip_test_is_deterministic():
    values = np.asarray([1.0, 1.0, 1.0, 1.0])
    a = sign_flip_test(values, seed=7, permutations=300)
    b = sign_flip_test(values, seed=7, permutations=300)
    assert a == b
    assert 0.0 <= a["permutation_p"] <= 1.0


def test_replicate_returns_all_causal_conditions():
    result = run_replicate(seed=20261027, warmup_cycles=6, evaluation_cycles=8)
    required = {
        "intact_regret_mean",
        "prediction_lesion_regret_mean",
        "frozen_update_regret_mean",
        "intact_minus_prediction_lesion_regret",
        "intact_minus_frozen_update_regret",
        "prediction_lesion_choice_dependence_rate",
        "frozen_update_choice_dependence_rate",
    }
    assert required <= set(result)
    assert 0.0 <= result["prediction_lesion_choice_dependence_rate"] <= 1.0
    assert 0.0 <= result["frozen_update_choice_dependence_rate"] <= 1.0
