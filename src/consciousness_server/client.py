from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any


class ConsciousnessClient:
    """Small fail-open client for the local Consciousness Server."""

    def __init__(self, base_url: str, timeout: float = 2.5):
        self.base_url = base_url.rstrip("/")
        self.timeout = float(timeout)

    def _request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        body = None
        headers = {"Accept": "application/json"}
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = urllib.request.Request(
            f"{self.base_url}{path}",
            data=body,
            headers=headers,
            method=method,
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}

    def health(self) -> dict[str, Any]:
        return self._request("GET", "/health")

    def get_instance(self, instance_id: str) -> dict[str, Any]:
        return self._request("GET", f"/instances/{instance_id}")

    def ensure_instance(self, instance_id: str, identity: str) -> dict[str, Any]:
        try:
            return self.get_instance(instance_id)
        except urllib.error.HTTPError as exc:
            if exc.code != 404:
                raise
        return self._request(
            "POST",
            "/instances",
            {"instance_id": instance_id, "identity": identity},
        )

    def register_node(
        self,
        node_id: str,
        endpoint: str | None = None,
        capabilities: list[str] | None = None,
    ) -> dict[str, Any]:
        return self._request(
            "POST",
            "/nodes/register",
            {
                "node_id": node_id,
                "endpoint": endpoint,
                "capabilities": capabilities or [],
            },
        )

    def get_node(self, node_id: str) -> dict[str, Any]:
        return self._request("GET", f"/nodes/{node_id}")

    def list_nodes(self, stale_after_seconds: float = 30.0) -> dict[str, Any]:
        return self._request(
            "GET",
            f"/nodes?stale_after_seconds={float(stale_after_seconds)}",
        )

    def heartbeat(
        self,
        node_id: str,
        endpoint: str | None = None,
        capabilities: list[str] | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {}
        if endpoint is not None:
            body["endpoint"] = endpoint
        if capabilities is not None:
            body["capabilities"] = list(capabilities)
        return self._request(
            "POST",
            f"/nodes/{node_id}/heartbeat",
            body,
        )

    def emit(
        self,
        instance_id: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/instances/{instance_id}/events",
            {
                "event_type": event_type,
                "payload": payload or {},
            },
        )

    @staticmethod
    def deterministic_event_id(
        instance_id: str,
        event_type: str,
        payload: dict[str, Any],
        logical_revision: int,
        parent_event_id: str | None,
    ) -> str:
        from .core import ConsciousnessStore

        return ConsciousnessStore.deterministic_event_id(
            instance_id,
            event_type,
            payload,
            logical_revision,
            parent_event_id,
        )

    def emit(
        self,
        instance_id: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
        *,
        expected_revision: int | None = None,
        event_id: str | None = None,
        logical_revision: int | None = None,
        parent_event_id: str | None = None,
        created_at: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "event_type": event_type,
            "payload": payload or {},
        }
        if expected_revision is not None:
            body["expected_revision"] = int(expected_revision)
        if event_id:
            body["event_id"] = event_id
        if logical_revision is not None:
            body["logical_revision"] = int(logical_revision)
        if parent_event_id is not None:
            body["parent_event_id"] = parent_event_id
        if created_at is not None:
            body["created_at"] = created_at
        return self._request(
            "POST",
            f"/instances/{instance_id}/events",
            body,
        )

    def list_events(
        self,
        instance_id: str,
        limit: int = 100,
    ) -> dict[str, Any]:
        return self._request(
            "GET",
            f"/instances/{instance_id}/events?limit={max(1, min(int(limit), 1000))}",
        )

    def export_delta(
        self,
        instance_id: str,
        after_revision: int,
        limit: int = 1000,
    ) -> dict[str, Any]:
        return self._request(
            "GET",
            f"/instances/{instance_id}/events/delta?after_revision={int(after_revision)}&limit={max(1, min(int(limit), 1000))}",
        )

    def replay_delta(
        self,
        instance_id: str,
        *,
        base_revision: int,
        events: list[dict[str, Any]],
        base_state_hash: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "base_revision": int(base_revision),
            "events": events,
        }
        if base_state_hash is not None:
            body["base_state_hash"] = base_state_hash
        return self._request(
            "POST",
            f"/instances/{instance_id}/replay",
            body,
        )

    def checkpoint(
        self,
        instance_id: str,
        runtime_mode: str,
        organism_mode: str,
        payload: dict[str, Any] | None = None,
        checkpoint_id: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "runtime_mode": runtime_mode,
            "organism_mode": organism_mode,
            "payload": payload or {},
        }
        if checkpoint_id:
            body["checkpoint_id"] = checkpoint_id
        return self._request(
            "POST",
            f"/instances/{instance_id}/checkpoints",
            body,
        )

    def list_checkpoints(
        self,
        instance_id: str,
        limit: int = 50,
    ) -> dict[str, Any]:
        return self._request(
            "GET",
            f"/instances/{instance_id}/checkpoints?limit={max(1, min(int(limit), 1000))}",
        )

    def latest_checkpoint(self, instance_id: str) -> dict[str, Any] | None:
        payload = self.list_checkpoints(instance_id, limit=1)
        checkpoints = payload.get("checkpoints", [])
        return checkpoints[-1] if checkpoints else None
