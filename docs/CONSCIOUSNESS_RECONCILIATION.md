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

The next layer is peer synchronization: using the durable event boundary to transfer only the missing deterministic delta, while blocking equal-revision divergence and verifying the post-replay boundary.


<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Reconciliación de continuidad

La reconciliación compara el organismo local en ejecución con el último checkpoint observado por Consciousness Server.
No sobrescribe estado ni inventa datos faltantes. Informa si el organismo está alineado, adelantado, atrasado o divergente respecto del último checkpoint.

## Estados
- ALIGNED — fingerprints y conteos local/remoto coinciden.
- LOCAL_AHEAD — el journal local avanzó desde el checkpoint.
- LOCAL_BEHIND — el journal local contiene menos eventos o memorias registradas que el checkpoint.
- DIVERGED — los conteos coinciden pero los fingerprints difieren.
- NO_CHECKPOINT — todavía no existe checkpoint para esa instancia.

LOCAL_AHEAD es normal entre checkpoints y se vuelve accionable cuando un nodo se reconecta después de una interrupción prolongada.

## Runtime
SERVER reconcilia durante el arranque después del registro de instancia/nodo y emite un evento RECONCILE. LOCAL no contacta al servidor.

## Diagnóstico
```bash
python -m src.consciousness_server.cli reconcile \
  --server http://127.0.0.1:8787 \
  --instance consciencia-001 \
  --local-db data/ontto.db
```

El comando emite un reporte JSON adecuado para logs, automatización y futura reconciliación NodeZero.

## Por qué importa
El protocolo de checkpoints responde qué fue observado por última vez. La reconciliación responde si el organismo local todavía coincide con esa observación.

</details>


