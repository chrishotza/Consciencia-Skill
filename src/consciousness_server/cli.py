from __future__ import annotations

import argparse

from .server import serve


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Consciousness Server — local-first continuity runtime."
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--db", default="data/consciousness.db")
    args = parser.parse_args()
    serve(host=args.host, port=args.port, db_path=args.db)


if __name__ == "__main__":
    main()
