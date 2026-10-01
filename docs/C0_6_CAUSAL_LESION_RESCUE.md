# C0.6 — Causal Lesion / Rescue

## Question

C0.6 asks whether the organizational effects measured in C0 depend causally on the learned self-observer and self-policy, rather than merely co-occurring with them.

The system is trained once. After training, the same observer/policy snapshots are used for all conditions.

## Lesions

- **FULL** — trained self-observer + trained self-policy.
- **OBSERVER_LESION** — observer memory is reset after training; policy remains trained.
- **POLICY_LESION** — policy memory is reset after training; observer remains trained.
- **BOTH_LESION** — both are reset after training.
- **OBSERVER_RESCUE** — six recovery steps with the observer lesioned, followed by restoration of the original trained observer/policy.
- **POLICY_RESCUE** — six recovery steps with the policy lesioned, followed by restoration of the original trained observer/policy.

No semantic input is provided during the probe and there is no external retraining during the probe.

## Primary contrasts

The primary outputs are:

1. Full recovery-gain minus observer-lesion recovery-gain.
2. Full recovery-gain minus policy-lesion recovery-gain.
3. Full recovery-gain minus both-lesion recovery-gain.
4. Late rescue gain minus the corresponding early-lesion gain.
5. Lesion effect on final state distance from the post-intervention trajectory.

Positive necessity contrasts indicate that the corresponding trained component contributes causally to the measured organizational behavior under this protocol.

A rescue lift indicates recovery after restoration of the trained components within the same post-intervention trajectory.

## Scientific boundary

C0.6 is a causal organizational test. It does **not** provide a phenomenal-consciousness claim by itself.
