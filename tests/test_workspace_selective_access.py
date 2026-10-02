import numpy as np

from src.ontto.attention_controller import AttentionSchema
from src.ontto.storage import OntologicalState
from src.ontto.workspace_controller import WorkspaceRuntimeConfig
from src.ontto.workspace_selective_access import WorkspaceSelectiveAccessController


def make_state() -> OntologicalState:
    return OntologicalState(
        dynamic_state=0.4,
        dynamic_prev_state=0.2,
        dynamic_memory=0.3,
        dynamic_pressure=0.1,
        dynamic_attractor_distance=0.4,
        dynamic_last_input=1.0,
        self_prediction=0.5,
        self_prediction_gain=0.2,
        self_prediction_confidence=0.8,
        self_prediction_error=0.1,
        memory_strength=0.7,
    )


def test_query_and_attention_are_both_recorded():
    controller = WorkspaceSelectiveAccessController(
        WorkspaceRuntimeConfig(capacity=2),
        query_mode="full",
        attention_mode="full",
        access_weight=0.35,
    )
    candidates = ()
    state = make_state()
    vectors, _ = controller.workspace_controller.module_vectors(state)
    selection = controller.workspace_controller.select(state)
    broadcast = selection.broadcast
    query = controller.query.query(vectors, broadcast)
    attention = AttentionSchema().allocate(broadcast)
    assert query.module_index in (2, 3, 4, 5)
    assert len(attention.weights) == 4


def test_modes_change_broadcast_or_attention():
    state = make_state()
    candidates = ()
    full = WorkspaceSelectiveAccessController(
        WorkspaceRuntimeConfig(capacity=2), query_mode="full", attention_mode="full"
    )
    shuffled = WorkspaceSelectiveAccessController(
        WorkspaceRuntimeConfig(capacity=2), query_mode="shuffled", attention_mode="full"
    )
    fsel = full.workspace_controller.select(state)
    ssel = shuffled.workspace_controller.select(state)
    assert not np.allclose(fsel.broadcast[::-1], ssel.broadcast)
