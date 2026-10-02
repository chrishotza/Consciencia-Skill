# C0.13 — Action-Conditioned Second-Order Self-Model

## Question

C0.12 showed that a second-order model can predict first-order self-model error, but target permutation did not change behavior. C0.13 strengthens the representation so that the second-order model explicitly receives the first-order predicted state and candidate action.

The question becomes:

`candidate action → first-order prediction → predicted first-order error → action selection`

## Conditions

- **META_TRUE** — action-conditioned second-order observer.
- **META_PERMUTED** — identical feature vectors, target-permuted second-order observer.
- **META_BLIND** — constant second-order error baseline.

## Primary outputs

1. TRUE − PERMUTED action;
2. TRUE − PERMUTED self-prediction gain;
3. TRUE − BLIND action;
4. TRUE − BLIND gain;
5. held-out meta-model MAE advantage over the constant baseline.

## Controls

Same first-order observer, episode contexts, candidate signals, dynamic seeds, and training budget. No semantic input and no external retraining during the probe.

## Interpretation

A TRUE-vs-PERMUTED behavioral separation would support causal specificity of the action-conditioned second-order mapping. It remains a computational result and does not establish phenomenal consciousness.
