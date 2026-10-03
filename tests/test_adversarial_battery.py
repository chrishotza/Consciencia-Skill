from skill_conscious.adversarial_battery import (
    run_adversarial_battery,
    run_condition,
    CONDITIONS,
)


def test_persistent_causal_self_diverges_and_reverses():
    condition = next(
        item
        for item in CONDITIONS
        if item.name == "persistent_causal_self"
    )
    result = run_condition(condition)

    assert result["downstream_divergence"] is True
    assert result["reversible"] is True
    assert result["baseline_selection"] == "learn"
    assert result["intervention_selection"] == "preserve"
    assert result["restored_selection"] == "learn"


def test_mechanism_controls_do_not_attribute_self_model_intervention_to_themselves():
    results = run_adversarial_battery()
    controls = [
        item
        for item in results
        if item["condition"] != "persistent_causal_self"
    ]

    assert len(controls) == 6
    assert all(item["downstream_divergence"] is False for item in controls)


def test_adversarial_isolation_summary():
    from skill_conscious.adversarial_battery import summarize_battery

    summary = summarize_battery(run_adversarial_battery())

    assert summary["self_model_causal_effect"] is True
    assert summary["self_model_reversal"] is True
    assert summary["control_divergence_count"] == 0
    assert summary["adversarial_isolation_pass"] is True
