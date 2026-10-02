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
