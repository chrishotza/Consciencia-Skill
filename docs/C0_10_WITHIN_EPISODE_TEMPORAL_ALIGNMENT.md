# C0.10 — Within-Episode Temporal Observer→Policy Alignment

## Question

C0.10 narrows C0.9 by preserving the same episode on both sides of the interface.

The observer and policy are unchanged. The target episode and environment are unchanged. Only the observer readout supplied to the policy is temporally shifted from the current post-intervention state to the same episode's immediately pre-intervention state.

## Conditions

- **NORMAL** — current post-intervention observer readout.
- **WITHIN-EPISODE LAG** — immediately pre-intervention observer readout.

The environment executes on the same post-intervention target context in both conditions, with the same bridge seed.

## Primary contrasts

1. signed action difference, NORMAL − LAG;
2. self-prediction gain difference, NORMAL − LAG;
3. signed next-state difference after one identical-seed environment step.

Absolute action/state differences are retained only as descriptive secondary outputs. Primary inference is paired by episode seed.

## Controls

No semantic input is provided during the probe. No external retraining occurs during the probe. The learned observer and policy are trained once and then frozen.

Intervention integrity is checked explicitly.

## Interpretation

A paired separation after replacing only the observer readout with a temporally lagged readout would indicate sensitivity to temporal observer→policy alignment. This is a computational organizational result, not a demonstration of phenomenal consciousness.


## Verified result

GitHub Actions run **36944920225**; artifact **11201258435**; SHA256 **7d24c622c02a331e2d3844037abccbd93365ea9de54149da77e68fc2ac631e75**.

- Current-vs-lagged observer prediction gap: **0.1624331804**
- Signed action contrast: **0.0**, p **1.0**
- Signed gain contrast: **0.0**, p **1.0**
- Signed next-state contrast: **0.0**, p **1.0**
- Maximum intervention error: **0.0**

The observer produced different readouts for current and pre-intervention states, but the policy behavior was unchanged. C0.10 is therefore **null for the tested behavioral sensitivity to temporal observer→policy alignment**.
