# I4.3 — Structural OOD Metacognitive Generalization

## Status

**Protocol frozen for confirmatory execution. No result is interpreted yet.**

## Question

> Does a second-order reliability model trained under one hidden-disturbance structure remain useful when the structure of the disturbance changes, without online retraining?

I4.2 established persistence, serialization/restore, lesion/permutation separation, and rescue under the I4.1 disturbance family. I4.3 attacks the remaining external-validity weakness by changing the causal structure of the hidden disturbance after training.

## Training condition

The metacognitive observer is trained only under:

\`linear_action_pressure\`

with hidden risk:

\`0.04 + 0.09 * |action| + 0.06 * max(pressure, 0)\`

Training magnitude:

\`0.50\`

## OOD disturbance families

The trained observer is frozen before evaluation.

### 1. quadratic_action

\`0.035 + 0.075 * |action|^2 + 0.055 * pressure\`

### 2. pressure_threshold

\`0.025 + 0.03 * |action| + 0.10 * max(pressure - 0.18, 0)\`

The disturbance direction reverses above a fixed pressure threshold for non-zero actions.

### 3. state_coupled

\`0.02 + 0.06 * |action| + 0.08 * |state| * |action| + 0.04 * pressure\`

The disturbance direction depends on the joint sign relationship between state and action.

These structures are not shown during training.

## Conditions

- **META** — restored second-order model controls action selection.
- **LESION** — second-order layer removed; first-order selection remains.
- **PERMUTED** — restored model with targets permuted while retaining the learned feature distribution.
- **RANDOM** — matched candidate actions sampled randomly.

All conditions are paired by family, seed, initial state, perturbation magnitude, and deterministic world seeds.

No online updates occur during evaluation.

## Primary endpoint

Aggregate paired difference in mean prediction error:

\`META - LESION\`

across all OOD families and evaluation episodes.

## Secondary endpoints

- META - PERMUTED mean prediction error;
- META - RANDOM mean prediction error;
- META - LESION recovery;
- META - PERMUTED second-order prediction MAE;
- family-specific paired contrasts;
- policy-shift rate.

## Prespecified interpretation

A positive primary result supports structural OOD generalization of a computational metacognitive reliability mechanism.

A null or negative result is retained as evidence that the mechanism remains too tied to the training disturbance structure and should drive the next redesign.

No result from I4.3 is a consciousness score or evidence of subjective experience by itself.

## Reproducibility

The workflow records the exact commit, run identifier, and artifact. The trained second-order model is serialized and restored before every evaluation batch.

The protocol does not permit online meta-model updates during evaluation.
