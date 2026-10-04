# Metacognitive Uncertainty

Skill-Conscious can turn its runtime-owned estimate of predictive uncertainty into a causal pressure toward epistemic action.

## Causal chain

```text
prediction
   ↓
observed outcome
   ↓
prediction accuracy
   ↓
expected own accuracy
   ↓
metacognitive uncertainty
   ↓
epistemic value of a candidate
   ↓
trajectory selection
   ↓
new outcome
```

The runtime derives:

```text
uncertainty = 1 - expected_accuracy
```

For a candidate with `epistemic_value`:

```text
contribution =
    uncertainty
    × epistemic_value
    × metacognitive_uncertainty_weight
```

The contribution is calculated by the runtime and is therefore not an arbitrary label supplied by the model.

## Verification

The test battery verifies that:

- low uncertainty favors an ordinary goal-aligned trajectory;
- high uncertainty can causally select an epistemically valuable trajectory;
- an intervention on predictive self-trust reverses the selection;
- the effect persists through restart;
- model-generated frames cannot forge the runtime-owned uncertainty value.

This is an operational metacognitive mechanism. It is not evidence of phenomenal consciousness by itself.
