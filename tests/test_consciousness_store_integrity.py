from __future__ import annotations

import threading

import pytest

from src.consciousness_server.core import ConsciousnessStore


def test_replay_batch_is_atomic_on_late_event_conflict(tmp_path):
    store = ConsciousnessStore(tmp_path / "atomic-replay.db")
    try:
        store.create_instance("agent", "atomic-agent")
        store.append_event(
            "agent",
            "WAKE",
            {"cycle": 1},
            created_at="2026-10-02T05:00:00+00:00",
        )

        existing_event_id = store.list_events("agent")[-1]["event_id"]
        base_state = store.get_state("agent")
        assert base_state is not None
        base_revision = base_state.revision
        base_hash = store.state_hash("agent")

        events = [
            {
                "event_id": "replay-new-event",
                "event_type": "WAKE",
                "payload": {"cycle": 2},
                "logical_revision": base_revision + 1,
                "parent_event_id": existing_event_id,
                "created_at": "2026-10-02T05:00:01+00:00",
            },
            {
                "event_id": existing_event_id,
                "event_type": "WAKE",
                "payload": {"conflicting": True},
                "logical_revision": base_revision + 2,
                "parent_event_id": "replay-new-event",
                "created_at": "2026-10-02T05:00:02+00:00",
            },
        ]

        with pytest.raises(ValueError, match="event_id_conflict"):
            store.replay_events(
                "agent",
                events,
                base_revision=base_revision,
                base_state_hash=base_hash,
            )

        restored = store.get_state("agent")
        assert restored is not None
        assert restored.revision == base_revision
        assert store.state_hash("agent") == base_hash
        stored_events = store.list_events("agent")
        assert len(stored_events) == 1
        assert stored_events[-1]["event_id"] == existing_event_id
    finally:
        store.close()


def test_store_serializes_concurrent_writes(tmp_path):
    store = ConsciousnessStore(tmp_path / "concurrent.db")
    try:
        store.create_instance("agent", "concurrent-agent")
        worker_count = 12
        barrier = threading.Barrier(worker_count)
        errors: list[BaseException] = []

        def writer(index: int) -> None:
            try:
                barrier.wait(timeout=5)
                store.append_event(
                    "agent",
                    "WAKE",
                    {"worker": index},
                    created_at=f"2026-10-02T05:10:{index:02d}+00:00",
                )
            except BaseException as exc:
                errors.append(exc)

        threads = [
            threading.Thread(target=writer, args=(index,))
            for index in range(worker_count)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=5)

        assert not errors
        events = store.list_events("agent")
        assert len(events) == worker_count
        assert [event["logical_revision"] for event in events] == list(
            range(2, worker_count + 2)
        )
        assert {event["payload"]["worker"] for event in events} == set(
            range(worker_count)
        )
    finally:
        store.close()
