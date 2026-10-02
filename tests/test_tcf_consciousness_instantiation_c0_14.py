from __future__ import annotations

import json
import subprocess
import sys


def test_c0_14_schema(tmp_path):
    out = tmp_path / "c0_14"
    result = subprocess.run(
        [
            sys.executable,
            "experiments/tcf_consciousness_instantiation_c0_14.py",
            "--episodes", "2",
            "--out", str(out),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["experiment"] == "tcf_consciousness_instantiation_c0_14"
    assert summary["protocol_version"] == "C0.14"
    assert summary["analysis_note"].startswith("Continuous and restart")
    assert summary["matched_design"]["same_serialized_observer_and_meta_model"] is True
    assert summary["phenomenal_consciousness_claimed"] is False
    assert summary["analysis_note"].startswith("Continuous and restart")
    for value in summary["primary_outputs"].values():
        assert set(value) == {"mean", "p"}
        assert 0.0 <= value["p"] <= 1.0
