from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from src.consciousness_server.client import ConsciousnessClient
from src.ontto.runtime_mode import ConsciousnessMode
from src.ontto.storage import MemoryStore, OntologicalState


@runtime_checkable
class PersistenceBackend(Protocol):
    """Persistence boundary used by the persistent organism.

    The current implementation keeps the cognitive state local. In SERVER
    mode the backend can additionally mirror continuity-critical mutations to
    the Consciousness Server without changing the organism loop.
    """

    def load_state(self, agent_id: str) -> OntologicalState: ...
    def save_state(self, agent_id: str, state: OntologicalState) -> None: ...
    def add_event(
        self,
        agent_id: str,
        mode: str,
        kind: str,
        payload: dict[str, Any],
    ) -> None: ...
    def add_memory(
        self,
        agent_id: str,
        content: str,
        importance: float = 0.5,
    ) -> None: ...


class ServerMirroredPersistenceBackend(MemoryStore):
    """Local SQLite persistence with a fail-open continuity mirror.

    SQLite remains the execution source of truth. The server receives
    continuity-critical mutations after the local transaction commits.
    """

    def __init__(
        self,
        path: str | Path,
        client: ConsciousnessClient,
        *,
        agent_id: str,
    ):
        super().__init__(path)
        self._consciousness_client = client
        self._mirror_agent_id = agent_id

    def _mirror(
        self,
        event_type: str,
        payload: dict[str, Any],
    ) -> None:
        try:
            self._consciousness_client.emit(
                self._mirror_agent_id,
                event_type,
                payload,
            )
        except Exception as exc:
            print(
                f"[persistence-mirror] {event_type} failed: {exc!r}"
            )

    def save_state(self, agent_id: str, state: OntologicalState) -> None:
        super().save_state(agent_id, state)
        self._mirror(
            "STATE_SNAPSHOT",
            {
                "agent_id": agent_id,
                "state": state.to_json(),
                "state_fingerprint": self.state_fingerprint(agent_id),
            },
        )

    def add_event(
        self,
        agent_id: str,
        mode: str,
        kind: str,
        payload: dict[str, Any],
    ) -> None:
        super().add_event(agent_id, mode, kind, payload)
        self._mirror(
            "ORGANISM_EVENT",
            {
                "agent_id": agent_id,
                "mode": mode,
                "kind": kind,
                "payload": payload,
                "event_count": self.event_count(agent_id),
                "trajectory_fingerprint": self.trajectory_fingerprint(agent_id),
            },
        )

    def add_memory(
        self,
        agent_id: str,
        content: str,
        importance: float = 0.5,
    ) -> None:
        super().add_memory(agent_id, content, importance)
        self._mirror(
            "MEMORY_UPDATE",
            {
                "agent_id": agent_id,
                "content": content,
                "importance": float(importance),
                "memory_count": self.memory_count(agent_id),
                "memory_fingerprint": self.memory_fingerprint(agent_id),
            },
        )


def build_persistence_backend(
    path: str | Path,
    *,
    mode: ConsciousnessMode,
    client: ConsciousnessClient | None = None,
    agent_id: str | None = None,
) -> MemoryStore:
    if mode is ConsciousnessMode.SERVER:
        if client is None or not agent_id:
            raise ValueError(
                "SERVER persistence requires a ConsciousnessClient and agent_id"
            )
        return ServerMirroredPersistenceBackend(
            path,
            client,
            agent_id=agent_id,
        )

    return MemoryStore(path)
