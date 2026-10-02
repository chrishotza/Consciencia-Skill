# I0 — Interoceptive Instrumentation

## Status

**Instrumentation implemented; causal regulation not yet enabled.**

I0 is intentionally read-only. It does not change organism state, policy, rewards, or trajectory selection.

## Instrumented variables

The current probe exposes bounded internal signals derived from the persistent organism state:

| Signal | Source |
|---|---|
| prediction_error | `self_prediction_error` |
| prediction_confidence | `self_prediction_confidence` |
| dynamic_pressure | `dynamic_pressure` |
| attractor_distance | `dynamic_attractor_distance` |
| memory_load | memory count / configured memory limit |
| dynamic_activity | magnitude of dynamic state + dynamic memory |
| state_change | absolute current-vs-previous dynamic state |
| operating_condition | declared weighted aggregate of the above signals |

The aggregate is an engineering diagnostic, not a biological claim and not a consciousness score.

## Invariance requirements

The probe must:

- be deterministic for identical state inputs;
- leave the supplied `OntologicalState` unchanged;
- keep readout variables in the declared [0,1] range;
- expose each component separately so the aggregate can be audited;
- remain independent of semantic self-report.

These requirements are covered by unit tests.

## Next confirmatory step

I1 should preregister the viability ranges and test whether the organism can estimate its internal operating condition after controlled perturbations without semantic labels.

Before enabling any interoceptive controller, the protocol should specify:

- primary endpoint;
- perturbation distribution;
- viability bounds;
- recovery horizon;
- matched controls;
- target-permuted controls;
- lesion of the interoceptive readout;
- replication count and seed policy;
- analysis rule;
- artifact validation.

Only after I1 passes should the interoceptive signal be permitted to modulate policy.

## External motivation

Lee et al. (2026) propose interoceptive AI as an architecture in which artificial systems explicitly factor internal and external states and use mathematically represented internal states to modulate adaptive behaviour. The Skill-Conscious I0 layer is a narrower instrumentation step toward testing such mechanisms.

Reference: Lee et al. (2026), *Life-inspired interoceptive artificial intelligence for autonomous and adaptive agents*, Nature Machine Intelligence 8, 1335–1346.

https://doi.org/10.1038/s42256-026-01296-8
