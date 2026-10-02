import numpy as np
from src.ontto.interoception import InteroceptiveSnapshot
from src.ontto.interoceptive_meta_observer import InteroceptiveMetaObserver

def snap():
    return InteroceptiveSnapshot(0.2,0.75,0.3,0.4,0.25,0.55,0.35,0.68)

def test_meta_observer_learns():
    m=InteroceptiveMetaObserver(); s=snap()
    for i in range(32):
        action=-1.0 if i%2 else 1.0
        pred=0.6+0.01*i
        m.observe(snapshot=s, action=action, predicted_operating_condition=pred,
                  actual_operating_condition=pred+0.02+0.01*abs(action))
    p=m.predict(snapshot=s, action=1.0, predicted_operating_condition=0.9)
    assert p.samples==32
    assert 0.0 <= p.predicted_error <= 1.0
    assert p.predicted_error > 0.0

def test_permutation_keeps_features():
    m=InteroceptiveMetaObserver(); s=snap()
    for i in range(8):
        m.observe(snapshot=s, action=float(i%2), predicted_operating_condition=0.5,
                  actual_operating_condition=0.5+0.02*i)
    q=m.permuted(123)
    assert len(q.features)==len(m.features)==8
    assert all(np.array_equal(a,b) for a,b in zip(m.features,q.features))
    assert q.targets != m.targets
