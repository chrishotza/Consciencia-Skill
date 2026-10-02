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
