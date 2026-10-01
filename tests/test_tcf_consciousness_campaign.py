from __future__ import annotations

import json
import subprocess
import sys


def test_campaign_schema(tmp_path):
    out = tmp_path / "campaign"
    result = subprocess.run(
        [
            sys.executable,
            "experiments/tcf_consciousness_campaign.py",
            "--group",
            "G1",
            "--replicate",
            "1",
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
    assert summary["experiment"] == "tcf_consciousness_campaign"
    assert summary["protocol_version"] == "C0-CAMPAIGN-1.0"
    assert summary["group"] == "G1"
    assert summary["replicate"] == 1
    assert summary["phenomenal_consciousness_claimed"] is False
    assert summary["semantic_input_during_probe"] is False
    assert summary["external_retraining_during_probe"] is False
    assert 0.0 <= summary["result"]["metric"]["p"] <= 1.0
