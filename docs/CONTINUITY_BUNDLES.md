# Continuity Bundles

A Continuity Bundle is a portable backup of one persistent organism.

It contains:

- `organism.sqlite3` — SQLite persistence for the organism;
- `manifest.json` — identity, persistence observables and SHA-256 integrity hash.

The bundle is useful for backup, migration, recovery and provenance.

## Workflow

`checkpoint → bundle → disconnect/migrate → verify → restore → reconcile`

A bundle is a portable local artifact. It is not a server replica and it is not a merge of divergent trajectories.

## Create

```bash
consciousness-bundle create --db data/ontto.db --agent consciencia-001 --out bundles/consciencia-001
```

## Verify

```bash
consciousness-bundle verify --bundle bundles/consciencia-001
```

## Restore

```bash
consciousness-bundle restore --bundle bundles/consciencia-001 --db data/ontto-restored.db
```

Restore refuses to overwrite an existing database unless `--overwrite` is supplied.

The bundle deliberately stops before replay/merge. Reconciliation remains the gate that decides whether a restored organism is aligned, ahead, behind or divergent.
