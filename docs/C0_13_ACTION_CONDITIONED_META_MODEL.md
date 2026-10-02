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


## Verified result

Artifact: run **36945340705**, artifact **11201464566**; SHA256 **971e0b39360eaa25828abc0162e1cf70b5c54ae4916611d7a8e06413165b7b56**.

- TRUE − PERMUTED action: **−1.71875**, p **4.99975e-05**
- TRUE − PERMUTED gain: **+0.4850290**, p **4.99975e-05**
- TRUE − BLIND action: **−1.0**, p **4.99975e-05**
- TRUE − BLIND gain: **+0.2590892**, p **4.99975e-05**
- held-out MAE advantage: **+0.00740228**, p **4.99975e-05**
- meta MAE: **0.03489674**
- constant-baseline MAE: **0.04229902**
- intervention target error: **0.0**

C0.13 shows that conditioning the second-order model on the candidate action and the first-order predicted state produces behavioral specificity relative to a target-permuted control under the tested protocol.
