# I5.24 — Global Shift × Lag Interaction

## Objective

I5.23 showed a structured six-shift specificity surface: five shifts were significant for absolute AUC and future-action change, +1 was null, and the strongest corrected cells clustered where shift and lag opposed one another.

I5.24 tests whether that two-dimensional structure survives as a **global interaction** rather than being explained by additive shift and lag main effects.

## Design

No new trajectories are collected.

Input is the frozen I5.23 summary. For each endpoint, the analysis reconstructs a replicate × 6-shift × 6-lag matrix.

The observed interaction statistic is the sum of squared residuals after removing:

- the grand mean;
- the shift main effect;
- the lag main effect.

The permutation null independently permutes shift labels and lag labels within each replicate, preserving every replicate's 6×6 value surface while breaking the specific shift×lag pairing.

20,000 permutations are used.

## Multiplicity

Three endpoint-specific global interaction tests are reported. Bonferroni correction is applied across the three endpoints.

## Boundaries

I5.24 tests a global statistical interaction in a deterministic computational harness. It does not establish consciousness, subjective experience, or a unique mechanistic interpretation.

## English

I5.24 is a statistical follow-up on frozen I5.23 data. It asks whether the shift×lag surface contains a non-additive interaction after accounting for shift and lag main effects. No new trajectories are collected.


## Resultado verificado / Verified result

## I5.24 — Interacción global shift×lag

Análisis estadístico sobre el summary congelado de I5.23; no se recogieron nuevas trayectorias. 24 réplicas, seis shifts, seis lags y 20.000 permutaciones por endpoint.

- AUC firmada: estadístico observado 1.44184684, p de permutación 0.89460527; Bonferroni 1.0.
- AUC absoluta: estadístico observado 81.40515552, p 0.0000499975; Bonferroni 0.0001499925.
- Cambio de acción futura: estadístico observado 0.88811039, p 0.0000499975; Bonferroni 0.0001499925.
- El nulo preserva la superficie completa 6×6 de cada réplica y rompe el emparejamiento específico entre shift y lag.
- La superficie I5.23 no se explica por efectos aditivos independientes de shift y lag para AUC absoluta y acción futura. AUC firmada no muestra esa interacción.
- El resultado no identifica por sí mismo un mecanismo causal único; describe una estructura estadística del arnés computacional.

Verificación: research-lab 37063264401, artifact 11252345042; tests 37063264520 y package 37063264454, todos exitosos.

### I5.25 — Control de orientación y simetría shift×lag

Separar formalmente el patrón de compensación entre shift y lag de un artefacto producido por la codificación direccional de ambas variables.

## I5.24 — Global shift×lag interaction

Statistical analysis on the frozen I5.23 summary; no new trajectories were collected. 24 replicates, six shifts, six lags, and 20,000 permutations per endpoint.

- Signed AUC: observed statistic 1.44184684, permutation p 0.89460527; Bonferroni 1.0.
- Absolute AUC: observed statistic 81.40515552, p 0.0000499975; Bonferroni 0.0001499925.
- Future-action change: observed statistic 0.88811039, p 0.0000499975; Bonferroni 0.0001499925.
- The null preserves each replicate's complete 6×6 surface and breaks the specific shift×lag pairing.
- The I5.23 surface is not explained by additive shift and lag main effects for absolute AUC and future-action change. Signed AUC does not show the same interaction.
- The result does not by itself identify a unique causal mechanism; it describes a statistical structure in the computational harness.

Verification: research-lab 37063264401, artifact 11252345042; tests 37063264520 and package check 37063264454, all successful.

### I5.25 — Shift×lag orientation and symmetry control

Formally separate the compensatory shift-versus-lag pattern from artifacts caused by the directional coding of the two axes.
