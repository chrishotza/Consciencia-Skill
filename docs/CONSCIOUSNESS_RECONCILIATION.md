# Continuity Reconciliation

Reconciliation compares the running local organism against the latest checkpoint observed by the Consciousness Server.

It does not overwrite state. It does not invent missing data. It reports whether the local organism is aligned, ahead, behind, or divergent relative to the last server checkpoint.

## Statuses

- **ALIGNED** — fingerprints and local/remote event-memory counts match.
- **LOCAL_AHEAD** — the local journal has advanced since the checkpoint.
- **LOCAL_BEHIND** — the local journal contains fewer recorded events or memories than the checkpoint.
- **DIVERGED** — counts match but the fingerprints differ.
- **NO_CHECKPOINT** — the server has no checkpoint for this instance yet.

A local-ahead result is expected during normal operation between checkpoints. It becomes actionable when a node reconnects after a long interruption.

## Runtime behavior

SERVER mode performs reconciliation during startup after instance/node registration and emits a `RECONCILE` control-plane event.

LOCAL mode does not contact the server.

## Manual diagnostic

```bash
python -m src.consciousness_server.cli reconcile \
  --server http://127.0.0.1:8787 \
  --instance consciencia-001 \
  --local-db data/ontto.db
```

The command emits a JSON report suitable for logs, automation, and future NodeZero reconciliation.

## Why this matters

The checkpoint protocol answers **what was last observed**.

Reconciliation answers **whether the local organism still matches that observation**.

The next layer is replay/recovery: using a durable event boundary to determine exactly what must be re-applied or transferred when a node reconnects.
