# C0.17 — Autonomous Acquisition of the Action-Conditioned Second-Order Self-Model

## Question

C0.16 integrated and persisted the action-conditioned second-order selector, but its model was pre-seeded.

C0.17 removes that second-order pre-seeding.

The first-order self-observer is available. The action-conditioned second-order model starts **empty** and is learned online by the `PersistentOrganism` itself from deterministic counterfactual evaluations of every candidate action.

The chain is:

`first-order self-model → counterfactual prediction errors → second-order self-model → autonomous selection`

## Training phase

For each autonomous cycle, the organism:

1. obtains the first-order prediction for every candidate signal;
2. evaluates the deterministic next state for each candidate without mutating its actual state;
3. records the resulting first-order prediction error into the action-conditioned second-order model;
4. selects using the learned second-order model;
5. executes the selected action and continues learning from the actual transition.

## Evaluation control

After online acquisition, the learned second-order model is frozen.

Two matched database clones are evaluated from the same state:

- **TRUE** — learned second-order mapping;
- **TARGET-PERMUTED** — same features and target multiset, but target assignments permuted.

No external retraining and no semantic input occur during evaluation.

## Primary outputs

- first evaluation action TRUE − PERMUTED;
- first evaluation gain TRUE − PERMUTED;
- mean evaluation action TRUE − PERMUTED;
- mean evaluation gain TRUE − PERMUTED.

## Interpretation

A separation after autonomous acquisition supports behavioral specificity of a second-order mapping learned inside the persistent organism. It remains computational evidence and does not establish phenomenal consciousness.


## Verified result

GitHub Actions run **36946964601**; artifact **11201784892**; SHA256 **bf4aed2caaaff14e3aac2dca54e584cc0c10d38f9dde13c0f4720db8eacc9ea8**.

- second-order model starts empty and reaches **48 samples per replica**;
- exact model recovery at the evaluation-pair construction: **100%**;
- first TRUE − PERMUTED action: **+0.2916667**, p **0.3417829**
- first TRUE − PERMUTED gain: **−0.0141513**, p **0.7728114**
- mean TRUE − PERMUTED action: **+0.0833333**, p **0.6331683**
- mean TRUE − PERMUTED gain: **+0.0256299**, p **0.4691765**

Interpretation: the persistent organism successfully learned the second-order model online from counterfactual prediction errors, but the learned mapping did not produce a statistically significant TRUE-vs-PERMUTED behavioral separation under this protocol.
