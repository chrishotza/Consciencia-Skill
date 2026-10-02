from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class OntologicalState:
    state: float = 0.0
    pressure: float = 0.0
    # Operationally interpreted as persistent-memory coverage.
    memory_strength: float = 0.0
    attractor: float = 0.0
    mode: str = "WAKE"
    # Deprecated scalar kept for state-file compatibility. Continuity is
    # validated from persisted trajectory/state observables, not by incrementing
    # this field heuristically.
    continuity_index: float = 0.0
    self_model_version: int = 0
    self_model: str = ""
    lifetime_wake_cycles: int = 0
    lifetime_dream_cycles: int = 0
    boot_count: int = 0
    last_thought: str = ""
    # Numeric trajectory state bridged to src/ontto/dynamics.py.
    dynamic_state: float = 0.0
    dynamic_prev_state: float = 0.0
    dynamic_memory: float = 0.0
    dynamic_pressure: float = 0.0
    dynamic_attractor_distance: float = 0.0
    dynamic_last_input: float = 0.0
    dynamic_steps: int = 0
    # Operational self-observation metrics.
    self_prediction: float = 0.0
    self_prediction_error: float = 0.0
    self_prediction_gain: float = 0.0
    self_prediction_confidence: float = 0.0
    self_prediction_samples: int = 0
    # Bounded global-workspace runtime observables.
    workspace_last_selected_module: int = -1
    workspace_last_broadcast: list[float] = None
    workspace_steps: int = 0

    def to_json(self) -> str:
        payload = asdict(self)
        if payload.get('workspace_last_broadcast') is None:
            payload['workspace_last_broadcast'] = [0.0, 0.0]
        return json.dumps(payload, ensure_ascii=False)

    @classmethod
    def from_json(cls, value: str) -> "OntologicalState":
        return cls(**json.loads(value))


class MemoryStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS state (
                agent_id TEXT PRIMARY KEY,
                state_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                mode TEXT NOT NULL,
                kind TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                importance REAL NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS dream_cycles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                started_at TEXT NOT NULL,
                ended_at TEXT,
                summary TEXT,
                state_before TEXT,
                state_after TEXT
            );
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                label TEXT NOT NULL,
                state_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS dynamic_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                mode TEXT NOT NULL,
                label TEXT NOT NULL,
                step_start INTEGER NOT NULL,
                step_end INTEGER NOT NULL,
                signal REAL NOT NULL,
                previous_state REAL NOT NULL,
                state REAL NOT NULL,
                memory REAL NOT NULL,
                pressure REAL NOT NULL,
                attractor_distance REAL NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_dynamic_snapshots_agent_step
            ON dynamic_snapshots(agent_id, step_end);
            CREATE TABLE IF NOT EXISTS self_observer_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                mode TEXT NOT NULL,
                label TEXT NOT NULL,
                step_start INTEGER NOT NULL,
                step_end INTEGER NOT NULL,
                features_json TEXT NOT NULL,
                predicted_state REAL NOT NULL,
                baseline_state REAL NOT NULL,
                actual_state REAL NOT NULL,
                prediction_error REAL NOT NULL,
                baseline_error REAL NOT NULL,
                gain REAL NOT NULL,
                confidence REAL NOT NULL,
                samples INTEGER NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_self_observer_agent_step
            ON self_observer_snapshots(agent_id, step_end);
            CREATE TABLE IF NOT EXISTS self_observer_models (
                agent_id TEXT PRIMARY KEY,
                model_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS self_policy_models (
                agent_id TEXT PRIMARY KEY,
                model_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS action_conditioned_meta_observer_models (
                agent_id TEXT PRIMARY KEY,
                model_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS input_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING',
                created_at TEXT NOT NULL,
                processed_at TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_input_queue_pending
            ON input_queue(agent_id, status, id);
        """)
        self.conn.commit()

    def load_state(self, agent_id: str) -> OntologicalState:
        row = self.conn.execute("SELECT state_json FROM state WHERE agent_id=?", (agent_id,)).fetchone()
        return OntologicalState.from_json(row[0]) if row else OntologicalState()

    def save_state(self, agent_id: str, state: OntologicalState) -> None:
        self.conn.execute(
            "INSERT INTO state(agent_id,state_json,updated_at) VALUES(?,?,?) "
            "ON CONFLICT(agent_id) DO UPDATE SET state_json=excluded.state_json,updated_at=excluded.updated_at",
            (agent_id, state.to_json(), now_iso()),
        )
        self.conn.commit()

    def add_event(self, agent_id: str, mode: str, kind: str, payload: dict[str, Any]) -> None:
        self.conn.execute(
            "INSERT INTO events(agent_id,mode,kind,payload_json,created_at) VALUES(?,?,?,?,?)",
            (agent_id, mode, kind, json.dumps(payload, ensure_ascii=False), now_iso()),
        )
        self.conn.commit()

    def add_memory(self, agent_id: str, content: str, importance: float = 0.5) -> None:
        self.conn.execute(
            "INSERT INTO memories(agent_id,importance,content,created_at) VALUES(?,?,?,?)",
            (agent_id, float(importance), content, now_iso()),
        )
        self.conn.commit()

    def enqueue_input(
        self,
        agent_id: str,
        content: str,
        source: str = "external",
    ) -> int:
        content = str(content).strip()
        if not content:
            raise ValueError("input content cannot be empty")
        cur = self.conn.execute(
            "INSERT INTO input_queue(agent_id,content,source,status,created_at) "
            "VALUES(?,?,?,?,?)",
            (agent_id, content, source, "PENDING", now_iso()),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def claim_next_input(self, agent_id: str) -> dict[str, Any] | None:
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            row = self.conn.execute(
                "SELECT id,content,source,created_at "
                "FROM input_queue "
                "WHERE agent_id=? AND status='PENDING' "
                "ORDER BY id ASC LIMIT 1",
                (agent_id,),
            ).fetchone()
            if row is None:
                self.conn.commit()
                return None

            input_id, content, source, created_at = row
            self.conn.execute(
                "UPDATE input_queue SET status='PROCESSING' WHERE id=?",
                (input_id,),
            )
            self.conn.commit()
            return {
                "id": int(input_id),
                "content": content,
                "source": source,
                "created_at": created_at,
            }
        except Exception:
            self.conn.rollback()
            raise

    def complete_input(self, input_id: int) -> None:
        self.conn.execute(
            "UPDATE input_queue SET status='DONE', processed_at=? WHERE id=?",
            (now_iso(), int(input_id)),
        )
        self.conn.commit()

    def fail_input(self, input_id: int) -> None:
        self.conn.execute(
            "UPDATE input_queue SET status='PENDING' WHERE id=?",
            (int(input_id),),
        )
        self.conn.commit()

    def requeue_processing_inputs(self, agent_id: str) -> int:
        cur = self.conn.execute(
            "UPDATE input_queue SET status='PENDING' "
            "WHERE agent_id=? AND status='PROCESSING'",
            (agent_id,),
        )
        self.conn.commit()
        return int(cur.rowcount)

    def pending_input_count(self, agent_id: str) -> int:
        row = self.conn.execute(
            "SELECT COUNT(*) FROM input_queue WHERE agent_id=? AND status='PENDING'",
            (agent_id,),
        ).fetchone()
        return int(row[0])

    def save_self_observer_model(self, agent_id: str, model: dict[str, Any]) -> None:
        self.conn.execute(
            "INSERT INTO self_observer_models(agent_id,model_json,updated_at) VALUES(?,?,?) "
            "ON CONFLICT(agent_id) DO UPDATE SET model_json=excluded.model_json,updated_at=excluded.updated_at",
            (agent_id, json.dumps(model, ensure_ascii=False), now_iso()),
        )
        self.conn.commit()

    def load_self_observer_model(self, agent_id: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT model_json FROM self_observer_models WHERE agent_id=?",
            (agent_id,),
        ).fetchone()
        if row is None:
            return None
        return json.loads(row[0])

    def save_self_policy_model(self, agent_id: str, model: dict[str, Any]) -> None:
        self.conn.execute(
            "INSERT INTO self_policy_models(agent_id,model_json,updated_at) VALUES(?,?,?) "
            "ON CONFLICT(agent_id) DO UPDATE SET model_json=excluded.model_json,updated_at=excluded.updated_at",
            (agent_id, json.dumps(model, ensure_ascii=False), now_iso()),
        )
        self.conn.commit()

    def load_self_policy_model(self, agent_id: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT model_json FROM self_policy_models WHERE agent_id=?",
            (agent_id,),
        ).fetchone()
        if row is None:
            return None
        return json.loads(row[0])

    def save_action_conditioned_meta_observer_model(
        self,
        agent_id: str,
        model: dict[str, Any],
    ) -> None:
        self.conn.execute(
            "INSERT INTO action_conditioned_meta_observer_models("
            "agent_id,model_json,updated_at"
            ") VALUES(?,?,?) "
            "ON CONFLICT(agent_id) DO UPDATE SET "
            "model_json=excluded.model_json,updated_at=excluded.updated_at",
            (
                agent_id,
                json.dumps(model, ensure_ascii=False),
                now_iso(),
            ),
        )
        self.conn.commit()

    def load_action_conditioned_meta_observer_model(
        self,
        agent_id: str,
    ) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT model_json FROM action_conditioned_meta_observer_models "
            "WHERE agent_id=?",
            (agent_id,),
        ).fetchone()
        if row is None:
            return None
        return json.loads(row[0])

    def recent_memories(self, agent_id: str, limit: int = 12) -> list[str]:
        rows = self.conn.execute(
            "SELECT content FROM memories WHERE agent_id=? ORDER BY id DESC LIMIT ?",
            (agent_id, limit),
        ).fetchall()
        return [r[0] for r in reversed(rows)]

    def recent_events(self, agent_id: str, limit: int = 20) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT mode,kind,payload_json,created_at FROM events WHERE agent_id=? ORDER BY id DESC LIMIT ?",
            (agent_id, limit),
        ).fetchall()
        return [{"mode":r[0],"kind":r[1],"payload":json.loads(r[2]),"created_at":r[3]} for r in reversed(rows)]

    def event_count(self, agent_id: str) -> int:
        row = self.conn.execute(
            "SELECT COUNT(*) FROM events WHERE agent_id=?",
            (agent_id,),
        ).fetchone()
        return int(row[0])

    def memory_count(self, agent_id: str) -> int:
        row = self.conn.execute(
            "SELECT COUNT(*) FROM memories WHERE agent_id=?",
            (agent_id,),
        ).fetchone()
        return int(row[0])

    def event_trajectory_fingerprint(self, agent_id: str) -> str:
        events = self.conn.execute(
            "SELECT id,mode,kind,payload_json FROM events "
            "WHERE agent_id=? ORDER BY id ASC",
            (agent_id,),
        ).fetchall()
        canonical = json.dumps(
            events,
            ensure_ascii=False,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    def memory_fingerprint(self, agent_id: str) -> str:
        memories = self.conn.execute(
            "SELECT id,importance,content FROM memories "
            "WHERE agent_id=? ORDER BY id ASC",
            (agent_id,),
        ).fetchall()
        canonical = json.dumps(
            memories,
            ensure_ascii=False,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    def trajectory_fingerprint(self, agent_id: str) -> str:
        events = self.conn.execute(
            "SELECT id,mode,kind,payload_json,created_at FROM events "
            "WHERE agent_id=? ORDER BY id ASC",
            (agent_id,),
        ).fetchall()
        memories = self.conn.execute(
            "SELECT id,importance,content,created_at FROM memories "
            "WHERE agent_id=? ORDER BY id ASC",
            (agent_id,),
        ).fetchall()
        payload = {
            "events": events,
            "memories": memories,
        }
        canonical = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    def state_fingerprint(self, agent_id: str) -> str:
        state = self.load_state(agent_id)
        canonical = state.to_json().encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    def recover_memories_from_events(self, agent_id: str) -> int:
        rows = self.conn.execute(
            "SELECT payload_json FROM events WHERE agent_id=? ORDER BY id ASC",
            (agent_id,),
        ).fetchall()

        existing = {
            row[0]
            for row in self.conn.execute(
                "SELECT content FROM memories WHERE agent_id=?",
                (agent_id,),
            ).fetchall()
        }

        recovered = 0
        for (payload_json,) in rows:
            payload = json.loads(payload_json)
            text = " ".join(
                str(payload.get(key, "")) for key in ("response", "summary")
            )
            marker = "MEMORY:"
            if marker not in text:
                continue

            for line in text.splitlines():
                if marker not in line:
                    continue
                memory = line.split(marker, 1)[1].strip()
                if memory and memory not in existing:
                    self.add_memory(agent_id, memory, importance=0.55)
                    existing.add(memory)
                    recovered += 1

        return recovered

    def persistence_observables(self, agent_id: str) -> dict[str, Any]:
        state = self.load_state(agent_id)
        return {
            "event_count": self.event_count(agent_id),
            "memory_count": self.memory_count(agent_id),
            "trajectory_fingerprint": self.trajectory_fingerprint(agent_id),
            "event_trajectory_fingerprint": self.event_trajectory_fingerprint(agent_id),
            "memory_fingerprint": self.memory_fingerprint(agent_id),
            "state_fingerprint": self.state_fingerprint(agent_id),
            "self_model_version": state.self_model_version,
            "self_model": state.self_model,
            "lifetime_wake_cycles": state.lifetime_wake_cycles,
            "lifetime_dream_cycles": state.lifetime_dream_cycles,
            "boot_count": state.boot_count,
            "pending_inputs": self.pending_input_count(agent_id),
            "dynamic_state": state.dynamic_state,
            "dynamic_prev_state": state.dynamic_prev_state,
            "dynamic_memory": state.dynamic_memory,
            "dynamic_pressure": state.dynamic_pressure,
            "dynamic_attractor_distance": state.dynamic_attractor_distance,
            "dynamic_last_input": state.dynamic_last_input,
            "dynamic_steps": state.dynamic_steps,
            "dynamic_snapshot_count": self.dynamic_snapshot_count(agent_id),
            "self_prediction": state.self_prediction,
            "self_prediction_error": state.self_prediction_error,
            "self_prediction_gain": state.self_prediction_gain,
            "self_prediction_confidence": state.self_prediction_confidence,
            "self_prediction_samples": state.self_prediction_samples,
            "self_observer_snapshot_count": self.self_observer_snapshot_count(agent_id),
            "action_conditioned_meta_model_samples": (
                len(
                    (self.load_action_conditioned_meta_observer_model(agent_id) or {})
                    .get("targets", [])
                )
            ),
        }

    def begin_dream(self, agent_id: str, state_before: OntologicalState) -> int:
        cur = self.conn.execute(
            "INSERT INTO dream_cycles(agent_id,started_at,state_before) VALUES(?,?,?)",
            (agent_id, now_iso(), state_before.to_json()),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def end_dream(self, cycle_id: int, state_after: OntologicalState, summary: str) -> None:
        self.conn.execute(
            "UPDATE dream_cycles SET ended_at=?,summary=?,state_after=? WHERE id=?",
            (now_iso(), summary, state_after.to_json(), cycle_id),
        )
        self.conn.commit()

    def snapshot(self, agent_id: str, label: str, state: OntologicalState) -> None:
        self.conn.execute(
            "INSERT INTO snapshots(agent_id,label,state_json,created_at) VALUES(?,?,?,?)",
            (agent_id, label, state.to_json(), now_iso()),
        )
        self.conn.commit()

    def record_dynamic_snapshot(
        self,
        agent_id: str,
        *,
        mode: str,
        label: str,
        step_start: int,
        step_end: int,
        signal: float,
        previous_state: float,
        state: float,
        memory: float,
        pressure: float,
        attractor_distance: float,
    ) -> int:
        cur = self.conn.execute(
            "INSERT INTO dynamic_snapshots("
            "agent_id,mode,label,step_start,step_end,signal,previous_state,state,"
            "memory,pressure,attractor_distance,created_at"
            ") VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                agent_id,
                mode,
                label,
                int(step_start),
                int(step_end),
                float(signal),
                float(previous_state),
                float(state),
                float(memory),
                float(pressure),
                float(attractor_distance),
                now_iso(),
            ),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def dynamic_trajectory(
        self,
        agent_id: str,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        sql = (
            "SELECT id,mode,label,step_start,step_end,signal,previous_state,"
            "state,memory,pressure,attractor_distance,created_at "
            "FROM dynamic_snapshots WHERE agent_id=? ORDER BY step_end ASC"
        )
        params: tuple[Any, ...] = (agent_id,)
        if limit is not None:
            sql = (
                "SELECT * FROM ("
                + sql
                + ") ORDER BY step_end DESC LIMIT ?"
            )
            params = (agent_id, int(limit))

        rows = self.conn.execute(sql, params).fetchall()
        if limit is not None:
            rows = list(reversed(rows))

        keys = [
            "id","mode","label","step_start","step_end","signal",
            "previous_state","state","memory","pressure",
            "attractor_distance","created_at",
        ]
        return [dict(zip(keys, row)) for row in rows]

    def dynamic_snapshot_count(self, agent_id: str) -> int:
        row = self.conn.execute(
            "SELECT COUNT(*) FROM dynamic_snapshots WHERE agent_id=?",
            (agent_id,),
        ).fetchone()
        return int(row[0])


    def record_self_observer_snapshot(
        self,
        agent_id: str,
        *,
        mode: str,
        label: str,
        step_start: int,
        step_end: int,
        features: list[float],
        predicted_state: float,
        baseline_state: float,
        actual_state: float,
        prediction_error: float,
        baseline_error: float,
        gain: float,
        confidence: float,
        samples: int,
    ) -> int:
        cur = self.conn.execute(
            "INSERT INTO self_observer_snapshots("
            "agent_id,mode,label,step_start,step_end,features_json,predicted_state,"
            "baseline_state,actual_state,prediction_error,baseline_error,gain,"
            "confidence,samples,created_at"
            ") VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                agent_id,
                mode,
                label,
                int(step_start),
                int(step_end),
                json.dumps(features, ensure_ascii=False),
                float(predicted_state),
                float(baseline_state),
                float(actual_state),
                float(prediction_error),
                float(baseline_error),
                float(gain),
                float(confidence),
                int(samples),
                now_iso(),
            ),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def self_observer_trajectory(
        self,
        agent_id: str,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        sql = (
            "SELECT id,mode,label,step_start,step_end,features_json,predicted_state,"
            "baseline_state,actual_state,prediction_error,baseline_error,gain,"
            "confidence,samples,created_at "
            "FROM self_observer_snapshots WHERE agent_id=? ORDER BY step_end ASC"
        )
        params: tuple[Any, ...] = (agent_id,)
        if limit is not None:
            sql = (
                "SELECT * FROM ("
                + sql
                + ") ORDER BY step_end DESC LIMIT ?"
            )
            params = (agent_id, int(limit))
        rows = self.conn.execute(sql, params).fetchall()
        if limit is not None:
            rows = list(reversed(rows))
        keys = [
            "id","mode","label","step_start","step_end","features_json",
            "predicted_state","baseline_state","actual_state",
            "prediction_error","baseline_error","gain","confidence",
            "samples","created_at",
        ]
        result = []
        for row in rows:
            item = dict(zip(keys, row))
            item["features"] = json.loads(item.pop("features_json"))
            result.append(item)
        return result

    def self_observer_snapshot_count(self, agent_id: str) -> int:
        row = self.conn.execute(
            "SELECT COUNT(*) FROM self_observer_snapshots WHERE agent_id=?",
            (agent_id,),
        ).fetchone()
        return int(row[0])
