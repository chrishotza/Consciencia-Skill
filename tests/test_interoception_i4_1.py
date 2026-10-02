from src.ontto.interoceptive_meta_observer import InteroceptiveMetaObserver
from src.ontto.interoception import InteroceptiveSnapshot

def test_observer_can_learn_action_conditioned_error():
    m=InteroceptiveMetaObserver()
    s=InteroceptiveSnapshot(0.2,0.8,0.3,0.4,0.2,0.5,0.3,0.7)
    for action in (-1.0,0.0,1.0):
        for i in range(12):
            predicted=0.7
            actual=predicted + 0.03 + 0.08*abs(action)
            m.observe(snapshot=s,action=action,predicted_operating_condition=predicted,actual_operating_condition=actual)
    low=m.predict_error(snapshot=s,action=0.0,predicted_operating_condition=0.7)
    high=m.predict_error(snapshot=s,action=1.0,predicted_operating_condition=0.7)
    assert high > low

def test_permuted_keeps_sample_count_and_changes_targets():
    m=InteroceptiveMetaObserver()
    s=InteroceptiveSnapshot(0.2,0.8,0.3,0.4,0.2,0.5,0.3,0.7)
    for i in range(16):
        m.observe(
            snapshot=s,
            action=float(i%2),
            predicted_operating_condition=0.7,
            actual_operating_condition=0.70 + 0.01*i,
        )
    q=m.permuted(7)
    assert len(q.targets)==len(m.targets)
    assert q.targets != m.targets
