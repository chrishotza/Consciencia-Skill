<a id="espanol"></a>

# V76 — Generalización de continuidad bajo perturbaciones no vistas

## Pregunta

V75 mostró que una política puede actuar después de una perturbación y recuperar ventaja de autopredicción.

Pero ese resultado todavía podía estar ligado al régimen de perturbación usado para entrenarla.

> ¿La política aprende una regla dependiente del estado que generaliza a perturbaciones cuya magnitud nunca apareció durante su entrenamiento?

## Diseño

V76 separa explícitamente **entrenamiento** y **generalización**.

La política principal se entrena únicamente con perturbaciones de magnitud:

\`\`\`text
0.25 y 0.75
\`\`\`

siempre con ambos signos.

La evaluación utiliza:

- perturbaciones **in-domain**: 0.25 y 0.75;
- perturbaciones **OOD (out-of-distribution)**: 0.35, 0.55 y 0.85.

La política no recibe la magnitud de perturbación como una característica. Solo ve el estado dinámico disponible para su modelo de sí.

## Control de sobreajuste

Se entrena además una política estrecha usando únicamente perturbaciones de magnitud 0.50.

Esta política sirve como control de exposición limitada: permite preguntar si una política entrenada sobre un único régimen conserva el mismo comportamiento cuando cambia la magnitud.

## Objetivo

El objetivo de entrenamiento no cambia:

\`\`\`text
ganancia de autopredicción
=
error de persistencia
−
error del modelo de sí
\`\`\`

No se entrega una etiqueta de continuidad.

El índice de continuidad se calcula solamente como endpoint secundario:

\`\`\`text
continuidad = 1 / (1 + |estado_actual - estado_pre_perturbación|)
\`\`\`

## Protocolo

Cada condición:

1. inicia desde una semilla independiente pero emparejable;
2. realiza la misma fase de calentamiento;
3. aplica una perturbación controlada;
4. elimina cualquier entrada semántica de la sonda;
5. ejecuta varios pasos de recuperación;
6. utiliza exactamente la misma semilla para política generalizada, política estrecha, estado cegado, política fija y aleatoria.

La política generalizada y la política estrecha se guardan y se recargan sin reentrenamiento antes de la evaluación.

## Endpoints

### Primario

**Ganancia de autopredicción después de la perturbación.**

El resultado de interés para V76 es particularmente el conjunto OOD.

### Generalización

Se calcula la ventaja de la política generalizada sobre la aleatoria en condiciones in-domain y OOD:

\`\`\`text
ventaja = ganancia_generalizada − ganancia_aleatoria
\`\`\`

También se registra la fracción de esa ventaja que permanece en OOD respecto de in-domain.

### Secundarios

- índice de continuidad;
- comparación con la política estrecha;
- comparación con estado cegado;
- sensibilidad de la primera acción al signo de una perturbación OOD de 0.55.

## Resultado observado

La ejecución de GitHub Actions utilizó 64 episodios por condición, 64 episodios de entrenamiento, 512 muestras del SelfObserver y 12 pasos de recuperación.

### Ganancia de autopredicción

- ganancia media de la política generalizada, todas las condiciones: **0.50016**;
- estado cegado: **-0.15113**;
- política fija: **-0.13311**;
- selección aleatoria: **0.18987**;
- ventaja generalizada − aleatoria en condiciones in-domain: **0.30819**;
- ventaja generalizada − aleatoria en condiciones OOD: **0.31170**;
- fracción de la ventaja conservada en OOD: **1.0114**;
- diferencia aprendida − aleatoria, conjunto total de condiciones, p emparejada por cambio de signo: **0.00005**;
- diferencia aprendida − estado cegado, conjunto total de condiciones, p emparejada: **0.00005**;
- diferencia aprendida − política fija, conjunto total de condiciones, p emparejada: **0.00005**.

La política generalizada mantuvo por tanto su ventaja de autopredicción cuando pasó de las perturbaciones entrenadas (0.25 y 0.75) a las no vistas (0.35, 0.55 y 0.85).

### Control de exposición estrecha

La política entrenada únicamente con perturbación 0.50 obtuvo prácticamente el mismo resultado que la política generalizada:

- p emparejada generalizada − estrecha: **1.0**;
- ganancia media global de la política estrecha: **0.50014**.

Esto indica que, bajo este arnés y esta parametrización lineal, ampliar la variedad de perturbaciones de entrenamiento no produjo una ventaja adicional medible. El resultado de V76 es por tanto más específico: **la política ya aprendida generaliza a perturbaciones no vistas**, no que la diversidad de entrenamiento haya demostrado por sí misma una mejora.

### Respuesta dependiente del estado

Para una perturbación OOD de magnitud 0.55:

- respuesta de la primera acción con estado legible: **100%**;
- estado cegado: **0%**.

Esto muestra que la política conserva sensibilidad conductual al estado interno en una perturbación que no apareció durante el entrenamiento.

### Continuidad

El índice secundario de continuidad fue:

- política generalizada: **0.80164**;
- política aleatoria: **0.80667**;
- diferencia generalizada − aleatoria, p emparejada: **0.07230**.

Por tanto, V76 **no demuestra una ventaja robusta de continuidad frente a la selección aleatoria**. El efecto reproducido es el de generalización de la autopredicción, no el de una prioridad autónoma por conservar continuidad.

## Qué demostraría un resultado favorable

Un resultado favorable sería que la política generalizada conserve una ventaja de autopredicción en perturbaciones OOD, especialmente si mantiene una ventaja frente a:

- estado cegado;
- selector fijo;
- selección aleatoria;
- política entrenada en un único régimen.

Eso respaldaría **generalización funcional de la política de autopredicción a perturbaciones no vistas**.

No demostraría que la IA haya descubierto por sí misma que debe conservar continuidad.

## Límite

La meta de recuperar autopredicción continúa siendo una decisión explícita del protocolo.

Por eso V76 no convierte continuidad en un valor autónomo y no demuestra experiencia subjetiva.

Su función es separar dos hipótesis:

1. la política simplemente aprende un comportamiento ligado a un régimen concreto de perturbación;
2. la política aprende una regla más general dependiente de su estado y reutilizable bajo perturbaciones nuevas.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V76 — Continuity Generalization under Unseen Perturbations

## Question

V75 showed that a policy can act after perturbation and recover self-prediction advantage.

But that result could still be tied to the perturbation regime used for training.

> Does the policy learn a state-dependent rule that generalizes to perturbation magnitudes never seen during training?

## Design

V76 explicitly separates **training** and **generalization**.

The main policy is trained only with perturbation magnitudes:

~~~text
0.25 and 0.75
~~~

always using both signs.

Evaluation uses:

- **in-domain:** 0.25 and 0.75;
- **OOD:** 0.35, 0.55, and 0.85.

Perturbation magnitude is not supplied as a feature. The policy sees only dynamic state available to its self-model.

## Exposure control

A narrow policy is also trained using only perturbation magnitude 0.50.

This serves as a limited-exposure control to ask whether a policy trained on a single regime behaves similarly when magnitude changes.

## Objective

Training objective remains:

~~~text
self-prediction gain
=
persistence error
−
self-model error
~~~

No continuity label is provided.

Continuity is calculated only as a secondary endpoint:

~~~text
continuity = 1 / (1 + |current_state - pre_perturbation_state|)
~~~

## Protocol

Each condition:

1. starts from an independent but pairable seed;
2. runs the same warm-up;
3. applies a controlled perturbation;
4. removes semantic input from the probe;
5. runs multiple recovery steps;
6. uses the same seed for generalized policy, narrow policy, blinded state, fixed policy, and random selection.

Both policies are saved and reloaded without retraining before evaluation.

## Endpoints

### Primary

**Post-perturbation self-prediction gain.**

V76 is especially focused on OOD conditions.

### Generalization

The generalized-policy advantage over random is computed in-domain and OOD:

~~~text
advantage = generalized_gain − random_gain
~~~

The retained OOD fraction relative to in-domain is also recorded.

### Secondary

- continuity index;
- narrow-policy comparison;
- blinded-state comparison;
- first-action sensitivity to the sign of an OOD 0.55 perturbation.

## Observed result

The GitHub Actions execution used 64 episodes per condition, 64 training episodes, 512 SelfObserver samples, and 12 recovery steps.

### Self-prediction gain

- generalized-policy mean gain, all conditions: **0.50016**;
- blinded-state gain: **-0.15113**;
- fixed-policy gain: **-0.13311**;
- random-selection gain: **0.18987**;
- generalized − random advantage in-domain: **0.30819**;
- generalized − random advantage OOD: **0.31170**;
- retained OOD fraction: **1.0114**;
- learned − random overall p-value: **0.00005**;
- learned − blinded overall p-value: **0.00005**;
- learned − fixed overall p-value: **0.00005**.

The generalized policy retained its self-prediction advantage when moving from trained perturbations (0.25, 0.75) to unseen perturbations (0.35, 0.55, 0.85).

### Narrow-exposure control

The policy trained only on perturbation 0.50 produced nearly the same result:

- generalized − narrow paired p-value: **1.0**;
- narrow-policy global mean gain: **0.50014**.

Under this harness and linear parameterization, expanding training perturbation variety did not produce an additional measurable advantage. V76 therefore supports the more specific claim that the learned policy already generalized to unseen perturbations, not that broader training diversity itself improved performance.

### State-dependent response

For an OOD perturbation of magnitude 0.55:

- first-action response with readable state: **100%**;
- blinded state: **0%**.

This shows that the policy retained behavioral sensitivity to internal state in a perturbation that did not appear during training.

### Continuity

Secondary continuity index:

- generalized policy: **0.80164**;
- random policy: **0.80667**;
- generalized − random paired p-value: **0.07230**.

Therefore V76 **does not demonstrate a robust continuity advantage over random selection**. The reproduced effect is self-prediction generalization, not demonstrated autonomous priority for continuity.

## What a favorable result would show

A favorable result would be retention of self-prediction advantage under OOD perturbations, especially relative to blinded state, fixed policy, random selection, and a single-regime training policy.

That would support **functional generalization of the self-prediction policy to unseen perturbations**.

It would not show that the AI discovered on its own that it should preserve continuity.

## Boundary

The goal of recovering self-prediction remains an explicit protocol choice.

V76 therefore does not convert continuity into an autonomous value and does not establish subjective experience.

Its role is to separate:

1. behavior tied to a specific perturbation regime;
2. a more general state-dependent rule reusable under novel perturbations.

</details>