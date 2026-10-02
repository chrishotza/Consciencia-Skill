from __future__ import annotations

import json
import threading
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from src.consciousness_server.server import ConsciousnessHandler


class ServerHarness:
    def __init__(self, db_path):
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), ConsciousnessHandler)
        from src.consciousness_server.core import ConsciousnessStore

        self.httpd.store = ConsciousnessStore(db_path)
        self.thread = threading.Thread(
            target=self.httpd.serve_forever,
            daemon=True,
        )
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


def test_second_node_replays_verified_delta_exactly(tmp_path):
    node_a = ServerHarness(tmp_path / "node_a.db")
    node_b = ServerHarness(tmp_path / "node_b.db")

    try:
        identity = "node-zero-probe"
        status_a, created = request_json(
            f"{node_a.url}/instances",
            "POST",
            {"instance_id": "ci_mesh_probe", "identity": identity},
        )
        assert status_a == 201

        status_b, created_b = request_json(
            f"{node_b.url}/instances",
            "POST",
            {"instance_id": "ci_mesh_probe", "identity": identity},
        )
        assert status_b == 201
        assert created["state_hash"] == created_b["state_hash"]

        request_json(
            f"{node_a.url}/instances/ci_mesh_probe/events",
            "POST",
            {"event_type": "WAKE", "payload": {"cycle": 1}, "created_at": "2026-10-02T04:00:00+00:00"},
        )
        request_json(
            f"{node_a.url}/instances/ci_mesh_probe/events",
            "POST",
            {"event_type": "DYNAMIC_UPDATE", "payload": {"delta": 0.75}, "created_at": "2026-10-02T04:00:01+00:00"},
        )

        _, source = request_json(
            f"{node_a.url}/instances/ci_mesh_probe/events/delta?after_revision=1"
        )

        status_replay, replay = request_json(
            f"{node_b.url}/instances/ci_mesh_probe/replay",
            "POST",
            {
                "base_revision": 1,
                "base_state_hash": created_b["state_hash"],
                "events": source["events"],
            },
        )
        assert status_replay == 200
        assert replay["replayed_event_count"] == 2

        _, state_a = request_json(f"{node_a.url}/instances/ci_mesh_probe")
        _, state_b = request_json(f"{node_b.url}/instances/ci_mesh_probe")
        assert state_b["state_hash"] == state_a["state_hash"]

        _, events_a = request_json(f"{node_a.url}/instances/ci_mesh_probe/events")
        _, events_b = request_json(f"{node_b.url}/instances/ci_mesh_probe/events")
        assert events_b["events"] == events_a["events"]
    finally:
        node_a.close()
        node_b.close()


def test_second_node_blocks_divergent_replay(tmp_path):
    node_a = ServerHarness(tmp_path / "node_a.db")
    node_b = ServerHarness(tmp_path / "node_b.db")

    try:
        for node in (node_a, node_b):
            request_json(
                f"{node.url}/instances",
                "POST",
                {"instance_id": "ci_mesh_diverge", "identity": "mesh-diverge"},
            )

        request_json(
            f"{node_a.url}/instances/ci_mesh_diverge/events",
            "POST",
            {"event_type": "WAKE", "payload": {"cycle": 1}, "created_at": "2026-10-02T04:10:00+00:00"},
        )
        _, source = request_json(
            f"{node_a.url}/instances/ci_mesh_diverge/events/delta?after_revision=1"
        )

        request_json(
            f"{node_b.url}/instances/ci_mesh_diverge/events",
            "POST",
            {"event_type": "DYNAMIC_UPDATE", "payload": {"delta": 9.0}, "created_at": "2026-10-02T04:10:01+00:00"},
        )

        _, state_b = request_json(f"{node_b.url}/instances/ci_mesh_diverge")
        try:
            request_json(
                f"{node_b.url}/instances/ci_mesh_diverge/replay",
                "POST",
                {
                    "base_revision": 1,
                    "base_state_hash": state_b["state_hash"],
                    "events": source["events"],
                },
            )
        except HTTPError as exc:
            assert exc.code == 409
            return
        raise AssertionError("divergent replay was unexpectedly accepted")
    finally:
        node_a.close()
        node_b.close()
