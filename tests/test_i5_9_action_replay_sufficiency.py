from experiments.i5_9_action_replay_sufficiency import trajectory_metrics


def row(cycle, state, action):
    return {
        "cycle": cycle,
        "dynamic_state": state,
        "chosen_signal": action,
        "applied_signal": action,
    }


def test_replay_metric_detects_divergence():
    full = [row(0, 0.0, 1.0), row(1, 0.1, 1.0), row(2, 0.2, -1.0)]
    pulse = [row(0, 0.0, -1.0), row(1, 0.4, -1.0), row(2, 0.3, 1.0)]
    replay = [row(0, 0.0, 1.0), row(1, 0.35, -1.0), row(2, 0.25, 1.0)]
    metric = trajectory_metrics(pulse, replay, full)
    assert metric["pulse_vs_replay_state_t1"] > 0
    assert metric["pulse_vs_replay_auc_post"] > 0


def test_exact_action_match_is_reported():
    full = [row(0, 0.0, 1.0), row(1, 0.1, 1.0)]
    pulse = [row(0, 0.0, -1.0), row(1, 0.4, -1.0)]
    replay = [row(0, 0.0, -1.0), row(1, 0.4, -1.0)]
    metric = trajectory_metrics(pulse, replay, full)
    assert metric["applied_action_exact_match"] is True
