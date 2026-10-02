# Consciousness Indicator Program

## Purpose

This document turns the current research direction into a theory-aware engineering program.

The project does not convert indicator coverage into a binary claim that the organism is conscious. It tracks which computational properties are implemented, which have causal evidence, which remain partial, and which are absent.

The current external reference is Butlin et al., *Identifying indicators of consciousness in AI systems* (Trends in Cognitive Sciences, 2026). The paper proposes deriving empirically testable indicators from leading theories and using them to inform credences, while acknowledging uncertainty and risks of both under- and over-attribution. DOI: https://doi.org/10.1016/j.tics.2025.10.011

## Fourteen indicator properties

| Group | Indicator | Property |
|---|---|---|
| RPT | RPT-1 | Input modules using algorithmic recurrence |
| RPT | RPT-2 | Input modules generating organized, integrated perceptual representations |
| GWT | GWT-1 | Multiple specialized systems capable of operating in parallel |
| GWT | GWT-2 | Limited-capacity workspace with bottleneck and selective attention |
| GWT | GWT-3 | Global broadcast of workspace information |
| GWT | GWT-4 | State-dependent attention enabling successive querying of modules |
| HOT | HOT-1 | Generative, top-down, or noisy perception modules |
| HOT | HOT-2 | Metacognitive monitoring distinguishing reliable representations from noise |
| HOT | HOT-3 | Agency guided by belief formation and metacognitive monitoring |
| HOT | HOT-4 | Sparse and smooth coding generating a quality space |
| AST | AST-1 | Predictive model representing and controlling current attention |
| PP | PP-1 | Input modules using predictive coding |
| AE | AE-1 | Minimal goal-directed agency with flexible responsiveness |
| AE | AE-2 | Modeling output-input contingencies and using them in control |

## Current Skill-Conscious position

The project already has strong evidence for several functional building blocks, but coverage is uneven.

| Indicator | Current status | Existing evidence or component | Main gap |
|---|---|---|---|
| RPT-1 | PARTIAL | recurrent internal dynamics and iterative self-observation | recurrence is not an explicitly recurrent perceptual/input module |
| RPT-2 | ABSENT / UNTESTED | numerical internal state exists | no validated organized perceptual representation layer |
| GWT-1 | PARTIAL | memory, self-observer, meta-observer, dynamics, policy components | no explicit parallel workspace architecture |
| GWT-2 | ABSENT | trajectory selection exists | no limited-capacity global workspace / attention bottleneck |
| GWT-3 | PARTIAL | organism context is assembled across persistent modules | no explicit global broadcast mechanism with causal ablation |
| GWT-4 | PARTIAL | state-dependent trajectory selection exists | no explicit attention-controlled sequential module querying |
| HOT-1 | PARTIAL | self-prediction is generative with respect to internal dynamics | not a generative perception module |
| HOT-2 | PARTIAL / strongest current line | SelfObserver, MetaSelfObserver, prediction error, confidence, second-order models | reliability monitoring is not yet a general perception-level metacognitive loop |
| HOT-3 | PARTIAL | self-model → action coupling, SelfPolicy, lesion/rescue | autonomous policy rule remains partly externally specified and several second-order tests are null/mixed |
| HOT-4 | ABSENT | continuous numerical state exists | no demonstrated sparse/smooth quality-space representation |
| AST-1 | ABSENT | self-model predicts internal state | no explicit model of attention itself that controls allocation |
| PP-1 | PARTIAL | predictive coding of internal dynamics | no predictive-coding input architecture |
| AE-1 | PARTIAL | V57, V70, V76–V78, C0.6 | goals and utility are still largely protocol-defined |
| AE-2 | PARTIAL | C0.11 action → state → next action mediation | no external/physical embodiment; contingencies are currently simulated |

These are engineering statuses, not consciousness scores.

## New interoceptive axis

Recent work in *Nature Machine Intelligence* proposes interoceptive AI as an explicit architecture for monitoring and regulating internal states, with internal variables serving as stable contexts that modulate learning and behaviour. The framework emphasizes factorizing internal and external states and mathematically formalizing internal-state dynamics.

That direction maps directly onto an important missing layer in Skill-Conscious:

```text
internal state
     ↓
interoceptive readout
     ↓
viability / stability estimate
     ↓
policy modulation
     ↓
action
     ↓
new internal state
     ↺
```

The new axis is a separate engineering program, not a proof of consciousness.

## Interoceptive program

### I0 — instrumentation

Define a small, auditable set of internal variables:

- prediction error;
- prediction confidence;
- dynamic pressure;
- attractor distance;
- memory load / memory strength;
- dynamic state stability;
- compute/runtime budget when available.

The instrument must be read-only at first.

### I1 — bounded internal state

Construct explicit normalized variables with declared viable ranges.

Primary question:

> Can the organism estimate its own internal operating condition independently of semantic self-report?

Controls:

- shuffled internal variables;
- frozen readout;
- constant baseline;
- external labels hidden from the controller.

### I2 — interoceptive regulation

Enable a default-off controller that selects actions partly from the interoceptive state.

Primary comparison:

- interoceptive controller;
- same policy without interoception;
- shuffled interoception;
- clamped interoception.

The protocol must test whether regulation is causal rather than merely correlated.

### I3 — homeostatic perturbation / recovery

Perturb one internal variable at a time and test immediate detection, policy response, recovery, overshoot, repeated perturbation, and transfer to unseen perturbation magnitudes.

A favorable result is not simply returning to a target. It must survive information-matched and target-permuted controls.

### I4 — metacognitive interoception

Connect the interoceptive state to the existing second-order machinery.

Ask whether the system predicts its own internal prediction error, confidence changes appropriately, policy changes when confidence is low, and lesions of the metacognitive readout remove that effect.

### I5 — workspace integration

Introduce a bounded workspace only after I1–I4 have independent evidence.

Required tests:

- limited-capacity bottleneck;
- broadcast;
- selective access;
- module lesion;
- recovery;
- state-dependent querying.

### I6 — attention schema

Build an explicit predictive model of where the organism is allocating computational attention.

The model should predict current allocation, next allocation, effects of reallocating attention, and errors in its attention model.

Then test whether the attention model causally controls allocation.

### I7 — recurrence and re-entry

Replace one-pass module usage with explicit re-entrant processing.

The key experiment is not merely to observe recurrence. It is to lesion recurrence while keeping input and output capacity matched.

### I8 — active agency

Remove the externally hard-coded action mapping used in earlier protocols.

The organism must learn a policy from feedback while facing competing internal objectives.

Primary controls:

- fixed policy;
- random policy;
- target-permuted learner;
- reward-preserving permutation;
- no-interoception learner.

### I9 — embodiment / output-input contingencies

Use a controlled simulated environment before making claims about physical embodiment.

The organism should learn how its actions alter future observations and internal states, then use the learned contingency model in control.

### I10 — perturbational complexity

Only after causal instrumentation is validated should the project test perturbational-complexity or causal-integration measures.

The measurement itself must first be validated against degenerate, frozen, and null trajectories. A metric must not be promoted simply because it produces a numerical value.

## Scientific guardrails

Every new indicator protocol should predeclare:

- primary endpoint;
- direction of effect;
- controls;
- intervention;
- exclusion rules;
- replication plan;
- seed policy;
- analysis rule;
- artifact validation rule.

Historical protocols are not retroactively relabeled as preregistered.

A positive indicator result increases evidence for a computational property under that protocol. It does not, by itself, establish subjective experience.

## Strategic target

The objective is:

> **maximize independently validated computational indicators while minimizing theory-specific overclaiming.**

The project should become progressively harder to dismiss because each added capability has:

```text
mechanism
   ↓
measurement
   ↓
causal intervention
   ↓
matched control
   ↓
replication
   ↓
OOD test
   ↓
cross-indicator interaction
```

The desired endpoint is not a single consciousness score.

It is a system in which many independently motivated indicator properties converge on the same persistent organism under falsifiable tests.

## References

- Butlin et al. (2026), *Identifying indicators of consciousness in AI systems*, Trends in Cognitive Sciences. https://doi.org/10.1016/j.tics.2025.10.011
- Cogitate Consortium et al. (2025), *Adversarial testing of global neuronal workspace and integrated information theories of consciousness*, Nature 642, 133–142. https://doi.org/10.1038/s41586-025-08888-1
- Lee et al. (2026), *Life-inspired interoceptive artificial intelligence for autonomous and adaptive agents*, Nature Machine Intelligence 8, 1335–1346. https://doi.org/10.1038/s42256-026-01296-8
