# I1 — Interoceptive Self-Assessment

## Question

> Can the organism estimate a future internal operating condition from a bounded readout of its own current internal state, without semantic self-report?

I1 is the first step after read-only instrumentation. It does not allow the interoceptive signal to control policy yet.

## Design

The protocol uses the deterministic internal dynamics as the environment.

- training perturbation magnitudes: `0.25, 0.50, 0.75`;
- OOD perturbation magnitudes: `0.35, 0.65, 0.90`;
- snapshot immediately after the controlled perturbation;
- recovery horizon: 8 internal steps;
- no semantic input during the probe;
- no model-provider output is required.

At each snapshot, I0 produces eight bounded internal variables. The hidden target is a future recovery score computed from the subsequent internal trajectory:

```text
recovery = 1 / (1 + |future_state| + future_pressure)
```

The target is never supplied to the organism during the probe.

## Controls

I1 compares four predictors:

| Predictor | Purpose |
|---|---|
| Interoceptive | full bounded internal readout |
| Single-signal | strongest single interoceptive variable baseline used here |
| Target-permuted | tests whether feature→target mapping carries predictive information |
| Constant | predicts the training-set mean recovery |

The primary OOD comparison is the full interoceptive predictor against a single-signal baseline, a target-permuted control, and a constant baseline.

## Primary endpoint

Mean absolute error (MAE) on the held-out OOD perturbations.

Paired sign tests compare per-episode absolute errors between the full interoceptive predictor and each control.

## Why this is not yet regulation

I1 only tests **readability of future internal condition**.

It does not allow the readout to change actions, rewards, or dynamics. A favorable I1 result would therefore support an internal predictive representation, not homeostatic agency.

## Interpretation boundary

A positive result would show that the bounded interoceptive representation contains predictive information about near-future internal recovery under the tested dynamics.

It would not establish subjective experience, consciousness, or biological interoception.

## Preregistration status

This document defines the confirmatory structure before the first dedicated I1 workflow result is published. The historical protocol family is not retroactively treated as globally preregistered.

Before extending I1, the primary endpoint, perturbation distribution, controls, exclusion rules, replication count, and analysis rule should remain frozen for the confirmatory run.

## Next step

I2 can only enable interoceptive policy modulation after I1 has a validated readout. I2 should then compare regulation with full, no-interoception, shuffled, and clamped conditions under the same perturbation schedule.
