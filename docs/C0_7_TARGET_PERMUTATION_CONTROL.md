# C0.7 — Target-Permutation Specificity Control

## Question

C0.7 asks whether the organizational behavior attributed to the learned self-model depends on the **specific mapping** learned by the observer, rather than merely on having a model with the same number of stored feature rows and the same multiset of targets.

## Protocol

1. Train the self-observer normally.
2. Create a matched control by permuting only the observer targets while preserving the feature matrix and target multiset.
3. Train two policies with the same budget and seed: one on the true observer and one on the target-permuted observer.
4. Test both systems on the exact same episode seeds and perturbations.
5. Compare recovery gain, final state distance, state variance, and action magnitude.

No semantic input is provided during the probe. There is no external retraining during the probe.

## Interpretation

A reproducible separation between the true observer and the target-permuted control indicates dependence on the specific learned state-transition mapping under this control.

A null result means the tested behavioral effects are compatible with this matched permutation control.

Neither outcome, by itself, demonstrates phenomenal consciousness.
