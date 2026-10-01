from __future__ import annotations

import json
import subprocess
import sys


def test_c0_9_schema(tmp_path):
    out = tmp_path / "c0_9"
    result = subprocess.run(
        [
            sys.executable,
            "experiments/tcf_consciousness_instantiation_c0_9.py",
            "--episodes",
            "4",
            "--train-episodes",
            "4",
            "--observer-samples",
            "32",
            "--out",
            str(out),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["experiment"] == "tcf_consciousness_instantiation_c0_9"
    assert summary["protocol_version"] == "C0.9"
    assert summary["matched_design"]["same_target_contexts"] is True
    assert summary["matched_design"]["same_dynamic_bridge_seed_per_pair"] is True
    assert summary["matched_design"]["donor_mapping_is_derangement"] is True
    assert summary["semantic_input_during_probe"] is False
    assert summary["external_retraining_during_probe"] is False
    assert summary["phenomenal_consciousness_claimed"] is False
    assert "no constant-value pseudo-replication" in summary["analysis_note"]
    assert summary["secondary_outputs"]["intervention_target_error_max"] < 1e-12
    assert "action_difference_normal_minus_donor" in summary["primary_outputs"]
    assert "gain_contrast_normal_minus_donor_shuffle" in summary["primary_outputs"]
    assert "state_delta_after_step_normal_minus_donor" in summary["primary_outputs"]
    for value in summary["primary_outputs"].values():
        assert set(value) == {"mean", "p"}
        assert 0.0 <= value["p"] <= 1.0
