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
