<a id="espanol"></a>

# V75 — Continuidad activa bajo perturbación

## Pregunta

V74 mostró que una política puede seleccionar trayectorias utilizando la ganancia de autopredicción como criterio, eliminando el atractor externo de la función objetivo principal.

V75 introduce una perturbación sobre el estado interno y convierte la selección en un proceso de recuperación activa.

> ¿Puede una política basada en el modelo de sí elegir, durante varios pasos posteriores a una perturbación, trayectorias que recuperen la ventaja predictiva del propio modelo de sí?

## Hipótesis operacional

La perturbación desplaza deliberadamente el estado dinámico fuera de la trayectoria que el organismo venía recorriendo.

La política no recibe una etiqueta de "estado correcto". Su objetivo primario sigue siendo:

\`\`\`text
ganancia de autopredicción
=
error de persistencia
−
error del modelo de sí
\`\`\`

pero ahora se entrena y se evalúa específicamente en el régimen posterior a perturbación.

## Protocolo

Cada réplica:

1. entrena un SelfObserver;
2. entrena una SelfPolicy con transiciones posteriores a perturbaciones de signo aleatorio;
3. persiste la política;
4. la recarga sin reentrenamiento;
5. ejecuta una fase de vigilia dinámica de calentamiento;
6. aplica una perturbación controlada de magnitud 0.50 al estado interno;
7. elimina cualquier entrada semántica de la sonda;
8. permite varios pasos de recuperación activa;
9. compara política con estado propio, la misma política con estado cegado, política fija y selección aleatoria.

## Endpoints

### Primario

**Ganancia media de autopredicción durante la recuperación.**

La pregunta es si el organismo puede recuperar funcionalmente la ventaja de su propio modelo después de haber sido perturbado.

### Secundario

**Índice de continuidad.**

\`\`\`text
continuidad = 1 / (1 + |estado_actual - estado_pre_perturbación|)
\`\`\`

Este índice no forma parte del objetivo de entrenamiento. Sirve para preguntar si una política entrenada para recuperar autopredicción produce además una conservación medible de continuidad interna.

También se registra la **respuesta dependiente del estado**: si el signo de la perturbación cambia la primera acción elegida. Se calcula además con el estado cegado como control.

## Controles

- política aprendida con acceso al estado;
- misma política con estado dinámico cegado;
- selector fijo existente;
- selección aleatoria;
- comparación emparejada con la misma semilla y perturbación;
- intercambio de signo de la perturbación para evaluar sensibilidad causal de la decisión.

## Qué cambia respecto de V74

V74 preguntó si una política puede aprender a seleccionar utilizando ganancia de autopredicción.

V75 pregunta algo más exigente: si, después de romper deliberadamente la trayectoria interna, el sistema puede **actuar durante varios pasos para recuperar su propia capacidad de predecirse**.

La continuidad no se impone como etiqueta de entrenamiento. Se observa como endpoint secundario.

## Límite

El deseo operativo de recuperar autopredicción sigue siendo una decisión del protocolo.

Por tanto, un resultado positivo no demostraría que el organismo haya creado autónomamente un valor de continuidad ni que exista experiencia subjetiva.

El resultado válido sería más acotado: evidencia de **mantenimiento activo de la autopredicción bajo perturbación**, con una posible consecuencia secundaria sobre la continuidad interna.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V75 — Active Continuity under Perturbation

## Question

V74 showed that a policy can select trajectories using self-prediction gain as its criterion, removing the external attractor from the primary objective.

V75 perturbs internal state and turns selection into active recovery.

> Can a self-model-based policy choose trajectories for several steps after perturbation that recover the self-model's predictive advantage?

## Operational hypothesis

The perturbation deliberately moves dynamic state away from the trajectory previously occupied by the organism.

The policy receives no “correct state” label. Its primary objective remains:

~~~text
self-prediction gain
=
persistence error
−
self-model error
~~~

but training and evaluation now occur specifically in the post-perturbation regime.

## Protocol

Each replicate:

1. trains a SelfObserver;
2. trains a SelfPolicy with post-perturbation transitions of random sign;
3. persists the policy;
4. reloads it without retraining;
5. runs a dynamic WAKE warm-up;
6. applies a controlled perturbation of magnitude 0.50 to internal state;
7. removes semantic input from the probe;
8. allows several active-recovery steps;
9. compares policy with self-state access, the same policy with blinded state, the fixed policy, and random selection.

## Endpoints

### Primary

**Mean self-prediction gain during recovery.**

The question is whether the organism can functionally recover its own predictive advantage after perturbation.

### Secondary

**Continuity index.**

~~~text
continuity = 1 / (1 + |current_state - pre_perturbation_state|)
~~~

This index is not part of the training objective. It tests whether a policy trained to recover self-prediction also produces measurable preservation of internal continuity.

State-dependent response is also recorded: whether perturbation sign changes the first chosen action. The same is calculated with blinded state as control.

## Controls

- learned policy with state access;
- same policy with dynamic state blinded;
- existing fixed selector;
- random selection;
- paired comparison with the same seed and perturbation;
- perturbation-sign exchange to test causal sensitivity of the decision.

## What changes versus V74

V74 asks whether a policy can learn to select using self-prediction gain.

V75 asks the stronger question: after deliberately breaking internal trajectory, can the system **act over several steps to recover its own predictive capability**?

Continuity is not imposed as a training label. It is observed as a secondary endpoint.

## Boundary

The operational desire to recover self-prediction is still a protocol decision.

A positive result would therefore not show that the organism autonomously created a continuity value or that subjective experience exists.

The narrower valid result would be evidence of **active self-prediction maintenance under perturbation**, with a possible secondary effect on internal continuity.

</details>