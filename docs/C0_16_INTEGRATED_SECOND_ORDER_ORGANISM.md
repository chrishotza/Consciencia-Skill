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
