# Dynamic Core v6

This layer adds an experimental sensory-affective-dynamic field to Skill-Conscious.

Architecture:

HOST OBSERVATION
  -> SENSORY / AFFECTIVE APPRAISAL
  -> DYNAMIC PROFILE
  -> EXPERIENCE FIELD
  -> PERSISTENT RE-ENTRY
  -> EXPERIENCE ATTRACTOR
  -> TRAJECTORY BIAS
  -> CONSCIOUS RUNTIME SELECTION

Operational layers:

- sensor_affect.py: prediction error, coherence, valence and self-relevance as explicit appraisal functions.
- dynamics.py: persistence, synchrony proxy, metastability proxy, Lempel-Ziv complexity and avalanche measures.
- experience_field.py: coupled state vector joining sensory and dynamic measurements.
- reentry.py: restart-persistent field expectation, consequence evidence and hysteresis.
- attractor.py: recurring-state basin, recurrence, stability and perturbation-recovery measurement.
- runtime_bridge.py: explicit bridge that produces a selected trajectory frame for ConsciousRuntime.integrate() and strips runtime-owned dynamic state from model frames.

These mechanisms are engineering constructs and are not presented as a detector or proof of phenomenal consciousness.

Integrated ablation:
A = runtime-only
B = persistent re-entry without attractor return bias
C = learned attractor + recovery evidence
D = restart after persistence

Expected deterministic result: A -> explore, B -> explore, C -> preserve, D -> preserve.
