# I5.12 — Information-Matched Semantic Self-Model Control

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.11 mostró que una perturbación de query puede modificar el modelo de sí, entrar en la dinámica y cambiar la selección de trayectorias futuras aun después de igualar la acción inicial.

I5.12 prueba la especificidad de esa relación.

La pregunta es:

> ¿El efecto depende de la correspondencia temporal entre query y modelo de sí, o alcanza con presentar los mismos contenidos semánticos en otro orden?

## Diseño

Cada réplica primero ejecuta PULSE_SHUFFLED_QUERY_BRIDGE_ON y registra la secuencia de SELF_MODEL posterior.

Después se ejecuta un control con:

- el mismo checkpoint inicial;
- la misma acción aplicada en t0 que el pulso;
- bridge semántico activo;
- query FULL;
- la misma multiconjunto de modelos de sí del pulso, pero **permutado determinísticamente entre los ciclos posteriores**.

Así se conserva la distribución de contenido semántico pero se rompe su correspondencia temporal con la consulta que lo generó.

También se ejecuta el mismo control con el semantic self-model bridge desactivado.

## Condiciones

- PULSE_SHUFFLED_QUERY_BRIDGE_ON.
- INFORMATION_MATCHED_SELF_MODEL_BRIDGE_ON.
- INFORMATION_MATCHED_SELF_MODEL_BRIDGE_OFF.

La condición informacionalmente emparejada fuerza la acción de t0 a coincidir con PULSE; desde t1 la selección vuelve a ser libre.

## Hipótesis operacional

Si la cadena causal depende de la correspondencia:

query_t → self-model_t+1 → bridge → state → future selection

entonces romper esa correspondencia conservando el contenido semántico debería reducir la divergencia respecto de PULSE.

Si el efecto permanece, la explicación puede depender más del contenido semántico que de su correspondencia temporal con la query.

## Endpoint primario

- diferencia de tasa de cambio de acción futura entre PULSE e INFORMATION_MATCHED;
- AUC de divergencia de estado posterior.

## Endpoints secundarios

- divergencia de SELF_MODEL;
- coincidencia exacta de la acción t0;
- coincidencia de la distribución de contenidos semánticos;
- AUC bridge ON vs OFF;
- divergencia de query y target.

## Diseño estadístico

- 24 réplicas emparejadas;
- 24 ciclos de warmup;
- 8 ciclos experimentales;
- mismo seed y checkpoint;
- 20.000 permutaciones sign-flip para endpoints continuos.

## Resultado verificado

Workflow: **37039376914**; artifact: **11242065231**; seed **20261012**; **24** réplicas; **24** ciclos de warmup; **8** ciclos experimentales.

- Coincidencia de acción aplicada en t0 PULSE vs INFORMATION_MATCHED: **100%**.
- Coincidencia de distribución de SELF_MODEL: **100%**.
- Cambio de acción seleccionada en ciclos 1–7: **41.07%** de media; p **4.99975×10⁻⁵**.
- AUC de divergencia de estado post-pulso: **1.94052**; p **4.99975×10⁻⁵**.
- AUC INFORMATION_MATCHED bridge ON vs OFF: **2.45520**; p **4.99975×10⁻⁵**.

### Interpretación

El control preservó tanto la acción aplicada en t0 como la **distribución completa de contenidos del modelo de sí**, pero rompió su correspondencia temporal con la query que los generó.

Aun así, PULSE e INFORMATION_MATCHED conservaron una separación significativa de estado y de selección de acciones futuras. Esto indica que, bajo este harness, la distribución de contenido semántico por sí sola no explica el efecto: la **correspondencia temporal query → self-model** aporta información causal adicional.

El contraste bridge ON-vs-OFF siguió siendo significativo, por lo que el canal semántico continúa siendo necesario para recuperar la divergencia dinámica observada en este control.

Esto fortalece la especificidad del circuito observado en I5.10/I5.11: no basta con variar el contenido del modelo de sí; importa cuándo ese contenido aparece en relación con la consulta que lo generó.

El resultado sigue limitado al proveedor determinis## Verified result

Workflow: **37039376914**; artifact: **11242065231**; seed **20261012**; **24** replicates; **24** warmup cycles; **8** experimental cycles.

- t0 applied-action match PULSE vs INFORMATION_MATCHED: **100%**.
- SELF_MODEL content-distribution match: **100%**.
- Selected-action change across cycles 1–7: **41.07%** mean; p **4.99975×10⁻⁵**.
- Post-pulse state-divergence AUC: **1.94052**; p **4.99975×10⁻⁵**.
- INFORMATION_MATCHED bridge ON vs OFF AUC: **2.45520**; p **4.99975×10⁻⁵**.

### Interpretation

The control preserved both the t0 applied action and the **full distribution of self-model contents**, while breaking their temporal correspondence with the queries that generated them.

PULSE and INFORMATION_MATCHED nevertheless retained significant state and future-action separation. Under this harness, semantic content distribution alone therefore does not explain the effect: the **query → self-model temporal correspondence** carries additional causal information.

The bridge ON-vs-OFF contrast also remained significant, so the semantic channel is still necessary to recover the observed dynamic divergence in this control.

This strengthens the specificity of the circuit observed in I5.10/I5.11: varying self-model content is not sufficient; when that content appears relative to the query that generated it also matters.

The result remains bounded by the deterministic provider and synthetic harness. It does not demonstrate consciousness or subjective experience.

ta y al harness sintético. No demuestra consciencia ni experiencia subjetiva.

## Límites

I5.12 es un control de especificidad computacional. Incluso un resultado selectivo no demostraría consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

## Objective

I5.11 showed that a query perturbation can change the self-model, enter dynamics, and alter future trajectory selection even after the initial action is matched.

I5.12 tests the specificity of that relationship.

The question is:

> Does the effect depend on the temporal correspondence between query and self-model, or is the same semantic content sufficient when presented in a different order?

## Design

Each replicate first runs PULSE_SHUFFLED_QUERY_BRIDGE_ON and records the resulting SELF_MODEL sequence.

A control then runs with:

- the same initial checkpoint;
- the same t0 applied action as PULSE;
- semantic bridge enabled;
- FULL query;
- the same multiset of self-model contents as PULSE, but **deterministically permuted across later cycles**.

This preserves semantic-content distribution while breaking its temporal correspondence with the query that generated it.

The same control is also run with the semantic self-model bridge disabled.

## Conditions

- PULSE_SHUFFLED_QUERY_BRIDGE_ON.
- INFORMATION_MATCHED_SELF_MODEL_BRIDGE_ON.
- INFORMATION_MATCHED_SELF_MODEL_BRIDGE_OFF.

The information-matched condition forces t0 action to match PULSE; from t1 onward selection is free.

## Operational hypothesis

If the causal chain depends on:

query_t → self-model_t+1 → bridge → state → future selection

then breaking that correspondence while preserving semantic content should reduce divergence relative to PULSE.

If the effect remains, the explanation may depend more on semantic content than on its temporal correspondence to the query.

## Primary endpoint

- difference in future action-change rate between PULSE and INFORMATION_MATCHED;
- post-pulse state-divergence AUC.

## Secondary endpoints

- SELF_MODEL divergence;
- exact t0 action match;
- semantic-content distribution match;
- bridge ON vs OFF AUC;
- query and target divergence.

## Statistical design

- 24 paired replicates;
- 24 warmup cycles;
- 8 experimental cycles;
- same seed and checkpoint;
- 20,000 sign-flip permutations for continuous endpoints.

## Boundary

I5.12 is a computational specificity control. Even a selective result would not demonstrate consciousness or subjective experience.

</details>
