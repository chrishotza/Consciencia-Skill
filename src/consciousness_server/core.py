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
                event_id TEXT,
                instance_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                logical_revision INTEGER NOT NULL DEFAULT 0,
                parent_event_id TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(instance_id) REFERENCES instances(instance_id)
            );

            CREATE INDEX IF NOT EXISTS idx_events_instance_id
            ON events(instance_id, id);

            CREATE TABLE IF NOT EXISTS checkpoints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                checkpoint_id TEXT UNIQUE NOT NULL,
                instance_id TEXT NOT NULL,
                local_revision INTEGER NOT NULL,
                runtime_mode TEXT NOT NULL,
                organism_mode TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                state_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(instance_id) REFERENCES instances(instance_id)
            );

            CREATE INDEX IF NOT EXISTS idx_checkpoints_instance_id
            ON checkpoints(instance_id, id);

            CREATE TABLE IF NOT EXISTS nodes (
                node_id TEXT PRIMARY KEY,
                endpoint TEXT,
                capabilities_json TEXT NOT NULL,
                status TEXT NOT NULL,
                last_seen_at TEXT NOT NULL
            );
            """
        )

        existing_columns = {
            str(row["name"])
            for row in self.conn.execute("PRAGMA table_info(events)").fetchall()
        }
        if "event_id" not in existing_columns:
            self.conn.execute("ALTER TABLE events ADD COLUMN event_id TEXT")
        if "logical_revision" not in existing_columns:
            self.conn.execute(
                "ALTER TABLE events ADD COLUMN logical_revision INTEGER NOT NULL DEFAULT 0"
            )
        if "parent_event_id" not in existing_columns:
            self.conn.execute("ALTER TABLE events ADD COLUMN parent_event_id TEXT")
        self.conn.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_events_event_id ON events(event_id)"
        )
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_events_instance_revision ON events(instance_id, logical_revision)"
        )

        # Backfill deterministic identity and logical position for legacy event rows.
        rows = self.conn.execute(
            """
            SELECT id,instance_id,event_type,payload_json,
                   logical_revision,parent_event_id,event_id
            FROM events
            ORDER BY instance_id ASC, id ASC
            """
        ).fetchall()
        revision_by_instance: dict[str, int] = {}
        parent_by_instance: dict[str, str | None] = {}
        for row in rows:
            instance_id = str(row["instance_id"])
            revision = revision_by_instance.get(instance_id, 1)
            logical_revision = int(row["logical_revision"] or 0)
            if logical_revision <= revision:
                logical_revision = revision + 1
            parent_event_id = row["parent_event_id"] or parent_by_instance.get(instance_id)
            event_id = row["event_id"] or self.deterministic_event_id(
                instance_id,
                str(row["event_type"]),
                json.loads(row["payload_json"]),
                logical_revision,
                parent_event_id,
            )
            self.conn.execute(
                """
                UPDATE events
                SET event_id=?, logical_revision=?, parent_event_id=?
                WHERE id=?
                """,
                (event_id, logical_revision, parent_event_id, int(row["id"])),
            )
            revision_by_instance[instance_id] = logical_revision
            parent_by_instance[instance_id] = event_id

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

    @staticmethod
    def deterministic_event_id(
        instance_id: str,
        event_type: str,
        payload: dict[str, Any],
        logical_revision: int,
        parent_event_id: str | None,
    ) -> str:
        canonical = json.dumps(
            {
                "instance_id": instance_id,
                "event_type": event_type,
                "payload": payload,
                "logical_revision": int(logical_revision),
                "parent_event_id": parent_event_id,
            },
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    def latest_event_id(self, instance_id: str) -> str | None:
        row = self.conn.execute(
            """
            SELECT event_id FROM events
            WHERE instance_id=?
            ORDER BY logical_revision DESC, id DESC
            LIMIT 1
            """,
            (instance_id,),
        ).fetchone()
        return str(row["event_id"]) if row and row["event_id"] else None

    def _append_event(
        self,
        instance_id: str,
        event_type: str,
        payload: dict[str, Any],
        *,
        event_id: str | None = None,
        expected_revision: int | None = None,
        logical_revision: int | None = None,
        parent_event_id: str | None = None,
        created_at: str | None = None,
    ) -> ConsciousnessState:
        state = self.get_state(instance_id)
        if state is None:
            raise KeyError(f"unknown instance: {instance_id}")

        payload = dict(payload)
        if event_id:
            existing = self.conn.execute(
                "SELECT instance_id,event_type,payload_json FROM events WHERE event_id=?",
                (event_id,),
            ).fetchone()
            if existing is not None:
                if (
                    existing["instance_id"] != instance_id
                    or existing["event_type"] != event_type
                    or json.loads(existing["payload_json"]) != payload
                ):
                    raise ValueError("event_id_conflict")
                return state

        if expected_revision is not None and state.revision != int(expected_revision):
            raise ValueError("revision_conflict")

        next_revision = state.revision + 1
        if logical_revision is not None and int(logical_revision) != next_revision:
            raise ValueError("logical_revision_conflict")

        current_parent = self.latest_event_id(instance_id)
        if parent_event_id is not None and parent_event_id != current_parent:
            raise ValueError("parent_event_conflict")
        parent_event_id = current_parent

        event_id = event_id or self.deterministic_event_id(
            instance_id,
            event_type,
            payload,
            next_revision,
            parent_event_id,
        )
        now = created_at or now_iso()
        state.revision = next_revision
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
            """
            INSERT INTO events(
                event_id, instance_id, event_type, payload_json,
                logical_revision, parent_event_id, created_at
            ) VALUES(?,?,?,?,?,?,?)
            """,
            (
                event_id,
                instance_id,
                event_type,
                json.dumps(payload, ensure_ascii=False),
                next_revision,
                parent_event_id,
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

    def append_event(
        self,
        instance_id: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
        *,
        event_id: str | None = None,
        expected_revision: int | None = None,
        logical_revision: int | None = None,
        parent_event_id: str | None = None,
        created_at: str | None = None,
    ) -> ConsciousnessState:
        return self._append_event(
            instance_id,
            event_type,
            payload or {},
            event_id=event_id,
            expected_revision=expected_revision,
            logical_revision=logical_revision,
            parent_event_id=parent_event_id,
            created_at=created_at,
        )

    def list_events(self, instance_id: str, limit: int = 100) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            """
            SELECT id,event_id,event_type,payload_json,logical_revision,parent_event_id,created_at
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
                "event_id": row["event_id"],
                "event_type": row["event_type"],
                "payload": json.loads(row["payload_json"]),
                "logical_revision": int(row["logical_revision"]),
                "parent_event_id": row["parent_event_id"],
                "created_at": row["created_at"],
            }
            for row in reversed(rows)
        ]

    def list_events_after(
        self,
        instance_id: str,
        after_revision: int,
        limit: int = 1000,
    ) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            """
            SELECT id,event_id,event_type,payload_json,logical_revision,parent_event_id,created_at
            FROM events
            WHERE instance_id=? AND logical_revision>?
            ORDER BY logical_revision ASC, id ASC
            LIMIT ?
            """,
            (instance_id, int(after_revision), max(1, min(int(limit), 1000))),
        ).fetchall()
        return [
            {
                "id": int(row["id"]),
                "event_id": row["event_id"],
                "event_type": row["event_type"],
                "payload": json.loads(row["payload_json"]),
                "logical_revision": int(row["logical_revision"]),
                "parent_event_id": row["parent_event_id"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]

    def replay_events(
        self,
        instance_id: str,
        events: list[dict[str, Any]],
        *,
        base_revision: int,
        base_state_hash: str | None = None,
    ) -> ConsciousnessState:
        state = self.get_state(instance_id)
        if state is None:
            raise KeyError(f"unknown instance: {instance_id}")
        if not events:
            return state

        ids = [str(event.get("event_id", "")) for event in events]
        existing = {
            row["event_id"]
            for row in self.conn.execute(
                "SELECT event_id FROM events WHERE instance_id=? AND event_id IN (%s)"
                % ",".join("?" for _ in ids),
                (instance_id, *ids),
            ).fetchall()
            if row["event_id"]
        }
        if ids and len(existing) == len(ids) and len(set(ids)) == len(ids):
            return state

        if state.revision != int(base_revision):
            raise ValueError("base_revision_mismatch")
        if base_state_hash is not None and self.state_hash(instance_id) != base_state_hash:
            raise ValueError("base_state_hash_mismatch")

        expected_revision = state.revision
        expected_parent = self.latest_event_id(instance_id)
        for event in events:
            logical_revision = int(event["logical_revision"])
            if logical_revision != expected_revision + 1:
                raise ValueError("replay_revision_gap")
            if event.get("parent_event_id") != expected_parent:
                raise ValueError("replay_parent_mismatch")
            expected_revision = logical_revision
            expected_parent = str(event["event_id"])

        for event in events:
            state = self._append_event(
                instance_id,
                str(event["event_type"]),
                dict(event.get("payload", {})),
                event_id=str(event["event_id"]),
                expected_revision=state.revision,
                logical_revision=int(event["logical_revision"]),
                parent_event_id=event.get("parent_event_id"),
                created_at=str(event["created_at"]),
            )
        return state

    def state_hash(self, instance_id: str) -> str | None:
        row = self.conn.execute(
            "SELECT state_hash FROM instances WHERE instance_id=?",
            (instance_id,),
        ).fetchone()
        return str(row["state_hash"]) if row else None

    def create_checkpoint(
        self,
        instance_id: str,
        runtime_mode: str,
        organism_mode: str,
        payload: dict[str, Any] | None = None,
        checkpoint_id: str | None = None,
    ) -> dict[str, Any]:
        state = self.get_state(instance_id)
        if state is None:
            raise KeyError(f"unknown instance: {instance_id}")

        checkpoint_id = checkpoint_id or f"cp_{uuid.uuid4().hex[:20]}"
        now = now_iso()
        state_hash = self._hash_state(state)
        payload = payload or {}

        self.conn.execute(
            """
            INSERT INTO checkpoints(
                checkpoint_id, instance_id, local_revision,
                runtime_mode, organism_mode, payload_json,
                state_hash, created_at
            ) VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                checkpoint_id,
                instance_id,
                state.revision,
                str(runtime_mode),
                str(organism_mode),
                json.dumps(payload, ensure_ascii=False),
                state_hash,
                now,
            ),
        )
        self.conn.commit()

        return {
            "checkpoint_id": checkpoint_id,
            "instance_id": instance_id,
            "local_revision": state.revision,
            "runtime_mode": str(runtime_mode),
            "organism_mode": str(organism_mode),
            "payload": payload,
            "state_hash": state_hash,
            "created_at": now,
        }

    def list_checkpoints(
        self,
        instance_id: str,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            """
            SELECT
                checkpoint_id, instance_id, local_revision,
                runtime_mode, organism_mode, payload_json,
                state_hash, created_at
            FROM checkpoints
            WHERE instance_id=?
            ORDER BY id DESC
            LIMIT ?
            """,
            (instance_id, max(1, min(int(limit), 1000))),
        ).fetchall()

        return [
            {
                "checkpoint_id": row["checkpoint_id"],
                "instance_id": row["instance_id"],
                "local_revision": int(row["local_revision"]),
                "runtime_mode": row["runtime_mode"],
                "organism_mode": row["organism_mode"],
                "payload": json.loads(row["payload_json"]),
                "state_hash": row["state_hash"],
                "created_at": row["created_at"],
            }
            for row in reversed(rows)
        ]

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
