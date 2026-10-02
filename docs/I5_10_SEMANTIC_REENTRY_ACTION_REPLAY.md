# I5.10 — Semantic Re-entry Under Action Replay

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.9 mostró que, cuando la secuencia de acciones aplicadas queda fijada, la trayectoria dinámica del pulso se reconstruye exactamente bajo query FULL.

I5.10 separa ahora **dinámica** de **estado semántico**:

> ¿Dos organismos con la misma secuencia de acciones aplicadas pueden desarrollar modelos de sí diferentes debido únicamente a la diferencia de query, y puede esa diferencia semántica volver a entrar en la dinámica mediante el semantic self-model bridge?

## Condiciones

- FULL_BRIDGE_ON — query y acción normales; semantic self-model bridge activo.
- PULSE_SHUFFLED_QUERY_BRIDGE_ON — query barajada solo en ciclo 0; bridge activo.
- ACTION_REPLAY_FULL_QUERY_BRIDGE_ON — query FULL; se reproducen exactamente las acciones aplicadas por el pulso; bridge activo.
- ACTION_REPLAY_FULL_QUERY_BRIDGE_OFF — mismo action replay, pero semantic self-model bridge desactivado.

Todas las condiciones parten del mismo checkpoint.

El proveedor determinista genera el siguiente SELF_MODEL a partir del query_module registrado por el ciclo anterior. Esto hace explícita la ruta:

query anterior → modelo de sí siguiente → bridge semántico → dinámica siguiente.

## Endpoint primario

Diferencia entre PULSE_SHUFFLED_QUERY_BRIDGE_ON y ACTION_REPLAY_FULL_QUERY_BRIDGE_ON en:

1. divergencia del SELF_MODEL durante los ciclos posteriores;
2. Δ estado dinámico t+1;
3. AUC de divergencia de estado.

## Endpoint de mediación semántica

Se compara ACTION_REPLAY_FULL_QUERY_BRIDGE_ON frente a ACTION_REPLAY_FULL_QUERY_BRIDGE_OFF.

Si el bridge está transmitiendo el estado semántico, una diferencia entre esos brazos pese a idéntica secuencia de acciones aplicadas indica una ruta:

query → self-model → semantic bridge → state.

## Controles

- coincidencia exacta de acciones aplicadas;
- coincidencia del checkpoint inicial;
- mismo seed;
- persistencia de la diferencia de modelo de sí;
- versión del modelo de sí;
- módulo de query previo.

## Diseño estadístico

- 24 réplicas emparejadas;
- 24 ciclos de warmup;
- 8 ciclos experimentales;
- mismo seed por réplica;
- 20.000 permutaciones sign-flip para los endpoints continuos.

## Resultado verificado

Workflow: **37038527924**; artifact: **11240619196**; seed **20261010**; **24** réplicas; **24** ciclos de warmup; **8** ciclos experimentales.

- Coincidencia exacta de acciones aplicadas PULSE vs ACTION_REPLAY: **100%**.
- Divergencia post-pulso de SELF_MODEL entre PULSE y ACTION_REPLAY: **45.83%** de media.
- Δ estado PULSE vs ACTION_REPLAY en t+1: **0.09551** de media, p **4.99975×10⁻⁵**.
- AUC de divergencia de estado PULSE vs ACTION_REPLAY: **0.93484**, p **4.99975×10⁻⁵**.
- AUC de estado ACTION_REPLAY_BRIDGE_ON vs BRIDGE_OFF: **1.29205**, p **4.99975×10⁻⁵**.
- Diferencia máxima media de versión del modelo de sí: **2.29**.

### Interpretación

Con la secuencia de acciones aplicada exactamente igual entre PULSE y ACTION_REPLAY, las ejecuciones desarrollaron modelos de sí diferentes en una media del **45.83%** de los ciclos posteriores.

Además, con el semantic self-model bridge activo apareció una separación significativa del estado dinámico tanto frente al replay como frente al mismo replay con el bridge desactivado.

El resultado es consistente con una ruta causal computacional adicional:

**query → self-model → semantic self-model bridge → dinámica**

Esto es diferente de I5.9: allí la trayectoria dinámica era idéntica cuando solo se fijaba la secuencia de acciones. I5.10 muestra que, cuando el estado semántico tiene permiso para entrar en la dinámica, una diferencia de query puede sobrevivir a la igualación de acciones.

El resultado sigue estando limitado al proveedor determinista y al harness sintético. No demuestra consciencia ni experiencia subjetiva.

La siguiente prueba es liberar la acción después del primer ciclo y comprobar si esta diferencia semántico-dinám## Verified result

Workflow: **37038527924**; artifact: **11240619196**; seed **20261010**; **24** replicates; **24** warmup cycles; **8** experimental cycles.

- Exact applied-action match between PULSE and ACTION_REPLAY: **100%**.
- Post-pulse SELF_MODEL divergence between PULSE and ACTION_REPLAY: **45.83%** mean.
- PULSE vs ACTION_REPLAY state delta at t+1: **0.09551** mean, p **4.99975×10⁻⁵**.
- PULSE vs ACTION_REPLAY state-divergence AUC: **0.93484**, p **4.99975×10⁻⁵**.
- ACTION_REPLAY_BRIDGE_ON vs BRIDGE_OFF state AUC: **1.29205**, p **4.99975×10⁻⁵**.
- Mean maximum self-model-version difference: **2.29**.

### Interpretation

With the applied-action sequence held exactly equal between PULSE and ACTION_REPLAY, the runs developed different self-models in **45.83%** of later cycles on average.

With the semantic self-model bridge enabled, the dynamic state also separated significantly both from replay and from the same replay with the bridge disabled.

The result is consistent with an additional computational causal pathway:

**query → self-model → semantic self-model bridge → dynamics**

This differs from I5.9: there, the dynamic trajectory was identical when only the applied action sequence was fixed. I5.10 shows that when semantic state is allowed to enter dynamics, a query difference can survive action matching.

The result remains bounded by the deterministic provider and synthetic harness. It does not demonstrate consciousness or subjective experience.

The next test is to release action after the first cycle and ask whether this semantic-dynamic difference actually changes **future trajectory selection**.

ica modifica realmente la **selección de trayectorias futuras**.

## Límites

I5.10 estudia una ruta semántica causal computacional dentro del runtime probado. Un efecto semantic self-model → dinámica no demuestra consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

## Objective

I5.9 showed that when the applied action sequence is fixed, the pulse's dynamic trajectory is reconstructed exactly under FULL query.

I5.10 now separates **dynamics** from **semantic state**:

> Can two organisms with the same applied-action sequence develop different self-models solely because of a query difference, and can that semantic difference re-enter dynamics through the semantic self-model bridge?

## Conditions

- FULL_BRIDGE_ON — normal query and action; semantic self-model bridge enabled.
- PULSE_SHUFFLED_QUERY_BRIDGE_ON — query shuffled only in cycle 0; bridge enabled.
- ACTION_REPLAY_FULL_QUERY_BRIDGE_ON — FULL query; exactly replay the pulse's applied actions; bridge enabled.
- ACTION_REPLAY_FULL_QUERY_BRIDGE_OFF — same action replay, but semantic self-model bridge disabled.

All conditions start from the same checkpoint.

The deterministic provider generates the next SELF_MODEL from the query_module recorded in the previous cycle. This makes the path explicit:

previous query → next self-model → semantic bridge → next dynamics.

## Primary endpoint

Difference between PULSE_SHUFFLED_QUERY_BRIDGE_ON and ACTION_REPLAY_FULL_QUERY_BRIDGE_ON in:

1. self-model divergence across later cycles;
2. state delta at t+1;
3. state-divergence AUC.

## Semantic mediation endpoint

Compare ACTION_REPLAY_FULL_QUERY_BRIDGE_ON against ACTION_REPLAY_FULL_QUERY_BRIDGE_OFF.

If the bridge transmits semantic state, a difference between these arms despite identical applied actions indicates:

query → self-model → semantic bridge → state.

## Controls

- exact applied-action match;
- identical initial checkpoint;
- same seed;
- persistence of self-model divergence;
- self-model version;
- previous query module.

## Statistical design

- 24 paired replicates;
- 24 warmup cycles;
- 8 experimental cycles;
- same seed per replicate;
- 20,000 sign-flip permutations for continuous endpoints.

## Boundary

I5.10 studies a computational semantic causal pathway inside the tested runtime. A self-model-to-dynamics effect would not demonstrate consciousness or subjective experience.

</details>
