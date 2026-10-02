# I3 — Repeated Interoceptive Perturbation and Recovery

## Status

**Harness and workflow implemented; scientific interpretation is gated on the I1/I2 evidence review.**

## Question

> Can an interoceptive controller repeatedly detect and regulate internal perturbations across one trajectory, while preserving recovery and limiting overshoot on unseen perturbation magnitudes?

I3 extends I2 from one intervention to a repeated sequence.

## Design

Each episode contains three controlled perturbation events.

- training/reference magnitude: `0.50`;
- OOD magnitudes: `0.35, 0.65, 0.90`;
- three perturbation events per episode;
- eight recovery steps after each event;
- alternating perturbation signs across events;
- no semantic input;
- no external retraining during the probe.

The second and third events are applied from the state produced by the preceding recovery period. This prevents the task from being reducible to three independent one-shot tests.

## Conditions

The same I2 controls are retained:

| Condition | Purpose |
|---|---|
| FULL | interoceptive controller uses the full readout |
| NO-INTEROCEPTION | action choice does not use interoception |
| SHUFFLED | internal readout variables are shuffled before scoring |
| CLAMPED | candidates receive the same interoceptive state |
| LESION | interoceptive information is neutralized |
| RESCUE | first event begins lesioned, then the full controller is restored |

All conditions are paired by seed and share the same initial trajectory and perturbation schedule.

## Primary endpoint

Mean recovery across the three events:

```text
recovery = 1 / (1 + |state_after_recovery - state_before_event| + pressure_after_recovery)
```

## Secondary endpoints

- recovery after the final event;
- mean overshoot across events;
- maximum overshoot;
- operating condition;
- OOD recovery;
- rescue after interoceptive lesion.

## Why overshoot matters

A controller that merely pushes the system strongly can sometimes return close to baseline while causing larger transient deviations.

I3 therefore separates **recovery** from **regulation quality**. A positive result should not be reduced to a single final-state number.

## Repeated-use criterion

A strong result would require the FULL condition to preserve a recovery advantage after the first intervention rather than only during the first event.

Event-wise analysis is retained in the artifact so attenuation can be measured explicitly.

## Interpretation boundary

A positive I3 result would support repeated causal use of an internal-state representation for regulation under the tested simulated dynamics.

It would not establish biological homeostasis, subjective experience, or consciousness.

## Scientific gate

I3 is not entered into the scientific result ledger merely because the workflow succeeds. The artifact must first be checked for:

- deterministic replay;
- matched seeds;
- exact perturbation schedule;
- control integrity;
- absence of semantic labels;
- absence of hidden action shortcuts;
- endpoint integrity;
- OOD separation;
- lesion/rescue integrity.

## Next step

I4 should connect interoceptive state to the existing second-order machinery and test whether the organism can model its own uncertainty about internal-state prediction, then use that uncertainty to alter policy.


<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# I3 — Perturbación y recuperación interoceptiva repetida

## Estado

**Arnés y workflow implementados; la interpretación científica está condicionada a la revisión de evidencia I1/I2.**

## Pregunta

> ¿Puede un controlador interoceptivo detectar y regular repetidamente perturbaciones internas a lo largo de una trayectoria, preservando la recuperación y limitando el overshoot en magnitudes no vistas?

I3 extiende I2 desde una intervención a una secuencia repetida.

## Diseño

Cada episodio contiene tres eventos de perturbación controlada.

- magnitud de referencia/entrenamiento: 0.50;
- magnitudes OOD: 0.35, 0.65, 0.90;
- tres eventos por episodio;
- ocho pasos de recuperación después de cada evento;
- signos alternados entre eventos;
- sin entrada semántica;
- sin reentrenamiento externo durante la sonda.

El segundo y tercer evento se aplican sobre el estado producido por el período de recuperación anterior. Esto evita reducir la tarea a tres tests independientes de una sola intervención.

## Condiciones

Se mantienen los mismos controles de I2:

| Condición | Propósito |
|---|---|
| FULL | controlador interoceptivo usa el readout completo |
| NO-INTEROCEPTION | selección de acción sin interocepción |
| SHUFFLED | readout interno barajado antes de puntuar |
| CLAMPED | todos los candidatos reciben el mismo estado interoceptivo |
| LESION | información interoceptiva neutralizada |
| RESCUE | primer evento lesionado, luego restauración FULL |

Todas las condiciones están emparejadas por seed y comparten trayectoria inicial y calendario de perturbaciones.

## Endpoint primario

Recuperación media en los tres eventos:

recovery = 1 / (1 + |state_after_recovery - state_before_event| + pressure_after_recovery)

## Endpoints secundarios

- recuperación después del evento final;
- overshoot medio;
- overshoot máximo;
- operating condition;
- recuperación OOD;
- rescate después de lesión interoceptiva.

## Por qué importa el overshoot

Un controlador que simplemente empuja con fuerza puede volver cerca del baseline y producir desviaciones transitorias mayores.

I3 separa por eso **recuperación** de **calidad de regulación**. Un resultado positivo no debe reducirse a un único número final.

## Criterio de uso repetido

Un resultado fuerte exigiría que FULL conserve una ventaja de recuperación después de la primera intervención y no solo durante el primer evento.

El análisis por evento se conserva en el artifact para medir atenuación explícitamente.

## Límite de interpretación

Un resultado positivo apoyaría el uso causal repetido de una representación de estado interno para regular bajo las dinámicas simuladas probadas.

No establecería homeostasis biológica, experiencia subjetiva ni consciencia.

## Puerta científica

I3 no entra al ledger científico simplemente porque el workflow tenga éxito. El artifact debe comprobar:

- replay determinista;
- seeds emparejadas;
- calendario exacto de perturbaciones;
- integridad de controles;
- ausencia de etiquetas semánticas;
- ausencia de atajos de acción ocultos;
- integridad de endpoints;
- separación OOD;
- integridad de lesión/rescate.

## Próximo paso

I4 debe conectar el estado interoceptivo con la maquinaria existente de segundo orden y probar si el organismo puede modelar su propia incertidumbre sobre la predicción del estado interno y después usar esa incertidumbre para modificar la política.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# I3 — Repeated Interoceptive Perturbation and Recovery

## Status

**Harness and workflow implemented; scientific interpretation is gated on I1/I2 evidence review.**

## Question

> Can an interoceptive controller repeatedly detect and regulate internal perturbations across one trajectory while preserving recovery and limiting overshoot on unseen perturbation magnitudes?

I3 extends I2 from one intervention to a repeated sequence.

## Design

Each episode contains three controlled perturbation events.

- training/reference magnitude: 0.50;
- OOD magnitudes: 0.35, 0.65, 0.90;
- three perturbation events per episode;
- eight recovery steps after each event;
- alternating perturbation signs across events;
- no semantic input;
- no external retraining during the probe.

The second and third events are applied from the state produced by the preceding recovery period, preventing reduction to three independent one-shot tests.

## Conditions

The same I2 controls are retained: FULL, NO-INTEROCEPTION, SHUFFLED, CLAMPED, LESION, and RESCUE.

All conditions are paired by seed and share the same initial trajectory and perturbation schedule.

## Primary endpoint

Mean recovery across the three events:

recovery = 1 / (1 + |state_after_recovery - state_before_event| + pressure_after_recovery)

## Secondary endpoints

- recovery after the final event;
- mean overshoot;
- maximum overshoot;
- operating condition;
- OOD recovery;
- rescue after interoceptive lesion.

## Why overshoot matters

A controller that simply pushes the system strongly can sometimes return close to baseline while causing larger transient deviations.

I3 therefore separates **recovery** from **regulation quality**. A positive result should not be reduced to a single final-state number.

## Repeated-use criterion

A strong result would require FULL to preserve a recovery advantage after the first intervention rather than only during the first event.

Event-wise analysis is retained in the artifact so attenuation can be measured explicitly.

## Interpretation boundary

A positive I3 result would support repeated causal use of an internal-state representation for regulation under the tested simulated dynamics.

It would not establish biological homeostasis, subjective experience, or consciousness.

## Scientific gate

I3 is not entered into the scientific ledger merely because the workflow succeeds. The artifact must be checked for deterministic replay, matched seeds, exact perturbation schedule, control integrity, absence of semantic labels, absence of hidden action shortcuts, endpoint integrity, OOD separation, and lesion/rescue integrity.

## Next step

I4 should connect interoceptive state to the existing second-order machinery and test whether the organism can model its own uncertainty about internal-state prediction and then use that uncertainty to alter policy.

</details>