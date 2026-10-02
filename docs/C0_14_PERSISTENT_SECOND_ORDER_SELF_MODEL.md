# C0.14 — Persistent Action-Conditioned Second-Order Self-Model

## Question

After C0.13 establishes second-order action specificity in a controlled probe, C0.14 asks whether that machinery remains the organism's own computational state after a restart boundary.

The tested chain is:

`persistent first-order self-model → persistent action-conditioned second-order model → autonomous selection`

## Design

Each replica calibrates a first-order self-observer and an action-conditioned second-order observer.

Two matched arms then execute the same autonomous sequence:

- **CONTINUOUS** — 16 steps without restart.
- **RESTART** — 8 steps, serialize both models and dynamic context, reconstruct them, then continue for 8 more steps.

## Primary outputs

1. action mismatch after restart;
2. gain mismatch after restart.

Secondary output: exact model-digest recovery at the restart boundary.

## Controls

No semantic input during the probe. No external retraining during the persistence test. Both arms start from the same model and the same dynamic seed.

## Interpretation

Near-zero post-restart mismatch with exact model recovery supports persistence of the second-order self-monitoring machinery across restart. It is a computational persistence result and does not establish subjective experience.
