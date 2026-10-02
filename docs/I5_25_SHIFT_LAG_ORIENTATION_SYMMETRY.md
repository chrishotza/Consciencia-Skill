# I5.25 — Shift × Lag Orientation and Symmetry Control

## Objective

I5.24 established a global non-additive shift×lag interaction for absolute AUC and future-action change on frozen I5.23 data.

I5.25 separates two possibilities:

1. orientation asymmetry: the surface changes when both shift and lag signs are reversed;
2. compensatory alignment: cells on lag = −shift are enriched relative to the other 30 cells.

## Frozen-data design

No new trajectories are collected.

For each endpoint, the analysis uses the frozen replicate × 6-shift × 6-lag I5.23 surface.

Orientation symmetry:
- pair each cell (shift, lag) with (−shift, −lag);
- compute the 18 paired differences;
- max-T control across the 18 orientation pairs;
- global any-pair test by replicate-level sign flips.

Compensatory diagonal:
- average the six cells satisfying lag = −shift;
- compare that average with the mean of the remaining 30 cells within each replicate;
- sign-flip test across replicates.

Bonferroni correction is applied across the six primary endpoint-family tests.

## Boundary

I5.25 characterizes the geometry of the frozen computational surface. It does not establish consciousness, subjective experience, or a unique causal mechanism.
