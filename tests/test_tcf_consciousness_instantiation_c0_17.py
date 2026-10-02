from __future__ import annotations

import json
import subprocess
import sys


def test_c0_17_schema(tmp_path):
    out = tmp_path / "c0_17"
    result = subprocess.run(
        [
            sys.executable,
            "experiments/tcf_consciousness_instantiation_c0_17.py",
            "--episodes", "1",
            "--out", str(out),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)

    assert summary["experiment"] == "tcf_consciousness_instantiation_c0_17"
    assert summary["protocol_version"] == "C0.17"
    assert summary["matched_design"]["second_order_model_starts_empty"] is True
    assert summary["matched_design"]["counterfactual_second_order_learning_occurs_inside_organism"] is True
    assert summary["matched_design"]["external_retraining_during_probe"] is False
    assert summary["matched_design"]["semantic_input_during_probe"] is False
    assert summary["phenomenal_consciousness_claimed"] is False
    assert summary["secondary_outputs"]["exact_model_recovery_fraction"] == 1.0
    assert summary["secondary_outputs"]["mean_learned_meta_samples"] > 0
