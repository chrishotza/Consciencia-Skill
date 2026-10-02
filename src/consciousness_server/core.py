from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ConsciousnessState:
    instance_id: str
    identity: str
    status: str = "INITIALIZING"
    revision: int = 0
    continuity_revision: int = 0
    self_model_version: int = 0
    memory_version: int = 0
    dynamic_revision: int = 0
    last_event_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ConsciousnessStore:
    """Local-first persistent control plane.

    This is the first bootstrap layer. It does not claim subjective
    consciousness. It provides durable identity, continuity, events and
    node registration so an external organism runtime can persist and
    eventually federate across NodeZero.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS instances (
                instance_id TEXT PRIMARY KEY,
                identity TEXT NOT NULL,
                state_json TEXT NOT NULL,
                state_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                instance_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(instance_id) REFERENCES instances(instance_id)
            );

            CREATE INDEX IF NOT EXISTS idx_events_instance_id
            ON events(instance_id, id);

            CREATE TABLE IF NOT EXISTS nodes (
                node_id TEXT PRIMARY KEY,
                endpoint TEXT,
                capabilities_json TEXT NOT NULL,
                status TEXT NOT NULL,
                last_seen_at TEXT NOT NULL
            );
            """
        )
        self.conn.commit()

    @staticmethod
    def _hash_state(state: ConsciousnessState) -> str:
        payload = json.dumps(
            state.to_dict(),
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def create_instance(
        self,
        identity: str,
        instance_id: str | None = None,
    ) -> ConsciousnessState:
        instance_id = instance_id or f"ci_{uuid.uuid4().hex[:16]}"
        state = ConsciousnessState(
            instance_id=instance_id,
            identity=identity,
            status="ACTIVE",
            revision=1,
            continuity_revision=1,
        )
        now = now_iso()
        self.conn.execute(
            """
            INSERT INTO instances(
                instance_id, identity, state_json, state_hash, created_at, updated_at
            ) VALUES(?,?,?,?,?,?)
            """,
            (
                instance_id,
                identity,
                json.dumps(state.to_dict(), ensure_ascii=False),
                self._hash_state(state),
                now,
                now,
            ),
        )
        self.conn.commit()
        return state

    def get_state(self, instance_id: str) -> ConsciousnessState | None:
        row = self.conn.execute(
            "SELECT state_json FROM instances WHERE instance_id=?",
            (instance_id,),
        ).fetchone()
        if row is None:
            return None
        return ConsciousnessState(**json.loads(row["state_json"]))

    def append_event(
        self,
        instance_id: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
    ) -> ConsciousnessState:
        state = self.get_state(instance_id)
        if state is None:
            raise KeyError(f"unknown instance: {instance_id}")

        payload = payload or {}
        now = now_iso()
        state.revision += 1
        state.continuity_revision += 1
        state.last_event_at = now

        if event_type == "SELF_MODEL_UPDATE":
            state.self_model_version += 1
        elif event_type == "MEMORY_UPDATE":
            state.memory_version += 1
        elif event_type == "DYNAMIC_UPDATE":
            state.dynamic_revision += 1
        elif event_type in {"STOP", "SLEEP"}:
            state.status = "SLEEPING"
        elif event_type in {"START", "WAKE"}:
            state.status = "ACTIVE"

        self.conn.execute(
            "INSERT INTO events(instance_id,event_type,payload_json,created_at) VALUES(?,?,?,?)",
            (
                instance_id,
                event_type,
                json.dumps(payload, ensure_ascii=False),
                now,
            ),
        )
        self.conn.execute(
            """
            UPDATE instances
            SET state_json=?, state_hash=?, updated_at=?
            WHERE instance_id=?
            """,
            (
                json.dumps(state.to_dict(), ensure_ascii=False),
                self._hash_state(state),
                now,
                instance_id,
            ),
        )
        self.conn.commit()
        return state

    def list_events(self, instance_id: str, limit: int = 100) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            """
            SELECT id,event_type,payload_json,created_at
            FROM events
            WHERE instance_id=?
            ORDER BY id DESC
            LIMIT ?
            """,
            (instance_id, max(1, min(limit, 1000))),
        ).fetchall()
        return [
            {
                "id": int(row["id"]),
                "event_type": row["event_type"],
                "payload": json.loads(row["payload_json"]),
                "created_at": row["created_at"],
            }
            for row in reversed(rows)
        ]

    def state_hash(self, instance_id: str) -> str | None:
        row = self.conn.execute(
            "SELECT state_hash FROM instances WHERE instance_id=?",
            (instance_id,),
        ).fetchone()
        return str(row["state_hash"]) if row else None

    def register_node(
        self,
        node_id: str,
        endpoint: str | None = None,
        capabilities: list[str] | None = None,
    ) -> dict[str, Any]:
        now = now_iso()
        self.conn.execute(
            """
            INSERT INTO nodes(node_id,endpoint,capabilities_json,status,last_seen_at)
            VALUES(?,?,?,?,?)
            ON CONFLICT(node_id) DO UPDATE SET
                endpoint=excluded.endpoint,
                capabilities_json=excluded.capabilities_json,
                status='ONLINE',
                last_seen_at=excluded.last_seen_at
            """,
            (
                node_id,
                endpoint,
                json.dumps(capabilities or [], ensure_ascii=False),
                "ONLINE",
                now,
            ),
        )
        self.conn.commit()
        return {
            "node_id": node_id,
            "endpoint": endpoint,
            "capabilities": capabilities or [],
            "status": "ONLINE",
            "last_seen_at": now,
        }

    def list_nodes(self) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT node_id,endpoint,capabilities_json,status,last_seen_at FROM nodes ORDER BY node_id"
        ).fetchall()
        return [
            {
                "node_id": row["node_id"],
                "endpoint": row["endpoint"],
                "capabilities": json.loads(row["capabilities_json"]),
                "status": row["status"],
                "last_seen_at": row["last_seen_at"],
            }
            for row in rows
        ]

    def close(self) -> None:
        self.conn.close()
