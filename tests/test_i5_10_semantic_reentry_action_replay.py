from experiments.i5_10_semantic_reentry_under_action_replay import metrics


def row(cycle, state, action, model, version):
    return {
        "cycle": cycle,
        "dynamic_state": state,
        "applied_signal": action,
        "self_model": model,
        "self_model_version": version,
    }


def test_semantic_divergence_can_be_measured_under_identical_actions():
    pulse = [row(0, 0.0, 1.0, "A", 1), row(1, 0.2, 1.0, "A", 2), row(2, 0.4, -1.0, "B", 3)]
    replay_on = [row(0, 0.0, 1.0, "B", 1), row(1, 0.2, 1.0, "B", 2), row(2, 0.4, -1.0, "B", 3)]
    replay_off = [row(0, 0.0, 1.0, "B", 1), row(1, 0.2, 1.0, "B", 2), row(2, 0.4, -1.0, "B", 3)]
    out = metrics(pulse, replay_on, replay_off)
    assert out["applied_action_exact_match"]
    assert out["self_model_divergence_rate_post"] > 0
