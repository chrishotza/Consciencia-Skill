from __future__ import annotations

import json
import subprocess
import sys


def test_c0_18_schema(tmp_path):
    out = tmp_path / "c0_18"
    result = subprocess.run(
        [
            sys.executable,
            "experiments/tcf_consciousness_instantiation_c0_18.py",
            "--episodes", "1",
            "--out", str(out),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["experiment"] == "tcf_consciousness_instantiation_c0_18"
    assert summary["protocol_version"] == "C0.18"
    assert summary["matched_design"]["second_order_was_acquired_inside_organism"] is True
    assert summary["matched_design"]["base_state_same_for_full_lesion_rescue"] is True
    assert summary["phenomenal_consciousness_claimed"] is False
    assert summary["secondary_outputs"]["mean_learned_meta_samples"] > 0
    assert summary["secondary_outputs"]["exact_learned_model_recovery_fraction"] == 1.0
    assert summary["analysis_note"].startswith("The lesion and rescue probes")
