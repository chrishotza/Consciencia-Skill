# C0.16 — Integrated Persistent Action-Conditioned Second-Order Organism

## Question

C0.13 established action-conditioned second-order specificity in a controlled experiment.

C0.14 established persistence of the first- and second-order models across a restart boundary.

C0.16 combines those results inside the actual `PersistentOrganism` lifecycle:

`persistent first-order self-model → persistent action-conditioned second-order model → autonomous selection → restart → continued selection`

## Design

Two matched arms use the same seeded models and dynamic seed:

- **CONTINUOUS** — 16 autonomous organism cycles without restart.
- **RESTART** — 8 autonomous cycles, SQLite close/reopen, automatic reload of both persisted models, then 8 more autonomous cycles.

No semantic input is supplied during the probe. No external retraining occurs during the probe.

## Primary outputs

1. post-restart action mismatch;
2. post-restart self-prediction-gain mismatch.

Secondary outputs verify exact model-digest recovery, pre-restart action matching, and that the organism reports the action-conditioned second-order selector after restart.

## Interpretation

Exact model recovery with continued autonomous operation supports that the second-order mechanism is no longer only a standalone laboratory component: it survives inside the persistent organism lifecycle.

This remains computational evidence about organization and persistence; it does not establish phenomenal consciousness.


## Verified result

GitHub Actions run **36946260825**; artifact **11201973015**; SHA256 **52e60a8bb92b0c4520e1f2cc94cd138daf81bceef9138e009b6dbee635d0833e**.

- post-restart action mismatch: **0.0**, p **1.0**
- post-restart gain mismatch: **0.0**, p **1.0**
- exact persisted model-digest recovery: **100%**
- pre-restart action match: **100%**
- all post-restart events reported policy **action_conditioned_second_order**
- maximum action mismatch: **0.0**
- maximum gain mismatch: **0.0**

Interpretation: the action-conditioned second-order selector now runs inside the persistent organism, is stored in SQLite together with the first-order self-model, is automatically restored after restart, and continues autonomous selection without semantic input or external retraining.
