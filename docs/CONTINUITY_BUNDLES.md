# Continuity Bundles

Continuity Bundles are portable backups of a persistent organism.

A bundle contains:

- `organism.sqlite3` — a SQLite backup of the organism persistence store;
- `manifest.json` — bundle version, organism identity, persistence observables, and a SHA-256 hash of the database.

The bundle is designed for:

- backup before experiments;
- migration to another machine;
- manual recovery after a node failure;
- provenance of a concrete organism state;
- future transfer between local nodes.

## Create

```bash
consciousness-bundle create ^
  --db data/ontto.db ^
  --agent consciencia-001 ^
  --out bundles/consciencia-001-01
```

On PowerShell or a shell that does not use `^` for line continuation, place the command on one line.

## Verify

```bash
consciousness-bundle verify ^
  --bundle bundles/consciencia-001-01
```

Verification compares the SHA-256 hash stored in the manifest with the current bundle database.

## Restore

```bash
consciousness-bundle restore ^
  --bundle bundles/consciencia-001-01 ^
  --db data/ontto-restored.db
```

Restore refuses to overwrite an existing database unless `--overwrite` is supplied.

## Design boundary

A bundle is a **local continuity artifact**. It is not a server replica and it does not by itself merge two divergent organism trajectories.

That separation is intentional:

`bundle` = portable state

`checkpoint` = server-observed state

`reconciliation` = comparison

`replay/recovery` = future transfer/merge protocol

The next distributed layer can use bundle manifests and checkpoint hashes to verify that a recovered database corresponds to a known continuity point before replaying or exchanging events.
