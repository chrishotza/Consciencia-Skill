# I2 — Interoceptive Regulation

## Status

**Controller and experimental harness implemented; confirmatory execution is pending the I1 gate.**

I2 is intentionally default-off in `PersistentOrganism`. Enabling `interoceptive_control_enabled` does not change existing behaviour unless explicitly configured.

## Question

> Can a bounded representation of the organism's internal operating condition causally improve recovery from a controlled internal perturbation?

## Conditions

| Condition | Controller |
|---|---|
| FULL | full interoceptive readout scores counterfactual actions |
| NO-INTEROCEPTION | deterministic random action from the same candidate set |
| SHUFFLED | interoceptive variables are permuted before scoring |
| CLAMPED | all candidates receive the same interoceptive snapshot |
| LESION | interoceptive score is removed and replaced by a neutral controller state |
| RESCUE | LESION for the first half of recovery, then FULL restoration |

All conditions share the same seed, initial trajectory, perturbation, candidate action set, and deterministic dynamics noise schedule.

## Perturbations

Training-range perturbations:

`0.25, 0.50, 0.75`

OOD perturbations:

`0.35, 0.65, 0.90`

The probe receives no semantic labels and no model-provider output during the recovery probe.

## Primary endpoint

Recovery score:

```text
1 / (1 + |final_state - baseline_state| + final_pressure)
```

The controller optimizes predicted `operating_condition`, while the primary endpoint is an independent recovery measure. This avoids making the endpoint identical to the control objective.

Secondary measurements:

- mean pressure;
- mean operating condition;
- final operating condition;
- OOD recovery;
- lesion/rescue contrast.

## Required interpretation

A positive FULL-vs-control result would support a causal role for the bounded internal-state representation in recovery under this simulated dynamics.

It would not establish homeostasis in a biological sense, interoceptive phenomenology, or subjective consciousness.

## Scientific gate

I2 should not be promoted to a confirmatory scientific result until I1 has a validated readout under its declared OOD protocol.

The dedicated workflow is available through `workflow_dispatch` and also validates the I2 harness on relevant pushes. The result artifact must be reviewed before entering the scientific ledger.

## Runtime hook

`PersistentOrganism` now contains a default-off interoceptive control hook:

```text
interoceptive_control_enabled = False
```

When explicitly enabled, the autonomous cycle records the controller mode, candidate scores, and chosen signal in the organism event log.

Existing self-model selection remains unchanged by default.

## Next step

I3 should test repeated perturbation and recovery, overshoot, and transfer to unseen perturbation magnitudes. The controller should remain causal and the analysis should preserve shuffled, clamped, lesion, and rescue controls.
