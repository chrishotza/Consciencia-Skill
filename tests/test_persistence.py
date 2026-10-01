from src.ontto.storage import MemoryStore, OntologicalState


def test_state_survives_restart(tmp_path):
    db = tmp_path / "state.db"
    a = MemoryStore(db)
    state = OntologicalState(
        state=0.7,
        mode="DREAM",
        continuity_index=0.8,
        self_model_version=3,
        dynamic_state=0.4,
        dynamic_memory=0.2,
        dynamic_pressure=0.1,
        dynamic_steps=7,
    )
    a.save_state("agent", state)
    a.conn.close()

    b = MemoryStore(db)
    restored = b.load_state("agent")
    assert restored.state == 0.7
    assert restored.mode == "DREAM"
    assert restored.continuity_index == 0.8
    assert restored.self_model_version == 3
    assert restored.dynamic_state == 0.4
    assert restored.dynamic_memory == 0.2
    assert restored.dynamic_pressure == 0.1
    assert restored.dynamic_steps == 7
    b.conn.close()



def test_memory_recovery_from_event_log(tmp_path):
    db = tmp_path / "recovery.db"
    store = MemoryStore(db)

    store.add_memory("agent", "recuerdo A")
    store.add_event(
        "agent",
        "WAKE",
        "interaction",
        {"response": "MEMORY: recuerdo A"},
    )
    store.add_event(
        "agent",
        "WAKE",
        "interaction",
        {"response": "MEMORY: recuerdo B"},
    )

    store.conn.execute("DELETE FROM memories WHERE agent_id=?", ("agent",))
    store.conn.commit()

    recovered = store.recover_memories_from_events("agent")

    assert recovered == 2
    assert store.recent_memories("agent") == ["recuerdo A", "recuerdo B"]



def test_input_queue_survives_restart_and_requeues_processing(tmp_path):
    db = tmp_path / "queue.db"
    first = MemoryStore(db)

    input_id = first.enqueue_input(
        "agent",
        "mensaje persistente",
        source="test",
    )
    claimed = first.claim_next_input("agent")

    assert claimed is not None
    assert claimed["id"] == input_id
    assert claimed["content"] == "mensaje persistente"
    assert first.pending_input_count("agent") == 0

    first.conn.close()

    second = MemoryStore(db)
    requeued = second.requeue_processing_inputs("agent")
    assert requeued == 1

    restored = second.claim_next_input("agent")
    assert restored is not None
    assert restored["id"] == input_id

    second.complete_input(input_id)
    assert second.pending_input_count("agent") == 0
