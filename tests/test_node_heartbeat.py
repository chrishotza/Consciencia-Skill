from __future__ import annotations

import json
import threading
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen

from src.consciousness_server.server import ConsciousnessHandler


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


def test_node_heartbeat_recovers_stale_node(tmp_path):
    node = ServerHarness(tmp_path / "heartbeat.db")
    try:
        status, registered = request_json(
            f"{node.url}/nodes/register",
            "POST",
            {
                "node_id": "node-heartbeat-01",
                "endpoint": "http://127.0.0.1:9101",
                "capabilities": ["continuity", "replay"],
            },
        )
        assert status == 200
        assert registered["status"] == "ONLINE"

        status, listed = request_json(
            f"{node.url}/nodes?stale_after_seconds=0",
        )
        assert status == 200
        assert listed["nodes"][0]["status"] == "STALE"

        status, heartbeat = request_json(
            f"{node.url}/nodes/node-heartbeat-01/heartbeat",
            "POST",
            {"endpoint": "http://127.0.0.1:9101"},
        )
        assert status == 200
        assert heartbeat["status"] == "ONLINE"

        status, fetched = request_json(
            f"{node.url}/nodes/node-heartbeat-01",
        )
        assert status == 200
        assert fetched["status"] == "ONLINE"
        assert fetched["capabilities"] == ["continuity", "replay"]
        assert fetched["last_seen_at"] == heartbeat["last_seen_at"]
    finally:
        node.close()


def test_unknown_node_heartbeat_registers_it(tmp_path):
    node = ServerHarness(tmp_path / "heartbeat_bootstrap.db")
    try:
        status, heartbeat = request_json(
            f"{node.url}/nodes/node-bootstrap/heartbeat",
            "POST",
            {
                "endpoint": "http://127.0.0.1:9102",
                "capabilities": ["mesh"],
            },
        )
        assert status == 200
        assert heartbeat["node_id"] == "node-bootstrap"
        assert heartbeat["status"] == "ONLINE"

        status, listed = request_json(f"{node.url}/nodes")
        assert status == 200
        assert listed["nodes"] == [heartbeat]
    finally:
        node.close()
