# C0.8 — Crossed Observer/Policy Coupling Test

## Question

C0.8 separates three possibilities that C0.7 cannot distinguish by itself:

1. dependence on the learned self-observer;
2. dependence on the learned self-policy;
3. dependence on the **matched coupling** between the two.

## Four conditions

- **TT** — true observer + true policy.
- **TP** — true observer + target-permuted policy.
- **PT** — target-permuted observer + true policy.
- **PP** — target-permuted observer + target-permuted policy.

All four use the same episode seeds, perturbations, training budget, target multiset, and evaluation horizon.

## Primary contrasts

- Observer effect: TT − PT.
- Policy effect: TT − TP.
- Observer × policy interaction: TT − TP − PT + PP.

The same contrasts are also evaluated for state variance and final state distance.

A nonzero interaction would indicate that the organizational effect depends on the particular pairing between the learned observer and learned policy, rather than being attributable to either component independently.

This is a causal organizational test. It does not establish phenomenal consciousness.


## First execution and correction

The first execution completed all four conditions with matched episode seeds and valid intervention checks. Its descriptive means were:

| Condition | Mean gain | Final-state distance | State variance |
|---|---:|---:|---:|
| TT | 0.21888936 | 0.15996548 | 0.06848248 |
| TP | -0.12484394 | 0.67765194 | 0.07943683 |
| PT | -0.31516985 | 0.67765194 | 0.07943683 |
| PP | 0.20488969 | 0.14799625 | 0.06747759 |

The original implementation incorrectly generated the interaction p-values by repeating one scalar interaction value across 64 pseudo-replicates. Those p-values are therefore not used.

The original final-distance interaction also used the opposite sign from the declared contrast. The implementation has now been corrected so that gain, variance, and final-distance interactions are all computed **elementwise per shared episode seed** using:

`TT - TP - PT + PP`

The next C0.8 artifact is the confirmatory statistical run.


Confirmatory execution trigger recorded from the corrected elementwise interaction implementation.
