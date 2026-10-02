from __future__ import annotations

import json
import subprocess
import sys


def test_c0_11_schema(tmp_path):
    out = tmp_path / "c0_11"
    result = subprocess.run(
        [
            sys.executable,
            "experiments/tcf_consciousness_instantiation_c0_11.py",
            "--episodes", "4",
            "--train-episodes", "4",
            "--observer-samples", "32",
            "--out", str(out),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)

    assert summary["experiment"] == "tcf_consciousness_instantiation_c0_11"
    assert summary["protocol_version"] == "C0.11"
    assert summary["matched_design"]["action_intervention_only"] is True
    assert summary["matched_design"]["same_dynamic_seed_per_pair"] is True
    assert summary["semantic_input_during_probe"] is False
    assert summary["external_retraining_during_probe"] is False
    assert summary["phenomenal_consciousness_claimed"] is False
    assert summary["secondary_outputs"]["intervention_target_error_max"] < 1e-12

    assert "next_action_difference_factual_minus_forced" in summary["primary_outputs"]
    assert "next_state_difference_factual_minus_forced" in summary["primary_outputs"]
    assert "gain_difference_factual_minus_forced" in summary["primary_outputs"]

    for value in summary["primary_outputs"].values():
        assert set(value) == {"mean", "p"}
        assert 0.0 <= value["p"] <= 1.0
