# Metacognitive Plasticity

Skill-Conscious can use its runtime-owned estimate of predictive reliability to modulate how strongly observed consequences update its persistent trajectory priorities.

## Causal chain

```
prediction
   ↓
predicted confidence
   ↓
prediction error
   ↓
expected own accuracy
   ↓
trust-adjusted confidence
   ↓
metacognitive plasticity factor
   ↓
consequence learning rate
   ↓
trajectory weights
   ↓
future trajectory selection
```

The factor is deliberately bounded:

```text
trust_adjusted =
    0.5 + (reported_confidence - 0.5)
          * (2 * expected_accuracy - 1)

plasticity_factor =
    clamp(0.5 + trust_adjusted, 0.5, 1.5)
```

When no trajectory-level confidence is available, the runtime falls back to its own expected accuracy. An expected accuracy of 0.5 is neutral: the factor is 1.0.

The mechanism is causal because the factor is applied to the actual consequence-learning delta. The same evidence therefore produces a different persistent self-model update when the runtime's own predictive trust is experimentally intervened.

## Verification

The test battery checks:

- higher trusted confidence produces a larger consequence update than lower trusted confidence under identical evidence;
- changing expected accuracy reversibly changes the downstream learning delta;
- the effect survives deterministic restart;
- direct legacy consequence deltas are also passed through the runtime-owned gate;
- a longitudinal experiment verifies intervention, persistence, suppression and restoration.

This is a computational metacognitive/plasticity mechanism. It is not evidence of phenomenal consciousness by itself.
