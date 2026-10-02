# Context Persistence — V8b

V8b is the corrected version of the context-reset intervention experiment. Both history branches use the same noise seed during continuation, removing the confound present in V8.

## Regimes

- persistence ridge: beta=0.99730, relaxation=1.205, pressure_gain=0.125, cross_gain=0.15
- critical ridge: beta=0.998606, relaxation=1.205, pressure_gain=0.125, cross_gain=0.15
- baseline: beta=0.92, relaxation=0.32, pressure_gain=0.55, cross_gain=0.85

## Continuation

After 300 history steps, both branches receive 500 zero-input steps.

Interventions:
- full: preserve both branches' state, memory and pressure
- reset_state: synchronize the two recent state values, preserve branch-specific memory and pressure
- reset_memory: synchronize branch memory, preserve state and pressure
- reset_pressure: synchronize pressure, preserve state and memory
- reset_all: synchronize state, memory and pressure

## Corrected results

| Regime | Mode | End gap | Retention |
|---|---|---:|---:|
| baseline | full | ~5.8e-16 | ~0 |
| baseline | reset_memory | 1.6e-6 | ~3.2e-5 |
| baseline | reset_state | ~5.8e-16 | ~0 |
| baseline | reset_pressure | ~5.8e-16 | ~0 |
| critical | full | 1.2631 | 0.9534 |
| critical | reset_memory | 0.9785 | 0.9892 |
| critical | reset_state | 0.6755 | 0.9514 |
| critical | reset_pressure | 1.2631 | 0.9529 |
| persistence | full | 1.2500 | 1.0375 |
| persistence | reset_memory | 1.2023 | 0.9935 |
| persistence | reset_state | 1.2553 | 1.1079 |
| persistence | reset_pressure | 1.2500 | 1.0374 |

## Interpretation

1. The baseline rapidly erases historical separation under identical zero future.
2. The high-persistence regimes retain large separation even when the external future input is exactly zero.
3. The persistence is not localized in the explicit memory or pressure scalar. Resetting either does not eliminate the effect. Synchronizing the current state reduces the absolute separation in the critical ridge but does not erase the subsequent persistence.

The operational interpretation is distributed dynamical context: historical differences are carried jointly by recurrent state and hidden trajectory variables rather than by one explicit memory accumulator.

This does not establish consciousness or subjective experience. It establishes a reproducible intervention result about the implemented dynamical system.

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Persistencia de contexto — V8b

V8b es la versión corregida del experimento de intervención de reset de contexto. Ambas ramas de historia utilizan el mismo noise seed durante la continuación, eliminando el confound presente en V8.

## Regímenes

- persistence ridge: beta=0.99730, relaxation=1.205, pressure_gain=0.125, cross_gain=0.15
- critical ridge: beta=0.998606, relaxation=1.205, pressure_gain=0.125, cross_gain=0.15
- baseline: beta=0.92, relaxation=0.32, pressure_gain=0.55, cross_gain=0.85

## Continuación

Después de 300 pasos de historia, ambas ramas reciben 500 pasos sin input.

Intervenciones:

- full: conservar state, memory y pressure de ambas ramas;
- reset_state: sincronizar los dos valores de estado recientes, conservar memory y pressure específicos de la rama;
- reset_memory: sincronizar memory, conservar state y pressure;
- reset_pressure: sincronizar pressure, conservar state y memory;
- reset_all: sincronizar state, memory y pressure.

## Resultados corregidos

| Régimen | Modo | End gap | Retention |
|---|---|---:|---:|
| baseline | full | ~5.8e-16 | ~0 |
| baseline | reset_memory | 1.6e-6 | ~3.2e-5 |
| baseline | reset_state | ~5.8e-16 | ~0 |
| baseline | reset_pressure | ~5.8e-16 | ~0 |
| critical | full | 1.2631 | 0.9534 |
| critical | reset_memory | 0.9785 | 0.9892 |
| critical | reset_state | 0.6755 | 0.9514 |
| critical | reset_pressure | 1.2631 | 0.9529 |
| persistence | full | 1.2500 | 1.0375 |
| persistence | reset_memory | 1.2023 | 0.9935 |
| persistence | reset_state | 1.2553 | 1.1079 |
| persistence | reset_pressure | 1.2500 | 1.0374 |

## Interpretación

1. El baseline elimina rápidamente la separación histórica bajo un futuro idéntico y cero.
2. Los regímenes de alta persistencia conservan una separación grande aunque el input futuro sea exactamente cero.
3. La persistencia no está localizada en la memoria explícita ni en el escalar de pressure. Resetear cualquiera de ellos no elimina el efecto. Sincronizar el estado actual reduce la separación absoluta en la cresta crítica, pero no elimina la persistencia posterior.

La interpretación operacional es contexto dinámico distribuido: las diferencias históricas son transportadas conjuntamente por el estado recurrente y variables latentes de trayectoria, no por un único acumulador de memoria explícita.

No establece consciencia ni experiencia subjetiva. Establece un resultado reproducible de intervención sobre el sistema dinámico implementado.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# Context Persistence — V8b

V8b is the corrected context-reset intervention experiment. Both history branches use the same noise seed during continuation, removing the confound present in V8.

## Regimes

- persistence ridge: beta=0.99730, relaxation=1.205, pressure_gain=0.125, cross_gain=0.15
- critical ridge: beta=0.998606, relaxation=1.205, pressure_gain=0.125, cross_gain=0.15
- baseline: beta=0.92, relaxation=0.32, pressure_gain=0.55, cross_gain=0.85

## Continuation

After 300 history steps, both branches receive 500 zero-input steps.

Interventions are full, reset_state, reset_memory, reset_pressure, and reset_all exactly as recorded in the canonical protocol.

## Corrected results

| Regime | Mode | End gap | Retention |
|---|---|---:|---:|
| baseline | full | ~5.8e-16 | ~0 |
| baseline | reset_memory | 1.6e-6 | ~3.2e-5 |
| baseline | reset_state | ~5.8e-16 | ~0 |
| baseline | reset_pressure | ~5.8e-16 | ~0 |
| critical | full | 1.2631 | 0.9534 |
| critical | reset_memory | 0.9785 | 0.9892 |
| critical | reset_state | 0.6755 | 0.9514 |
| critical | reset_pressure | 1.2631 | 0.9529 |
| persistence | full | 1.2500 | 1.0375 |
| persistence | reset_memory | 1.2023 | 0.9935 |
| persistence | reset_state | 1.2553 | 1.1079 |
| persistence | reset_pressure | 1.2500 | 1.0374 |

## Interpretation

1. The baseline rapidly erases historical separation under identical zero future.
2. High-persistence regimes retain large separation even when future input is exactly zero.
3. Persistence is not localized in explicit memory or pressure. Resetting either does not eliminate the effect. Synchronizing current state reduces absolute separation in the critical ridge but does not erase subsequent persistence.

The operational interpretation is distributed dynamical context: historical differences are jointly carried by recurrent state and hidden trajectory variables rather than one explicit memory accumulator.

This does not establish consciousness or subjective experience. It establishes a reproducible intervention result about the implemented dynamical system.

</details>