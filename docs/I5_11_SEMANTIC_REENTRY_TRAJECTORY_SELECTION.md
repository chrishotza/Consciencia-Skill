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

## Resultado verificado

Workflow: **37038961982**; artifact: **11241544037**; seed **20261011**; **24** réplicas; **24** ciclos de warmup; **8** ciclos experimentales.

- Coincidencia de acción aplicada en t0 PULSE vs ACTION_MATCH: **100%**.
- Cambio de acción seleccionada en ciclos 1–7: **55.95%** de media; p **4.99975×10⁻⁵**.
- Δ estado en t+1: **0.49647** de media; p **4.99975×10⁻⁵**.
- AUC de divergencia de estado post-pulso: **2.23957**; p **4.99975×10⁻⁵**.
- AUC ACTION_MATCH_BRIDGE_ON vs BRIDGE_OFF: **2.63688**; p **4.99975×10⁻⁵**.
- Divergencia post-pulso de SELF_MODEL: **50.0%** de media.

### Interpretación

Después de igualar exactamente la acción aplicada del primer ciclo, la perturbación de query produjo una separación significativa de estado y, más importante, cambió la **selección de acciones futuras** en una media del **55.95%** de los ciclos posteriores.

La diferencia desapareció parcialmente cuando el semantic self-model bridge fue desactivado, con una diferencia de AUC ON-vs-OFF también significativa.

Esto completa, bajo el harness determinista, una cadena computacional mucho más fuerte:

query → self-model → semantic bridge → own state → future trajectory selection.

El resultado no demuestra consciencia ni experiencia subjetiva. El siguiente control debe romper específicamente la correspondencia query → self-model manteniendo la distribución de modelos de sí, para comprobar que el efecto no pr## Verified result

Workflow: **37038961982**; artifact: **11241544037**; seed **20261011**; **24** replicates; **24** warmup cycles; **8** experimental cycles.

- t0 applied-action match PULSE vs ACTION_MATCH: **100%**.
- Selected-action change across cycles 1–7: **55.95%** mean; p **4.99975×10⁻⁵**.
- State delta at t+1: **0.49647** mean; p **4.99975×10⁻⁵**.
- Post-pulse state-divergence AUC: **2.23957**; p **4.99975×10⁻⁵**.
- ACTION_MATCH_BRIDGE_ON vs BRIDGE_OFF AUC: **2.63688**; p **4.99975×10⁻⁵**.
- Post-pulse SELF_MODEL divergence: **50.0%** mean.

### Interpretation

After the first-cycle applied action was matched exactly, the query perturbation still produced significant state separation and, importantly, changed **future action selection** in a mean **55.95%** of later cycles.

The difference was reduced when the semantic self-model bridge was disabled, with the ON-vs-OFF AUC contrast also significant.

Under this deterministic harness, this completes a substantially stronger computational chain:

query → self-model → semantic bridge → own state → future trajectory selection.

This does not demonstrate consciousness or subjective experience. The next control should specifically break the query → self-model correspondence while preserving the self-model distribution, testing whether the effect is more than a consequence of varying semantic content.

oviene solo de variar el contenido semántico.

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
