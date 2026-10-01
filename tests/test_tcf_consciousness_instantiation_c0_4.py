from __future__ import annotations

import json
import subprocess
import sys


def test_c0_4_output_schema(tmp_path):
    out=tmp_path/"c0_4"
    result=subprocess.run(
        [
            sys.executable,
            "experiments/tcf_consciousness_instantiation_c0_4.py",
            "--episodes","4",
            "--train-episodes","4",
            "--observer-samples","32",
            "--out",str(out),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode==0,result.stderr
    summary=json.loads(result.stdout)
    assert summary["experiment"]=="tcf_consciousness_instantiation_c0_4"
    assert summary["protocol_version"]=="C0.4"
    assert summary["control"]=="information_matched_action_replay"
    assert summary["phenomenal_consciousness_claimed"] is False
    assert summary["semantic_input_during_probe"] is False
    assert summary["external_retraining_during_probe"] is False
    assert summary["episodes"]==4
    assert summary["replays_per_episode"]==8
    assert 0.0 <= summary["contrast_p"] <= 1.0
