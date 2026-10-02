import json
import sys
from pathlib import Path

from experiments.i5_6_persistent_query_task import main


def test_i5_6_contract(tmp_path: Path, monkeypatch):
    out = tmp_path / "i5_6"
    monkeypatch.setattr(
        sys,
        "argv",
        ["i5_6_persistent_query_task.py", "--replicates", "2", "--warmup", "2", "--out", str(out)],
    )
    main()
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["replicates"] == 2
    assert 0.0 <= summary["endpoints"]["full_actual_action_accuracy"] <= 1.0
    assert 0.0 <= summary["endpoints"]["full_persistence_rate"] <= 1.0
