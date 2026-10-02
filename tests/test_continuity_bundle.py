from __future__ import annotations

import json

from src.ontto.continuity_bundle import (
    create_bundle,
    restore_bundle,
    verify_bundle,
)
from src.ontto.storage import MemoryStore


def test_continuity_bundle_round_trip(tmp_path):
    source_db = tmp_path / "source.db"
    bundle_dir = tmp_path / "bundle"
    restored_db = tmp_path / "restored.db"

    source = MemoryStore(source_db)
    state = source.load_state("agent")
    state.boot_count = 3
    state.dynamic_state = 0.42
    source.save_state("agent", state)
    source.add_memory("agent", "persistent continuity")
    source.add_event(
        "agent",
        "WAKE",
        "test",
        {"value": 7},
    )
    source.save_self_observer_model(
        "agent",
        {"weights": [1.0, 2.0], "targets": [0.3, 0.4]},
    )
    expected = source.persistence_observables("agent")
    source.conn.close()

    manifest = create_bundle(
        db_path=source_db,
        agent_id="agent",
        out_dir=bundle_dir,
    )

    assert manifest["agent_id"] == "agent"
    assert (bundle_dir / "manifest.json").exists()
    assert (bundle_dir / "organism.sqlite3").exists()

    verification = verify_bundle(bundle_dir)
    assert verification["valid"] is True
    assert verification["observables"]["event_count"] == expected["event_count"]
    assert verification["observables"]["memory_count"] == expected["memory_count"]

    restore_bundle(
        bundle_dir=bundle_dir,
        target_db=restored_db,
    )

    restored = MemoryStore(restored_db)
    observed = restored.persistence_observables("agent")
    assert observed["state_fingerprint"] == expected["state_fingerprint"]
    assert observed["trajectory_fingerprint"] == expected["trajectory_fingerprint"]
    assert observed["memory_fingerprint"] == expected["memory_fingerprint"]
    assert observed["self_model_version"] == expected["self_model_version"]
    assert observed["dynamic_state"] == expected["dynamic_state"]

    stored_manifest = json.loads(
        (bundle_dir / "manifest.json").read_text(encoding="utf-8")
    )
    assert stored_manifest["database_sha256"] == verification["actual_sha256"]
    restored.conn.close()


def test_continuity_bundle_rejects_tampering(tmp_path):
    source_db = tmp_path / "source.db"
    bundle_dir = tmp_path / "bundle"

    source = MemoryStore(source_db)
    source.save_state("agent", source.load_state("agent"))
    source.conn.close()

    create_bundle(
        db_path=source_db,
        agent_id="agent",
        out_dir=bundle_dir,
    )

    database = bundle_dir / "organism.sqlite3"
    with database.open("ab") as handle:
        handle.write(b"tamper")

    verification = verify_bundle(bundle_dir)
    assert verification["valid"] is False
