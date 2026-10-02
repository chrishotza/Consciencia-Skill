from src.ontto.interoception import InteroceptiveProbe
from src.ontto.storage import OntologicalState


def test_read_only_bounded():
    state = OntologicalState(dynamic_state=0.8, dynamic_prev_state=-0.2, dynamic_pressure=2.5, dynamic_attractor_distance=3.0, self_prediction_error=0.35, self_prediction_confidence=0.8)
    before = state.to_json()
    read = InteroceptiveProbe(memory_limit=10).read(state, memory_count=4)
    assert state.to_json() == before
    assert all(0.0 <= value <= 1.0 for value in read.to_dict().values())


def test_internal_change_changes_operating_condition():
    probe = InteroceptiveProbe()
    stable = OntologicalState(self_prediction_error=0.0, self_prediction_confidence=1.0)
    stressed = OntologicalState(dynamic_state=0.8, dynamic_prev_state=-0.8, dynamic_pressure=2.0, dynamic_attractor_distance=2.0, self_prediction_error=1.0, self_prediction_confidence=0.0)
    assert probe.read(stressed, memory_count=12).operating_condition < probe.read(stable).operating_condition


def test_invalid_memory_limit():
    try:
        InteroceptiveProbe(0)
    except ValueError:
        return
    raise AssertionError("invalid memory limit accepted")
