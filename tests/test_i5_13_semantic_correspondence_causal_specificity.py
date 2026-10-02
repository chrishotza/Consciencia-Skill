from experiments.i5_13_semantic_correspondence_causal_specificity import metrics


def row(cycle, state, action, model):
    return {
        "cycle": cycle,
        "dynamic_state": state,
        "chosen_signal": action,
        "applied_signal": action,
        "self_model": model,
    }


def test_one_cycle_shift_metrics():
    pulse = [row(0, 0.0, 1.0, "A"), row(1, 0.2, 1.0, "A"), row(2, 0.4, -1.0, "B")]
    shifted_on = [row(0, 0.0, 1.0, "A"), row(1, 0.3, -1.0, "B"), row(2, 0.2, 1.0, "A")]
    shifted_off = shifted_on
    out = metrics(pulse, shifted_on, shifted_off)
    assert out["t0_action_match"]
    assert out["model_distribution_match"]
    assert out["future_action_change_rate"] > 0
