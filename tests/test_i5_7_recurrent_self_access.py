from experiments.i5_7_recurrent_self_access import CYCLES, paired_metrics


def row(cycle, state, prediction, action, target_module, target_action, query_module, action_accuracy):
    return {
        "cycle": cycle,
        "dynamic_state": state,
        "self_prediction": prediction,
        "chosen_signal": action,
        "target_module": target_module,
        "target_action": target_action,
        "query_module": query_module,
        "action_accuracy": action_accuracy,
    }


def test_paired_metrics_detects_post_pulse_reentry():
    full = [
        row(0, 0.0, 0.0, 1.0, 2, 1.0, 2, 1.0),
        row(1, 0.10, 0.05, 1.0, 2, 1.0, 2, 1.0),
        row(2, 0.20, 0.08, -1.0, 3, -1.0, 3, 1.0),
        row(3, 0.15, 0.06, -1.0, 3, -1.0, 3, 1.0),
    ]
    pulse = [
        row(0, 0.0, 0.0, -1.0, 2, 1.0, 3, 0.0),
        row(1, 0.14, 0.07, -1.0, 3, -1.0, 3, 1.0),
        row(2, 0.28, 0.15, 1.0, 4, 1.0, 4, 1.0),
        row(3, 0.24, 0.13, 1.0, 4, 1.0, 4, 1.0),
    ]
    metrics = paired_metrics(pulse, full, cycles=4)

    assert metrics["state_abs_delta_t1"] > 0
    assert metrics["reentry_persistence_cycles"] > 0
    assert metrics["action_change_count"] > 0
    assert metrics["query_change_count"] > 0
    assert metrics["target_change_count"] > 0
    assert metrics["state_divergence_auc"] > 0


def test_paired_metrics_has_expected_horizon():
    assert CYCLES == 8
