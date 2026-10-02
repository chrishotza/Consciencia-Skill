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


<details>
<summary>🇪🇸 Español — abrir</summary>

# Checkpoints de Consciousness

Los checkpoints del Consciousness Server son la primera primitiva de continuidad durable por encima del diario de eventos.

## Qué contiene un checkpoint

Cada checkpoint registra:

- modo de runtime (local o server);
- modo del organismo (WAKE o SLEEP, según el runtime);
- revisión del estado del servidor observada en el momento del checkpoint;
- hash de estado del servidor;
- payload compacto del runtime.

El payload actual incluye fingerprint de estado local y trayectoria, contadores de ciclo/boot, estado dinámico, fuerza de memoria, versión del modelo de sí y cantidades de eventos/memorias.

## API

Crear: `POST /instances/{instance_id}/checkpoints`

Listar: `GET /instances/{instance_id}/checkpoints?limit=50`

La API es deliberadamente pequeña para poder convertirse más adelante en un límite de replicación para NodeZero.

## Regla de diseño

Un checkpoint no es una afirmación de consciencia subjetiva. Es una observación durable de continuidad que permite responder preguntas prácticas como:

- ¿qué estado local fue observado por última vez por el servidor?
- ¿qué modo de runtime/organismo estaba activo?
- ¿cambió el fingerprint de trayectoria local?
- ¿cuál era el último checkpoint conocido antes de que un nodo se desconectara?

La siguiente capa puede usar estos checkpoints para reconciliación y replay sin acoplar el ciclo del organismo a una implementación concreta de servidor.


</details>

> 🌐 Language convention: [docs/LANGUAGE.md](LANGUAGE.md)
