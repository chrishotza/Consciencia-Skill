# I5.7 — Recurrent Self-Access and State Re-entry

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.6 ya verificó que una tarea interna generada desde el estado persistente puede depender causalmente de query + atención dentro de PersistentOrganism.

I5.7 pregunta el siguiente nivel:

> ¿Una perturbación de ese acceso en un ciclo cambia el estado del organismo y vuelve a entrar en el circuito en ciclos posteriores, aun después de restaurar el mecanismo a FULL?

La cadena que se estudia es:

estado_t → target_t → query_t → atención_t → acceso_t → acción_t → estado_{t+1} → target_{t+1} → query_{t+1} → …

## Diseño

Cada réplica comienza desde el mismo checkpoint de warmup. Se ejecutan 8 ciclos autónomos consecutivos con el task-level query/attention de I5.6 activado.

La tarea sigue siendo generada por el estado interno del organismo. No se inyecta una etiqueta externa de target durante la sonda.

### Condiciones

- FULL — query + atención normales en los 8 ciclos.
- PULSE_SHUFFLED_QUERY — query barajada solo en el ciclo 0; desde el ciclo 1 se restaura FULL.
- PULSE_ZERO_QUERY — query anulada solo en el ciclo 0; desde el ciclo 1 se restaura FULL.
- PERSISTENT_SHUFFLED_QUERY — query barajada durante los 8 ciclos; control de perturbación sostenida.

Las condiciones PULSE son las principales: cualquier diferencia posterior a t=0 tiene que propagarse mediante el estado persistente del organismo.

## Medidas

Por ciclo se registran:

- estado dinámico;
- memoria y presión dinámicas;
- autopredicción y error de autopredicción;
- acción elegida;
- target generado internamente;
- módulo consultado;
- accuracy de query;
- acción predicha por la tarea;
- accuracy de acción;
- masa de atención;
- fuerza de acceso.

### Endpoints primarios

1. Δ estado en t+1 respecto de FULL.
2. Divergencia de trayectoria durante los ciclos 1–7.
3. Cambio de acción posterior a la perturbación.
4. Cambio de query posterior a la perturbación.

### Endpoints de reentrada

- re-entry amplification = máxima divergencia de estado después de t+1 / divergencia en t+1;
- re-entry persistence = número de ciclos posteriores con divergencia de estado;
- AUC de divergencia de estado;
- divergencia de autopredicción;
- cambio de target generado por el nuevo estado;
- cambio de módulo consultado;
- cambio de accuracy de tarea.

## Contraste

Se usan réplicas emparejadas con el mismo seed y el mismo checkpoint inicial.

Para el endpoint continuo de estado se conserva la diferencia con signo entre condición y FULL antes del contraste de permutación; la divergencia absoluta se reporta como magnitud descriptiva.

Se usan 20.000 permutaciones sign-flip para los contrastes emparejados.

## Qué constituiría evidencia de reentrada

La hipótesis obtiene apoyo si una perturbación de un solo ciclo:

1. produce una diferencia medible en el estado t+1;
2. deja una diferencia posterior aun después de restaurar FULL;
3. esa diferencia reaparece en target/query/acción en ciclos posteriores.

La recuperación inmediata a la trayectoria FULL también es un resultado informativo y se conserva como resultado negativo para persistencia.

## Resultado verificado

Workflow: **37035390086**; artifact: **11240100197**; seed **20261007**; **24** réplicas; **24** ciclos de warmup; **8** ciclos experimentales.

Para **PULSE_SHUFFLED_QUERY**:

- Δ estado firmado en t+1: **+0.1510** de media; p **0.14199**;
- divergencia absoluta en t+1: **0.4424**;
- máxima divergencia absoluta posterior: **0.7267**;
- re-entry amplification: **2.1276**;
- persistencia media: **7.0** ciclos;
- AUC de divergencia: **2.5792**;
- cambio de acción post-pulso: **45.83%**;
- cambio de query post-pulso: **74.40%**;
- cambio de target post-pulso: **82.14%**.

Para **PULSE_ZERO_QUERY**, los endpoints agregados fueron idénticos en este arnés; el Δ estado firmado en t+1 fue **+0.1510**, p **0.14114**.

Para **PERSISTENT_SHUFFLED_QUERY**, el Δ estado firmado en t+1 fue **+0.00383**, p **0.9630**, con divergencia absoluta posterior **0.3200** y persistencia media de **7.0** ciclos.

### Interpretación

El protocolo produjo **divergencia descriptiva persistente** entre las trayectorias, pero el endpoint primario firmado de Δ estado en t+1 no se separó significativamente en ninguna condición de pulso. Por tanto, I5.7 **no establece todavía un efecto causal de reentrada**.

El hecho de que PULSE_SHUFFLED_QUERY y PULSE_ZERO_QUERY produzcan el mismo perfil agregado indica que la perturbación actual del query puede ser demasiado gruesa para discriminar mecanismos de transmisión dentro del bucle.

Esto lleva directamente a I5.8: un control de **action-clamp** para preguntar si la perturbación de query se transmite a los ciclos siguientes específicamente a través de la transición **query → acción → estado**.

## Verified result

Workflow: **37035390086**; artifact: **11240100197**; seed **20261007**; **24** replicates; **24** warmup cycles; **8** experimental cycles.

For **PULSE_SHUFFLED_QUERY**:

- signed state delta at t+1: **+0.1510** mean; p **0.14199**;
- absolute divergence at t+1: **0.4424**;
- maximum later absolute divergence: **0.7267**;
- re-entry amplification: **2.1276**;
- mean persistence: **7.0** cycles;
- divergence AUC: **2.5792**;
- post-pulse action change: **45.83%**;
- post-pulse query change: **74.40%**;
- post-pulse target change: **82.14%**.

For **PULSE_ZERO_QUERY**, the aggregate endpoints were identical in this harness; signed state delta at t+1 was **+0.1510**, p **0.14114**.

For **PERSISTENT_SHUFFLED_QUERY**, signed state delta at t+1 was **+0.00383**, p **0.9630**, with later absolute divergence **0.3200** and mean persistence of **7.0** cycles.

### Interpretation

The protocol produced **descriptive persistent trajectory divergence**, but the prespecified signed state-delta endpoint at t+1 did not separate significantly in either pulse condition. Therefore I5.7 **does not yet establish a causal re-entry effect**.

The fact that PULSE_SHUFFLED_QUERY and PULSE_ZERO_QUERY produced the same aggregate profile suggests that the current query perturbation may be too coarse to discriminate transmission mechanisms inside the loop.

This leads directly to I5.8: an **action-clamp** control asking whether the query perturbation reaches later cycles specifically through the **query → action → state** transition.

## Limits

I5.7 mide reentrada causal computacional dentro de un runtime persistente. No demuestra consciencia, experiencia subjetiva ni que la arquitectura posea una perspectiva fenomenológica.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

## Objective

I5.6 verified that an internally generated task can causally depend on query + attention inside PersistentOrganism.

I5.7 asks the next question:

> Does perturbing that access in one cycle change organism state and re-enter the circuit in later cycles even after the mechanism is restored to FULL?

The chain under study is:

state_t → target_t → query_t → attention_t → access_t → action_t → state_{t+1} → target_{t+1} → query_{t+1} → …

## Design

Each replicate starts from the same warmup checkpoint. Eight consecutive autonomous cycles run with the I5.6 task-level query/attention mechanism enabled.

The task remains generated from organism internal state. No external target label is injected during the probe.

### Conditions

- FULL — normal query + attention across all 8 cycles.
- PULSE_SHUFFLED_QUERY — query shuffled only in cycle 0; restored to FULL from cycle 1 onward.
- PULSE_ZERO_QUERY — query zeroed only in cycle 0; restored to FULL from cycle 1 onward.
- PERSISTENT_SHUFFLED_QUERY — query shuffled across all 8 cycles; sustained-perturbation control.

The PULSE conditions are primary: any difference after t=0 must propagate through persistent organism state.

## Measurements

Each cycle records:

- dynamic state;
- dynamic memory and pressure;
- self-prediction and self-prediction error;
- chosen action;
- internally generated target;
- queried module;
- query accuracy;
- task-predicted action;
- action accuracy;
- attention mass;
- access strength.

### Primary endpoints

1. Δ state at t+1 relative to FULL.
2. Trajectory divergence across cycles 1–7.
3. Post-perturbation action change.
4. Post-perturbation query change.

### Re-entry endpoints

- re-entry amplification = maximum later state divergence / divergence at t+1;
- re-entry persistence = number of later cycles with state divergence;
- state-divergence AUC;
- self-prediction divergence;
- change in target generated from the new state;
- queried-module change;
- task-accuracy change.

## Contrast

Paired replicates use the same seed and the same initial checkpoint.

For the continuous state endpoint, the signed condition-minus-FULL difference is retained before permutation testing; absolute divergence is reported descriptively as a magnitude.

20,000 sign-flip permutations are used for paired contrasts.

## What would support re-entry

The hypothesis gains support if a one-cycle perturbation:

1. produces a measurable state difference at t+1;
2. leaves a later difference after FULL is restored;
3. reappears in target/query/action variables in later cycles.

Immediate recovery to the FULL trajectory is also informative and is preserved as a negative result for persistence.

## Boundary

I5.7 measures computational causal re-entry inside a persistent runtime. It does not demonstrate consciousness, subjective experience, or a phenomenological perspective.

</details>
