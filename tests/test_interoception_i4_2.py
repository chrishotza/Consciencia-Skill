from src.ontto.interoceptive_meta_observer import InteroceptiveMetaObserver
from src.ontto.interoception import InteroceptiveSnapshot

def test_roundtrip_is_exact():
    m=InteroceptiveMetaObserver()
    s=InteroceptiveSnapshot(0.2,0.8,0.3,0.4,0.2,0.5,0.3,0.7)
    for i in range(12):
        m.observe(snapshot=s,action=float(i%3-1),predicted_operating_condition=0.7,actual_operating_condition=0.70+0.01*i)
    payload=m.to_dict()
    restored=InteroceptiveMetaObserver.from_dict(payload)
    assert payload==restored.to_dict()

def test_permuted_is_not_identical():
    m=InteroceptiveMetaObserver()
    s=InteroceptiveSnapshot(0.2,0.8,0.3,0.4,0.2,0.5,0.3,0.7)
    for i in range(12):
        m.observe(snapshot=s,action=float(i%2),predicted_operating_condition=0.7,actual_operating_condition=0.70+0.01*i)
    q=m.permuted(11)
    assert q.targets != m.targets
