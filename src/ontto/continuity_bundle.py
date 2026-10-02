from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .storage import MemoryStore

BUNDLE_VERSION = "1.0"
DATABASE_FILENAME = "organism.sqlite3"
MANIFEST_FILENAME = "manifest.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def create_bundle(
    *,
    db_path: str | Path,
    agent_id: str,
    out_dir: str | Path,
    overwrite: bool = False,
) -> dict[str, Any]:
    source = Path(db_path)
    out = Path(out_dir)

    if not source.exists():
        raise FileNotFoundError(f"database not found: {source}")
    if out.exists():
        if not overwrite:
            raise FileExistsError(
                f"bundle directory already exists: {out}; use --overwrite"
            )
        shutil.rmtree(out)

    out.mkdir(parents=True, exist_ok=True)
    database = out / DATABASE_FILENAME

    source_store = MemoryStore(source)
    try:
        observables = source_store.persistence_observables(agent_id)
        source_conn = source_store.conn
        target_conn = sqlite3.connect(database)
        try:
            source_conn.backup(target_conn)
        finally:
            target_conn.close()
    finally:
        source_store.conn.close()

    manifest = {
        "bundle_version": BUNDLE_VERSION,
        "created_at": now_iso(),
        "agent_id": agent_id,
        "database_filename": DATABASE_FILENAME,
        "database_sha256": sha256_file(database),
        "observables": observables,
    }

    (out / MANIFEST_FILENAME).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def verify_bundle(bundle_dir: str | Path) -> dict[str, Any]:
    bundle = Path(bundle_dir)
    manifest_path = bundle / MANIFEST_FILENAME
    database = bundle / DATABASE_FILENAME

    if not manifest_path.exists():
        raise FileNotFoundError(f"missing manifest: {manifest_path}")
    if not database.exists():
        raise FileNotFoundError(f"missing database: {database}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = str(manifest.get("database_sha256", ""))
    actual = sha256_file(database)

    result = {
        "valid": bool(expected) and expected == actual,
        "bundle_version": manifest.get("bundle_version"),
        "agent_id": manifest.get("agent_id"),
        "database": str(database),
        "expected_sha256": expected,
        "actual_sha256": actual,
        "observables": manifest.get("observables", {}),
    }
    return result


def restore_bundle(
    *,
    bundle_dir: str | Path,
    target_db: str | Path,
    overwrite: bool = False,
) -> dict[str, Any]:
    verification = verify_bundle(bundle_dir)
    if not verification["valid"]:
        raise ValueError(
            "bundle verification failed: database hash does not match manifest"
        )

    target = Path(target_db)
    if target.exists() and not overwrite:
        raise FileExistsError(
            f"target database already exists: {target}; use --overwrite"
        )

    target.parent.mkdir(parents=True, exist_ok=True)
    source = Path(bundle_dir) / DATABASE_FILENAME
    shutil.copy2(source, target)

    restored_sha256 = sha256_file(target)
    if restored_sha256 != verification["actual_sha256"]:
        raise IOError("restored database hash mismatch")

    verification["restored_to"] = str(target)
    return verification


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Portable continuity bundles for persistent AI organisms."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser(
        "create",
        help="create a portable organism bundle",
    )
    create.add_argument("--db", required=True)
    create.add_argument("--agent", required=True)
    create.add_argument("--out", required=True)
    create.add_argument("--overwrite", action="store_true")

    verify = subparsers.add_parser(
        "verify",
        help="verify bundle integrity",
    )
    verify.add_argument("--bundle", required=True)

    restore = subparsers.add_parser(
        "restore",
        help="restore a verified bundle to a database path",
    )
    restore.add_argument("--bundle", required=True)
    restore.add_argument("--db", required=True)
    restore.add_argument("--overwrite", action="store_true")

    args = parser.parse_args()

    if args.command == "create":
        result = create_bundle(
            db_path=args.db,
            agent_id=args.agent,
            out_dir=args.out,
            overwrite=args.overwrite,
        )
    elif args.command == "verify":
        result = verify_bundle(args.bundle)
    else:
        result = restore_bundle(
            bundle_dir=args.bundle,
            target_db=args.db,
            overwrite=args.overwrite,
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
