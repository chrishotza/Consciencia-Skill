import json
import sys
from pathlib import Path

from experiments.i5_3_causal_attention_allocation import main


def test_experiment_contract(tmp_path: Path, monkeypatch):
    out = tmp_path / "i5_3"
    monkeypatch.setattr(
        sys,
        "argv",
        ["i5_3_causal_attention_allocation.py", "--episodes", "16", "--out", str(out)],
    )
    main()
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["episodes"] == 16
    assert 0.0 <= summary["endpoints"]["full_target_attention_mass"] <= 1.0
    assert summary["endpoints"]["full_minus_shuffled_p"] >= 0.0
