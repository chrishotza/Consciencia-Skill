# C0.15 — Lesion/Rescue of the Persistent Second-Order Selector

## Question

C0.15 crosses the two prior findings:

- C0.13: action-conditioned second-order specificity;
- C0.14: persistence across restart.

The new question is whether the **persistent second-order component is causally necessary** for autonomous selection and whether restoring the serialized component rescues the behavior.

## Conditions

- **FULL** — second-order model active throughout.
- **LESION** — second-order model disabled from steps 9–16.
- **RESCUE** — second-order model disabled from steps 9–12, then restored from the serialized checkpoint for steps 13–16.

The first-order self-observer and dynamic system remain intact in all conditions.

## Primary outputs

- FULL − LESION action contrast during the lesion period.
- FULL − LESION self-prediction-gain contrast during the lesion period.
- FULL − RESCUE action contrast after restoration.
- FULL − RESCUE gain contrast after restoration.

A strong lesion effect combined with recovery after restoration would provide a causal necessity/rescue result for the second-order selector under this protocol.

It remains a computational organizational result and does not establish subjective experience.


## Verified result

Run **36945882211**; artifact **11202160302**; SHA256 **5c297e25f01036b87f63ab0355555faf80dc4a2462199f5c7e115b62cbadcd6f**.

- FULL − LESION late action: **+0.271484375**, p **0.00064997**
- FULL − LESION late gain: **+0.03751679**, p **0.08415**
- FULL − RESCUE post-restore action: **+0.02734375**, p **0.68607**
- FULL − RESCUE post-restore gain: **−0.03525716**, p **0.03860**
- exact checkpoint fraction: **100%**

Interpretation: the second-order component affected later action selection when removed, but the gain endpoint was not significant. Restoring the component made the action contrast small, but did not reproduce the full arm's gain; therefore rescue is not established as a clean functional recovery under this protocol.
