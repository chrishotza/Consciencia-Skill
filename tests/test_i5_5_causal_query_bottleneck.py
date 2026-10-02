import json
import sys
from pathlib import Path

from experiments.i5_5_causal_query_bottleneck import main


def test_i5_5_contract(tmp_path: Path, monkeypatch):
    out = tmp_path / "i5_5"
    monkeypatch.setattr(
        sys,
        "argv",
        ["i5_5_causal_query_bottleneck.py", "--episodes", "16", "--out", str(out)],
    )
    main()
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["episodes"] == 16
    assert 0.0 <= summary["endpoints"]["full_action_accuracy"] <= 1.0
