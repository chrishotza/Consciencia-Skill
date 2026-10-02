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

## Boundary

I5.13 is a computational causal-specificity control. It does not demonstrate consciousness or subjective experience.

</details>
