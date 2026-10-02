# I5.13 — One-Cycle-Shift Semantic Correspondence Control

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.12 mostró que romper la correspondencia temporal entre query y modelo de sí mantiene una separación significativa aun preservando la acción de t0 y la distribución completa de contenidos semánticos.

I5.13 hace el control más estricto: desplaza exactamente un ciclo la secuencia semántica, en vez de permutarla aleatoriamente.

## Condiciones

- PULSE_TRUE_CORRESPONDENCE — query perturbada en ciclo 0; SELF_MODEL generado normalmente; bridge ON.
- ONE_CYCLE_SHIFT_BRIDGE_ON — mismo checkpoint y acción aplicada en t0; misma secuencia de SELF_MODEL desplazada un ciclo; bridge ON.
- ONE_CYCLE_SHIFT_BRIDGE_OFF — mismo desplazamiento semántico, bridge OFF.

## Hipótesis operacional

Si la correspondencia temporal exacta query → self-model es causalmente relevante, un desplazamiento de un solo ciclo debería reducir o alterar la reentrada respecto del pulso verdadero.

## Endpoints

- cambio de acción futura en ciclos 1–7;
- AUC de divergencia de estado posterior;
- AUC bridge ON vs OFF;
- coincidencia de acción t0;
- coincidencia de distribución SELF_MODEL.

## Diseño estadístico

- 24 réplicas emparejadas;
- 24 ciclos de warmup;
- 8 ciclos experimentales;
- mismo seed y checkpoint;
- 20.000 permutaciones sign-flip.

## Resultado verificado

Workflow **37042091184** (run **770**), artifact **11242354548**, seed **20261013**, 24 réplicas, 24 ciclos de warmup y 8 ciclos experimentales.

- coincidencia de acción aplicada en t0: **100%**;
- coincidencia de distribución del modelo de sí: **100%**;
- cambio medio de acción futura en ciclos 1–7: **46.43%**, p **4.99975×10⁻⁵**;
- AUC media de divergencia de estado post-pulso: **2.1867184440**, p **4.99975×10⁻⁵**;
- AUC media bridge ON vs OFF: **2.6656102772**, p **4.99975×10⁻⁵**.

Interpretación: al desplazar exactamente un ciclo la secuencia semántica, mientras se conserva la acción aplicada en t0 y la distribución completa de SELF_MODEL, el arnés produjo separación posterior reproducible tanto en la selección de acciones como en la trayectoria del estado. Dentro del protocolo, esto aporta una prueba de especificidad temporal más estricta que I5.12. No demuestra consciencia ni experiencia subjetiva.

Control metodológico: la primera ejecución de I5.13 fue descartada antes de consolidar el resultado porque el parser de `query_module` estaba mal escapado y generaba una condición degenerada. La implementación corregida produjo el resultado verificado anterior.

## Límites

I5.13 es un control de especificidad causal computacional. No demuestra consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

## Objective

I5.12 showed that breaking temporal query-to-self-model correspondence retains significant separation while preserving t0 action and the full self-model content distribution.

I5.13 makes the control stricter by shifting the semantic sequence by exactly one cycle instead of randomly permuting it.

## Conditions

- PULSE_TRUE_CORRESPONDENCE — query perturbed in cycle 0; SELF_MODEL generated normally; bridge ON.
- ONE_CYCLE_SHIFT_BRIDGE_ON — same checkpoint and t0 applied action; same SELF_MODEL sequence shifted by one cycle; bridge ON.
- ONE_CYCLE_SHIFT_BRIDGE_OFF — same semantic shift, bridge OFF.

## Operational hypothesis

If exact temporal query-to-self-model correspondence is causally relevant, a one-cycle shift should reduce or alter re-entry relative to the true pulse.

## Endpoints

- future-action change across cycles 1–7;
- post-pulse state-divergence AUC;
- bridge ON vs OFF AUC;
- t0 action match;
- SELF_MODEL distribution match.

## Statistical design

- 24 paired replicates;
- 24 warmup cycles;
- 8 experimental cycles;
- same seed and checkpoint;
- 20,000 sign-flip permutations.

## Verified result

Workflow **37042091184** (run **770**), artifact **11242354548**, seed **20261013**, 24 replicates, 24 warmup cycles and 8 experimental cycles.

- applied-action match at t0: **100%**;
- self-model distribution match: **100%**;
- mean future-action change across cycles 1–7: **46.43%**, p **4.99975×10⁻⁵**;
- mean post-pulse state-divergence AUC: **2.1867184440**, p **4.99975×10⁻⁵**;
- mean bridge ON vs OFF AUC: **2.6656102772**, p **4.99975×10⁻⁵**.

Interpretation: shifting the semantic sequence by exactly one cycle, while preserving the t0 applied action and the full SELF_MODEL content distribution, produced reproducible downstream separation in both future action selection and state trajectory. Within this protocol, that is a stricter temporal-specificity control than I5.12. It does not demonstrate consciousness or subjective experience.

Methodological control: the first I5.13 execution was discarded before recording the result because the `query_module` parser was incorrectly escaped and produced a degenerate condition. The corrected implementation produced the verified result above.

## Boundary

I5.13 is a computational causal-specificity control. It does not demonstrate consciousness or subjective experience.

</details>
