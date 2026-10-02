from __future__ import annotations

import json
import subprocess
import sys


def test_c0_16_schema(tmp_path):
    out = tmp_path / "c0_16"
    result = subprocess.run(
        [
            sys.executable,
            "experiments/tcf_consciousness_instantiation_c0_16.py",
            "--episodes", "1",
            "--out", str(out),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)

    assert summary["experiment"] == "tcf_consciousness_instantiation_c0_16"
    assert summary["protocol_version"] == "C0.16"
    assert summary["matched_design"]["same_seeded_first_order_observer"] is True
    assert summary["matched_design"]["semantic_input_during_probe"] is False
    assert summary["matched_design"]["external_retraining_during_probe"] is False
    assert summary["phenomenal_consciousness_claimed"] is False
    assert summary["secondary_outputs"]["exact_model_digest_fraction"] == 1.0
    assert summary["secondary_outputs"]["pre_restart_action_match_fraction"] == 1.0
    assert summary["secondary_outputs"]["all_post_restart_policies_second_order"] is True
