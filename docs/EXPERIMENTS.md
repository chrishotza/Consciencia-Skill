# Experimental Program — Latent Self and Causal Re-entry

## Objective

Test whether persistent latent self-structure adds predictive and causal capability beyond transcript memory and an explicit self-model.

This program does not test subjective experience directly.

It tests whether adding latent self-structure changes measurable longitudinal behavior.

## Conditions

### A — transcript/state baseline

Persistent identity, memory, and ordinary runtime state.

### B — explicit self-model

Condition A plus a structured self-model that participates in trajectory selection.

### C — latent self

Condition B plus endogenous latent-pattern learning and self-dissonance. The runtime discovers recurrent self-state structure from longitudinal history rather than receiving the latent pattern directly from the host.

### D — reconciled latent self

Condition C plus explicit self-model reconciliation after detected discrepancy.

## Primary measurements

- trajectory sensitivity to self-model perturbation;
- self-dissonance before and after reconciliation;
- persistence of latent patterns across restart;
- latent-pattern formation and activation trajectories;
- longitudinal trajectory stability;
- regime selection and transition frequency;
- coherence changes;
- transformation-log density;
- identity continuity across restart.

## Required controls

Every experiment should hold constant:

- model;
- prompt sequence;
- candidate-future set when externally supplied;
- random seed where randomness exists;
- state-store format;
- number of cycles.

Only the condition-specific mechanism should change. For the ablation implementation, endogenous latent learning is enabled only for C/D; A/B run the same runtime with `learn_latent_patterns=False`.

## Falsification-oriented questions

1. Does adding latent structure change behavior compared with an otherwise identical runtime?
2. Does self-dissonance predict later self-model revision?
3. Does reconciliation reduce measured self-dissonance without simply collapsing the model into the current state?
4. Does latent structure remain useful after restart?
5. Can any observed advantage be explained by extra stored information alone?
6. Does endogenous recurrence detection add information not present in the latest state alone?
7. Do learned patterns alter regime selection, not merely trajectory scoring?

## Interpretation rule

A positive result means:

> the added mechanism changes the measured dynamics.

It does not mean:

> the mechanism produces phenomenal consciousness.

The experiment must separate behavioral advantage, self-model dynamics, and any claim about subjective experience.

## Current priority experiment

**Latent-self ablation**

Compare A, B, C, and D over the same deterministic sequence.

Report:

~~~text
condition
initial state hash
final state hash
trajectory changes
self-dissonance trajectory
self-model revisions
regime transitions
latent pattern persistence
regime trajectory
regime transitions
restart continuity
~~~

The result should be stored as machine-readable JSON alongside a human-readable summary.
