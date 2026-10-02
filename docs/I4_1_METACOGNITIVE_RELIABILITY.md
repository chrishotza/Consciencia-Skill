# I4.1 — Metacognitive Reliability Under Hidden Action Disturbance

## Status

Verified run completed. The result supports a computational metacognitive reliability effect under the declared simulated hidden-disturbance protocol.

## Question

Can a second-order model learn when a first-order interoceptive prediction is likely to be unreliable, and can that estimate alter action selection?

## Protocol

The first-order model predicts the next operating condition for candidate actions.

The executed world contains an additional deterministic hidden disturbance:

risk = 0.04 + 0.09 * |action| + 0.06 * max(pressure, 0)

The first-order model does not receive this disturbance term.

The second-order observer learns:

current interoceptive state + candidate action + first-order prediction
→ observed first-order prediction error

Training uses magnitude 0.50. Evaluation uses held-out magnitudes 0.35, 0.65, and 0.90.

## Conditions

FIRST_ORDER, META, PERMUTED, RANDOM.

All evaluation conditions are paired by seed.

## Verified execution

- Workflow: interoception-i4-1-v02
- Run: 36973517099
- Head commit: ebb8176c615bf71a8f77920b0d9a2e43d8b3be2c
- Harness: 4 passed
- Run completed successfully
- Artifact: interoception-i4-1-v02

## Primary observed contrasts

| Contrast | Mean difference | p |
|---|---:|---:|
| META − FIRST_ORDER mean error | −0.00138238 | 7.0953e-21 |
| META − PERMUTED mean error | −0.00125732 | 3.8474e-18 |
| META − FIRST_ORDER recovery | +0.00166219 | 1.3172e-07 |
| META − PERMUTED recovery | +0.00130404 | 3.6700e-05 |

The metacognitive policy shifted its action choice on 11.04% of evaluation steps versus 2.34% for the permuted control.

Mean metacognitive prediction MAE was 0.0036884 for META versus 0.0090787 for PERMUTED.

## Interpretation boundary

This run provides evidence for a computational metacognitive property in the tested simulated environment: the second-order observer learned information about the reliability of the first-order internal-state prediction, and the resulting estimate was used in action selection.

The result does not establish subjective experience, biological consciousness, or a consciousness score.

The hidden disturbance is deliberately engineered, so external validity remains an open question.

## Scientific next step

The next protocol should increase independence from the hand-designed disturbance:

1. vary hidden disturbance structure without changing the meta objective;
2. introduce regime switches that are not directly encoded by action magnitude;
3. test persistence of the second-order model across restart/sleep;
4. add a lesion/rescue intervention targeting only the metacognitive layer;
5. preserve the first-order/permuted controls.
