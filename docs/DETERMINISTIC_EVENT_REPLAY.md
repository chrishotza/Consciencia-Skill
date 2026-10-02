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