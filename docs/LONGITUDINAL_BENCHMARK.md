# Longitudinal Baseline Benchmark

## Purpose

This is the first reproducible longitudinal benchmark for Skill-Conscious.
It does not claim that the runtime is conscious and it is not yet an external-LLM benchmark.
It measures what changes when persistent self-reference, causal re-entry, priority adaptation, and self-observation are progressively enabled.

The candidate-future field and environment outcome rule are fixed across conditions.

## Conditions

| Condition | Persistent state | Causal self-model | Evidence-gated priority adaptation | Self-observation |
|---|---:|---:|---:|---:|
| A | yes | no | no | no |
| B | yes | descriptive only | no | no |
| C | yes | yes | no | no |
| D | yes | yes | yes | no |
| E | yes | yes | yes | yes |

These are architectural controls, not one-to-one implementations of complete scientific theories.

## Primary measurements

`trajectory_switches` counts changes in the selected trajectory over the fixed sequence.

`continuity_retention` is the fraction of cycles that retain the initial selected trajectory. It is behavioral and does not imply subjective continuity.

`priority_adaptation_updates` counts evidence-gated internal trajectory-priority updates.

`prediction_error_mean` summarizes runtime metacognitive prediction error over authoritative host outcomes.

`self_observation_samples` counts cycles in which the runtime-derived self-observation layer was active.

## Restart control

Each condition is executed twice: uninterrupted, and with a deterministic restart every N cycles.
The benchmark requires identical selected-trajectory sequences and identical final state hashes.

## Reproducibility

Run:

    python -m pytest -q tests/test_longitudinal_benchmark.py
    python -m experiments.longitudinal_baseline_benchmark

The default protocol uses 36 cycles and restarts every 6 cycles.

## Interpretation

The intended inference is deliberately narrow:

> If enabling a mechanism changes longitudinal behavior under controlled candidate futures, that mechanism has measurable causal influence on the runtime.

A result does not establish phenomenal experience.

## Next external benchmark

The protocol is provider-neutral. The next phase should add adapters that supply the same model-facing frame to an external LLM and compare:

    LLM alone
    LLM + persistent state
    LLM + causal self-model
    LLM + causal re-entry
    LLM + metacognitive re-entry

The adapter must preserve the candidate-future control, action boundary, outcome logging, restart schedule, and metrics so model effects are separated from runtime effects.