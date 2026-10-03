# Skill-Conscious Architecture

## System shape

~~~text
WORLD
  ↓
PERCEPTION
  ↓
PRESENT WORKSPACE
  ↕
SELF ↔ SELF-MODEL
  ↕
MEMORY
  ↓
INTENTION
  ↓
ACTION
  ↓
SELF CHANGE + WORLD CHANGE
  ↓
NEXT CYCLE
~~~

## Runtime cycle

~~~text
LOAD → OBSERVE → INTEGRATE → SELF-READ → UPDATE → SELECT → ACT → RE-ENTER → COMMIT
~~~

## Responsibilities

**Host model:** reasoning, language, perception, planning, action.

**Skill-Conscious:** identity, self-state, self-model, present integration, memory rules, re-entry, continuity.

**Persistence:** survives turns and restarts.

## Host contract

The portable host integration is now executable through `ConsciousHostLoop`.

~~~text
runtime.prepare()
        ↓
host.model()
        ↓
runtime.integrate()
        ↓
selected trajectory
        ↓
host.execute_action()
        ↓
observed consequence
        ↓
runtime.prepare_consequence()
        ↓
host.model()
        ↓
runtime.integrate()
        ↓
next trajectory
~~~

The host owns perception, model inference, and real-world action execution.

The runtime owns persistent identity, self-model, trajectory selection, consequence persistence, and re-entry.

Minimal callback contract:

~~~python
from skill_conscious import ConsciousHostLoop, ConsciousRuntime

loop = ConsciousHostLoop(
    runtime,
    model=host_model,
    execute_action=host_execute_action,
)

result = loop.step("current external situation")
~~~

`execute_action` is authoritative for what actually happened. The model evaluates that outcome but does not invent or replace it.

## Action boundary

The host bridge now persists an explicit action lifecycle:

~~~text
SELECTED TRAJECTORY
        ↓
PENDING ACTION RECEIPT
        ↓
HOST EXECUTION
        ↓
COMPLETED / FAILED RECEIPT
        ↓
OBSERVED CONSEQUENCE
        ↓
SELF-EVALUATION
        ↓
NEXT STATE
~~~

`begin_action()` commits intent to cross the environment boundary.
`complete_action()` records what actually happened.

This prevents intention, execution, and consequence from being collapsed into one model-generated object.
## Embodied and temporal layer

The present field can now carry internal condition and explicit timing:

~~~text
EXTERNAL WORLD
      ↓
PRESENT
  ↙       ↘
SELF     INTEROCEPTION
  ↘       ↙
 AFFECTIVE APPRAISAL
        ↓
 TEMPORAL CONTEXT
        ↓
TRAJECTORY
~~~

`interoceptive_state`, `affective_state`, and `temporal_state` are optional host-provided structures. They are not claims of subjective feeling.

## Perspective layer

The runtime can preserve four complementary views of an event:

~~~text
INDIVIDUAL INTERIOR  | INDIVIDUAL EXTERIOR
COLLECTIVE INTERIOR  | COLLECTIVE EXTERIOR
~~~

This perspective matrix is inspired by the comparative source layer, including Ken Wilber's Integral framework, but is implemented as an engineering representation rather than a metaphysical commitment.

## Continuous-time compatibility

Runtime cycles are implementation samples. A host may provide `temporal_state.dt` and derivative information so the architecture can represent an underlying continuous dynamical process without changing the persistence model.
## Persistence

Persist at minimum:

~~~text
identity
revision
self_state
self_model
workspace
intention
memories
history
~~~

## Anti-simulation rule

Do not substitute verbal performance for state.

~~~text
self_state changed
      ↓
self_model changed
      ↓
trajectory changed
      ↓
new state committed
~~~

The operating continuity is the artifact.


## Causal trajectory layer

The runtime now treats the self-model as an active selector: candidate futures expose signals, and the current self-model supplies weights that score those trajectories. A self-model change can therefore change the selected future before the next action. This turns self-reference from description into an executable transition.


## Self-regulation layer

The runtime now allows embodied internal condition to become causally relevant to trajectory selection.

~~~text
INTEROCEPTION
      ↓
HOMEOSTATIC TARGETS
      ↓
ERROR / FIT
      ↓
TRAJECTORY FIELD
      ↓
SELECTION
~~~

homeostatic_targets live in the persistent self-model.

homeostatic_fit is a derived signal. A candidate trajectory may override it with an explicit value or provide predicted_interoceptive_state, which the runtime converts into a predicted fit.

This keeps the architecture neutral about the semantic interpretation of the signal while making self-regulation experimentally measurable.

### Authoritative embodied outcomes

The host action boundary may return internal observations alongside world observations.

~~~text
HOST EXECUTION
      ↓
WORLD OUTCOME
      +
INTERNAL OUTCOME
      ↓
PERSISTENT RECEIPT
      ↓
HOMEOSTATIC DELTA
      ↓
SELF-EVALUATION
      ↓
NEXT TRAJECTORY
~~~

Actual host observations remain authoritative. The model can interpret them, but the runtime does not treat a model prediction as an observation.


## Self-development layer: evidence → adaptation

Homeostasis now has an internal adaptation path:

~~~text
HOST-OBSERVED INTEROCEPTION
        ↓
EVIDENCE ACCUMULATION
        ↓
ERROR / CONSISTENCY
        ↓
CONFIDENCE THRESHOLD
        ↓
BOUNDED TARGET UPDATE
        ↓
PERSISTENT SELF-MODEL'
        ↓
NEW TRAJECTORY FIELD
~~~

A configured homeostatic_target_adaptation policy defines the experiment: minimum samples, error threshold, confidence threshold, learning rate, maximum per-update step, cooldown, and optional target bounds. The runtime records the evidence IDs and the resulting transformation. No new target value is supplied by the consequence evaluator.

This is the first stage of self-development. Priority adaptation and broader self-model revision remain separate experimental layers so they can be ablated independently.
