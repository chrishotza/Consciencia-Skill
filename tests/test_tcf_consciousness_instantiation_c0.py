from __future__ import annotations

import json
import subprocess
import sys


def test_c0_output_schema(tmp_path):
    out = tmp_path / "c0"
    result = subprocess.run(
        [
            sys.executable,
            "experiments/tcf_consciousness_instantiation_c0.py",
            "--episodes",
            "3",
            "--train-episodes",
            "3",
            "--observer-samples",
            "32",
            "--recovery-steps",
            "3",
            "--out",
            str(out),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)

    assert summary["experiment"] == "tcf_consciousness_instantiation_c0"
    assert summary["protocol_version"] == "C0.1"
    assert summary["primary_outputs_are_criterion_vectors"] is True
    assert summary["no_composite_consciousness_score"] is True
    assert summary["phenomenal_consciousness_claimed"] is False
    assert summary["semantic_input_during_probe"] is False
    assert summary["external_retraining_during_probe"] is False
    assert summary["policy_snapshot_shared_across_conditions"] is True
    assert summary["criteria"] == [
        "C1_own_state_persistence",
        "C2_self_environment_differentiation",
        "C3_causal_self_reference",
        "C4_trajectory_continuity",
        "C5_intrinsic_dynamics",
        "C6_reorganization",
        "C7_recurrent_closure",
    ]
    assert summary["conditions"] == [
        "full",
        "state_blind",
        "no_persistence",
        "open_loop",
    ]
    assert set(summary["criterion_effects_mean"]) == set(summary["criteria"])
    assert set(summary["criterion_effects_p"]) == set(summary["criteria"])
    assert set(summary["conditions_summary"]) == set(summary["conditions"])
    assert summary["intervention_target_error_max"] < 1e-12
