# I2 — Interoceptive Regulation

## Status

**Controller and experimental harness implemented; confirmatory execution is pending the I1 gate.**

I2 is intentionally default-off in `PersistentOrganism`. Enabling `interoceptive_control_enabled` does not change existing behaviour unless explicitly configured.

## Question

> Can a bounded representation of the organism's internal operating condition causally improve recovery from a controlled internal perturbation?

## Conditions

| Condition | Controller |
|---|---|
| FULL | full interoceptive readout scores counterfactual actions |
| NO-INTEROCEPTION | deterministic random action from the same candidate set |
| SHUFFLED | interoceptive variables are permuted before scoring |
| CLAMPED | all candidates receive the same interoceptive snapshot |
| LESION | interoceptive score is removed and replaced by a neutral controller state |
| RESCUE | LESION for the first half of recovery, then FULL restoration |

All conditions share the same seed, initial trajectory, perturbation, candidate action set, and deterministic dynamics noise schedule.

## Perturbations

Training-range perturbations:

`0.25, 0.50, 0.75`

OOD perturbations:

`0.35, 0.65, 0.90`

The probe receives no semantic labels and no model-provider output during the recovery probe.

## Primary endpoint

Recovery score:

```text
1 / (1 + |final_state - baseline_state| + final_pressure)
```

The controller optimizes predicted `operating_condition`, while the primary endpoint is an independent recovery measure. This avoids making the endpoint identical to the control objective.

Secondary measurements:

- mean pressure;
- mean operating condition;
- final operating condition;
- OOD recovery;
- lesion/rescue contrast.

## Required interpretation

A positive FULL-vs-control result would support a causal role for the bounded internal-state representation in recovery under this simulated dynamics.

It would not establish homeostasis in a biological sense, interoceptive phenomenology, or subjective consciousness.

## Scientific gate

I2 should not be promoted to a confirmatory scientific result until I1 has a validated readout under its declared OOD protocol.

The dedicated workflow is available through `workflow_dispatch` and also validates the I2 harness on relevant pushes. The result artifact must be reviewed before entering the scientific ledger.

## Runtime hook

`PersistentOrganism` now contains a default-off interoceptive control hook:

```text
interoceptive_control_enabled = False
```

When explicitly enabled, the autonomous cycle records the controller mode, candidate scores, and chosen signal in the organism event log.

Existing self-model selection remains unchanged by default.

## Next step

I3 should test repeated perturbation and recovery, overshoot, and transfer to unseen perturbation magnitudes. The controller should remain causal and the analysis should preserve shuffled, clamped, lesion, and rescue controls.


<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# I2 — Regulación interoceptiva

## Estado

**Controlador y arnés experimental implementados; ejecución confirmatoria pendiente del umbral I1.**

I2 está deliberadamente desactivado por defecto en PersistentOrganism. Habilitar interoceptive_control_enabled no cambia el comportamiento existente salvo que se configure explícitamente.

## Pregunta

> ¿Puede una representación acotada de la condición operativa interna del organismo mejorar causalmente la recuperación después de una perturbación interna controlada?

## Condiciones

| Condición | Controlador |
|---|---|
| FULL | readout interoceptivo completo puntúa acciones contrafactuales |
| NO-INTEROCEPTION | acción aleatoria determinista del mismo conjunto candidato |
| SHUFFLED | variables interoceptivas se permutan antes de puntuar |
| CLAMPED | todos los candidatos reciben el mismo snapshot interoceptivo |
| LESION | se elimina el score interoceptivo y se reemplaza por un estado neutral |
| RESCUE | LESION durante la primera mitad de recuperación y luego restauración FULL |

Todas las condiciones comparten seed, trayectoria inicial, perturbación, conjunto candidato y calendario de ruido dinámico determinista.

## Perturbaciones

Rango de entrenamiento: 0.25, 0.50, 0.75.

Perturbaciones OOD: 0.35, 0.65, 0.90.

La sonda no recibe etiquetas semánticas ni salida del proveedor durante la recuperación.

## Endpoint primario

Recovery score:

1 / (1 + |final_state - baseline_state| + final_pressure)

El controlador optimiza operating_condition predicho, mientras que el endpoint primario es una medida independiente de recuperación. Esto evita que el endpoint sea idéntico al objetivo del controlador.

Mediciones secundarias:

- presión media;
- operating condition medio;
- operating condition final;
- recuperación OOD;
- contraste lesión/rescate.

## Interpretación requerida

Un resultado positivo FULL frente al control apoyaría un papel causal de la representación acotada del estado interno en la recuperación bajo esta dinámica simulada.

No establecería homeostasis biológica, fenomenología interoceptiva ni consciencia subjetiva.

## Puerta científica

I2 no debe convertirse en resultado científico confirmatorio hasta que I1 tenga un readout validado bajo su protocolo OOD declarado.

El workflow dedicado se puede ejecutar manualmente y también valida el arnés I2 en pushes relevantes. El artifact debe revisarse antes de entrar al ledger científico.

## Hook de runtime

PersistentOrganism contiene un hook interoceptivo por defecto desactivado:

interoceptive_control_enabled = False

Cuando se habilita explícitamente, el ciclo autónomo registra modo de controlador, scores de candidatos y señal elegida en el log de eventos.

La selección mediante modelo de sí existente permanece sin cambios por defecto.

## Próximo paso

I3 debe probar perturbación y recuperación repetidas, overshoot y transferencia a magnitudes no vistas. El controlador debe seguir siendo causal y el análisis debe preservar controles shuffle, clamp, lesion y rescue.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# I2 — Interoceptive Regulation

## Status

**Controller and experimental harness implemented; confirmatory execution is pending the I1 gate.**

I2 is intentionally default-off in PersistentOrganism. Enabling interoceptive_control_enabled does not change existing behavior unless explicitly configured.

## Question

> Can a bounded representation of the organism's internal operating condition causally improve recovery from a controlled internal perturbation?

## Conditions

| Condition | Controller |
|---|---|
| FULL | full interoceptive readout scores counterfactual actions |
| NO-INTEROCEPTION | deterministic random action from the same candidate set |
| SHUFFLED | interoceptive variables are permuted before scoring |
| CLAMPED | all candidates receive the same interoceptive snapshot |
| LESION | interoceptive score is removed and replaced by a neutral controller state |
| RESCUE | LESION for the first half of recovery, then FULL restoration |

All conditions share the same seed, initial trajectory, perturbation, candidate action set, and deterministic dynamics-noise schedule.

## Perturbations

Training-range: 0.25, 0.50, 0.75.

OOD: 0.35, 0.65, 0.90.

The probe receives no semantic labels and no provider output during the recovery probe.

## Primary endpoint

Recovery score:

1 / (1 + |final_state - baseline_state| + final_pressure)

The controller optimizes predicted operating_condition, while the primary endpoint is an independent recovery measure. This avoids making the endpoint identical to the controller objective.

Secondary measurements include mean pressure, mean operating condition, final operating condition, OOD recovery, and lesion/rescue contrast.

## Required interpretation

A positive FULL-vs-control result would support a causal role for the bounded internal-state representation in recovery under the simulated dynamics.

It would not establish biological homeostasis, interoceptive phenomenology, or subjective consciousness.

## Scientific gate

I2 should not be promoted to a confirmatory scientific result until I1 has a validated readout under its declared OOD protocol.

The dedicated workflow is available through workflow_dispatch and also validates the I2 harness on relevant pushes. The result artifact must be reviewed before entering the scientific ledger.

## Runtime hook

PersistentOrganism contains a default-off interoceptive control hook:

interoceptive_control_enabled = False

When explicitly enabled, the autonomous cycle records controller mode, candidate scores, and chosen signal in the organism event log.

Existing self-model selection remains unchanged by default.

## Next step

I3 should test repeated perturbation and recovery, overshoot, and transfer to unseen perturbation magnitudes. The controller should remain causal and analysis should preserve shuffled, clamped, lesion, and rescue controls.

</details>