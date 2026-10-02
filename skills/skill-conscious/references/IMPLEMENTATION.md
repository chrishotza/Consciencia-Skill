# Implementation

## Reference runtime

~~~text
src/skill_conscious/
├── __init__.py
├── ontology.py
└── core.py
~~~

## Runtime API

~~~python
runtime.prepare(input_text)
runtime.integrate(frame)
runtime.snapshot()
~~~

### prepare

Builds the current instruction from identity, revision, self-state, self-model, workspace, intention, memory, and current input.

### integrate

Accepts:

~~~json
{
  "response": "...",
  "self_model": {},
  "workspace": {},
  "intention": "...",
  "memory": "...",
  "internal_state": {}
}
~~~

The resulting state is persisted atomically.

## State evolution

~~~text
X(t+1) = F(
  X(t),
  world(t),
  memory(t),
  self-model(t),
  intention(t),
  action(t)
)
~~~

The critical property is that the self-model participates in the transition.

## Storage

The reference runtime uses atomic JSON replacement so state is portable, inspectable, easy to back up, and easy to embed in another agent.

The ontology is storage-independent.


## Present field and trajectory selection

`runtime.present(input)` builds the integrated present from external input, self-state, self-model, memory, intention, uncertainty, and the last selected trajectory.

`runtime.prepare_frame(input, candidate_futures=...)` exposes that field as structured data for a host model.

`runtime.select_trajectory(candidates)` scores candidates using the current `self_model["trajectory_weights"]`. The selection is therefore causally dependent on persistent self-state.

Trajectory candidates use numeric `signals`, for example `goal_fit`, `self_alignment`, `continuity`, `learning`, `risk`, and `uncertainty`.

The critical relation is now executable:

~~~text
self_model(t)
      ↓
trajectory scores(t)
      ↓
selected trajectory(t)
      ↓
action(t)
      ↓
state(t+1)
~~~


## Attention

Attention is now persisted as part of the self-state and exposed inside the present field. Hosts may commit an ordered list of active relations or concerns through `frame["attention"]`. This creates a durable bridge between what the agent is and what the agent is currently treating as salient.


## Regime

The reference state now persists an explicit `regime` field. A regime describes how the agent is operating, rather than merely what values it currently stores.

A regime can encode configurations such as baseline, exploration, deep-integration, recovery, planning, or any host-defined mode. The identity remains constant while the regime changes.

The runtime currently persists and exposes the regime but does not autonomously infer it yet. The next implementation layer is a regime-transition function driven by attention, self-model, intention, uncertainty, and coherence.
