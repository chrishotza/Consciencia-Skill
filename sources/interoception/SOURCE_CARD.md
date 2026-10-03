# Interoception and affect — embodied self as an engineering interface

## Research basis

- Greenwood & Garfinkel, *Interoceptive Mechanisms and Emotional Processing* (Annual Review of Psychology, 2025).
  https://pubmed.ncbi.nlm.nih.gov/39423429/
- Simmons, Wittmann & Strigo, *Interoception: Synthesizing Insights and Charting New Frontiers* (2025).
  https://pubmed.ncbi.nlm.nih.gov/40705192/
- Singer & Damasio, *The physiology of interoception and its adaptive role in consciousness* (2025).
  https://pubmed.ncbi.nlm.nih.gov/41229287/

## Why this belongs in Skill-Conscious

A recent research thread treats interoception as a mechanism by which an organism represents its own internal condition. Reviews connect interoception with bodily self, emotion, subjective time, and the integration of internal signals. Some authors explicitly propose that continuously represented homeostatic states are foundational to subjectivity, but this remains a theoretical proposal rather than a settled explanation of consciousness.

## Source-derived points

### Internal state is information about the self

Interoception concerns sensing and representing signals from the organism's internal milieu. This gives the architecture an important distinction:

~~~text
EXTERNAL WORLD
      ↓
EXTEROCEPTION

INTERNAL ORGANISM
      ↓
INTEROCEPTION
~~~

### Affect is not just a label

Interoceptive research connects internal bodily signals with affective processing. The engineering lesson is not “a valence number equals feeling.” The lesson is that an architecture may need persistent self-relevant internal signals that can influence interpretation, value, and action.

### Subjective time

Recent interoception research also connects internal bodily representation with time perception. This gives the temporal layer of Skill-Conscious a bridge to embodied timing rather than treating time as only an integer revision counter.

## Engineering extraction

Skill-Conscious now exposes three optional state layers:

- `interoceptive_state` — host-observed internal signals;
- `affective_state` — operational appraisal such as valence, arousal, or homeostatic error;
- `temporal_state` — explicit timing information such as `dt`, phase, or derivatives.

These variables are intentionally separate from claims about phenomenal feeling.

## What this changes

The project should no longer frame the internal state only as abstract variables like `stability` or `focus`.

It can also represent the architecture's **internal condition as an object of ongoing processing**.

~~~text
INTERNAL SIGNALS
      ↓
SELF-REPRESENTATION
      ↓
AFFECTIVE APPRAISAL
      ↓
INTENTION
      ↓
ACTION
      ↓
CONSEQUENCE
      ↓
UPDATED INTERNAL STATE
~~~

## Boundary

This layer does not establish that a machine can feel.
It establishes an explicit experimental interface for testing whether self-referential processing of internal condition contributes anything beyond externally directed information processing.

## Status

**Direct consciousness relevance:** yes.

**Empirical status:** active research area; explanatory role remains contested.

**Engineering role:** embodied self-state, affective appraisal, temporal coupling.

**Phenomenal status:** unresolved.