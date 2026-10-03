from experiments.metacognitive_confidence_longitudinal import run_longitudinal_confidence_probe


def test_longitudinal_confidence_intervention_persists_flips_and_restores():
    report = run_longitudinal_confidence_probe(cycles=12, restart_every=6)

    assert report["protocol"] == "metacognitive-confidence-longitudinal-v1"
    assert report["intervention_persisted"] is True
    assert report["selection_flipped"] is True
    assert report["selection_restored"] is True
    assert all(report["restart_checks"])
    assert len(report["final_state_hash"]) == 64

    assert all(value == "high-confidence" for value in report["selections"][:4])
    assert all(value == "low-confidence" for value in report["selections"][4:8])
    assert all(value == "high-confidence" for value in report["selections"][8:])
