# Deterministic Event Replay

Phase 4 turns the Consciousness Server event journal into a transferable continuity stream.

## Event identity

Every event has:

- event_id — SHA-256 identity derived from instance, event type, canonical payload, logical revision, and parent event;
- logical_revision — deterministic continuity position;
- parent_event_id — the previous event in the instance chain;
- created_at — preserved during replay so the resulting state fingerprint can remain identical.

The event identity intentionally excludes wall-clock creation time. Two nodes replaying the same event at the same logical position therefore derive the same identity.

## Delta export

```http
GET /instances/{instance_id}/events/delta?after_revision=1&limit=1000
```

The response contains an ordered event delta. The caller can persist it as a transfer artifact before applying it to another node.

Client helper:

```python
client.export_delta(instance_id, after_revision=checkpoint_revision)
```

## Replay

```http
POST /instances/{instance_id}/replay
Content-Type: application/json
```

Payload:

```json
{
  "base_revision": 1,
  "base_state_hash": "<checkpoint-state-hash>",
  "events": [
    {
      "event_id": "<sha256>",
      "event_type": "WAKE",
      "payload": {"cycle": 1},
      "logical_revision": 2,
      "parent_event_id": null,
      "created_at": "2026-10-02T03:00:00+00:00"
    }
  ]
}
```

Replay is accepted only when the receiving node matches the declared base revision and, when supplied, the base state hash. Every event must extend the current parent chain exactly.

## Safety properties

A replay request is rejected on:

- base revision mismatch;
- base state hash mismatch;
- logical revision gaps;
- parent-chain mismatch;
- event identity collision with different content.

An exact retransmission of an already-applied event delta is idempotent.

The server never overwrites a divergent local branch automatically.

## Scope

This phase transfers control-plane continuity events. It does not yet replace the organism's SQLite MemoryStore or claim that event replay alone recreates every internal cognitive artifact.

The next layer is to connect verified replay boundaries with portable organism bundles and a server-backed persistence abstraction.

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Replay determinista de eventos

La Fase 4 convierte el diario de eventos del Consciousness Server en un flujo de continuidad transferible.

## Identidad del evento

Cada evento tiene:

- `event_id` — identidad SHA-256 derivada de instancia, tipo de evento, payload canónico, revisión lógica y evento padre;
- `logical_revision` — posición determinista dentro de la continuidad;
- `parent_event_id` — evento anterior de la cadena de instancia;
- `created_at` — preservado durante el replay para que el fingerprint resultante pueda permanecer idéntico.

La identidad excluye deliberadamente la hora de reloj. Dos nodos que reproduzcan el mismo evento en la misma posición lógica derivan la misma identidad.

## Exportación de deltas

```http
GET /instances/{instance_id}/events/delta?after_revision=1&limit=1000
```

La respuesta contiene un delta de eventos ordenado. El receptor puede persistirlo como artifact de transferencia antes de aplicarlo a otro nodo.

Helper del cliente:

```python
client.export_delta(instance_id, after_revision=checkpoint_revision)
```

## Replay

```http
POST /instances/{instance_id}/replay
Content-Type: application/json
```

El payload declara la revisión base, opcionalmente su hash de estado, y una lista ordenada de eventos.

El replay solo se acepta cuando el nodo receptor coincide con la revisión base declarada y, si se proporciona, con el hash de estado base. Cada evento debe extender exactamente la cadena padre actual.

## Propiedades de seguridad

Una petición de replay se rechaza por:

- mismatch de revisión base;
- mismatch de hash de estado base;
- saltos en la revisión lógica;
- mismatch de cadena padre;
- colisión de identidad de evento con contenido diferente.

Una retransmisión exacta de un delta ya aplicado es idempotente.

El servidor nunca sobrescribe automáticamente una rama local divergente.

## Alcance

Esta fase transfiere eventos de continuidad del plano de control. Todavía no sustituye el MemoryStore SQLite del organismo ni afirma que el replay de eventos por sí solo reconstruya todos los artifacts cognitivos internos.

La siguiente capa conecta los límites verificados de replay con bundles portables del organismo y con el backend de persistencia espejado por servidor.


</details>

> 🌐 Language convention: [docs/LANGUAGE.md](LANGUAGE.md)
