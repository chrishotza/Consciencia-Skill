from __future__ import annotations

import json
import threading
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from src.consciousness_server.client import ConsciousnessClient
from src.consciousness_server.server import ConsciousnessHandler
from src.consciousness_server.synchronization import (
    SynchronizationStatus,
    synchronize_pair,
)


class ServerHarness:
    def __init__(self, db_path):
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), ConsciousnessHandler)
        from src.consciousness_server.core import ConsciousnessStore

        self.httpd.store = ConsciousnessStore(db_path)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    @property
    def url(self):
        return f"http://127.0.0.1:{self.httpd.server_address[1]}"

    def close(self):
        self.httpd.shutdown()
        self.thread.join(timeout=2)
        self.httpd.store.close()


def request_json(url, method="GET", payload=None):
    body = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = Request(url, data=body, headers=headers, method=method)
    with urlopen(req, timeout=3) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def build_instance(url, instance_id, identity="mesh-sync"):
    status, payload = request_json(
        f"{url}/instances",
        "POST",
        {"instance_id": instance_id, "identity": identity},
    )
    assert status == 201
    return payload


def append_event(url, instance_id, event_type, payload, created_at):
    status, result = request_json(
        f"{url}/instances/{instance_id}/events",
        "POST",
        {
            "event_type": event_type,
            "payload": payload,
            "created_at": created_at,
        },
    )
    assert status == 200
    return result


def test_peer_sync_pulls_missing_delta_and_verifies_exact_state(tmp_path):
    local = ServerHarness(tmp_path / "local.db")
    peer = ServerHarness(tmp_path / "peer.db")
    try:
        build_instance(local.url, "ci_sync", "sync-agent")
        build_instance(peer.url, "ci_sync", "sync-agent")

        append_event(
            peer.url,
            "ci_sync",
            "WAKE",
            {"cycle": 1},
            "2026-10-02T05:00:00+00:00",
        )
        append_event(
            peer.url,
            "ci_sync",
            "DYNAMIC_UPDATE",
            {"delta": 0.4},
            "2026-10-02T05:00:01+00:00",
        )

        local_client = ConsciousnessClient(local.url)
        peer_client = ConsciousnessClient(peer.url)

        report = synchronize_pair(
            local_client,
            peer_client,
            instance_id="ci_sync",
        )

        assert report.status is SynchronizationStatus.LOCAL_UPDATED
        assert report.direction == "PEER_TO_LOCAL"
        assert report.applied_event_count == 2

        local_state = local_client.get_instance("ci_sync")
        peer_state = peer_client.get_instance("ci_sync")
        assert local_state["state_hash"] == peer_state["state_hash"]
        assert local_state["state"]["revision"] == peer_state["state"]["revision"]

        again = synchronize_pair(
            local_client,
            peer_client,
            instance_id="ci_sync",
        )
        assert again.status is SynchronizationStatus.ALIGNED
        assert again.applied_event_count == 0
    finally:
        local.close()
        peer.close()


def test_peer_sync_pushes_when_local_is_ahead(tmp_path):
    local = ServerHarness(tmp_path / "local.db")
    peer = ServerHarness(tmp_path / "peer.db")
    try:
        build_instance(local.url, "ci_push", "sync-agent")
        build_instance(peer.url, "ci_push", "sync-agent")

        append_event(
            local.url,
            "ci_push",
            "WAKE",
            {"cycle": 1},
            "2026-10-02T05:10:00+00:00",
        )

        report = synchronize_pair(
            ConsciousnessClient(local.url),
            ConsciousnessClient(peer.url),
            instance_id="ci_push",
        )

        assert report.status is SynchronizationStatus.PEER_UPDATED
        assert report.direction == "LOCAL_TO_PEER"
        assert report.applied_event_count == 1

        local_state = ConsciousnessClient(local.url).get_instance("ci_push")
        peer_state = ConsciousnessClient(peer.url).get_instance("ci_push")
        assert local_state["state_hash"] == peer_state["state_hash"]
    finally:
        local.close()
        peer.close()


def test_peer_sync_blocks_equal_revision_divergence(tmp_path):
    local = ServerHarness(tmp_path / "local.db")
    peer = ServerHarness(tmp_path / "peer.db")
    try:
        build_instance(local.url, "ci_diverge_sync", "sync-agent")
        build_instance(peer.url, "ci_diverge_sync", "sync-agent")

        append_event(
            local.url,
            "ci_diverge_sync",
            "WAKE",
            {"cycle": 1},
            "2026-10-02T05:20:00+00:00",
        )
        append_event(
            peer.url,
            "ci_diverge_sync",
            "DYNAMIC_UPDATE",
            {"delta": 9.0},
            "2026-10-02T05:20:00+00:00",
        )

        report = synchronize_pair(
            ConsciousnessClient(local.url),
            ConsciousnessClient(peer.url),
            instance_id="ci_diverge_sync",
        )

        assert report.status is SynchronizationStatus.DIVERGED
        assert report.direction == "none"
        assert "overwrite" in report.reason
    finally:
        local.close()
        peer.close()
