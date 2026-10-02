# Shared Persistence Backend

Phase 5 introduces a persistence boundary between the organism loop and the concrete storage implementation.

## Current implementation

`PersistenceBackend` is the contract consumed by `PersistentOrganism` for continuity-critical persistence operations.

`MemoryStore` remains the local SQLite implementation and therefore remains the execution source of truth for the organism's cognitive artifacts.

`ServerMirroredPersistenceBackend` extends the local SQLite store and mirrors continuity-critical mutations to the Consciousness Server:

- persisted ontological state → `STATE_SNAPSHOT`;
- new memory → `MEMORY_UPDATE`;
- organism event → `ORGANISM_EVENT`.

The local transaction commits first. Mirror publication is fail-open: a temporary server failure does not stop or roll back the organism's local cognitive loop.

## Runtime selection

`run_daemon.py` now selects the backend from `CONSCIOUSNESS_MODE`:

- `local` → `MemoryStore`;
- `server` → `ServerMirroredPersistenceBackend` with the active `ConsciousnessClient`.

This keeps the organism loop independent of the concrete backend while preserving the local-first safety model.

## Boundary

This is the first persistence abstraction, not yet a full remote replacement for every SQLite table. Cognitive models, snapshots, dream records, and input queues remain local until their transfer semantics are separately specified and tested.

The next infrastructure step is to make portable bundles and deterministic replay consume the same persistence boundary, followed by a second-node interoperability test.