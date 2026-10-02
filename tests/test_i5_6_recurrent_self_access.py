from experiments.i5_6_recurrent_self_access import CANDIDATE_SIGNALS, paired_metrics


def row(cycle: int, state: float, prediction: float, query_distance: float, signal: float):
    return {
        "cycle": cycle,
        "dynamic_state": state,
        "self_prediction": prediction,
        "query_distance": query_distance,
        "chosen_signal": signal,
    }


def test_paired_metrics_detects_reentry():
    full = [
        row(0, 0.0, 0.0, 0.0, 1.0),
        row(1, 0.10, 0.05, 0.1, 1.0),
        row(2, 0.20, 0.10, 0.2, -1.0),
        row(3, 0.15, 0.08, 0.3, -1.0),
        row(4, 0.05, 0.04, 0.2, 1.0),
    ]
    perturbed = [
        row(0, 0.0, 0.0, 0.0, 1.0),
        row(1, 0.14, 0.06, 0.2, -1.0),
        row(2, 0.28, 0.18, 0.5, 1.0),
        row(3, 0.25, 0.15, 0.4, 1.0),
        row(4, 0.17, 0.11, 0.3, -1.0),
    ]
    metrics = paired_metrics(perturbed, full, cycles=5)
    assert metrics["state_delta_t1"] > 0
    assert metrics["state_divergence_auc"] > 0
    assert metrics["reentry_persistence_cycles"] > 0
    assert metrics["action_change_count"] > 0
    assert metrics["query_distance_delta_max"] > 0


def test_candidate_signals_are_balanced():
    assert CANDIDATE_SIGNALS == (-1.0, 1.0)
