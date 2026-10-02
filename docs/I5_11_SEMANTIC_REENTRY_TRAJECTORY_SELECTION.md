# I5.11 — Semantic Re-entry into Future Trajectory Selection

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.10 mostró que una diferencia de query puede producir divergencia de modelo de sí y volver a entrar en la dinámica aun cuando las acciones aplicadas estén igualadas.

I5.11 libera ahora la acción después del primer ciclo para comprobar si esa diferencia semántico-dinámica cambia la **selección de trayectorias futuras**.

La comparación principal es:

query perturbado en t0 + acción t0 igualada

frente a:

query FULL + la misma acción t0

Después de t0, ambas condiciones vuelven a seleccionar acciones libremente.

## Condiciones

- **PULSE_SHUFFLED_QUERY_BRIDGE_ON** — query barajada solo en ciclo 0; bridge ON; selección libre.
- **ACTION_MATCH_FULL_QUERY_BRIDGE_ON** — query FULL; solo la acción aplicada del ciclo 0 se fuerza a ser la acción del pulso; desde ciclo 1 selección libre; bridge ON.
- **ACTION_MATCH_FULL_QUERY_BRIDGE_OFF** — mismo control de acción en t0, pero bridge OFF.
- **FULL_BRIDGE_ON** — control completo sin perturbación.

Todas las condiciones parten del mismo checkpoint.

## Hipótesis operacional

Si la ruta semántica detectada en I5.10 entra en la selección futura, entonces después de igualar la acción del ciclo 0 debería observarse una divergencia posterior entre PULSE y ACTION_MATCH con bridge ON.

Esa divergencia debería reducirse cuando el semantic self-model bridge está desactivado.

La prueba importante ya no es solo si cambia el estado: es si cambia la **acción elegida en ciclos posteriores**.

## Endpoint primario

- tasa de cambio de acción seleccionada en ciclos 1–7 entre PULSE y ACTION_MATCH;
- AUC de divergencia de estado en ciclos 1–7.

## Endpoints secundarios

- Δ estado en t+1;
- divergencia post-pulso del modelo de sí;
- persistencia de divergencia de acción;
- coincidencia exacta de la acción aplicada en t0;
- AUC ACTION_MATCH_BRIDGE_ON vs BRIDGE_OFF;
- divergencia de query y target.

## Diseño estadístico

- 24 réplicas emparejadas;
- 24 ciclos de warmup;
- 8 ciclos experimentales;
- mismo seed y checkpoint;
- 20.000 permutaciones sign-flip para endpoints continuos.

## Límites

I5.11 prueba reentrada causal computacional hacia selección de trayectorias dentro del harness sintético. Un efecto positivo no demostraría consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

## Objective

I5.10 showed that a query difference can produce self-model divergence and re-enter dynamics even when applied actions are matched.

I5.11 now releases action after the first cycle to test whether that semantic-dynamic difference changes **future trajectory selection**.

The main comparison is:

query perturbed at t0 + matched t0 action

versus:

FULL query + the same t0 action

After t0, both conditions select actions freely.

## Conditions

- **PULSE_SHUFFLED_QUERY_BRIDGE_ON** — query shuffled only in cycle 0; bridge ON; free selection.
- **ACTION_MATCH_FULL_QUERY_BRIDGE_ON** — FULL query; only cycle-0 applied action is forced to the pulse action; free selection from cycle 1; bridge ON.
- **ACTION_MATCH_FULL_QUERY_BRIDGE_OFF** — same t0 action control, but bridge OFF.
- **FULL_BRIDGE_ON** — unperturbed full control.

All conditions start from the same checkpoint.

## Operational hypothesis

If the semantic pathway detected in I5.10 enters future selection, then after matching the cycle-0 action there should be a later divergence between PULSE and ACTION_MATCH with bridge ON.

That divergence should be reduced when the semantic self-model bridge is disabled.

The key question is no longer only whether state changes, but whether it changes the **action selected in later cycles**.

## Primary endpoint

- selected-action change rate across cycles 1–7 between PULSE and ACTION_MATCH;
- state-divergence AUC across cycles 1–7.

## Secondary endpoints

- state delta at t+1;
- post-pulse self-model divergence;
- action-divergence persistence;
- exact cycle-0 applied-action match;
- ACTION_MATCH_BRIDGE_ON vs BRIDGE_OFF AUC;
- query and target divergence.

## Statistical design

- 24 paired replicates;
- 24 warmup cycles;
- 8 experimental cycles;
- same seed and checkpoint;
- 20,000 sign-flip permutations for continuous endpoints.

## Boundary

I5.11 tests computational causal re-entry into trajectory selection within the synthetic harness. A positive result would not demonstrate consciousness or subjective experience.

</details>
