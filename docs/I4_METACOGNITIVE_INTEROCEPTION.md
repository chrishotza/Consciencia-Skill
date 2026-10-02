# I4 — Metacognitive Interoception

## Question

Can the organism predict when its own internal-state estimate is likely to be wrong and use that uncertainty to change action selection?

## Protocol

A first-order controller predicts internal operating condition for candidate actions. A separate deterministic world trajectory executes the chosen action, producing an observed prediction error.

A second-order observer learns from internal state, candidate action, first-order prediction, and observed error. The evaluation compares the first-order policy with a metacognitive policy, a target-permuted control, and a random control on held-out perturbation magnitudes.

## Primary endpoint

Paired mean recovery on held-out perturbations.

## Secondary endpoints

- prediction-error MAE;
- operating-condition error;
- rate of action changes caused by the second-order estimate.

## Gate

No result is promoted to the evidence ledger until the artifact, seed pairing, evaluation freeze, and control integrity are inspected.
