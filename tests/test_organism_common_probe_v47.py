import json
import sys
from pathlib import Path

from experiments.organism_common_probe_v47 import main


def test_v47_fake_protocol(tmp_path: Path, monkeypatch):
    out = tmp_path / "v47"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "organism_common_probe_v47.py",
            "--mode",
            "fake",
            "--out",
            str(out),
        ],
    )

    main()

    summary = json.loads(
        (out / "summary.json").read_text(encoding="utf-8")
    )

    assert summary["same_probe"] is True
    assert summary["history_discriminates"] is True
    assert summary["reopen_preserves_choice"] is True
    assert summary["text_history_ablation_changes_choice"] is True
