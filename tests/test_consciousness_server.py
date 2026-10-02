from src.consciousness_server.core import ConsciousnessStore


def test_instance_and_continuity_survive_restart(tmp_path):
    db = tmp_path / "consciousness.db"

    first = ConsciousnessStore(db)
    state = first.create_instance("test-ai")
    first.append_event(
        state.instance_id,
        "SELF_MODEL_UPDATE",
        {"model_version": "v1"},
    )
    expected_hash = first.state_hash(state.instance_id)
    first.close()

    second = ConsciousnessStore(db)
    restored = second.get_state(state.instance_id)

    assert restored is not None
    assert restored.identity == "test-ai"
    assert restored.self_model_version == 1
    assert restored.continuity_revision == 2
    assert second.state_hash(state.instance_id) == expected_hash
    second.close()


def test_nodes_and_events_are_persistent(tmp_path):
    db = tmp_path / "consciousness.db"
    store = ConsciousnessStore(db)

    instance = store.create_instance("node-backed-ai", "ci_demo")
    node = store.register_node(
        "node-local-01",
        "http://127.0.0.1:8787",
        ["continuity", "storage"],
    )
    store.append_event(
        instance.instance_id,
        "DYNAMIC_UPDATE",
        {"delta": 0.25},
    )

    assert node["status"] == "ONLINE"
    assert store.list_nodes()[0]["node_id"] == "node-local-01"
    events = store.list_events(instance.instance_id)
    assert events[-1]["event_type"] == "DYNAMIC_UPDATE"
    assert events[-1]["payload"]["delta"] == 0.25
    store.close()


def test_checkpoints_persist_and_capture_local_state(tmp_path):
    db = tmp_path / "consciousness.db"
    store = ConsciousnessStore(db)

    instance = store.create_instance("checkpoint-ai", "ci_checkpoint")
    checkpoint = store.create_checkpoint(
        instance.instance_id,
        runtime_mode="server",
        organism_mode="WAKE",
        payload={"cycle": 7, "state_fingerprint": "abc"},
        checkpoint_id="cp-test-001",
    )

    assert checkpoint["checkpoint_id"] == "cp-test-001"
    assert checkpoint["local_revision"] == 1
    assert checkpoint["payload"]["cycle"] == 7

    rows = store.list_checkpoints(instance.instance_id)
    assert len(rows) == 1
    assert rows[0]["checkpoint_id"] == "cp-test-001"

    store.close()

    reopened = ConsciousnessStore(db)
    rows = reopened.list_checkpoints(instance.instance_id)
    assert rows[0]["state_hash"] == checkpoint["state_hash"]
    assert rows[0]["payload"]["state_fingerprint"] == "abc"
    reopened.close()


def test_reconciliation_statuses(tmp_path):
    from src.consciousness_server.reconciliation import (
        ReconciliationStatus,
        reconcile,
    )

    store = ConsciousnessStore(tmp_path / "continuity.db")
    state = store.create_instance("reconcile-ai", "ci_reconcile")
    store.append_event(state.instance_id, "WAKE", {"cycle": 1})
    store.create_checkpoint(
        state.instance_id,
        runtime_mode="server",
        organism_mode="WAKE",
        payload={
            "state_fingerprint": "local-state-001",
            "trajectory_fingerprint": "local-trajectory-001",
            "event_count": 2,
            "memory_count": 0,
        },
        checkpoint_id="cp-reconcile-001",
    )

    aligned = reconcile(
        local_state_fingerprint="local-state-001",
        local_trajectory_fingerprint="local-trajectory-001",
        local_event_count=2,
        local_memory_count=0,
        checkpoints=store.list_checkpoints(state.instance_id),
    )
    assert aligned.status is ReconciliationStatus.ALIGNED

    store.append_event(state.instance_id, "DYNAMIC_UPDATE", {"delta": 1.0})
    ahead = reconcile(
        local_state_fingerprint="local-state-002",
        local_trajectory_fingerprint="local-trajectory-002",
        local_event_count=3,
        local_memory_count=0,
        checkpoints=store.list_checkpoints(state.instance_id),
    )
    assert ahead.status is ReconciliationStatus.LOCAL_AHEAD
    store.close()


def test_reconciliation_detects_divergence(tmp_path):
    from src.consciousness_server.reconciliation import (
        ReconciliationStatus,
        reconcile,
    )

    report = reconcile(
        local_state_fingerprint="local-state",
        local_trajectory_fingerprint="local-trajectory",
        local_event_count=5,
        local_memory_count=2,
        checkpoints=[
            {
                "checkpoint_id": "cp-diverged",
                "payload": {
                    "state_fingerprint": "remote-state",
                    "trajectory_fingerprint": "remote-trajectory",
                    "event_count": 5,
                    "memory_count": 2,
                },
            }
        ],
    )

    assert report.status is ReconciliationStatus.DIVERGED
