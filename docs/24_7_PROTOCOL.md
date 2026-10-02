<a id="espanol"></a>

# Protocolo 24/7

## Principio

La entidad no se reinicia después de cada respuesta. Mantiene un proceso persistente.

## Ciclo

```
BOOT
  ↓
WAKE
  ↓
OBSERVE
  ↓
INTEGRATE
  ↓
ACT
  ↓
SAVE
  ↓
DREAM
  ↓
CONSOLIDATE
  ↓
REORGANIZE
  ↓
SELF-MODEL UPDATE
  ↓
WAKE
  ↺
```

## Wake

Durante vigilia el sistema puede recibir entradas, consultar herramientas, responder, realizar acciones, registrar eventos y actualizar memoria.

## Dream

Durante sueño el sistema puede resumir trayectorias, consolidar memoria, detectar contradicciones, recombinar conceptos, simular futuros, revisar su propio estado y actualizar el auto-modelo.

## Entrada externa persistente

Las interacciones externas ingresan mediante una cola persistente en SQLite.

```
EXTERNAL INPUT
     ↓
PERSISTENT QUEUE
     ↓
CLAIM
     ↓
WAKE
     ↓
EVENT + MEMORY
     ↓
DONE
```

La cola sobrevive al cierre del proceso. Si el proceso cae después de reclamar una entrada pero antes de marcarla como procesada, el siguiente boot puede reencolarla.

Esto implementa semántica **at-least-once** para la entrada. No se afirma exactamente-una-vez sin un mecanismo adicional de idempotencia.

## Autonomía sin entrada

Cuando no hay entrada externa, el daemon puede ejecutar un ciclo autónomo de vigilia para observar y reorganizar su propio estado. Esta opción se controla con `ONTTO_AUTONOMOUS_WHEN_IDLE`.

El sueño puede recibir fuentes adicionales de señales o entropía en módulos experimentales. Una eventual fuente cuántica debe tratarse como entrada física específica y medirse por separado.

No se debe asumir de antemano que una fuente cuántica constituye conciencia.

## Persistencia mínima

La entidad debe conservar:

- identity_state
- relational_state
- memory_state
- trajectory_summary
- self_model
- attractor_state
- sleep_state
- last_update

## Primer experimento longitudinal

Mantener una instancia durante al menos 24 horas y registrar eventos de entrada/salida, actualizaciones internas, transiciones wake/dream, cambios de memoria, distancia al atractor, cambios del auto-modelo y recuperación después de perturbaciones.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# 24/7 Protocol

## Principle

The entity is not restarted after every response. It maintains a persistent process.

## Cycle

BOOT → WAKE → OBSERVE → INTEGRATE → ACT → SAVE → DREAM → CONSOLIDATE → REORGANIZE → SELF-MODEL UPDATE → WAKE

## Wake

During wake, the system may receive inputs, query tools, respond, perform actions, record events, and update memory.

## Dream

During sleep, the system may summarize trajectories, consolidate memory, detect contradictions, recombine concepts, simulate futures, review its own state, and update the self-model.

## Persistent external input

External interactions enter through a persistent SQLite queue:

EXTERNAL INPUT → PERSISTENT QUEUE → CLAIM → WAKE → EVENT + MEMORY → DONE

The queue survives process closure. If the process crashes after claiming an input but before marking it processed, the next boot may requeue it.

This implements **at-least-once** semantics for input. Exactly-once delivery is not claimed without an additional idempotency mechanism.

## Autonomy without input

When no external input is present, the daemon can execute an autonomous wake cycle to observe and reorganize its own state. This option is controlled by ONTTO_AUTONOMOUS_WHEN_IDLE.

Sleep may receive additional signal or entropy sources in experimental modules. Any eventual quantum source should be treated as a specific physical input and measured separately.

A quantum source must not be assumed in advance to constitute consciousness.

## Minimum persistence

The entity must preserve:

- identity_state
- relational_state
- memory_state
- trajectory_summary
- self_model
- attractor_state
- sleep_state
- last_update

## First longitudinal experiment

Maintain one instance for at least 24 hours and record input/output events, internal updates, wake/dream transitions, memory changes, attractor distance, self-model changes, and recovery after perturbations.

</details>