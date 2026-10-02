# I6.1 — Causal Closure of the Self-Model

## Objective

I5.26 closed the descriptive shift×lag control sequence. I6.1 changes question class: instead of asking whether a self-model correlates with future behavior, ask whether using the self-model is causally necessary for the organism's trajectory selection.

## Conditions

### Intact

The learned SelfObserver predicts the next state for each candidate action. TrajectorySelector uses those predictions to choose the next trajectory. The self-model is then updated from the realized transition.

### Prediction lesion

The organism receives the same candidate actions and state information, and the SelfObserver continues learning, but trajectory selection is deprived of its prediction. All candidates receive the same baseline current-state prediction, producing a sham selection path.

### Frozen-update

The learned self-model continues to drive trajectory selection, but its parameters are frozen during evaluation. This separates the causal contribution of using a self-model from the contribution of continuously updating it.

## Frozen protocol

- 24 replicates;
- 24 exploratory warmup cycles;
- 48 evaluation cycles;
- candidate signals −1, 0, +1;
- 20,000 replicate-level sign permutations.

The warmup phase is shared so that all three conditions begin from matched dynamical state and matched self-model evidence.

## Primary endpoint

Counterfactual regret is the chosen candidate's true next-state distance from the attractor minus the best candidate's true next-state distance.

Primary contrast:

intact regret − prediction-lesion regret.

A negative value means the intact self-model-guided selector achieved lower counterfactual regret.

## Causal criterion

The key observation is not merely prediction accuracy. It is a change in the selected trajectory and its realized counterfactual quality when the predictive self-model is removed from the selection pathway while the information stream is kept matched.

## Boundary

I6.1 is a causal computational test of self-model-dependent agency. A positive result would support that the self-model is an operational causal component of the organism's behavior; it would still not establish subjective experience or consciousness.
