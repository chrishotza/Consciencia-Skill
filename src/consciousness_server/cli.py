from __future__ import annotations

import argparse
import json

from src.ontto.storage import MemoryStore

from .client import ConsciousnessClient
from .reconciliation import reconcile
from .recovery import plan_recovery


def run_recovery_plan(
    server_url: str,
    instance_id: str,
    local_db: str,
    timeout: float,
) -> None:
    client = ConsciousnessClient(server_url, timeout=timeout)
    remote = client.list_checkpoints(instance_id, limit=1)
    store = MemoryStore(local_db)
    try:
        report = reconcile(
            local_state_fingerprint=store.state_fingerprint(instance_id),
            local_trajectory_fingerprint=store.trajectory_fingerprint(instance_id),
            local_event_count=store.event_count(instance_id),
            local_memory_count=store.memory_count(instance_id),
            checkpoints=remote.get("checkpoints", []),
        )
        plan = plan_recovery(report)
        payload = {
            "reconciliation": report.to_dict(),
            "recovery": plan.to_dict(),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    finally:
        store.conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Consciousness continuity control plane."
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--db", default="data/consciousness.db")

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("serve", help="start the Consciousness Server")

    reconcile_parser = subparsers.add_parser(
        "reconcile",
        help="compare local organism continuity against its latest server checkpoint",
    )
    reconcile_parser.add_argument("--server", required=True)
    reconcile_parser.add_argument("--instance", required=True)
    reconcile_parser.add_argument("--local-db", default="data/ontto.db")
    reconcile_parser.add_argument("--timeout", type=float, default=2.5)

    recovery_parser = subparsers.add_parser(
        "recover",
        help="build a non-destructive continuity recovery plan",
    )
    recovery_parser.add_argument("--server", required=True)
    recovery_parser.add_argument("--instance", required=True)
    recovery_parser.add_argument("--local-db", default="data/ontto.db")
    recovery_parser.add_argument("--timeout", type=float, default=2.5)

    args = parser.parse_args()

    if args.command in (None, "serve"):
        from .server import serve

        serve(host=args.host, port=args.port, db_path=args.db)
    elif args.command == "reconcile":
        from .reconciliation import reconcile
        from .client import ConsciousnessClient
        client = ConsciousnessClient(args.server, timeout=args.timeout)
        remote = client.list_checkpoints(args.instance, limit=1)
        store = MemoryStore(args.local_db)
        try:
            report = reconcile(
                local_state_fingerprint=store.state_fingerprint(args.instance),
                local_trajectory_fingerprint=store.trajectory_fingerprint(args.instance),
                local_event_count=store.event_count(args.instance),
                local_memory_count=store.memory_count(args.instance),
                checkpoints=remote.get("checkpoints", []),
            )
            print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
        finally:
            store.conn.close()
    elif args.command == "recover":
        run_recovery_plan(
            server_url=args.server,
            instance_id=args.instance,
            local_db=args.local_db,
            timeout=args.timeout,
        )


if __name__ == "__main__":
    main()
