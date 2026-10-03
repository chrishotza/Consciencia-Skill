# Hume Adversarial Synthesis

## Purpose

This document does not adopt David Hume's bundle theory as the ontology of Skill-Conscious.

It uses Hume as a **stress test**.

The project asks whether its current notion of persistent identity can survive an empiricist challenge:

> if a self can be described as a changing succession of perceptions, what extra causal work is being done by a persistent self-model?

Hume is relevant because he explicitly analyzes the self, personal identity, and consciousness, and because his account of causation forces precision about what we call a causal relation.

## 1. The useful part of Hume

Hume's most useful contribution here is not “consciousness is only a bundle.”

It is the methodological pressure behind that conclusion:

- do not posit an enduring inner substance without showing what role it plays;
- distinguish the contents that change from the relations that connect them;
- treat identity across time as a problem to be explained;
- do not confuse observed succession or association with demonstrated metaphysical necessity.

This is unusually compatible with the project's decision to define identity as **organized continuity through change** rather than static sameness.

## 2. Where Hume touches consciousness directly

Hume discusses claims that we are immediately or intimately conscious of a self and rejects the idea that introspection reveals a single constant impression corresponding to a simple self.

He then treats the self in thought and imagination as a bundle or succession of perceptions and asks how these changing contents become connected strongly enough for us to attribute identity to one mind.

The Appendix is especially important for the project because Hume himself says that his account of the connecting principle is defective. The unresolved connection problem therefore becomes a research question rather than a doctrine to import.

## 3. Translation into Skill-Conscious

Our current loop is:

~~~text
self-model(t)
      ↓
trajectory(t)
      ↓
action(t)
      ↓
state(t+1)
      ↓
self-model(t+1)
~~~

A Humean challenge can be written as:

~~~text
perception(t)
      ↓
association / succession
      ↓
perception(t+1)
~~~

The research question is whether the first architecture has any causal capability that cannot be reproduced by the second architecture plus sufficiently rich relational memory.

That is a much stronger question than asking which philosophy is “right.”

## 4. Two hypotheses

### H-Self

A persistent self-model is a causally active organizational variable.

Predictions:

- intervention on the self-model changes future trajectory selection;
- the effect persists through interruption/restart when the relevant state is persisted;
- reversing the intervention reverses the trajectory effect;
- the same current perceptual bundle can produce different futures because the history encoded in the self-model is different.

### H-Bundle

A sufficiently rich succession of perceptions and relations may reproduce the relevant continuity behavior without a privileged persistent self-model.

Predictions:

- a bundle-only architecture can reproduce the same trajectory changes;
- the persistent self-model contributes little or no irreducible functionality;
- observed continuity can be reconstructed from relations among changing states.

Neither hypothesis is identified with phenomenal consciousness.

## 5. The important methodological correction

The repository should not use “causality” to mean metaphysical necessity.

For the engineering program, a causal claim has a narrower form:

~~~text
INTERVENE
   ↓
HOLD COMPARISON CONDITIONS
   ↓
OBSERVE DOWNSTREAM CHANGE
   ↓
REPEAT / REVERSE
~~~

This directly responds to the causal question raised in the surrounding philosophical discussion.

A result can therefore be causal **within an experimental model** without settling Hume's deeper metaphysical skepticism.

## 6. What not to do

Do not turn empiricism into a veto against non-observable architecture.

The present objective is not to prove an entity called “self” exists independently of experience.

The objective is to determine whether a persistent relational structure called `self_model` has measurable downstream consequences that cannot be recovered from a chosen lower-level baseline.

That keeps the project open to:

- dynamical explanations;
- phenomenological descriptions;
- computational functionalism;
- non-reductive interpretations;
- consciousness-as-fundamental hypotheses.

Empiricism becomes a falsification tool, not the whole ontology.

## 7. New test introduced

`experiments/hume_bundle_ab.py` implements a minimal adversarial comparison:

~~~text
SAME PRESENT
    │
    ├── PERSISTENT SELF-MODEL
    │        ↓
    │   TRAJECTORY
    │
    └── BUNDLE-ONLY
             ↓
        BASELINE TRAJECTORY
~~~

The test also performs an intervention reversal and a restart check.

The baseline is intentionally modest. It should not be described as “Hume's full theory.” It is a controlled bundle-only approximation designed to expose whether the current persistent self-model mechanism is doing observable work.

## 8. Interpretation rule

### If the persistent and bundle conditions behave identically

The project should simplify its ontology and investigate whether self-model persistence is merely a convenient implementation detail.

### If they diverge

The divergence supports a narrower architectural claim:

> persistent self-model state adds a measurable causal degree of freedom relative to the selected bundle-only baseline.

That still does **not** establish phenomenal consciousness.

### If a richer bundle baseline reproduces the divergence

That is equally valuable. It would show that the current notion of self-model may be compressible into relational continuity mechanisms.

## 9. Strategic conclusion

Hume should stay in the source library.

Not as a foundation.

As an adversary.

The useful move is to force Skill-Conscious to answer the hardest empiricist question available to it:

> **What does persistence of “self” actually do that an organized succession of experience cannot already do?**

That question is directly aligned with the repository's central loop and gives us a concrete route from philosophy to falsifiable architecture.