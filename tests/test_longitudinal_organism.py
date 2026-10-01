from pathlib import Path

from experiments.longitudinal_organism_v1 import run_protocol


def test_longitudinal_protocol_reopens_and_records_trajectory(tmp_path: Path):
    report = run_protocol(
        db_path=tmp_path / "results.db",
        agent_id="protocol-test",
        mode="fake",
        cycles=6,
        dream_every=3,
        sleep_seconds=0.0,
    )

    assert report["before_reopen"]["dynamic_snapshot_count"] >= 6
    assert report["after_reopen"]["dynamic_snapshot_count"] >= 7
    assert report["after_reopen"]["dynamic_steps"] >= 7
    assert report["recovery_passed"] is True
    assert report["new_trajectory_after_reopen"] is True
    assert report["trajectory_summary"]["mode_counts"]["WAKE"] >= 1
    assert report["trajectory_summary"]["mode_counts"]["DREAM"] >= 1
