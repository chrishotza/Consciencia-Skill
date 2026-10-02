import json
import sys
from pathlib import Path

from experiments.i5_4_persistent_selective_access import main


def test_i5_4_contract(tmp_path: Path, monkeypatch):
    out = tmp_path / "i5_4"
    monkeypatch.setattr(
        sys,
        "argv",
        ["i5_4_persistent_selective_access.py", "--replicates", "2", "--warmup", "2", "--out", str(out)],
    )
    main()
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["replicates"] == 2
    assert 0.0 <= summary["endpoints"]["full_persistence_rate"] <= 1.0
