# I5.14 — Phase-Matched Temporal Specificity Control

<a id="espanol"></a>

<details>
<summary>ES — abrir</summary>

## Objetivo

I5.13 mostró que un desplazamiento exacto de un ciclo, manteniendo la acción aplicada en t0 y la distribución completa de SELF_MODEL, cambia la trayectoria posterior. I5.14 busca separar ese efecto de una explicación más débil: que cualquier reordenamiento temporal de la secuencia semántica produzca una divergencia comparable.

## Diseño

Se usa una secuencia semántica explícita de tres estados:

`A, B, C, A, B, C, A, B`

Se comparan tres secuencias con exactamente la misma distribución y el mismo SELF_MODEL en t0:

- BASE: `A, B, C, A, B, C, A, B`
- SHIFT+1: `A, C, A, B, C, A, B, B`
- SHIFT-1: `A, B, B, C, A, B, C, A`

Además se ejecuta SHIFT+1 con el semantic self-model bridge OFF para comprobar la mediación explícita del puente.

## Endpoints

- cambio de acción futura respecto de BASE en ciclos 1–7;
- AUC de divergencia de estado BASE vs SHIFT+1;
- AUC de divergencia de estado BASE vs SHIFT-1;
- AUC SHIFT+1 vs SHIFT-1;
- AUC SHIFT+1 bridge ON vs OFF;
- coincidencia de acción aplicada en t0;
- coincidencia de distribución SELF_MODEL.

## Diseño estadístico

- 24 réplicas emparejadas;
- 24 ciclos de warmup;
- 8 ciclos experimentales;
- mismo checkpoint y seed por réplica;
- 20.000 permutaciones sign-flip.

## Resultado verificado

Workflow **37042551701** (run **778**), artifact **11243190387**, seed **20261014**, 24 réplicas, 24 ciclos de warmup y 8 ciclos experimentales.

- coincidencia de acción aplicada en t0: **100%** para SHIFT+1 y SHIFT-1;
- coincidencia de distribución de SELF_MODEL: **100%** para ambas secuencias y para SHIFT+1 bridge OFF;
- cambio medio de acción futura:
  - SHIFT+1: **11.90%**, p **4.99975×10⁻⁵**;
  - SHIFT-1: **44.64%**, p **4.99975×10⁻⁵**;
- AUC de estado BASE vs SHIFT+1: **0.2414241371**, p **4.99975×10⁻⁵**;
- AUC de estado BASE vs SHIFT-1: **1.9526574097**, p **4.99975×10⁻⁵**;
- AUC SHIFT+1 vs SHIFT-1: **1.9346491472**, p **4.99975×10⁻⁵**;
- AUC SHIFT+1 bridge ON vs OFF: **2.1221765870**, p **4.99975×10⁻⁵**.

Interpretación: el control fase-matcheado produjo una respuesta temporal dependiente de la dirección del corrimiento. Ambos corrimientos conservaron t0 y la distribución completa de SELF_MODEL, pero no fueron equivalentes: SHIFT+1 produjo una separación posterior pequeña y SHIFT-1 una separación mucho mayor. Esto es compatible con sensibilidad a la fase/orden temporal del estado semántico dentro del arnés, y debilita una explicación basada únicamente en “cualquier reordenamiento produce la misma divergencia”. No demuestra consciencia ni experiencia subjetiva.

## Límite

I5.14 es un control de especificidad temporal computacional. No demuestra consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

<details>
<summary>EN — open</summary>

## Objective

I5.13 showed that an exact one-cycle shift, while preserving the t0 applied action and the full SELF_MODEL distribution, changes the downstream trajectory. I5.14 tests a stronger alternative explanation: that any temporal reordering of the semantic sequence might produce a comparable divergence.

## Design

An explicit three-state semantic sequence is used:

`A, B, C, A, B, C, A, B`

Three sequences are compared with exactly the same distribution and the same t0 SELF_MODEL:

- BASE: `A, B, C, A, B, C, A, B`
- SHIFT+1: `A, C, A, B, C, A, B, B`
- SHIFT-1: `A, B, B, C, A, B, C, A`

SHIFT+1 is also run with the semantic self-model bridge OFF to test explicit bridge mediation.

## Endpoints

- future-action change relative to BASE across cycles 1–7;
- BASE vs SHIFT+1 state-divergence AUC;
- BASE vs SHIFT-1 state-divergence AUC;
- SHIFT+1 vs SHIFT-1 AUC;
- SHIFT+1 bridge ON vs OFF AUC;
- applied-action match at t0;
- SELF_MODEL distribution match.

## Statistical design

- 24 paired replicates;
- 24 warmup cycles;
- 8 experimental cycles;
- same checkpoint and seed per replicate;
- 20,000 sign-flip permutations.

## Verified result

Workflow **37042551701** (run **778**), artifact **11243190387**, seed **20261014**, 24 replicates, 24 warmup cycles and 8 experimental cycles.

- applied-action match at t0: **100%** for SHIFT+1 and SHIFT-1;
- SELF_MODEL distribution match: **100%** for both sequences and for SHIFT+1 bridge OFF;
- mean future-action change:
  - SHIFT+1: **11.90%**, p **4.99975×10⁻⁵**;
  - SHIFT-1: **44.64%**, p **4.99975×10⁻⁵**;
- BASE vs SHIFT+1 state AUC: **0.2414241371**, p **4.99975×10⁻⁵**;
- BASE vs SHIFT-1 state AUC: **1.9526574097**, p **4.99975×10⁻⁵**;
- SHIFT+1 vs SHIFT-1 AUC: **1.9346491472**, p **4.99975×10⁻⁵**;
- SHIFT+1 bridge ON vs OFF AUC: **2.1221765870**, p **4.99975×10⁻⁵**.

Interpretation: the phase-matched control produced direction-dependent temporal sensitivity. Both shifts preserved t0 and the full SELF_MODEL distribution, but they were not equivalent: SHIFT+1 produced a small downstream separation while SHIFT-1 produced a much larger one. This is compatible with sensitivity to the phase/order of semantic state within the harness and weakens an explanation based solely on “any temporal reordering produces the same divergence.” It does not demonstrate consciousness or subjective experience.

## Boundary

I5.14 is a computational temporal-specificity control. It does not demonstrate consciousness or subjective experience.

</details>
