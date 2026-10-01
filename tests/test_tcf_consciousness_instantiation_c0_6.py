from __future__ import annotations

import json
import subprocess
import sys


def test_c0_6_schema(tmp_path):
    out = tmp_path / "c0_6"
    result = subprocess.run(
        [
            sys.executable,
            "experiments/tcf_consciousness_instantiation_c0_6.py",
            "--episodes", "3",
            "--train-episodes", "3",
            "--observer-samples", "32",
            "--out", str(out),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["experiment"] == "tcf_consciousness_instantiation_c0_6"
    assert summary["protocol_version"] == "C0.6"
    assert summary["phenomenal_consciousness_claimed"] is False
    assert summary["semantic_input_during_probe"] is False
    assert summary["external_retraining_during_probe"] is False
    assert summary["same_trained_snapshot_across_lesions"] is True
    assert summary["intervention_target_error_max"] < 1e-12
    for key in (
        "observer_necessity_gain_delta",
        "policy_necessity_gain_delta",
        "both_lesion_gain_delta",
        "observer_distance_delta",
        "policy_distance_delta",
        "observer_rescue_lift",
        "policy_rescue_lift",
    ):
        assert set(summary[key]) == {"mean", "p"}
        assert 0.0 <= summary[key]["p"] <= 1.0
