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

~~~text
load_state()
observe()
model(context)
save_state()
~~~

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
