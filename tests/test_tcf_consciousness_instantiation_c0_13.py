from __future__ import annotations

import json
import subprocess
import sys


def test_c0_13_schema(tmp_path):
    out = tmp_path / "c0_13"
    result = subprocess.run(
        [
            sys.executable,
            "experiments/tcf_consciousness_instantiation_c0_13.py",
            "--episodes", "4",
            "--observer-samples", "32",
            "--meta-samples", "32",
            "--out", str(out),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["experiment"] == "tcf_consciousness_instantiation_c0_13"
    assert summary["protocol_version"] == "C0.13"
    assert summary["matched_design"]["same_target_multiset_for_meta_permutation"] is True
    assert summary["semantic_input_during_probe"] is False
    assert summary["external_retraining_during_probe"] is False
    assert summary["phenomenal_consciousness_claimed"] is False
    assert summary["secondary_outputs"]["intervention_target_error_max"] < 1e-12
    assert summary["analysis_note"].startswith("All primary contrasts are signed")
    for value in summary["primary_outputs"].values():
        assert set(value) == {"mean", "p"}
        assert 0.0 <= value["p"] <= 1.0
