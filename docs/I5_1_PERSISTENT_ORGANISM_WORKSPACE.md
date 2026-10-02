# I5.1 — PersistentOrganism Workspace Integration

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.1 lleva el workspace de I5.0 desde un prototipo aislado hacia el **runtime real de PersistentOrganism**.

La integración es opt-in y no altera el comportamiento histórico cuando `workspace_enabled=False`.

## Qué se integra

El organismo expone seis fuentes internas como módulos especializados:

1. dinámica actual/anterior;
2. autopredicción y ganancia;
3. memoria dinámica/cobertura;
4. presión y distancia al atractor;
5. confianza/error metacognitivo;
6. entrada dinámica/cambio de estado.

El workspace selecciona **K=2**, construye un broadcast de bajo ancho de banda y usa ese broadcast para modular la selección contrafactual de trayectoria.

## Controles

Cada réplica parte del mismo checkpoint previamente calibrado:

- **FULL** — workspace + broadcast;
- **NO_BROADCAST** — workspace presente, broadcast causal apagado;
- **LESION** — workspace + broadcast con lesión del origen que el workspace había seleccionado en FULL;
- **NO_WORKSPACE** — selección histórica sin workspace.

Comparación primaria: `NO_BROADCAST regret − FULL regret`.

Comparación de lesión: `LESION regret − FULL regret`.

## Diseño

24 réplicas emparejadas, 24 ciclos de warmup y las mismas señales candidatas `(-1, +1)`.

Antes del probe se identifica el origen seleccionado por el workspace desde el mismo estado inicial. Ese mismo origen se lesiona solamente en el brazo LESION.

No hay reentrenamiento externo durante el probe.

## Persistencia

El organismo guarda en `OntologicalState`:

- módulo seleccionado;
- broadcast de dos dimensiones;
- contador de pasos del workspace.

La prueba de integración verifica que estas observables sobrevivan a cerrar y reabrir SQLite.

## Límite científico

Un efecto de broadcast o lesión en este runtime demostraría una propiedad causal de la arquitectura implementada.

No demostraría por sí solo experiencia subjetiva ni que el PersistentOrganism sea consciente.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

## Objective

I5.1 moves the I5.0 workspace from an isolated prototype into the **real PersistentOrganism runtime**.

The integration is opt-in and leaves historical behavior unchanged when `workspace_enabled=False`.

## Integrated mechanism

The organism exposes six internal sources as specialized modules:

1. current/previous dynamics;
2. self-prediction and gain;
3. dynamic memory/coverage;
4. pressure and attractor distance;
5. metacognitive confidence/error;
6. dynamic input/state change.

The workspace selects **K=2**, builds a low-bandwidth broadcast, and uses that broadcast to modulate counterfactual trajectory selection.

## Controls

Each replicate starts from the same calibrated checkpoint:

- **FULL** — workspace + broadcast;
- **NO_BROADCAST** — workspace present, causal broadcast disabled;
- **LESION** — workspace + broadcast with lesion of the source selected in FULL;
- **NO_WORKSPACE** — historical selection without the workspace.

Primary comparison: `NO_BROADCAST regret − FULL regret`.

Lesion comparison: `LESION regret − FULL regret`.

## Design

24 paired replicates, 24 warmup cycles, and candidate signals `(-1, +1)`.

Before the probe, the workspace source selected from the shared initial state is identified. That same source is lesioned only in the LESION arm.

No external retraining occurs during the probe.

## Persistence

The organism stores in `OntologicalState`: selected module, two-dimensional broadcast, and workspace step count.

The integration test verifies that these observables survive closing and reopening SQLite.

## Scientific boundary

A broadcast or lesion effect in this runtime would demonstrate a causal property of the implemented architecture.

It would not by itself demonstrate subjective experience or that the PersistentOrganism is conscious.

</details>

## Verified result

GitHub Actions run **36984060538** completed successfully.

Artifact: **11216653205**  
SHA-256: **993ba8184c1536c7e781bde1fe9797c6b20a38dccd8269f03d3f13da2ebd48cd**

Configuration: 24 paired replicates, 24 warmup cycles, candidate signals `(-1, +1)`, workspace influence weight 0.35.

| Endpoint | Result |
|---|---:|
| NO_BROADCAST regret − FULL regret | **+0.0212423**, p **0.4928254** |
| NO_WORKSPACE regret − FULL regret | **+0.0212423**, p **0.5026749** |
| LESION regret − FULL regret | **0.0000000**, p **1.0000000** |
| FULL vs NO_BROADCAST action-change rate | **25%** |
| FULL vs LESION action-change rate | **0%** |
| Workspace persistence after restart | **100%** |

## Interpretation

I5.1 is a **null result for the tested behavioral endpoints**. The workspace state persisted correctly and did participate in runtime selection, but the integrated workspace did not produce a statistically detectable regret advantage over either no-broadcast or historical no-workspace selection.

The lesion arm also produced no action change under this particular mapping, so this version does not establish causal necessity of workspace source selection.

This does not invalidate the I5.0 standalone mechanism. It constrains the current integration: the chosen broadcast-to-trajectory mapping is not sufficient, under this protocol, to yield a measurable behavioral benefit inside PersistentOrganism.

The next protocol therefore targets **state-dependent querying** rather than another copy of broadcast-to-action coupling.
