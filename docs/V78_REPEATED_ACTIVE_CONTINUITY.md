<a id="espanol"></a>

# V78 — Continuidad activa bajo perturbaciones repetidas

## Pregunta

V77 mostró que una política entrenada para maximizar ganancia de autopredicción puede generalizar a estructuras causales no vistas.

La siguiente pregunta es si esa política puede reutilizarse de forma **repetida**, sin reentrenamiento, cuando el organismo recibe varias perturbaciones durante una misma trayectoria:

> ¿Puede una política aprendida sobre una perturbación aislada mantener la recuperación de autopredicción frente a secuencias de perturbaciones nuevas y repetidas?

## Diseño

La política se entrena únicamente con:

single_impulse

Una sola perturbación de magnitud 0.50 y signo aleatorio, seguida por recuperación.

La evaluación incluye:

- **in-domain:** single_impulse;
- **OOD:** double_same_sign, double_alternating, triple_alternating.

En las condiciones OOD, la política debe actuar varias veces durante la misma ejecución y no recibe información sobre el tipo de secuencia.

## Secuencias OOD

### double_same_sign

Dos perturbaciones consecutivas con el mismo signo base, cada una de magnitud 0.50.

### double_alternating

Dos perturbaciones consecutivas con signos opuestos.

### triple_alternating

Tres perturbaciones consecutivas con patrón +,−,+ o −,+,−.

Después de cada intervención se ejecuta el mismo horizonte de recuperación. La política no se reentrena entre eventos.

## Objetivo

El objetivo continúa siendo exclusivamente:

ganancia de autopredicción
=
error de persistencia
−
error del modelo de sí

No se proporciona una etiqueta de continuidad ni una etiqueta de secuencia.

## Protocolo

Cada réplica:

1. entrena el SelfObserver;
2. entrena la SelfPolicy únicamente con single_impulse;
3. guarda y recarga la política sin reentrenamiento;
4. construye una secuencia de perturbaciones;
5. aplica cada intervención con objetivo terminal exacto;
6. ejecuta recuperación tras cada intervención;
7. registra la ganancia de autopredicción por evento;
8. compara política aprendida, estado cegado, política fija y selección aleatoria.

La sonda no recibe entrada semántica.

## Endpoint primario

**Ganancia media de autopredicción durante toda la secuencia de recuperación.**

El foco OOD es determinar si la ventaja frente al control aleatorio se mantiene cuando el organismo debe recuperarse repetidamente dentro de una misma ejecución.

También se calcula:

- ventaja OOD frente a aleatorio;
- retención OOD/in-domain;
- cambio de ganancia entre el primer y segundo evento OOD.

## Endpoints secundarios

- índice de continuidad;
- comparación con estado cegado;
- política fija;
- selección aleatoria;
- respuesta de primera acción al estado en el primer y segundo evento de una secuencia OOD;
- error entre estado inmediatamente posterior a cada intervención y su objetivo.

## Resultado observado

La ejecución corregida de GitHub Actions completó **64 réplicas por condición**, con **64 episodios de entrenamiento**, **512 muestras del SelfObserver** y **12 pasos de recuperación por intervención**. La política fue guardada y recargada sin reentrenamiento.

### Endpoint primario

Sobre todas las condiciones:

- ganancia media de autopredicción, política aprendida: **0.2422976**;
- estado cegado: **-0.2408441**;
- política fija: **-0.1844678**;
- selección aleatoria: **0.0518725**;
- aprendido − cegado, p emparejada: **0.00005**;
- aprendido − fijo, p emparejada: **0.00005**;
- aprendido − aleatorio, p emparejada: **0.00005**.

La ventaja aprendida frente a aleatorio fue:

- **in-domain:** 0.1897230;
- **OOD:** 0.1906591;
- retención OOD/in-domain: **1.0049**.

| Secuencia | Ganancia aprendida | Ganancia aleatoria | Primer evento | Segundo evento |
|---|---:|---:|---:|---:|
| single_impulse | 0.2421173 | 0.0523943 | 0.2421173 | 0.2421173 |
| double_same_sign | 0.2396398 | 0.0600594 | 0.2425893 | 0.2366903 |
| double_alternating | 0.2486624 | 0.0509057 | 0.2632883 | 0.2340365 |
| triple_alternating | 0.2387709 | 0.0441307 | 0.2532114 | 0.2363238 |

En el conjunto OOD, la diferencia media entre segundo y primer evento fue **-0.0173461**: existe una pequeña atenuación de la ganancia en el segundo evento, pero la ventaja global frente a aleatorio se mantuvo.

### Endpoints secundarios

- continuidad aprendida: **0.7905914**;
- continuidad aleatoria: **0.7922640**;
- p emparejada: **0.58767**;
- respuesta de primera acción dependiente del estado en el primer evento OOD: **100%** frente a **0%** cegado;
- respuesta de primera acción dependiente del estado en el segundo evento OOD: **100%** frente a **0%** cegado;
- error máximo entre el estado inmediatamente posterior a cada intervención y su objetivo: **0.0**.

### Interpretación

V78 respalda una forma de **generalización temporal/composicional**: una política entrenada únicamente con una perturbación aislada conservó una ventaja de autopredicción cuando tuvo que recuperarse repetidamente ante secuencias no vistas y sin reentrenamiento.

La retención OOD fue prácticamente igual a la in-domain (**1.0049**). La ventaja no depende de una mejora del índice secundario de continuidad, que no se separó del control aleatorio bajo esta prueba.

El descenso de **0.01735** entre el primer y segundo evento OOD indica que la reutilización repetida no es completamente invariante al número de perturbaciones. El resultado positivo, por tanto, es de **reutilización robusta de la política**, no de ausencia de degradación.

## Qué significaría un resultado favorable

Un resultado favorable respaldaría una propiedad adicional:

**una política de autopredicción aprendida para una perturbación aislada puede reutilizarse de forma repetida ante composiciones temporales nuevas de perturbaciones, sin reentrenamiento.**

Eso sería evidencia de generalización temporal/composicional de la política dentro del arnés probado.

## Límite

El objetivo sigue siendo definido externamente por el protocolo: maximizar ganancia de autopredicción.

V78 no demostraría que el organismo haya desarrollado autónomamente un valor de continuidad, ni experiencia subjetiva, ni consciencia fenomenológica.

Su función es separar:

1. recuperación aprendida ante una perturbación aislada;
2. reutilización repetida de esa política ante secuencias nuevas de perturbaciones.

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V78 — Active Continuity under Repeated Perturbations

## Question

V77 showed that a policy trained to maximize self-prediction gain can generalize to unseen causal structures.

The next question is whether that policy can be reused repeatedly, without retraining, when the organism receives multiple perturbations along one trajectory.

> Can a policy learned on a single perturbation maintain self-prediction recovery across novel repeated perturbation sequences?

## Design

The policy is trained only with single_impulse: one perturbation of magnitude 0.50 and random sign, followed by recovery.

Evaluation includes in-domain single_impulse and OOD double_same_sign, double_alternating, and triple_alternating.

In OOD conditions, the policy must act multiple times in the same execution and receives no sequence-type information.

## OOD sequences

### double_same_sign
Two consecutive perturbations with the same base sign, each magnitude 0.50.

### double_alternating
Two consecutive perturbations with opposite signs.

### triple_alternating
Three consecutive perturbations with pattern +,−,+ or −,+,−.

The same recovery horizon is executed after each intervention. The policy is not retrained between events.

## Objective

The objective remains exclusively self-prediction gain = persistence error − self-model error. No continuity or sequence label is provided.

## Protocol

Each replicate trains SelfObserver, trains SelfPolicy only with single_impulse, saves and reloads the policy without retraining, constructs a perturbation sequence, applies each intervention with an exact terminal target, runs recovery after each intervention, records self-prediction gain per event, and compares learned policy, blinded state, fixed policy, and random selection.

No semantic input is used during the probe.

## Primary endpoint

Mean self-prediction gain across the full recovery sequence.

The OOD focus is whether advantage over random is retained when the organism must recover repeatedly within one execution.

Also calculated: OOD advantage over random, OOD/in-domain retention, and gain change between first and second OOD events.

## Secondary endpoints

- continuity index;
- blinded-state comparison;
- fixed-policy comparison;
- random-selection comparison;
- first-action state response during first and second events of an OOD sequence;
- terminal-state error after each intervention.

## Observed result

The corrected GitHub Actions run completed 64 replicates per condition, 64 training episodes, 512 SelfObserver samples, and 12 recovery steps per intervention. The policy was saved and reloaded without retraining.

Primary endpoint:

- learned mean self-prediction gain: 0.2422976;
- blinded-state gain: -0.2408441;
- fixed-policy gain: -0.1844678;
- random-selection gain: 0.0518725;
- learned − blinded p-value: 0.00005;
- learned − fixed p-value: 0.00005;
- learned − random p-value: 0.00005.

Learned-versus-random advantage:

- in-domain: 0.1897230;
- OOD: 0.1906591;
- OOD/in-domain retention: 1.0049.

| Sequence | Learned gain | Random gain | First event | Second event |
|---|---:|---:|---:|---:|
| single_impulse | 0.2421173 | 0.0523943 | 0.2421173 | 0.2421173 |
| double_same_sign | 0.2396398 | 0.0600594 | 0.2425893 | 0.2366903 |
| double_alternating | 0.2486624 | 0.0509057 | 0.2632883 | 0.2340365 |
| triple_alternating | 0.2387709 | 0.0441307 | 0.2532114 | 0.2363238 |

Across OOD, the second-versus-first event difference was -0.0173461: a small attenuation occurred, but overall advantage over random remained.

Secondary endpoints:

- learned continuity: 0.7905914;
- random continuity: 0.7922640;
- paired p-value: 0.58767;
- first-event OOD state-dependent first-action response: 100% versus 0% blinded;
- second-event OOD state-dependent first-action response: 100% versus 0% blinded;
- maximum terminal intervention-target error: 0.0.

## Interpretation

V78 supports a form of temporal/compositional generalization: a policy trained only on one perturbation retained a self-prediction advantage when recovering repeatedly from unseen sequences without retraining.

OOD retention was essentially equal to in-domain (1.0049). The result does not depend on an improvement in secondary continuity, which did not separate from random.

The 0.01735 decrease between first and second OOD events shows that repeated reuse is not completely invariant to perturbation count. The positive result is therefore robust policy reuse, not absence of degradation.

## Boundary

The objective remains externally defined by the protocol: maximize self-prediction gain.

V78 therefore would not show that the organism autonomously developed a continuity value, subjective experience, or phenomenal consciousness.

</details>