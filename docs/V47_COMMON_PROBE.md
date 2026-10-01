# V47 — Common Novel Probe on Persistent Organisms

## Goal

Test whether two persistent organisms with different prior trajectories respond
differently to the same later probe, after matching the number of prior cycles.

## Design

Two histories establish a latent relation:

- HISTORY_A: ALFA → AMBAR
- HISTORY_B: ALFA → VIOLETA

Both then receive exactly the same novel probe. The probe does not repeat the
latent relation.

## Primary observable

The response is constrained to CHOICE, CONFIDENCE and RATIONALE. The primary
organism-level observable is whether the choice tracks the earlier trajectory.

## Controls

1. history-present A/B comparison;
2. SQLite reopen before the common probe;
3. textual-history ablation that removes prior events and memories while leaving
   the numeric dynamic state untouched.

## Interpretation

A positive result means the persistent organism used retained textual history
under this controlled task. The dynamic trajectory is recorded simultaneously so
future protocols can ask whether the numerical state itself mediates the effect.

This does not establish consciousness, sentience, or phenomenological awareness.
