# Continuity Recovery

Recovery is intentionally non-destructive.

The recovery planner consumes the reconciliation report and returns the next safe action:

| Status | Recovery action |
|---|---|
| NO_CHECKPOINT | INITIALIZE_CHECKPOINT |
| ALIGNED | NO_ACTION |
| LOCAL_AHEAD | EXPORT_LOCAL_DELTA |
| LOCAL_BEHIND | REQUEST_REMOTE_REPLAY |
| DIVERGED | BLOCK_DIVERGENCE |

No action automatically overwrites local state or server state.

## CLI

```bash
python -m src.consciousness_server.cli recover ^
  --server http://127.0.0.1:8787 ^
  --instance consciencia-001 ^
  --local-db data/ontto.db
```

The command emits the reconciliation report plus the recovery plan as JSON.

## Boundary

The current server does not yet expose a remote replay protocol. Therefore:

- `EXPORT_LOCAL_DELTA` means prepare the local side for a future transfer;
- `REQUEST_REMOTE_REPLAY` means the node must obtain a remote replay boundary before mutating local state;
- `BLOCK_DIVERGENCE` explicitly prevents silent overwrite;
- `INITIALIZE_CHECKPOINT` means establish a first known continuity boundary.

The next step is a deterministic event identity and replay API.
