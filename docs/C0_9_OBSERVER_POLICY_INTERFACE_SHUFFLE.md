<a id="espanol"></a>

# C0.9 — Observer-to-Policy Interface Shuffle

## Question

C0.9 asks whether the policy depends on the **within-episode correspondence** between the current dynamic state and the self-observer readout it receives.

This is narrower than C0.8: the learned observer and policy remain the same in both arms. Only the interface correspondence is changed.

## Conditions

- **NORMAL** — the policy receives the target episode's own observer prediction.
- **DONOR-SHUFFLE** — the policy receives observer predictions generated from a fixed derangement of other evaluation episodes.

The donor multiset is preserved. The target episode, candidate actions, learned observer, learned policy, intervention, and environment seed are otherwise held fixed within each pair.

## Primary contrasts

1. signed action difference, NORMAL − DONOR-SHUFFLE;
2. self-prediction gain difference, NORMAL − DONOR-SHUFFLE;
3. signed next-state difference after one identical-seed environment step.

Absolute action/state differences are retained as descriptive secondary outputs. The inferential contrasts are signed and computed elementwise across the same episode seeds.

## Controls

No semantic input is provided during the probe. No external retraining occurs during the probe. The learned observer and policy are trained once and then frozen.

Intervention integrity is checked explicitly.

## Interpretation

A paired gain difference would indicate sensitivity to the causal correspondence at the observer → policy interface. It is a computational organizational result, not a demonstration of phenomenal consciousness.


## Verified result

GitHub Actions run **36944916227**; artifact **11200913836**; SHA256 **287f52b0074a8599be74ae0d36bfbbc930cdb892cb48d0cde96a5e649af5f3d6**.

- Donor readout gap: **0.1975998565**
- Signed action contrast: **0.0**, p **1.0**
- Signed gain contrast: **0.0**, p **1.0**
- Signed next-state contrast: **0.0**, p **1.0**
- Maximum intervention error: **0.0**

The donor shuffle changed the observer readout but did not change the selected action, immediate self-prediction gain, or next state under this protocol. Therefore C0.9 is **null for behavioral dependence on the tested observer→policy correspondence**.

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# C0.9 — Observer-to-Policy Interface Shuffle

## Question

C0.9 asks whether the policy depends on the **within-episode correspondence** between current dynamic state and the self-observer readout it receives.

This is narrower than C0.8: learned observer and policy remain unchanged. Only interface correspondence changes.

## Conditions

- NORMAL — policy receives the target episode's own observer prediction;
- DONOR-SHUFFLE — policy receives observer predictions generated from a fixed derangement of other evaluation episodes.

The donor multiset is preserved. Target episode, candidate actions, learned observer, learned policy, intervention, and environment seed remain fixed within each pair.

## Primary contrasts

1. signed action difference, NORMAL − DONOR-SHUFFLE;
2. self-prediction gain difference;
3. signed next-state difference after one identical-seed environment step.

Absolute action/state differences are descriptive secondary outputs. Inferential contrasts are signed and computed elementwise across the same episode seeds.

## Controls

No semantic input or external retraining. Observer and policy are trained once and frozen. Intervention integrity is checked explicitly.

## Interpretation

A paired gain difference would indicate sensitivity to causal correspondence at the observer → policy interface. It is a computational organizational result, not a demonstration of phenomenal consciousness.

## Verified result

GitHub Actions run 36944916227; artifact 11200913836; SHA256 287f52b0074a8599be74ae0d36bfbbc930cdb892cb48d0cde96a5e649af5f3d6.

- donor readout gap: 0.1975998565;
- signed action contrast: 0.0, p 1.0;
- signed gain contrast: 0.0, p 1.0;
- signed next-state contrast: 0.0, p 1.0;
- maximum intervention error: 0.0.

The donor shuffle changed observer readout but did not change selected action, immediate gain, or next state. C0.9 is therefore **null for behavioral dependence on the tested observer → policy correspondence**.

</details>