from experiments.self_development_ablation import run


def test_self_development_ablation_has_four_conditions():
    report = run()

    assert [item["condition"] for item in report["conditions"]] == ["A", "B", "C", "D"]
    assert report["conditions"][0]["self_model_change_events"] == 0
    assert report["conditions"][1]["self_model_change_events"] == 0
    assert report["conditions"][1]["final_target"] == 0.8
    assert report["conditions"][2]["final_target"] < 0.8
    assert report["conditions"][3]["priority_updates"]
    assert report["conditions"][3]["final_goal_fit_weight"] > 1.0
