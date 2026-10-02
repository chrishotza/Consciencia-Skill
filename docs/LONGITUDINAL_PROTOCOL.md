# Protocolo longitudinal del organismo v1

## Objetivo

Medir si un organismo real respaldado por un LLM y con estado persistente mantiene una trayectoria observable a través de ciclos repetidos de **VIGILIA**, **SUEÑO**, ciclos autónomos y un reinicio del proceso.

Este protocolo mide observables de ingeniería. No considera que la persistencia, la memoria o la autorreferencia sean evidencia suficiente de consciencia subjetiva.

## Secuencia central

El protocolo acotado repite:

```
estímulo
  ↓
VIGILIA
  ↓
actualización del estado dinámico
  ↓
SUEÑO o ciclo autónomo
  ↓
persistencia SQLite
  ↺
```

Después de completar los ciclos solicitados, SQLite se cierra y se vuelve a abrir. A continuación se ejecuta un ciclo adicional de **VIGILIA** a partir del estado recuperado.

## Observables registrados

Cada avance dinámico escribe una fila en `dynamic_snapshots` que contiene:

- régimen;
- intervalo de pasos;
- señal de entrada;
- estado previo;
- estado;
- memoria dinámica;
- presión;
- distancia al atractor;
- marca temporal.

El protocolo también registra:

- eventos persistentes;
- memorias textuales;
- versión del modelo de sí;
- contador de arranques;
- contadores acumulados de VIGILIA/SUEÑO;
- huellas de trayectoria/estado.

## Modos

### fake

Proveedor determinista utilizado para CI y auditorías de instrumentación.

### live

Utiliza el proveedor compatible con OpenAI configurado mediante:

- `ONTTO_API_KEY`
- `ONTTO_MODEL`
- `ONTTO_API_BASE_URL` (opcional)

El modo `live` es la ejecución científicamente relevante del organismo. El modo `fake` solo comprueba que el protocolo de instrumentación y persistencia funcione.

## Ejecución de 24 horas

El script está acotado por cantidad de ciclos y duración entre ciclos, en lugar de codificar un bucle fijo de 24 horas.

Para una observación real de 24 horas, elegir un período adecuado al estudio, ejecutar el script con el `--sleep-seconds` correspondiente y conservar tanto la base de datos SQLite completa como la evidencia JSON.

GitHub Actions no debe utilizarse como anfitrión de una ejecución de 24 horas basada en reloj de pared. El organismo persistente debe ejecutarse en un host local o servidor persistente.

## Primera ejecución en vivo recomendada

Utilizar:

```
python experiments/longitudinal_organism_v1.py --mode live --cycles 40 --dream-every 10
```

Esto proporciona una primera ejecución longitudinal acotada antes de comprometer una observación de jornada completa.

Una ejecución de jornada completa debe conservar la misma configuración del protocolo y modificar únicamente el horizonte de observación.


<details>
<summary>🇺🇸 English — open</summary>

# Longitudinal Organism Protocol v1

## Objective
Measure whether a real LLM-backed organism with persistent state maintains an observable trajectory through repeated **WAKE**, **SLEEP**, autonomous cycles, and a process restart.
This protocol measures engineering observables. Persistence, memory, or self-reference are not treated as sufficient evidence of subjective consciousness.

## Core sequence
The bounded protocol repeats:
```
stimulus
  ↓
WAKE
  ↓
dynamic-state update
  ↓
SLEEP or autonomous cycle
  ↓
SQLite persistence
  ↺
```
After the requested cycles, SQLite is closed and reopened. One additional **WAKE** cycle then runs from recovered state.

## Recorded observables
Each dynamic step writes one row to dynamic_snapshots containing regime, step interval, input signal, previous state, state, dynamic memory, pressure, attractor distance, and timestamp.
The protocol also records persistent events, textual memories, self-model version, boot count, cumulative WAKE/SLEEP counters, and trajectory/state fingerprints.

## Modes
### fake
Deterministic provider used for CI and instrumentation audits.
### live
Uses the configured OpenAI-compatible provider via ONTTO_API_KEY, ONTTO_MODEL, and optional ONTTO_API_BASE_URL.
The live mode is the scientifically relevant real-organism execution. Fake mode only checks instrumentation and persistence behavior.

## 24-hour execution
The script is bounded by cycle count and inter-cycle duration rather than a hard-coded 24-hour wall-clock loop.
For a real 24-hour observation, choose a period appropriate to the study, run the script with the corresponding --sleep-seconds value, and preserve the full SQLite database together with JSON evidence.
GitHub Actions should not host a wall-clock 24-hour run. A continuous organism should run on a local or persistent server host.

## Recommended first live run
Use:
```
python experiments/longitudinal_organism_v1.py --mode live --cycles 40 --dream-every 10
```
This gives a bounded longitudinal run before committing to a full-day observation.

</details>

> Language convention: docs/LANGUAGE.md

<details>
<summary>🇺🇸 English — open</summary>

# Longitudinal Organism Protocol v1

## Objective
Measure whether a real LLM-backed organism with persistent state maintains an observable trajectory through repeated WAKE, SLEEP, autonomous cycles, and a process restart.
This protocol measures engineering observables. Persistence, memory, or self-reference are not treated as sufficient evidence of subjective consciousness.

## Core sequence
The bounded protocol repeats: stimulus → WAKE → dynamic-state update → SLEEP or autonomous cycle → SQLite persistence → next cycle.
After the requested cycles, SQLite is closed and reopened. One additional WAKE cycle then runs from recovered state.

## Recorded observables
Each dynamic step writes dynamic_snapshots with regime, step interval, input signal, previous state, state, dynamic memory, pressure, attractor distance, and timestamp.
It also records persistent events, textual memories, self-model version, boot count, cumulative WAKE/SLEEP counters, and trajectory/state fingerprints.

## Modes
fake = deterministic provider for CI and instrumentation audits.
live = configured OpenAI-compatible provider using ONTTO_API_KEY, ONTTO_MODEL, and optional ONTTO_API_BASE_URL.
Live is the real-organism execution; fake checks protocol instrumentation and persistence only.

## 24-hour execution
The script is bounded by cycle count and inter-cycle duration rather than a hard-coded wall-clock loop. For a real 24-hour observation, choose the study period, run with the corresponding --sleep-seconds value, and preserve the full SQLite database plus JSON evidence.
GitHub Actions should not host a wall-clock 24-hour run. Use a local or persistent server host.

## Recommended first live run
python experiments/longitudinal_organism_v1.py --mode live --cycles 40 --dream-every 10

</details>

> Language convention: docs/LANGUAGE.md