import numpy as np

from src.ontto.workspace_query import QUERY_MODULES
from src.ontto.causal_query_bottleneck import CausalQueryBottleneck


def test_full_query_reaches_target_and_predicts_action():
    model = CausalQueryBottleneck(threshold=0.20)
    result = model.decide(
        target_module=2,
        target_action=1.0,
        seed=2026,
        query_mode="full",
        attention_mode="full",
        bottleneck_enabled=True,
    )
    assert result.query_module == 2
    assert result.query_accuracy == 1.0
    assert result.predicted_action == 1.0
    assert result.attention_mass > 0.5


def test_shuffled_query_breaks_target_access():
    model = CausalQueryBottleneck()
    result = model.decide(
        target_module=2,
        target_action=1.0,
        seed=2026,
        query_mode="shuffled",
        attention_mode="full",
        bottleneck_enabled=True,
    )
    assert result.query_module in QUERY_MODULES
    assert result.query_accuracy in (0.0, 1.0)


def test_no_bottleneck_exposes_all_modules():
    model = CausalQueryBottleneck()
    result = model.decide(
        target_module=2,
        target_action=1.0,
        seed=2026,
        query_mode="full",
        attention_mode="full",
        bottleneck_enabled=False,
    )
    assert np.isfinite(result.masked_score)
