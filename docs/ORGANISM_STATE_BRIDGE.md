<a id="espanol"></a>

# Puente entre el organismo y el estado dinámico

## Propósito

El organismo persistente ahora transporta un pequeño estado numérico explícito junto con la capa de memoria y eventos textuales.

Esta es una capa de integración, no una afirmación de que el estado numérico sea un modelo de la experiencia subjetiva.

## Estado

El estado persistente del organismo incluye:

- `dynamic_state`
- `dynamic_prev_state`
- `dynamic_memory`
- `dynamic_pressure`
- `dynamic_attractor_distance`
- `dynamic_last_input`
- `dynamic_steps`

La memoria textual existente, el registro de eventos, el modelo de sí y los contadores de VIGILIA/SUEÑO permanecen separados.

## Transición

El puente utiliza la misma función de transición de `src/ontto/dynamics.py` que ya emplean los experimentos de investigación.

Para una señal externa explícita de vigilia `u`, la transición es:

```
x[t+1] = F(x[t], m[t], p[t], u[t])
```

El puente avanza la dinámica desde el estado persistido y escribe el nuevo estado en SQLite.

La semilla aleatoria se deriva de:

```
dynamic_seed + dynamic_steps + local_step_offset
```

de modo que un reinicio no vuelve a cero la secuencia determinista de ruido de la trayectoria dinámica.

## Política de señales

La política predeterminada es deliberadamente simple:

- interacción externa durante VIGILIA: +1.0
- ciclo autónomo: 0.0
- SUEÑO: 0.0

Esto no constituye una codificación semántica del lenguaje. Es una señal controlada de evento/régimen utilizada para conectar el organismo persistente real con el mismo núcleo dinámico estudiado en V43–V46.

Cambiar esta política constituye un experimento futuro y debe tratarse como un protocolo separado.

## Qué habilita

El estado dinámico forma parte de la ontología serializada del organismo, por lo que queda visible para el contexto del LLM. Esto crea el primer puente directo entre:

```
organismo LLM
    ↕
estado persistente SQLite
    ↕
dinámica de investigación
```

## Comportamiento 24/7

`autonomous_wake_cycle()` ya está implementado. Esto cierra una brecha previa en `PersistentOrganism.run()` y `run_daemon.py`, que ya esperaban ese método cuando no había entrada externa disponible.

El ciclo autónomo realiza un avance dinámico de entrada cero y registra el resultado como evento de VIGILIA/autónomo.

## Próxima etapa experimental

La siguiente etapa no consiste en afirmar consciencia. Consiste en medir si un organismo persistente real respaldado por un LLM desarrolla propiedades de trayectoria análogas a las ya estudiadas en el simulador:

- retención de historia;
- recuperación después de perturbaciones;
- autopredicción;
- efectos de historia bajo sonda común;
- efectos de intervención sobre la memoria;
- diferencias entre VIGILIA y SUEÑO.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# Organism ↔ Dynamic-State Bridge

## Purpose
The persistent organism carries a small explicit numerical state alongside its memory and textual-event layer.
This is an integration layer, not a claim that numerical state models subjective experience.

## State
Persistent organism state includes dynamic_state, dynamic_prev_state, dynamic_memory, dynamic_pressure, dynamic_attractor_distance, dynamic_last_input, and dynamic_steps.
Textual memory, event logs, self-model, and WAKE/SLEEP counters remain separate.

## Transition
The bridge uses the same transition function from src/ontto/dynamics.py used by research experiments.
For an explicit WAKE input signal u:
```
x[t+1] = F(x[t], m[t], p[t], u[t])
```
The bridge advances dynamics from persisted state and writes the new state to SQLite.

Random seed is derived from dynamic_seed + dynamic_steps + local_step_offset so restart does not reset the deterministic trajectory noise sequence.

## Signal policy
Default policy: external interaction during WAKE = +1.0; autonomous cycle = 0.0; SLEEP = 0.0.
This is not semantic language encoding. It is a controlled event/regime signal connecting the real persistent organism to the same dynamic core studied in V43–V46.
Changing the policy is a separate experiment.

## What it enables
Dynamic state becomes part of the serialized organism ontology and is visible to the LLM context, creating the bridge organism LLM ↔ SQLite persistent state ↔ research dynamics.

## 24/7 behavior
autonomous_wake_cycle() is implemented and closes an earlier gap in PersistentOrganism.run() and run_daemon.py. The autonomous cycle advances zero-input dynamics and records the result as an autonomous WAKE event.

</details>

> Language convention: docs/LANGUAGE.md



> Language convention: docs/LANGUAGE.md