<a id="espanol"></a>

# V77 — Generalización ante perturbaciones de estructura no vista

## Pregunta

V76 mostró que una política de recuperación de autopredicción puede generalizar cuando cambia la magnitud de la perturbación.

Todavía quedaba una posibilidad: que la política funcione porque aprende una respuesta ligada principalmente al estado final después de un desplazamiento simple.

V77 cambia la **estructura causal de la perturbación** manteniendo constante su magnitud objetivo.

> ¿Puede la política conservar la recuperación de autopredicción cuando la perturbación cambia de forma temporal y causal, aunque el estado terminal después de la intervención sea el mismo?

## Diseño

La política se entrena únicamente con:

single_impulse

Una perturbación instantánea de magnitud 0.50 y signo aleatorio.

La evaluación incluye:

- **in-domain:** single_impulse;
- **OOD:** split_impulse, reversal_pulse, delayed_impulse.

En las cuatro condiciones la intervención se construye para terminar en el mismo estado objetivo:

estado objetivo = estado previo + desplazamiento

con desplazamiento de magnitud 0.50.

Lo que cambia entre estructuras es la trayectoria previa al estado terminal y, por tanto, variables internas latentes como el estado anterior, memoria y presión.

## Estructuras OOD

### split_impulse

La perturbación se divide en dos pasos, con una transición dinámica intermedia.

### reversal_pulse

La dinámica recibe primero un desplazamiento de mayor magnitud y después una corrección en dirección opuesta para terminar en el mismo estado objetivo.

### delayed_impulse

La dinámica realiza primero una transición interna sin perturbación y solo después recibe el desplazamiento.

## Objetivo

El objetivo de entrenamiento continúa siendo exclusivamente:

ganancia de autopredicción
=
error de persistencia
−
error del modelo de sí

No se proporciona una etiqueta de continuidad ni una etiqueta de tipo de perturbación.

## Protocolo

Cada réplica:

1. entrena el SelfObserver;
2. entrena la SelfPolicy exclusivamente con single_impulse;
3. guarda y recarga la política sin reentrenamiento;
4. construye condiciones emparejadas con la misma semilla base;
5. ejecuta una de las cuatro estructuras de perturbación;
6. verifica el objetivo terminal de la intervención;
7. ejecuta recuperación durante 12 pasos;
8. compara política aprendida, estado cegado, política fija y selección aleatoria.

La sonda no recibe entrada semántica.

## Endpoint primario

**Ganancia media de autopredicción durante la recuperación.**

El foco de V77 es especialmente el conjunto OOD: si la política conserva la ventaja cuando la perturbación ya no tiene la misma estructura temporal con la que fue entrenada.

También se calcula la retención:

ventaja OOD / ventaja in-domain

## Endpoints secundarios

- índice de continuidad;
- comparación con estado cegado;
- política fija;
- selección aleatoria;
- tasa de respuestas distintas al signo de una perturbación reversal_pulse;
- error entre el estado terminal de la intervención y el estado objetivo.

## Resultado observado

La ejecución corregida de GitHub Actions completó **64 réplicas por condición**, con **64 episodios de entrenamiento**, **512 muestras del SelfObserver** y **12 pasos de recuperación**. La política fue guardada y recargada sin reentrenamiento.

### Endpoint primario

Sobre todas las condiciones:

- ganancia media de autopredicción, política aprendida: **0.2377583**;
- estado cegado: **-0.1917033**;
- política fija: **-0.1566228**;
- selección aleatoria: **0.0632567**;
- aprendido − cegado, p emparejada: **0.00005**;
- aprendido − fijo, p emparejada: **0.00005**;
- aprendido − aleatorio, p emparejada: **0.00005**.

La ventaja aprendida frente a aleatorio fue:

- **in-domain:** 0.1715437;
- **OOD:** 0.1754876;
- retención OOD/in-domain: **1.0230**.

Por condición:

| Estructura | Ganancia aprendida | Ganancia aleatoria |
|---|---:|---:|
| single_impulse | 0.2439115 | 0.0723678 |
| split_impulse | 0.2341456 | 0.0764841 |
| reversal_pulse | 0.2352617 | 0.0547020 |
| delayed_impulse | 0.2377144 | 0.0494728 |

### Endpoints secundarios

El índice de continuidad no mostró una ventaja diferenciable:

- continuidad aprendida: **0.7926861**;
- continuidad aleatoria: **0.7950760**;
- p emparejada: **0.48033**.

La respuesta de primera acción dependiente del estado en la estructura OOD reversal_pulse fue:

- política con estado: **100%**;
- política con estado cegado: **0%**.

El error entre el estado inmediatamente posterior a la intervención y el objetivo terminal de la intervención fue **0.0** en todas las réplicas.

### Interpretación

V77 respalda que una política entrenada únicamente con single_impulse puede conservar una ventaja de autopredicción cuando la perturbación adopta estructuras temporales y causales no vistas durante el aprendizaje. La ventaja OOD no se redujo respecto de la condición in-domain bajo este arnés.

Esto es una **generalización computacional de la política de autopredicción**, no una demostración de que el organismo posea un valor autónomo de continuidad.

Además, el índice de continuidad como endpoint secundario no se separó de la selección aleatoria. Por tanto, el resultado fuerte de V77 es la **generalización de autopredicción**, no una preferencia demostrada por mantener continuidad en el sentido conductual más amplio.

## Qué significaría un resultado favorable

Un resultado favorable respaldaría una propiedad más fuerte que V76:

**la política de autopredicción no depende exclusivamente de la forma exacta de perturbación utilizada durante el aprendizaje y puede reutilizarse ante una estructura causal nueva.**

Eso seguiría siendo una propiedad computacional del protocolo.

## Límite

La política sigue siendo entrenada para maximizar una utilidad definida externamente: la ganancia de autopredicción.

Por tanto, V77 no demostraría que el organismo haya creado autónomamente el concepto de continuidad, ni que experimente la perturbación como una amenaza, ni que exista experiencia subjetiva.

Su función es separar:

1. recuperación aprendida para un tipo concreto de perturbación;
2. recuperación generalizada ante **formas causales nuevas de perturbación**.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V77 — Generalization to Unseen Perturbation Structures

## Question

V76 showed that a self-prediction recovery policy can generalize when perturbation magnitude changes.

Another possibility remained: the policy might work mainly by learning a response tied to the final state after a simple displacement.

V77 changes the **causal structure of the perturbation** while keeping its target magnitude constant.

> Can the policy preserve self-prediction recovery when perturbation form changes temporally and causally, even though the post-intervention terminal state is the same?

## Design

The policy is trained only with:

single_impulse

An instantaneous perturbation of magnitude 0.50 and random sign.

Evaluation includes:

- **in-domain:** single_impulse;
- **OOD:** split_impulse, reversal_pulse, delayed_impulse.

All four interventions are constructed to end at the same target state:

target state = pre-intervention state + displacement

with displacement magnitude 0.50.

What changes across structures is the trajectory before the terminal state and therefore latent variables such as previous state, memory, and pressure.

## OOD structures

### split_impulse
The perturbation is divided across two steps with an intermediate dynamic transition.

### reversal_pulse
The dynamics first receive a larger displacement and then an opposite-direction correction ending at the same target state.

### delayed_impulse
The dynamics first perform an internal transition without perturbation and only afterward receive the displacement.

## Objective

Training remains exclusively:

self-prediction gain = persistence error − self-model error

No continuity or perturbation-type label is provided.

## Protocol

Each replicate:

1. trains SelfObserver;
2. trains SelfPolicy exclusively with single_impulse;
3. saves and reloads policy without retraining;
4. constructs matched conditions with the same base seed;
5. executes one perturbation structure;
6. verifies the terminal intervention target;
7. runs 12 recovery steps;
8. compares learned policy, blinded state, fixed policy, and random selection.

No semantic input is used during the probe.

## Primary endpoint

**Mean self-prediction gain during recovery.**

The focus is especially OOD: whether the policy retains its advantage when perturbation no longer has the temporal structure used for training.

OOD/in-domain advantage retention is also calculated.

## Secondary endpoints

- continuity index;
- blinded-state comparison;
- fixed-policy comparison;
- random-selection comparison;
- first-action response to perturbation sign under reversal_pulse;
- error between terminal intervention state and target state.

## Observed result

The corrected GitHub Actions run completed **64 replicates per condition**, **64 training episodes**, **512 SelfObserver samples**, and **12 recovery steps**. The policy was saved and reloaded without retraining.

### Primary endpoint

Across all conditions:

- learned policy mean self-prediction gain: **0.2377583**;
- blinded-state gain: **-0.1917033**;
- fixed-policy gain: **-0.1566228**;
- random-selection gain: **0.0632567**;
- learned − blinded paired p-value: **0.00005**;
- learned − fixed paired p-value: **0.00005**;
- learned − random paired p-value: **0.00005**.

Learned-versus-random advantage:

- **in-domain:** 0.1715437;
- **OOD:** 0.1754876;
- OOD/in-domain retention: **1.0230**.

By condition:

| Structure | Learned gain | Random gain |
|---|---:|---:|
| single_impulse | 0.2439115 | 0.0723678 |
| split_impulse | 0.2341456 | 0.0764841 |
| reversal_pulse | 0.2352617 | 0.0547020 |
| delayed_impulse | 0.2377144 | 0.0494728 |

### Secondary endpoints

Continuity showed no differentiable advantage:

- learned continuity: **0.7926861**;
- random continuity: **0.7950760**;
- paired p-value: **0.48033**.

First-action state-dependent response under OOD reversal_pulse:

- state-readable policy: **100%**;
- blinded-state policy: **0%**.

Terminal intervention-state error was **0.0** in all replicates.

### Interpretation

V77 supports that a policy trained only on single_impulse can retain self-prediction advantage when perturbation adopts unseen temporal and causal structures. OOD advantage was not reduced relative to in-domain under this harness.

This is **computational generalization of the self-prediction policy**, not evidence that the organism has an autonomous continuity value.

Continuity as a secondary endpoint did not separate from random. The strong result is OOD self-prediction generalization, not demonstrated broad behavioral prioritization of continuity.

## What a favorable result would show

A favorable result supports a property stronger than V76:

**the self-prediction policy does not depend exclusively on the exact perturbation form used during training and can be reused under a novel causal structure.**

This remains a computational property of the tested protocol.

## Boundary

The policy is still trained to maximize an externally defined utility: self-prediction gain.

V77 therefore would not demonstrate that the organism autonomously created a concept of continuity, experiences perturbation as a threat, or has subjective experience.

Its role is to separate learning for one perturbation structure from generalization to **new causal forms of perturbation**.

</details>