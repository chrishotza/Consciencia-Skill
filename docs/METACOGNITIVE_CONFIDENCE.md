# Metacognitive Confidence Gate

The runtime now supports a causal confidence layer over explicit trajectory predictions.

## Mechanism

A candidate may expose:

- `predicted_outcome`
- `predicted_state_delta`
- `predicted_outcome_confidence`

The runtime reads a persistent estimate of its own prediction accuracy:

`metacognitive_prediction_expected_accuracy`

and transforms reported confidence as:

```
trust_adjusted =
    0.5 + (reported_confidence - 0.5)
          * (2 * expected_accuracy - 1)
```

The adjusted value enters trajectory scoring through a bounded runtime-owned contribution.

## Causal chain

```
PREDICTION
   ↓
OBSERVED OUTCOME
   ↓
PREDICTION ERROR
   ↓
ESTIMATED OWN ACCURACY
   ↓
TRUST IN NEXT PREDICTIONS
   ↓
TRAJECTORY SELECTION
```

The expected-accuracy value can be intervened on without adding prediction evidence and restored exactly. The reversible probe requires selection divergence, restoration, and unchanged evidence.

This is a computational self-calibration mechanism. It is not evidence of phenomenal consciousness.

## Longitudinal intervention

The repository also runs a multi-cycle protocol:

```text
cycles 0–3  expected accuracy = 0.9  → high-confidence selection
cycle 4   intervene to 0.1
cycles 4–7  expected accuracy = 0.1  → low-confidence selection
cycle 6   deterministic restart
cycle 8   restore the original snapshot
cycles 8–11 expected accuracy = 0.9  → high-confidence selection restored
```

The protocol checks that the intervention survives restart, flips downstream trajectory selection, and restores the original behavior without adding prediction evidence during the intervention.

