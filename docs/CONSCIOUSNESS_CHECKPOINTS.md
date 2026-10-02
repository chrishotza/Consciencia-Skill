# Consciousness Checkpoints

Consciousness Server checkpoints are the first durable continuity primitive above the event journal.

A checkpoint records a compact observation of the running organism without storing every token or every model output. The local organism remains the operational source of truth; the server keeps a durable control-plane mirror.

## What a checkpoint contains

Each checkpoint stores:

- runtime mode (local or server)
- organism mode (WAKE or SLEEP, as reported by the runtime)
- the server-side state revision observed at checkpoint time
- a server-side state hash
- a compact runtime payload

The current runtime payload includes local state and trajectory fingerprints, cycle/boot counters, dynamic state, memory strength, self-model version, and event/memory counts.

## API

Create: POST /instances/{instance_id}/checkpoints

List: GET /instances/{instance_id}/checkpoints?limit=50

The API is deliberately small so it can later become a replication boundary for NodeZero.

## Design rule

A checkpoint is not a claim of subjective consciousness. It is a durable continuity observation that lets the runtime and future nodes answer practical questions such as:

- which local state was last observed by the server?
- what runtime/organism mode was active?
- did the local trajectory fingerprint change?
- which checkpoint was the latest known state before a node disconnected?

The next infrastructure layer can use these checkpoints for reconciliation and replay without coupling the organism loop to a specific server implementation.
