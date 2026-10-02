<a id="espanol"></a>

# C0.11 — Causal Action-Mediation Through Internal Dynamics

## Question

C0.11 asks whether the policy's first action can causally alter the next internal state and, through the same learned observer and policy, alter the next action.

This is a direct intervention on the middle of the proposed chain:

`action_1 → internal_state_2 → observer_readout_2 → action_2`

## Conditions

- **FACTUAL** — the trained policy selects action 1.
- **FORCED COUNTERFACTUAL** — after the same policy selects action 1, the experiment replaces it with a different candidate action before the environment step.

The initial target state, learned observer, learned policy, candidate signal set, and dynamic seed are held fixed within each pair.

## Primary contrasts

1. signed second-action difference, FACTUAL − FORCED;
2. signed next-state difference, FACTUAL − FORCED;
3. self-prediction gain difference, FACTUAL − FORCED.

Absolute state/action differences are retained as descriptive secondary outputs.

## Controls

No semantic input is provided during the probe. No external retraining occurs during the probe. Observer and policy are identical across conditions.

## Interpretation

A paired difference in the second action after an intervention confined to the first action would support causal mediation through the tested internal dynamics and readout pathway. It does not establish phenomenal consciousness.


## Verified result

GitHub Actions run **36944924071**; artifact **11200748887**; SHA256 **d6f496ebe49b494a8af30932a30c73880a26981da079932d9ff8a9348b2d56cd**.

- Signed next-action contrast: **+1.78125**, p **4.99975e-05**
- Signed next-state contrast: **−0.5770045054**, p **4.99975e-05**
- Signed self-prediction-gain contrast: **+0.5278692817**, p **4.99975e-05**
- Maximum intervention error: **0.0**

The forced intervention changed only the first action. The following internal state and the next action then diverged under the same observer and policy. C0.11 is **positive for the tested computational causal chain** action → internal state → observer/policy → next action. It does not establish phenomenal consciousness.

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# C0.11 — Causal Action Mediation Through Internal Dynamics

## Question

C0.11 asks whether the policy's first action can causally alter the next internal state and, through the same learned observer and policy, alter the next action.

The tested chain is action_1 → internal_state_2 → observer_readout_2 → action_2.

## Conditions

- FACTUAL — trained policy selects action 1;
- FORCED COUNTERFACTUAL — after the same policy selects action 1, the experiment replaces it with a different candidate action before the environment step.

Initial target state, learned observer, learned policy, candidate signal set, and dynamic seed are held fixed within each pair.

## Primary contrasts

1. signed second-action difference, FACTUAL − FORCED;
2. signed next-state difference;
3. self-prediction-gain difference.

Absolute state/action differences are descriptive secondary outputs.

## Controls

No semantic input or external retraining. Observer and policy are identical across conditions.

## Verified result

GitHub Actions run 36944924071; artifact 11200748887; SHA256 d6f496ebe49b494a8af30932a30c73880a26981da079932d9ff8a9348b2d56cd.

- signed next-action contrast: +1.78125, p 4.99975e-05;
- signed next-state contrast: -0.5770045054, p 4.99975e-05;
- signed self-prediction-gain contrast: +0.5278692817, p 4.99975e-05;
- maximum intervention error: 0.0.

The forced intervention changed only the first action. The following internal state and next action then diverged under the same observer and policy. C0.11 is positive for the tested computational causal chain action → internal state → observer/policy → next action. It does not establish phenomenal consciousness.

</details>