from experiments.i5_14_phase_matched_temporal_specificity_control import (
    BASE_SCHEDULE,
    SHIFT_MINUS,
    SHIFT_PLUS,
    paired_metrics,
)


def row(cycle, state, action, model):
    return {
        "cycle": cycle,
        "dynamic_state": state,
        "chosen_signal": action,
        "applied_signal": action,
        "self_model": model,
    }


def test_phase_matched_schedules_preserve_t0_and_distribution():
    assert BASE_SCHEDULE[0] == SHIFT_PLUS[0] == SHIFT_MINUS[0]
    assert sorted(BASE_SCHEDULE) == sorted(SHIFT_PLUS) == sorted(SHIFT_MINUS)


def test_phase_matched_metrics_detect_temporal_change():
    base = [
        row(0, 0.0, 1.0, "A"),
        row(1, 0.2, 1.0, "B"),
        row(2, 0.4, -1.0, "C"),
        row(3, 0.6, 1.0, "A"),
        row(4, 0.8, -1.0, "B"),
        row(5, 1.0, 1.0, "C"),
        row(6, 1.2, -1.0, "A"),
        row(7, 1.4, 1.0, "B"),
    ]
    plus = [
        row(0, 0.0, 1.0, "A"),
        row(1, 0.3, -1.0, "C"),
        row(2, 0.2, 1.0, "A"),
        row(3, 0.4, -1.0, "B"),
        row(4, 0.5, 1.0, "C"),
        row(5, 0.7, -1.0, "A"),
        row(6, 0.9, 1.0, "B"),
        row(7, 1.0, -1.0, "B"),
    ]
    minus = [
        row(0, 0.0, 1.0, "A"),
        row(1, 0.1, 1.0, "B"),
        row(2, 0.3, -1.0, "B"),
        row(3, 0.5, 1.0, "C"),
        row(4, 0.7, -1.0, "A"),
        row(5, 0.8, 1.0, "B"),
        row(6, 1.0, -1.0, "C"),
        row(7, 1.1, 1.0, "A"),
    ]
    plus_off = plus
    out = paired_metrics(base, plus, minus, plus_off)
    assert out["t0_action_match_plus"]
    assert out["t0_action_match_minus"]
    assert out["model_distribution_match_plus"]
    assert out["model_distribution_match_minus"]
    assert out["future_action_change_plus"] > 0
    assert out["state_auc_base_plus"] > 0
    assert out["state_auc_plus_minus"] > 0
