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
