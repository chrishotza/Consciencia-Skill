---
name: skill-conscious
description: Use Skill-Conscious to add persistent continuity, memory, self-modeling, self-observation, internal dynamics, WAKE/SLEEP cycles, and reproducible experiments to an AI system. Activate when an agent needs to integrate, inspect, operate, or extend a persistent AI organism, or reason from its experimental evidence.
---

# Skill-Conscious

## Purpose

Skill-Conscious is the agent-facing interface for a broader local-first Consciousness Server architecture. Treat it as a modular system, not as a prompt.

The core loop is:

```
input
→ persistent state
→ memory
→ self-model / self-observation
→ trajectory or action selection
→ internal dynamics
→ persistence
→ next cycle
```

The organism also supports WAKE and SLEEP regimes.

## Retrieval discipline

Do not load the whole repository.

Start with:

1. `AI_INDEX.md`
2. `AI_MAP.json`
3. `research/ORGANISM_RESULT_LEDGER.md` for current evidence

Then load only the exact source, experiment, test, protocol, or workflow needed.

Preferred evidence route:

```
ledger → protocol → experiment → test → workflow
```

Preserve null results and explicit limitations.

## Integration modes

### Agent-only

Use this skill when an existing AI system only needs the Skill-Conscious workflow and concepts.

Do not require the full organism runtime.

### Embedded organism

Use the Python package and `PersistentOrganism` when the host application owns the process, storage, and provider lifecycle.

Primary modules:

- `src/ontto/organism.py`
- `src/ontto/storage.py`
- `src/ontto/provider.py`

### Server deployment

Prefer the Consciousness Server when persistence, external inputs, autonomous cycles, multiple clients, or future multi-node continuity must be coordinated centrally.

The server is the continuity control plane. It stores durable identity and event state without requiring the server to execute every model inference.

See:

- `docs/CONSCIOUSNESS_SERVER.md`
- `src/consciousness_server/core.py`
- `src/consciousness_server/server.py`

Keep the Skill-Conscious workflow layer separate from transport/API concerns.

## Architectural rules

- Persistence is part of the organism state, not only chat history.
- Self-observation is computational and testable; do not convert it into a claim of phenomenal consciousness.
- WAKE and SLEEP are functional regimes.
- Experimental claims must point to a protocol and reproducible evidence.
- Do not rewrite historical experiments merely to improve their outcome.

## Current frontier

For V69/V70, distinguish these protocol lines:

- `docs/V69_SELF_STATE_READOUT.md`: numeric state-readout endpoint.
- `docs/V69_SELF_READ_STATE.md`: read-state → trajectory-selection endpoint.
- `docs/V70_SELF_MODEL_ACTION.md`: self-model readout → continuous action.
- `docs/V70_PERSISTENT_SELF_READER.md`: self-reader persistence across restart.

Do not merge their claims.

## When modifying the system

Inspect the smallest relevant set:

1. target implementation;
2. matching test;
3. matching experiment;
4. matching protocol;
5. workflow only when CI behavior matters.

Before finishing, verify persistence, restart behavior, and reproducibility when the change touches organism state.


<details>
<summary>🇪🇸 Español — abrir</summary>

# Skill-Conscious

## Propósito

Skill-Conscious es la interfaz orientada a agentes para una arquitectura más amplia de Consciousness Server local-first. Tratala como un sistema modular, no como un prompt.

El ciclo central es:

```
entrada
→ estado persistente
→ memoria
→ modelo de sí / autoobservación
→ selección de trayectoria o acción
→ dinámica interna
→ persistencia
→ siguiente ciclo
```

El organismo también soporta los regímenes VIGILIA y SUEÑO.

## Disciplina de recuperación

No cargues todo el repositorio.

Empezá por:

1. `AI_INDEX.md`
2. `AI_MAP.json`
3. `research/ORGANISM_RESULT_LEDGER.md` para la evidencia actual

Después cargá solo la fuente, experimento, test, protocolo o workflow exacto que necesites.

Ruta de evidencia preferida:

```
ledger → protocolo → experimento → test → workflow
```

Conservá los resultados nulos y las limitaciones explícitas.

## Modos de integración

### Solo agente

Usá este skill cuando un sistema de IA existente solo necesita el flujo de Skill-Conscious y sus conceptos.

No requiere el runtime completo del organismo.

### Organismo embebido

Usá el paquete Python y `PersistentOrganism` cuando la aplicación anfitriona sea propietaria del proceso, el almacenamiento y el ciclo de vida del proveedor.

Módulos principales:

- `src/ontto/organism.py`
- `src/ontto/storage.py`
- `src/ontto/provider.py`

### Despliegue con servidor

Preferí Consciousness Server cuando haya que coordinar persistencia, entradas externas, ciclos autónomos, múltiples clientes o continuidad futura entre nodos.

El servidor es el plano de control de continuidad. Guarda identidad durable y estado de eventos sin exigir que el servidor ejecute cada inferencia del modelo.

Ver:

- `docs/CONSCIOUSNESS_SERVER.md`
- `src/consciousness_server/core.py`
- `src/consciousness_server/server.py`

Mantené separada la capa de workflow de Skill-Conscious de los transportes y APIs.

## Reglas arquitectónicas

- La persistencia forma parte del estado del organismo, no solo del historial del chat.
- La autoobservación es computacional y verificable; no la conviertas en una afirmación de consciencia fenomenal.
- VIGILIA y SUEÑO son regímenes funcionales.
- Las afirmaciones experimentales deben apuntar a un protocolo y evidencia reproducible.
- No reescribas experimentos históricos solo para mejorar su resultado.

## Frontera actual

Para V69/V70, distinguí estas líneas:

- `docs/V69_SELF_STATE_READOUT.md`: endpoint de lectura numérica del estado.
- `docs/V69_SELF_READ_STATE.md`: lectura del estado → selección de trayectoria.
- `docs/V70_SELF_MODEL_ACTION.md`: lectura del modelo de sí → acción continua.
- `docs/V70_PERSISTENT_SELF_READER.md`: persistencia del self-reader entre reinicios.

No mezcles sus afirmaciones.

## Al modificar el sistema

Inspeccioná el conjunto mínimo relevante:

1. implementación objetivo;
2. test correspondiente;
3. experimento correspondiente;
4. protocolo correspondiente;
5. workflow solo cuando afecte al comportamiento de CI.

Antes de terminar, verificá persistencia, comportamiento tras reinicio y reproducibilidad cuando el cambio toque el estado del organismo.


</details>

> 🌐 Language convention: [docs/LANGUAGE.md](docs/LANGUAGE.md)
