from src.ontto.storage import OntologicalState
from src.ontto.workspace_controller import WorkspaceRuntimeConfig, WorkspaceTrajectoryController

def test_workspace_controller_has_six_specialized_modules():
    state = OntologicalState(dynamic_state=0.4,dynamic_prev_state=0.2,dynamic_memory=0.3,dynamic_pressure=0.1,dynamic_attractor_distance=0.4,dynamic_last_input=1.0,self_prediction=0.5,self_prediction_gain=0.2,self_prediction_confidence=0.8,self_prediction_error=0.1,memory_strength=0.7)
    controller = WorkspaceTrajectoryController(WorkspaceRuntimeConfig(capacity=2))
    vectors, reliability = controller.module_vectors(state)
    assert vectors.shape == (6,2)
    assert reliability.shape == (6,)