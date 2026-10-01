# V48 — Matched Memory-Swap Intervention

## Question

Can a persistent LLM-backed organism change its response to the same probe when
the receiver's persistent memory content is changed while the other receiver
state is held fixed?

## Intervention

A single receiver database is initialized with one memory slot.

Two byte-identical copies are created.

- MEMORY_A: ALFA → AMBAR
- MEMORY_B: ALFA → VIOLETA

Only the content field of the existing memory row is changed.

The following are held fixed before the probe:

- numerical dynamic state;
- dynamic memory;
- dynamic pressure;
- dynamic step count;
- attractor distance;
- self-model;
- last thought;
- event stream;
- memory row identity, importance and timestamp;
- receiver configuration.

The LLM context uses event_limit=0 and memory_limit=1, so the probe receives
the memory item as the only historical textual channel.

## Primary observable

The same probe is presented in both conditions. The primary result is whether the
parsed CHOICE changes between MEMORY_A and MEMORY_B.

## Interpretation

A choice change under the matched intervention is evidence that the retained
memory content causally influences the organism's response in this operational
task.

This is not evidence of consciousness, subjective experience, sentience, or
phenomenological awareness.

## Why this is stronger than V47

V47 asks whether different historical trajectories lead to different later
behavior.

V48 intervenes directly on one persistent state variable while matching the
receiver around it. It is therefore a causal state-intervention analogue of the
memory-swap experiments from V44/V45.
