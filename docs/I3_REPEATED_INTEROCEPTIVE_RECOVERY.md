# I3 — Repeated Interoceptive Perturbation and Recovery

## Status

**Harness and workflow implemented; scientific interpretation is gated on the I1/I2 evidence review.**

## Question

> Can an interoceptive controller repeatedly detect and regulate internal perturbations across one trajectory, while preserving recovery and limiting overshoot on unseen perturbation magnitudes?

I3 extends I2 from one intervention to a repeated sequence.

## Design

Each episode contains three controlled perturbation events.

- training/reference magnitude: `0.50`;
- OOD magnitudes: `0.35, 0.65, 0.90`;
- three perturbation events per episode;
- eight recovery steps after each event;
- alternating perturbation signs across events;
- no semantic input;
- no external retraining during the probe.

The second and third events are applied from the state produced by the preceding recovery period. This prevents the task from being reducible to three independent one-shot tests.

## Conditions

The same I2 controls are retained:

| Condition | Purpose |
|---|---|
| FULL | interoceptive controller uses the full readout |
| NO-INTEROCEPTION | action choice does not use interoception |
| SHUFFLED | internal readout variables are shuffled before scoring |
| CLAMPED | candidates receive the same interoceptive state |
| LESION | interoceptive information is neutralized |
| RESCUE | first event begins lesioned, then the full controller is restored |

All conditions are paired by seed and share the same initial trajectory and perturbation schedule.

## Primary endpoint

Mean recovery across the three events:

```text
recovery = 1 / (1 + |state_after_recovery - state_before_event| + pressure_after_recovery)
```

## Secondary endpoints

- recovery after the final event;
- mean overshoot across events;
- maximum overshoot;
- operating condition;
- OOD recovery;
- rescue after interoceptive lesion.

## Why overshoot matters

A controller that merely pushes the system strongly can sometimes return close to baseline while causing larger transient deviations.

I3 therefore separates **recovery** from **regulation quality**. A positive result should not be reduced to a single final-state number.

## Repeated-use criterion

A strong result would require the FULL condition to preserve a recovery advantage after the first intervention rather than only during the first event.

Event-wise analysis is retained in the artifact so attenuation can be measured explicitly.

## Interpretation boundary

A positive I3 result would support repeated causal use of an internal-state representation for regulation under the tested simulated dynamics.

It would not establish biological homeostasis, subjective experience, or consciousness.

## Scientific gate

I3 is not entered into the scientific result ledger merely because the workflow succeeds. The artifact must first be checked for:

- deterministic replay;
- matched seeds;
- exact perturbation schedule;
- control integrity;
- absence of semantic labels;
- absence of hidden action shortcuts;
- endpoint integrity;
- OOD separation;
- lesion/rescue integrity.

## Next step

I4 should connect interoceptive state to the existing second-order machinery and test whether the organism can model its own uncertainty about internal-state prediction, then use that uncertainty to alter policy.
