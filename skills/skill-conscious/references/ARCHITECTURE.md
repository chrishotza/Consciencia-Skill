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
