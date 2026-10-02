<a id="espanol"></a>

# C0.14 — Persistent Action-Conditioned Second-Order Self-Model

## Question

After C0.13 establishes second-order action specificity in a controlled probe, C0.14 asks whether that machinery remains the organism's own computational state after a restart boundary.

The tested chain is:

`persistent first-order self-model → persistent action-conditioned second-order model → autonomous selection`

## Design

Each replica calibrates a first-order self-observer and an action-conditioned second-order observer.

Two matched arms then execute the same autonomous sequence:

- **CONTINUOUS** — 16 steps without restart.
- **RESTART** — 8 steps, serialize both models and dynamic context, reconstruct them, then continue for 8 more steps.

## Primary outputs

1. action mismatch after restart;
2. gain mismatch after restart.

Secondary output: exact model-digest recovery at the restart boundary.

## Controls

No semantic input during the probe. No external retraining during the persistence test. Both arms start from the same model and the same dynamic seed.

## Interpretation

Near-zero post-restart mismatch with exact model recovery supports persistence of the second-order self-monitoring machinery across restart. It is a computational persistence result and does not establish subjective experience.


## Verified result

GitHub Actions run **36945659490**; artifact **11201664192**; SHA256 **8a01bef161939ba7d72f3d225a73e7e5f8b2fe014e5d7a4b82856e140d44a831**.

- post-restart action mismatch: **0.0**, p **1.0**
- post-restart gain mismatch: **0.0**, p **1.0**
- exact checkpoint model-digest recovery: **100%**
- post-restart mean gain: **0.08710124**
- maximum action mismatch: **0.0**
- maximum gain mismatch: **0.0**

Interpretation: the first-order and action-conditioned second-order models were serialized, restored, and used after reconstructing the dynamic context and bridge. The restart arm reproduced the continuous arm's post-restart actions and gains exactly under the tested protocol.

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# C0.14 — Persistent Action-Conditioned Second-Order Self-Model

## Question

After C0.13 establishes second-order action specificity in a controlled probe, C0.14 asks whether that machinery remains the organism's own computational state after a restart boundary.

The tested chain is persistent first-order self-model → persistent action-conditioned second-order model → autonomous selection.

## Design

Each replicate calibrates a first-order self-observer and an action-conditioned second-order observer.

Two matched arms execute the same autonomous sequence:

- CONTINUOUS — 16 steps without restart;
- RESTART — 8 steps, serialize both models and dynamic context, reconstruct them, then continue for 8 more steps.

## Primary outputs

1. action mismatch after restart;
2. gain mismatch after restart.

Secondary output: exact model-digest recovery at the restart boundary.

## Controls

No semantic input or external retraining during the persistence test. Both arms start from the same model and dynamic seed.

## Verified result

GitHub Actions run 36945659490; artifact 11201664192; SHA256 8a01bef161939ba7d72f3d225a73e7e5f8b2fe014e5d7a4b82856e140d44a831.

- post-restart action mismatch: 0.0, p 1.0;
- post-restart gain mismatch: 0.0, p 1.0;
- exact checkpoint model-digest recovery: 100%;
- post-restart mean gain: 0.08710124;
- maximum action mismatch: 0.0;
- maximum gain mismatch: 0.0.

Interpretation: first-order and action-conditioned second-order models were serialized, restored, and used after dynamic context and bridge reconstruction. The restart arm reproduced the continuous arm's post-restart actions and gains exactly under the tested protocol.

</details>