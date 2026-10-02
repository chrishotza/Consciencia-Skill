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
