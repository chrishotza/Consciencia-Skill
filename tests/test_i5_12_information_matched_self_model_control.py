from experiments.i5_12_information_matched_self_model_control import metrics


def row(cycle, state, action, model):
    return {
        "cycle": cycle,
        "dynamic_state": state,
        "chosen_signal": action,
        "applied_signal": action,
        "self_model": model,
    }


def test_information_match_preserves_distribution():
    pulse = [
        row(0, 0.0, 1.0, "A"),
        row(1, 0.2, 1.0, "A"),
        row(2, 0.4, -1.0, "B"),
    ]
    matched_on = [
        row(0, 0.0, 1.0, "A"),
        row(1, 0.2, -1.0, "B"),
        row(2, 0.4, 1.0, "A"),
    ]
    matched_off = matched_on
    out = metrics(pulse, matched_on, matched_off)
    assert out["t0_action_match"]
    assert out["model_distribution_match"]


