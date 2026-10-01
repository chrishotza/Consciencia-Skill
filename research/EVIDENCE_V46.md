# V46 — Cross-Probe History Generalization

## Status

OFFICIAL — GitHub Actions run 36796263059.

- Workflow commit: 6c0e902153861fc9946a3aba17638215032b37f5
- Artifact: state-geometry-probe-generalization-v46
- Artifact ID: 11133289361

The run completed successfully.

## Protocol

V46 tests whether temporal-history information remains decodable when the
subsequent external stimulus changes.

There are three deterministic probes: A, B and C.

For each held-out parameter point and held-out probe:

1. train on the other five parameter points;
2. train on the other two probes;
3. predict the four history classes from the future state trajectory only.

No reference trajectory, angular transform, current memory feature, or current
pressure feature is given to the decoder.

There are 18 parameter × probe folds. Chance accuracy is 25%.

## Fold results

| Held-out parameter | Probe A | Probe B | Probe C |
|---|---:|---:|---:|
| p1 | 56.25% | 52.50% | 62.50% |
| p2 | 38.75% | 43.75% | 46.25% |
| p3 | 48.75% | 52.50% | 43.75% |
| p4 | 52.50% | 67.50% | 50.00% |
| p5 | 41.25% | 33.75% | 31.25% |
| p6 | 52.50% | 65.00% | 51.25% |

Summary:

- mean accuracy: 49.4444%
- SD across folds: 9.8819 percentage points
- minimum fold: 31.25%
- maximum fold: 67.50%
- chance: 25%

All 18 folds were above chance.

## Interpretation

V46 provides evidence that history information can generalize partially to a
subsequent deterministic probe that was not used for training.

The large drop relative to V43/V45 is itself informative. It means the stronger
history-decoding results do not automatically imply probe-invariant access to
history. The next question is how much of the retained information is invariant
across task/context changes versus tied to the particular probe family.

V46 should be treated as a generalization result, not as a universal-history
result.

## Relation to earlier controls

V37 and V39 already showed that the strongest V34–V36 angular/readout effect
does not survive every reference-free readout.

V43 then demonstrated reference-free history retention after external input was
set to zero.

V44 demonstrated causal downstream influence from memory replacement.

V45 showed that, under a common novel probe, the retained history changes the
future state trajectory even though the current external stimulus is identical.

V46 extends that line by asking whether the decoder can transfer across unseen
probes.

## Limitation

Nothing in V46 establishes consciousness, subjective experience, sentience, or
phenomenological awareness. It is evidence about information retention and
generalization in the project's computational dynamics.

## Reproducibility

The complete fold table is preserved in the GitHub Actions artifact. The
workflow was executed from commit 6c0e902153861fc9946a3aba17638215032b37f5.
