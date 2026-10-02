from experiments.i5_16_counterbalanced_pure_phase_temporal_control import (
    BASE_SCHEDULE,
    CYCLES,
    LAGS,
    PERIOD,
    PHASE_LABELS,
    build_schedule,
    metrics,
)


def test_all_phase_lags_preserve_cycle0_and_distribution():
    assert CYCLES == 15
    assert PERIOD == 7
    assert PHASE_LABELS == tuple("ABCDEFG")
    base = build_schedule(0, 0)
    for lag in LAGS:
        schedule = build_schedule(lag, 0)
        assert schedule[0].startswith("A — ")
        assert schedule[0] == base[0]
        assert sorted(schedule[1:]) == sorted(base[1:])
    assert BASE_SCHEDULE == base


def test_counterbalanced_rotation_preserves_distribution():
    base = build_schedule(0, 0)
    rotated = build_schedule(2, 3)
    assert sorted(rotated[1:]) != []
    base_semantics = sorted(item.split(" — ", 1)[1] for item in base[1:])
    rotated_semantics = sorted(item.split(" — ", 1)[1] for item in rotated[1:])
    assert rotated_semantics == base_semantics


def test_metrics():
    base = [
        {"cycle": i, "dynamic_state": 0.0, "chosen_signal": 1.0, "applied_signal": 1.0, "self_model": f"S{i}"}
        for i in range(CYCLES)
    ]
    condition = [
        {"cycle": i, "dynamic_state": float(i + 1) / 10.0, "chosen_signal": -1.0 if i == 1 else 1.0, "applied_signal": 1.0, "self_model": f"S{i}"}
        for i in range(CYCLES)
    ]
    result = metrics(base, condition)
    assert result["t0_action_match"] is True
    assert result["model_distribution_match"] is True
    assert result["future_action_change_rate"] > 0.0
    assert result["state_auc_abs"] > 0.0
    assert result["state_auc_signed"] > 0.0
    assert result["final_state_delta_signed"] > 0.0
