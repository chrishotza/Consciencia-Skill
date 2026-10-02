# I5.8 — Action-Clamp Mediation of Recurrent Self-Access

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.7 produjo divergencia descriptiva después de una perturbación de query, pero no separó significativamente el endpoint primario de estado firmado en t+1.

I5.8 prueba una pregunta más específica:

> ¿La perturbación de query se transmite hacia los ciclos posteriores a través de la transición query → acción → estado?

La estrategia mantiene la perturbación de query durante el ciclo 0, pero en una condición de control fuerza la acción aplicada a ser exactamente la acción que habría elegido FULL en ese mismo checkpoint.

## Condiciones

- FULL — query y acción normales durante todo el horizonte.
- FULL_ACTION_CLAMP — FULL, pero la acción del ciclo 0 se fuerza a la acción FULL de referencia.
- PULSE_SHUFFLED_QUERY — query barajada solo en el ciclo 0.
- PULSE_SHUFFLED_QUERY_ACTION_CLAMP — query barajada en el ciclo 0, pero la acción aplicada se fuerza a la acción FULL de referencia.
- PERSISTENT_SHUFFLED_QUERY — query barajada durante todos los ciclos.

En los brazos de pulso, desde el ciclo 1 el query vuelve a FULL.

## Hipótesis operacional

Si el efecto de I5.7 se transmite principalmente por:

query_t → acción_t → estado_{t+1}

entonces PULSE_SHUFFLED_QUERY_ACTION_CLAMP debería reducir la divergencia posterior respecto de PULSE_SHUFFLED_QUERY.

Además, FULL_ACTION_CLAMP debe permanecer prácticamente alineado con FULL; de lo contrario, el propio mecanismo de clamp introduciría una perturbación espuria.

## Endpoint primario

Diferencia emparejada entre:

|estado_{t+1}^{PULSE}| − |estado_{t+1}^{PULSE+CLAMP}|

y el mismo contraste acumulado sobre la AUC de divergencia posterior.

Un valor positivo indica menor divergencia cuando la acción del ciclo perturbado se mantiene igual a FULL.

## Endpoints secundarios

- divergencia absoluta de estado en t+1;
- AUC de divergencia;
- amplificación de reentrada;
- persistencia de divergencia;
- cambio de query posterior;
- cambio de target posterior;
- cambio de acción seleccionada;
- diferencia entre acción seleccionada y acción aplicada;
- contraste FULL vs FULL_ACTION_CLAMP.

## Diseño estadístico

- 24 réplicas emparejadas;
- 24 ciclos de warmup;
- 8 ciclos experimentales;
- mismo seed por réplica;
- mismo checkpoint inicial entre condiciones;
- 20.000 permutaciones sign-flip para los contrastes emparejados.

El contraste principal se realiza sobre la diferencia entre las dos condiciones de pulso, no sobre una conclusión previa de I5.7.

## Resultado verificado

Workflow: **37036909691**; artifact: **11241340710**; seed **20261008**; **24** réplicas; **24** ciclos de warmup; **8** ciclos experimentales.

- **FULL_ACTION_CLAMP vs FULL:** Δ estado en t+1 **0.0**, p **1.0**.
- **PULSE_SHUFFLED_QUERY − PULSE_SHUFFLED_QUERY_ACTION_CLAMP**, estado en t+1: **0.42596** de media, p **4.99975×10⁻⁵**.
- Diferencia de AUC post-pulso: **2.10472**, p **4.99975×10⁻⁵**.
- Divergencia t+1 del pulso: **0.42596**.
- Divergencia t+1 del pulso con clamp: **0.0**.
- Cambio post-pulso de acción en el pulso: **47.62%**; con clamp: **0%**.
- Cambio post-pulso de query en el pulso: **73.21%**; con clamp: **0%**.
- Cambio post-pulso de target en el pulso: **82.14%**; con clamp: **0%**.

### Interpretación

En este arnés determinista, el action-clamp eliminó por completo la divergencia de estado producida por la perturbación de query y el contraste pulse vs clamp fue significativo tanto en t+1 como en la AUC posterior.

Además, `FULL_ACTION_CLAMP` quedó idéntico a FULL en el endpoint de estado, por lo que el propio clamp no introdujo una separación detectable.

El resultado es **consistente con una mediación por la acción aplicada**: bajo este runtime, la perturbación de query solo produjo la divergencia observada cuando pudo modificar la acción que entró en la dinámica.

Esto todavía no demuestra consciencia ni reentrada fenomenológica. Tampoco demuestra que la acción sea la única ruta posible fuera de este arnés. La siguiente prueba será un control de **action replay**: tomar la secuencia de acciones generada por el pulso y reproducirla bajo query FULL para comprobar si la trayectoria din## Verified result

Workflow: **37036909691**; artifact: **11241340710**; seed **20261008**; **24** replicates; **24** warmup cycles; **8** experimental cycles.

- **FULL_ACTION_CLAMP vs FULL:** state delta at t+1 **0.0**, p **1.0**.
- **PULSE_SHUFFLED_QUERY − PULSE_SHUFFLED_QUERY_ACTION_CLAMP**, state at t+1: **0.42596** mean, p **4.99975×10⁻⁵**.
- Post-pulse AUC difference: **2.10472**, p **4.99975×10⁻⁵**.
- Pulse t+1 divergence: **0.42596**.
- Pulse action-clamp t+1 divergence: **0.0**.
- Post-pulse action change in pulse: **47.62%**; with clamp: **0%**.
- Post-pulse query change in pulse: **73.21%**; with clamp: **0%**.
- Post-pulse target change in pulse: **82.14%**; with clamp: **0%**.

### Interpretation

Under this deterministic harness, action-clamping completely removed the state divergence produced by the query perturbation, and the pulse vs clamp contrast was significant both at t+1 and across the later AUC.

`FULL_ACTION_CLAMP` also remained identical to FULL on the state endpoint, so the clamp itself did not introduce a detectable separation.

The result is **consistent with action-mediated propagation**: in this runtime, the observed query perturbation produced the measured state divergence only when it could alter the action entering the dynamics.

This still does not demonstrate consciousness or phenomenological re-entry, nor does it prove action is the only possible route outside this harness. The next test is an **action-replay** control: take the action sequence generated by the pulse and replay it under FULL query to test whether the dynamic trajectory can be reconstructed from that sequence alone.
ámica puede reconstruirse únicamente desde esa secuencia.
## Límites

I5.8 prueba una ruta causal computacional dentro de PersistentOrganism. Un resultado de mediación no demostraría consciencia ni experiencia subjetiva; demostraría, como máximo, que la intervención de query se transmite a través del canal acción → estado bajo este arnés.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

## Objective

I5.7 produced descriptive post-perturbation divergence, but the prespecified signed state endpoint at t+1 did not separate significantly.

I5.8 asks a more specific question:

> Does the query perturbation propagate into later cycles through the query → action → state transition?

The strategy keeps the query perturbation in cycle 0, while a control condition forces the applied action to be exactly the action FULL would have selected from the same checkpoint.

## Conditions

- FULL — normal query and action throughout the horizon.
- FULL_ACTION_CLAMP — FULL, but cycle-0 action is forced to the FULL reference action.
- PULSE_SHUFFLED_QUERY — query shuffled only in cycle 0.
- PULSE_SHUFFLED_QUERY_ACTION_CLAMP — query shuffled in cycle 0, but the applied action is forced to the FULL reference action.
- PERSISTENT_SHUFFLED_QUERY — query shuffled throughout all cycles.

In the pulse arms, query returns to FULL from cycle 1 onward.

## Operational hypothesis

If the I5.7 effect is transmitted mainly through:

query_t → action_t → state_{t+1}

then PULSE_SHUFFLED_QUERY_ACTION_CLAMP should reduce later divergence relative to PULSE_SHUFFLED_QUERY.

FULL_ACTION_CLAMP should remain essentially aligned with FULL; otherwise the clamp itself would introduce an artifact.

## Primary endpoint

Paired difference:

|state_{t+1}^{PULSE}| − |state_{t+1}^{PULSE+CLAMP}|

plus the analogous contrast in post-pulse trajectory-divergence AUC.

A positive value means the action clamp reduces divergence from FULL.

## Secondary endpoints

- absolute state divergence at t+1;
- divergence AUC;
- re-entry amplification;
- divergence persistence;
- later query change;
- later target change;
- selected-action change;
- selected vs applied action difference;
- FULL vs FULL_ACTION_CLAMP contrast.

## Statistical design

- 24 paired replicates;
- 24 warmup cycles;
- 8 experimental cycles;
- same seed per replicate;
- same initial checkpoint across conditions;
- 20,000 sign-flip permutations for paired contrasts.

The primary contrast is the difference between the two pulse conditions, rather than a re-test of the I5.7 null.

## Boundary

I5.8 tests a computational causal pathway inside PersistentOrganism. A mediation result would not demonstrate consciousness or subjective experience; at most, it would show that the query intervention propagates through the action → state channel under this harness.

</details>
