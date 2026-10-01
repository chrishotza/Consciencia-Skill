from __future__ import annotations

import json
import subprocess
import sys


def test_c0_8_schema(tmp_path):
    out = tmp_path / "c0_8"
    result = subprocess.run(
        [
            sys.executable,
            "experiments/tcf_consciousness_instantiation_c0_8.py",
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
    assert summary["experiment"] == "tcf_consciousness_instantiation_c0_8"
    assert summary["protocol_version"] == "C0.8"
    assert summary["matched_design"]["same_episode_seeds"] is True
    assert summary["matched_design"]["same_target_multiset"] is True
    assert summary["matched_design"]["same_training_budget"] is True
    assert summary["phenomenal_consciousness_claimed"] is False
    assert summary["semantic_input_during_probe"] is False
    assert summary["external_retraining_during_probe"] is False
    assert summary["intervention_target_error_max"] < 1e-12
    for value in summary["primary_outputs"].values():
        assert set(value) == {"mean", "p"}
        assert 0.0 <= value["p"] <= 1.0
