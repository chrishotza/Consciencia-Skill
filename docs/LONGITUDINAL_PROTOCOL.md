# Longitudinal Organism Protocol v1

## Goal

Measure whether a real persistent LLM-backed organism maintains an observable
trajectory across repeated WAKE cycles, DREAM cycles, autonomous cycles, and a
process restart.

This protocol measures engineering observables. It does not treat persistence,
memory, or self-reference as sufficient evidence of subjective consciousness.

## Core sequence

The bounded protocol repeats:

```
stimulus
  ↓
WAKE
  ↓
dynamic state update
  ↓
DREAM or autonomous cycle
  ↓
SQLite persistence
  ↺
```

After the requested cycles complete, SQLite is closed and reopened. One additional
WAKE cycle is then executed from the recovered state.

## Recorded observables

Every dynamic advancement writes one row to `dynamic_snapshots` containing:

- regime;
- step interval;
- input signal;
- previous state;
- state;
- dynamic memory;
- pressure;
- attractor distance;
- timestamp.

The protocol also records:

- persistent events;
- textual memories;
- self-model version;
- boot count;
- WAKE/DREAM lifetime counters;
- trajectory/state fingerprints.

## Modes

### fake

Deterministic provider used for CI and instrumentation audits.

### live

Uses the configured OpenAI-compatible provider:

- `ONTTO_API_KEY`
- `ONTTO_MODEL`
- `ONTTO_API_BASE_URL` (optional)

The live mode is the scientifically relevant organism run. The fake mode only
tests that the instrumentation and persistence protocol work.

## 24-hour execution

The script is bounded by cycle count and sleep duration rather than hard-coding a
24-hour wall-clock loop.

For a real 24-hour observation, choose a cycle period appropriate to the study,
run the script with the corresponding `--sleep-seconds`, and retain the full
SQLite database plus JSON evidence.

GitHub Actions should not be used as the host for a wall-clock 24-hour run.
The persistent organism should run on a persistent local/server host.

## Recommended first live run

Use:

```
python experiments/longitudinal_organism_v1.py --mode live --cycles 40 --dream-every 10
```

This gives an initial bounded longitudinal run before committing to a full-day
observation.

A full-day run should preserve the same protocol configuration and only change
the observation horizon.
