from experiments.i5_15_bidirectional_temporal_lag_response_map import (
    BASE_SCHEDULE,
    LAG_SCHEDULES,
    LAGS,
    metrics,
    rotated_schedule,
)


def row(cycle, state, action, model):
    return {
        "cycle": cycle,
        "dynamic_state": state,
        "chosen_signal": action,
        "applied_signal": action,
        "self_model": model,
    }


def test_lag_schedules_preserve_t0_and_distribution():
    assert BASE_SCHEDULE[0] == "A — continuidad persistente."
    for lag in LAGS:
        schedule = rotated_schedule(lag)
        assert schedule[0] == BASE_SCHEDULE[0]
        assert sorted(schedule) == sorted(BASE_SCHEDULE)
        assert LAG_SCHEDULES[lag] == schedule


def test_metrics_capture_signed_and_absolute_response():
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
    shifted = [
        row(0, 0.0, 1.0, "A"),
        row(1, 0.3, -1.0, "C"),
        row(2, 0.2, 1.0, "A"),
        row(3, 0.5, -1.0, "B"),
        row(4, 0.7, 1.0, "C"),
        row(5, 0.9, -1.0, "A"),
        row(6, 1.1, 1.0, "B"),
        row(7, 1.0, -1.0, "B"),
    ]
    out = metrics(base, shifted)
    assert out["t0_action_match"]
    assert out["model_distribution_match"]
    assert out["future_action_change_rate"] > 0
    assert out["state_auc_abs"] > 0
    assert out["state_auc_signed"] != 0
    assert out["final_state_delta_signed"] != 0
