from __future__ import annotations

import json
import subprocess
import sys


def test_c0_3_output_schema(tmp_path):
    out = tmp_path / "c0_3"
    result = subprocess.run(
        [
            sys.executable,
            "experiments/tcf_consciousness_instantiation_c0_3.py",
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

    assert summary["experiment"] == "tcf_consciousness_instantiation_c0_3"
    assert summary["protocol_version"] == "C0.3"
    assert summary["control"] == "information_matched_state_shuffle"
    assert summary["primary_output"] == "own_state_gap_minus_matched_shuffle_gap"
    assert summary["semantic_input_during_probe"] is False
    assert summary["external_retraining_during_probe"] is False
    assert summary["policy_snapshot_shared_across_control"] is True
    assert summary["phenomenal_consciousness_claimed"] is False
    assert summary["episodes"] == 4
    assert summary["shuffles_per_episode"] == 8
    assert 0.0 <= summary["contrast_p"] <= 1.0
    assert summary["own_state_gap_mean"] >= 0.0
    assert summary["matched_shuffle_gap_mean"] >= 0.0
    assert 0.0 <= summary["actual_vs_shuffle_action_mismatch_rate"] <= 1.0
