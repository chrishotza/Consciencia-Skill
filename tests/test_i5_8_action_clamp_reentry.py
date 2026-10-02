from experiments.i5_8_action_clamp_reentry import CYCLES, metric_against_full


def row(cycle, state, action, target_module=2, target_action=1.0, query_module=2):
    return {
        "cycle": cycle,
        "dynamic_state": state,
        "chosen_signal": action,
        "applied_signal": action,
        "target_module": target_module,
        "target_action": target_action,
        "query_module": query_module,
    }


def test_metric_captures_post_pulse_divergence():
    full = [row(0, 0.0, 1.0), row(1, 0.1, 1.0), row(2, 0.2, -1.0)]
    pulse = [row(0, 0.0, -1.0), row(1, 0.4, -1.0), row(2, 0.3, 1.0)]
    metric = metric_against_full(pulse, full)
    assert metric["state_abs_delta_t1"] > 0
    assert metric["state_divergence_auc_post"] > 0


def test_horizon():
    assert CYCLES == 8
