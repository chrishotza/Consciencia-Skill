from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .core import ConsciousnessStore


def _json_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False).encode("utf-8")


class ConsciousnessHandler(BaseHTTPRequestHandler):
    server_version = "ConsciousnessServer/0.1"

    @property
    def store(self) -> ConsciousnessStore:
        return self.server.store  # type: ignore[attr-defined]

    def _send(self, status: int, payload: object) -> None:
        body = _json_bytes(payload)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:
        path = urlparse(self.path)
        if path.path == "/health":
            self._send(
                200,
                {
                    "status": "ok",
                    "service": "consciousness-server",
                    "mode": "local-first",
                },
            )
            return

        if path.path == "/nodes":
            self._send(200, {"nodes": self.store.list_nodes()})
            return

        if path.path.startswith("/instances/"):
            parts = [p for p in path.path.split("/") if p]
            if len(parts) >= 2:
                state = self.store.get_state(parts[1])
                if state is None:
                    self._send(404, {"error": "instance_not_found"})
                    return
                payload = {
                    "state": state.to_dict(),
                    "state_hash": self.store.state_hash(parts[1]),
                }
                if len(parts) == 3:
                    query = parse_qs(path.query)
                    limit = int(query.get("limit", ["100"])[0])
                    if parts[2] == "events":
                        payload["events"] = self.store.list_events(
                            parts[1],
                            limit=limit,
                        )
                    elif parts[2] == "checkpoints":
                        payload["checkpoints"] = self.store.list_checkpoints(
                            parts[1],
                            limit=limit,
                        )
                self._send(200, payload)
                return

        self._send(404, {"error": "not_found"})

    def do_POST(self) -> None:
        path = urlparse(self.path)

        try:
            data = self._read_json()
        except json.JSONDecodeError:
            self._send(400, {"error": "invalid_json"})
            return

        if path.path == "/instances":
            identity = str(data.get("identity", "")).strip()
            if not identity:
                self._send(400, {"error": "identity_required"})
                return
            state = self.store.create_instance(
                identity=identity,
                instance_id=data.get("instance_id"),
            )
            self._send(
                201,
                {
                    "state": state.to_dict(),
                    "state_hash": self.store.state_hash(state.instance_id),
                },
            )
            return

        if path.path == "/nodes/register":
            node_id = str(data.get("node_id", "")).strip()
            if not node_id:
                self._send(400, {"error": "node_id_required"})
                return
            node = self.store.register_node(
                node_id=node_id,
                endpoint=data.get("endpoint"),
                capabilities=list(data.get("capabilities", [])),
            )
            self._send(200, node)
            return

        if path.path.startswith("/instances/") and path.path.endswith("/events"):
            parts = [p for p in path.path.split("/") if p]
            if len(parts) != 3:
                self._send(404, {"error": "not_found"})
                return
            try:
                state = self.store.append_event(
                    instance_id=parts[1],
                    event_type=str(data.get("event_type", "OBSERVE")),
                    payload=dict(data.get("payload", {})),
                )
            except KeyError:
                self._send(404, {"error": "instance_not_found"})
                return
            self._send(
                200,
                {
                    "state": state.to_dict(),
                    "state_hash": self.store.state_hash(state.instance_id),
                },
            )
            return

        if path.path.startswith("/instances/") and path.path.endswith("/checkpoints"):
            parts = [p for p in path.path.split("/") if p]
            if len(parts) != 3:
                self._send(404, {"error": "not_found"})
                return
            try:
                checkpoint = self.store.create_checkpoint(
                    instance_id=parts[1],
                    runtime_mode=str(data.get("runtime_mode", "local")),
                    organism_mode=str(data.get("organism_mode", "WAKE")),
                    payload=dict(data.get("payload", {})),
                    checkpoint_id=data.get("checkpoint_id"),
                )
                state = self.store.get_state(parts[1])
            except KeyError:
                self._send(404, {"error": "instance_not_found"})
                return
            except Exception as exc:
                if "UNIQUE constraint failed" in str(exc):
                    self._send(409, {"error": "checkpoint_id_exists"})
                    return
                raise
            self._send(
                201,
                {
                    "checkpoint": checkpoint,
                    "state": state.to_dict() if state is not None else None,
                    "state_hash": self.store.state_hash(parts[1]),
                },
            )
            return

        self._send(404, {"error": "not_found"})

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"[consciousness-server] {fmt % args}")


def serve(
    host: str = "127.0.0.1",
    port: int = 8787,
    db_path: str = "data/consciousness.db",
) -> None:
    httpd = ThreadingHTTPServer((host, port), ConsciousnessHandler)
    httpd.store = ConsciousnessStore(db_path)  # type: ignore[attr-defined]
    print(f"Consciousness Server listening on http://{host}:{port}")
    print(f"Continuity store: {db_path}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Consciousness Server...")
    finally:
        httpd.store.close()  # type: ignore[attr-defined]
        httpd.server_close()
