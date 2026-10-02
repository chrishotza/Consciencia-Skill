import json
import subprocess
import sys


def test_i4_3_small_run(tmp_path):
    out = tmp_path / "i4_3" / "summary.json"
    result = subprocess.run(
        [
            sys.executable,
            "experiments/interoception_i4_3.py",
            "--train-episodes", "4",
            "--eval-episodes-per-family", "2",
            "--output", str(out),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(out.read_text(encoding="utf-8"))
    assert summary["protocol"] == "I4.3_structural_ood_metacognitive_generalization"
    assert summary["train_family"] == "linear_action_pressure"
    assert summary["ood_families"] == [
        "quadratic_action",
        "pressure_threshold",
        "state_coupled",
    ]
    assert summary["serialization_exact"] is True
    assert summary["meta_samples"] > 0
    assert summary["no_online_updates"] is True
    assert set(summary["contrasts"]) >= {
        "META_minus_LESION_mean_error_aggregate",
        "META_minus_PERMUTED_prediction_MAE_aggregate",
    }
