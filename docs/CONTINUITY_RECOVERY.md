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

The server now exposes a deterministic replay boundary through:

- `GET /instances/{instance_id}/events/delta?after_revision=N`;
- `POST /instances/{instance_id}/replay`.

`EXPORT_LOCAL_DELTA` can now produce a transferable event delta. `REQUEST_REMOTE_REPLAY` can use the verified replay endpoint once the local node is anchored to the declared base checkpoint. `BLOCK_DIVERGENCE` still prevents silent overwrite when the base revision, state hash, or parent event chain does not match.

The replay protocol is documented in [Deterministic event replay](DETERMINISTIC_EVENT_REPLAY.md).


<details>
<summary>🇪🇸 Español — abrir</summary>

# Recuperación de continuidad

La recuperación es deliberadamente no destructiva.

El planificador de recuperación consume el reporte de reconciliación y devuelve la siguiente acción segura:

| Estado | Acción |
|---|---|
| NO_CHECKPOINT | INITIALIZE_CHECKPOINT |
| ALIGNED | NO_ACTION |
| LOCAL_AHEAD | EXPORT_LOCAL_DELTA |
| LOCAL_BEHIND | REQUEST_REMOTE_REPLAY |
| DIVERGED | BLOCK_DIVERGENCE |

Ninguna acción sobrescribe automáticamente el estado local o del servidor.

## CLI

```bash
python -m src.consciousness_server.cli recover ^
  --server http://127.0.0.1:8787 ^
  --instance consciencia-001 ^
  --local-db data/ontto.db
```

El comando emite el reporte de reconciliación y el plan de recuperación como JSON.

## Límite

El servidor expone ahora un límite determinista de replay mediante:

- `GET /instances/{instance_id}/events/delta?after_revision=N`;
- `POST /instances/{instance_id}/replay`.

`EXPORT_LOCAL_DELTA` puede producir un delta transferible. `REQUEST_REMOTE_REPLAY` puede utilizar el endpoint de replay verificado cuando el nodo local está anclado al checkpoint base declarado. `BLOCK_DIVERGENCE` continúa evitando sobrescritura silenciosa cuando no coincide la revisión base, el hash o la cadena padre.


</details>

> 🌐 Language convention: [docs/LANGUAGE.md](LANGUAGE.md)
