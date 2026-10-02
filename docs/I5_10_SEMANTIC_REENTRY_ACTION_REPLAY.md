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
