from __future__ import annotations

from src.ontto.persistence_backend import (
    ServerMirroredPersistenceBackend,
    build_persistence_backend,
)
from src.ontto.runtime_mode import ConsciousnessMode
from src.ontto.storage import OntologicalState


class FakeClient:
    def __init__(self):
        self.calls = []

    def emit(self, instance_id, event_type, payload=None):
        self.calls.append(
            {
                "instance_id": instance_id,
                "event_type": event_type,
                "payload": payload or {},
            }
        )
        return {"ok": True}


def test_local_backend_preserves_existing_store(tmp_path):
    backend = build_persistence_backend(
        tmp_path / "local.db",
        mode=ConsciousnessMode.LOCAL,
    )

    assert backend.__class__.__name__ == "MemoryStore"
    state = OntologicalState(dynamic_state=0.25)
    backend.save_state("agent", state)

    assert backend.load_state("agent").dynamic_state == 0.25
    backend.conn.close()


def test_server_backend_mirrors_after_local_commit(tmp_path):
    client = FakeClient()
    backend = build_persistence_backend(
        tmp_path / "mirror.db",
        mode=ConsciousnessMode.SERVER,
        client=client,
        agent_id="agent",
    )

    assert isinstance(backend, ServerMirroredPersistenceBackend)

    backend.save_state(
        "agent",
        OntologicalState(dynamic_state=0.5),
    )
    backend.add_memory("agent", "memory A", importance=0.8)
    backend.add_event(
        "agent",
        "WAKE",
        "cycle",
        {"signal": 1.0},
    )

    assert backend.load_state("agent").dynamic_state == 0.5
    assert len(client.calls) == 3
    assert [call["event_type"] for call in client.calls] == [
        "STATE_SNAPSHOT",
        "MEMORY_UPDATE",
        "ORGANISM_EVENT",
    ]
    assert client.calls[-1]["payload"]["event_count"] == 1
    assert client.calls[1]["payload"]["memory_count"] == 1
    backend.conn.close()


def test_server_mirror_failure_is_fail_open(tmp_path):
    class BrokenClient:
        def emit(self, *args, **kwargs):
            raise RuntimeError("server offline")

    backend = ServerMirroredPersistenceBackend(
        tmp_path / "fail-open.db",
        BrokenClient(),
        agent_id="agent",
    )
    backend.save_state("agent", OntologicalState(dynamic_state=0.75))
    backend.add_event(
        "agent",
        "SYSTEM",
        "test",
        {"ok": True},
    )

    assert backend.load_state("agent").dynamic_state == 0.75
    assert backend.event_count("agent") == 1
    backend.conn.close()
