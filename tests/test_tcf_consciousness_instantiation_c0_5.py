from __future__ import annotations

import json
import subprocess
import sys


def test_c0_5_output_schema(tmp_path):
    out = tmp_path / "c0_5"
    result = subprocess.run(
        [
            sys.executable,
            "experiments/tcf_consciousness_instantiation_c0_5.py",
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
    assert summary["experiment"] == "tcf_consciousness_instantiation_c0_5"
    assert summary["protocol_version"] == "C0.5"
    assert summary["control"] == "information_matched_action_chain_shuffle"
    assert summary["phenomenal_consciousness_claimed"] is False
    assert summary["episodes"] == 4
    assert summary["shuffles_per_episode"] == 8
    assert 0.0 <= summary["contrast_p"] <= 1.0
