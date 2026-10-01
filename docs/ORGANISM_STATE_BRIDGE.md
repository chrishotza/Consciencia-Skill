# Organism ↔ Dynamic State Bridge

## Purpose

The persistent organism now carries a small, explicit numerical state alongside
the textual memory/event layer.

This is an integration layer, not a claim that the numerical state is a model
of subjective experience.

## State

The persisted organism state now includes:

- dynamic_state
- dynamic_prev_state
- dynamic_memory
- dynamic_pressure
- dynamic_attractor_distance
- dynamic_last_input
- dynamic_steps

The existing textual memory, event log, self-model and WAKE/DREAM counters remain
separate.

## Transition

The bridge calls the same src/ontto/dynamics.py transition function already used
by the research experiments.

For an explicit external wake signal u, the transition is:

x[t+1] = F(x[t], m[t], p[t], u[t])

The bridge advances the dynamics from the persisted state and writes the new
state back into SQLite.

The random seed is derived from:

dynamic_seed + dynamic_steps + local_step_offset

so a restart does not reset the deterministic noise sequence for the dynamic
trajectory.

## Signal policy

The default policy is intentionally simple:

- WAKE external interaction: +1.0
- autonomous cycle: 0.0
- DREAM: 0.0

This is not a semantic encoding of language. It is a controlled event/regime
signal used to connect the real persistent organism to the same dynamical core
that has been studied in V43–V46.

Changing this policy is a future experiment and must be treated as a separate
protocol.

## What this enables

The dynamic state is included in the organism serialized ontology, so it is
visible to the LLM context. This creates the first direct bridge between:

LLM organism
    ↕
persistent SQLite state
    ↕
research dynamics

## 24/7 behavior

autonomous_wake_cycle() is now implemented. This closes a pre-existing gap in
PersistentOrganism.run() and run_daemon.py, which already expected that method
when no external input was available.

The autonomous cycle performs a zero-input dynamic advancement and records the
result as a WAKE/autonomous event.

## Next experimental stage

The next stage is not to claim consciousness. It is to measure whether a real
LLM-backed persistent organism develops trajectory properties analogous to those
already studied in the simulator:

- history retention
- recovery after perturbation
- self-prediction
- common-probe history effects
- memory intervention effects
- WAKE vs DREAM differences
