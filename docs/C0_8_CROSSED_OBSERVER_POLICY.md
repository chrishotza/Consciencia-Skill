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
