import json
import sys
from pathlib import Path

from experiments.organism_memory_swap_v48 import main


def test_v48_fake_memory_swap(tmp_path: Path, monkeypatch):
    out = tmp_path / "v48"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "organism_memory_swap_v48.py",
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

    assert summary["same_receiver_state_before_intervention"] is True
    assert summary["only_memory_content_changed"] is True
    assert summary["memory_swap_changes_choice"] is True
