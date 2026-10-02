from experiments.i5_17_phase_resolved_bridge_mediation_map import (
    CYCLES,
    LAGS,
    PERIOD,
    PHASE_LABELS,
    build_schedule,
    bridge_delta,
    metrics,
)


def test_phase_schedule_distribution_is_paired():
    assert CYCLES == 15
    assert PERIOD == 7
    assert PHASE_LABELS == tuple("ABCDEFG")
    base = build_schedule(0, 0)
    for lag in LAGS:
        schedule = build_schedule(lag, 0)
        assert schedule[0] == base[0]
        assert sorted(item.split(" — ", 1)[1] for item in schedule[1:]) == sorted(
            item.split(" — ", 1)[1] for item in base[1:]
        )


def test_bridge_delta():
    on = {"state_auc_abs": 5.0, "state_auc_signed": -1.0, "future_action_change_rate": 0.6}
    off = {"state_auc_abs": 3.0, "state_auc_signed": -0.5, "future_action_change_rate": 0.4}
    delta = bridge_delta(on, off)
    assert delta["abs_auc_delta"] == 2.0
    assert delta["signed_auc_delta"] == -0.5
    assert delta["future_action_change_delta"] == 0.2


def test_metrics():
    base = [
        {
            "cycle": i,
            "dynamic_state": 0.0,
            "chosen_signal": 1.0,
            "applied_signal": 1.0,
            "self_model": f"S{i}",
        }
        for i in range(CYCLES)
    ]
    condition = [
        {
            "cycle": i,
            "dynamic_state": float(i + 1) / 10.0,
            "chosen_signal": -1.0 if i == 1 else 1.0,
            "applied_signal": 1.0,
            "self_model": f"S{i}",
        }
        for i in range(CYCLES)
    ]
    result = metrics(base, condition)
    assert result["t0_action_match"] is True
    assert result["model_distribution_match"] is True
    assert result["future_action_change_rate"] > 0.0
    assert result["state_auc_abs"] > 0.0
    assert result["state_auc_signed"] > 0.0
    assert result["final_state_delta_signed"] > 0.0
