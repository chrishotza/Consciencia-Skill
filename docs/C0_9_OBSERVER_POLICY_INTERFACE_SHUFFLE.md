# C0.9 — Observer-to-Policy Interface Shuffle

## Question

C0.9 asks whether the policy depends on the **within-episode correspondence** between the current dynamic state and the self-observer readout it receives.

This is narrower than C0.8: the learned observer and policy remain the same in both arms. Only the interface correspondence is changed.

## Conditions

- **NORMAL** — the policy receives the target episode's own observer prediction.
- **DONOR-SHUFFLE** — the policy receives observer predictions generated from a fixed derangement of other evaluation episodes.

The donor multiset is preserved. The target episode, candidate actions, learned observer, learned policy, intervention, and environment seed are otherwise held fixed within each pair.

## Primary contrasts

1. action mismatch between NORMAL and DONOR-SHUFFLE;
2. self-prediction gain difference, NORMAL − DONOR-SHUFFLE;
3. next-state difference after one identical-seed environment step.

The gain contrast is computed elementwise across the same episode seeds.

## Controls

No semantic input is provided during the probe. No external retraining occurs during the probe. The learned observer and policy are trained once and then frozen.

Intervention integrity is checked explicitly.

## Interpretation

A paired gain difference would indicate sensitivity to the causal correspondence at the observer → policy interface. It is a computational organizational result, not a demonstration of phenomenal consciousness.
