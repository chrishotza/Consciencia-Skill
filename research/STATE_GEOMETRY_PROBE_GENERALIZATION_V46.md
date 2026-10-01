# V46 — Cross-Probe History Generalization

V46 tests whether temporal-history information retained by the system remains accessible when the subsequent external stimulus changes.

There are three deterministic probes (A, B, C). For each held-out parameter point and held-out probe, the classifier trains on the other five parameter points and the other two probes, then predicts the history class from the future **state trajectory only** under the unseen probe.

No reference trajectory, angular transform, or current memory/pressure feature is provided to the classifier.

Chance accuracy is 25%. The result is evaluated across all 18 parameter×probe folds.

This is a task/context generalization test for internal history access. It does not establish consciousness, subjective experience, sentience, or phenomenological awareness.
