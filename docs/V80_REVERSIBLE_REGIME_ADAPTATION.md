<a id="espanol"></a>

# V80 — Adaptación online ante cambios de régimen reversibles

## Pregunta

V79 produjo un resultado nulo: bajo el cambio dinámico probado, una política que incorporaba online sus ganancias de autopredicción no se separó de una copia congelada.

La explicación experimental inmediata es que aquel cambio no generó suficiente degradación como para exigir adaptación.

V80 aumenta la presión de prueba sin cambiar el principio de aprendizaje:

> ¿Puede una política que aprende online de sus propias consecuencias adaptarse durante una secuencia de regímenes dinámicos nuevos y, cuando el régimen original vuelve, recuperar su comportamiento?

## Diseño

La política inicial se entrena únicamente bajo el régimen base con:

single_impulse

Se crean dos brazos desde el mismo snapshot:

- **frozen:** no incorpora observaciones durante la prueba;
- **adaptive:** incorpora después de cada acción ejecutada la ganancia de autopredicción observada.

No existe reentrenamiento externo durante la prueba.

## Secuencia no estacionaria

Cada ejecución atraviesa cuatro etapas:

1. **base** — régimen original;
2. **shift_a** — régimen dinámico nuevo;
3. **shift_b** — segundo régimen dinámico nuevo;
4. **base_return** — retorno exacto al régimen original.

Los cambios son reversibles y están definidos antes de evaluar:

### shift_a

- relaxation = 0.18
- pressure_gain = 0.95
- cross_gain = 1.25

### shift_b

- relaxation = 0.50
- pressure_gain = 0.35
- cross_gain = 0.45

Cada etapa contiene tres perturbaciones alternantes y recuperación después de cada una.

## Objetivo

La política solo recibe como señal de aprendizaje:

ganancia de autopredicción = error de persistencia − error del modelo de sí

No recibe:

- etiqueta de régimen;
- etiqueta de perturbación;
- objetivo semántico;
- señal externa de éxito.

## Endpoint primario

Ganancia del evento 3 en base_return: adaptive − frozen.

Esto pregunta si la política adaptive conserva una ventaja después de haber atravesado dos regímenes nuevos y de regresar al régimen original.

## Endpoints secundarios

- ventaja adaptive − frozen en shift_a;
- ventaja adaptive − frozen en shift_b;
- cambio evento 3 − evento 1 en base_return;
- diferencia-de-diferencias entre adaptive y frozen durante el retorno;
- error de coincidencia del objetivo terminal de cada intervención.

## Qué significaría un resultado favorable

Un resultado favorable respaldaría una propiedad computacional más fuerte:

**la política puede aprender online bajo no estacionariedad, atravesar varios regímenes y reutilizar lo aprendido cuando el régimen previo reaparece.**

Eso distinguiría adaptación contextual de una simple respuesta fija a una única distribución OOD.

## Límite

La utilidad sigue definida externamente por el protocolo: maximizar ganancia de autopredicción.

V80 no demuestra valores autónomos ni experiencia subjetiva. Prueba adaptación online y recuperación de política bajo una dinámica deliberadamente no estacionaria y reversible.

## Resultado observado

Ejecución completa en GitHub Actions: **64 réplicas por condición**, 64 episodios de entrenamiento, 512 muestras del SelfObserver y 12 pasos de recuperación.

- endpoint primario, `base_return` evento 3: adaptive − frozen = **-0.0103649267**, p = **0.0504475**;
- `shift_a` evento 3: adaptive − frozen = **-0.0062218940**, p = **0.00114994**;
- `shift_b` evento 3: adaptive − frozen = **+0.0000024599**, p = **0.9976001**;
- recuperación evento 3 − evento 1, adaptive = **-0.0021765106**;
- recuperación evento 3 − evento 1, frozen = **-0.0004681112**;
- recuperación diferencial adaptive − frozen = **-0.0017083995**;
- error máximo de coincidencia con el objetivo de intervención = **0.0**.

En `base_return`, la política adaptativa no obtuvo una ventaja sobre la congelada; la diferencia fue ligeramente negativa y quedó cerca del umbral nominal de la prueba. En `shift_a`, la diferencia también favoreció numéricamente a la política congelada. En `shift_b` no hubo separación apreciable.

### Interpretación

**V80 no respalda una ventaja de adaptación online bajo el régimen reversible probado.**

El resultado fortalece el hallazgo nulo de V79 en lugar de resolverlo: cambiar la dinámica por dos regímenes reversibles y regresar al régimen original no produjo una mejora medible de la copia adaptive frente a frozen bajo el objetivo de ganancia de autopredicción.

La interpretación más prudente es que, en este arnés, la actualización online basada únicamente en la ganancia observada de autopredicción **no generó una ventaja adaptativa reproducible**.

Esto no demuestra que toda adaptación online sea inútil. El protocolo sigue evaluando una forma muy específica de aprendizaje online, con una política inicial entrenada bajo el régimen base y una señal de aprendizaje definida externamente.

La integridad de las intervenciones fue exacta (`max_intervention_target_error = 0.0`).

**Estado V80: resultado nulo para la ventaja adaptativa bajo el protocolo probado.**

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V80 — Online Adaptation under Reversible Regime Changes

## Question

V79 produced a null result: under its tested dynamic shift, a policy incorporating observed self-prediction gains online did not separate from a frozen copy.

The immediate explanation is that the previous shift did not create enough degradation to require adaptation.

V80 increases test pressure without changing the learning principle:

> Can a policy that learns online from its own consequences adapt across a sequence of new dynamic regimes and recover its behavior when the original regime returns?

## Design

The initial policy is trained only under the base regime with single_impulse.

Two arms are created from the same snapshot:

- frozen: no observations incorporated during testing;
- adaptive: after each action, incorporates observed self-prediction gain.

No external retraining occurs during testing.

## Non-stationary sequence

Each execution moves through:

1. base — original regime;
2. shift_a — new dynamic regime;
3. shift_b — second new dynamic regime;
4. base_return — exact return to the original regime.

Predefined reversible shifts:

### shift_a

- relaxation = 0.18
- pressure_gain = 0.95
- cross_gain = 1.25

### shift_b

- relaxation = 0.50
- pressure_gain = 0.35
- cross_gain = 0.45

Each stage contains three alternating perturbations followed by recovery.

## Objective

The policy receives only self-prediction gain = persistence error − self-model error.

It receives no regime label, perturbation label, semantic objective, or external success signal.

## Primary endpoint

Adaptive − frozen gain at event 3 in base_return.

This tests whether adaptive policy retains an advantage after traversing two new regimes and returning to the original regime.

## Secondary endpoints

- adaptive − frozen advantage at shift_a;
- adaptive − frozen advantage at shift_b;
- event 3 − event 1 change in base_return;
- adaptive-versus-frozen difference-in-differences during return;
- intervention terminal-target error.

## What a favorable result would show

It would support the stronger computational property that the policy can learn online under non-stationarity, traverse multiple regimes, and reuse what it learned when the prior regime returns.

This would distinguish contextual adaptation from a fixed response to one OOD distribution.

## Boundary

Utility remains externally defined: maximize self-prediction gain.

V80 does not demonstrate autonomous values or subjective experience. It tests online adaptation and policy recovery under deliberately non-stationary, reversible dynamics.

## Observed result

Complete GitHub Actions execution: 64 replicates per condition, 64 training episodes, 512 SelfObserver samples, and 12 recovery steps.

- primary endpoint, base_return event 3: adaptive − frozen = -0.0103649267, p = 0.0504475;
- shift_a event 3: adaptive − frozen = -0.0062218940, p = 0.00114994;
- shift_b event 3: adaptive − frozen = +0.0000024599, p = 0.9976001;
- event 3 − event 1, adaptive: -0.0021765106;
- event 3 − event 1, frozen: -0.0004681112;
- differential recovery adaptive − frozen: -0.0017083995;
- maximum intervention-target mismatch: 0.0.

At base_return, adaptive did not show an advantage over frozen; the difference was slightly negative and near the nominal test threshold. In shift_a, the difference also numerically favored frozen. In shift_b, there was no appreciable separation.

### Interpretation

V80 does not support an online-adaptation advantage under the tested reversible regime.

The result strengthens the null finding from V79: traversing two reversible regimes and returning to the original regime did not produce measurable improvement of adaptive over frozen under the self-prediction-gain objective.

The prudent interpretation is that, in this harness, online updating based only on observed self-prediction gain did not generate a reproducible adaptive advantage.

This does not show that all online adaptation is useless. The protocol tests one specific form of online learning, with a base-regime policy and an externally defined learning signal.

Intervention integrity remained exact: max_intervention_target_error = 0.0.

**V80 status: null result for adaptive advantage under the tested protocol.**

</details>