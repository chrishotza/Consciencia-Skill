import numpy as np
import pytest

from src.ontto.attention_controller import ATTENTION_MODULES, AttentionSchema


def test_prediction_normalizes():
    schema = AttentionSchema()
    weights = schema.predict(np.asarray([1.0, 0.0]))
    assert weights.shape == (4,)
    assert np.isclose(weights.sum(), 1.0)


def test_attention_tracks_state_code():
    schema = AttentionSchema()
    alloc = schema.allocate(np.asarray([-1.0, 0.0]))
    assert alloc.selected_index == 3


def test_modes_are_distinct():
    schema = AttentionSchema()
    state = np.asarray([1.0, 0.0])
    full = schema.allocate(state, mode="full")
    shuffled = schema.allocate(state, mode="shuffled")
    uniform = schema.allocate(state, mode="uniform")
    assert full.weights != shuffled.weights
    assert uniform.weights != full.weights


def test_invalid_state_rejected():
    schema = AttentionSchema()
    with pytest.raises(ValueError):
        schema.predict(np.zeros(3))


def test_module_set_is_fixed():
    assert ATTENTION_MODULES == (1, 2, 3, 4)
