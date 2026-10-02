from experiments.i5_11_semantic_reentry_trajectory_selection import metrics


def row(cycle, state, action, model):
    return {
        "cycle": cycle,
        "dynamic_state": state,
        "chosen_signal": action,
        "applied_signal": action,
        "self_model": model,
    }


def test_future_selection_metric_detects_change():
    pulse = [
        row(0, 0.0, 1.0, "A"),
        row(1, 0.2, 1.0, "A"),
        row(2, 0.4, -1.0, "B"),
    ]
    action_match_on = [
        row(0, 0.0, 1.0, "B"),
        row(1, 0.4, -1.0, "B"),
        row(2, 0.7, -1.0, "B"),
    ]
    action_match_off = [
        row(0, 0.0, 1.0, "B"),
        row(1, 0.2, 1.0, "B"),
        row(2, 0.4, -1.0, "B"),
    ]
    out = metrics(pulse, action_match_on, action_match_off)
    assert out["applied_t0_match"]
    assert out["future_action_change_rate"] > 0
    assert out["state_auc_post"] > 0
