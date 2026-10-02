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

## Boundary

I5.14 is a computational temporal-specificity control. It does not demonstrate consciousness or subjective experience.

</details>
