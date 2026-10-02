from src.ontto.self_observer import SelfPrediction
from src.ontto.storage import OntologicalState
from src.ontto.trajectory_selector import TrajectoryCandidate
from src.ontto.workspace_query_task import PersistentQueryTaskController


def make_state():
    return OntologicalState(
        dynamic_state=0.4,
        dynamic_prev_state=0.2,
        dynamic_memory=0.3,
        dynamic_pressure=0.1,
        dynamic_attractor_distance=0.4,
        dynamic_last_input=1.0,
        dynamic_steps=8,
    )


def make_candidates():
    pred = SelfPrediction(predicted_state=0.2, baseline_state=0.0, confidence=1.0, samples=1)
    return (
        TrajectoryCandidate(
            signal=-1.0,
            prediction=pred,
            attractor_distance=0.2,
            displacement=0.1,
            predicted_error=None,
            score=0.5,
        ),
        TrajectoryCandidate(
            signal=1.0,
            prediction=pred,
            attractor_distance=0.2,
            displacement=0.1,
            predicted_error=None,
            score=0.5,
        ),
    )


def test_full_mode_returns_persistable_task_result():
    controller = PersistentQueryTaskController()
    chosen, result = controller.choose(make_state(), make_candidates(), seed=100)
    assert chosen.signal in (-1.0, 1.0)
    assert result.target_module in (2, 3, 4, 5)
    assert result.query_module in (2, 3, 4, 5)
    assert 0.0 <= result.attention_mass <= 1.0
    assert result.access_strength >= 0.0


def test_invalid_modes_are_rejected():
    controller = PersistentQueryTaskController()
    try:
        controller.choose(make_state(), make_candidates(), seed=100, query_mode="bad")
    except ValueError:
        pass
    else:
        raise AssertionError("invalid mode must raise")


def test_default_weight_is_positive():
    assert PersistentQueryTaskController().task_weight > 0
