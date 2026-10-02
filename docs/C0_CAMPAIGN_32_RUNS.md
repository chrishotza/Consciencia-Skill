# C0 Campaign — 32 scheduled executions

## Window

Local time: Buenos Aires / ART (UTC−03:00)

Restarted campaign window: **20:30 → 03:30 ART**, 1–2 October 2026.

Frequency: **4 executions per hour**, implemented as four parallel replica jobs in each hourly group wave.

GitHub Actions cron is expressed in UTC. The eight scheduled waves are **23:30 UTC (1 Oct) → 06:30 UTC (2 Oct)**.

The historical 32-run campaign is retained as executed evidence. The restarted campaign uses eight hourly schedule entries with a four-job matrix and validates result files before artifact upload.

## Groups

| Group | Restarted wave (ART) | Criterion / question | Control |
|---|---|---|---|
| G1 | 20:30 — 1 Oct | C3 causal self-reference | information-matched state shuffle |
| G2 | 21:30 — 1 Oct | C5 intrinsic dynamics | information-matched action replay |
| G3 | 22:30 — 1 Oct | C7 recurrent closure | information-matched action-chain shuffle |
| G4 | 23:30 — 1 Oct | C4 trajectory continuity | FULL − NO_PERSISTENCE |
| G5 | 00:30 — 2 Oct | C1 own-state persistence | FULL − NO_PERSISTENCE |
| G6 | 01:30 — 2 Oct | C2 self/environment differentiation | FULL − STATE_BLIND |
| G7 | 02:30 — 2 Oct | C6 reorganization | FULL − STATE_BLIND |
| G8 | 03:30 — 2 Oct | C0 confirmatory battery | strong controls for C3/C5/C7 + matched controls for C1/C2/C4/C6 |

## Replica seeds

Each slot uses a deterministic, disjoint seed base:

\`100000 + group_index × 1000 + replicate × 100\`

Examples:

- G1-R1 = 101100
- G1-R4 = 101400
- G8-R1 = 108100
- G8-R4 = 108400

Training, trajectories, controls, and statistics derive separate seeds from the slot seed base.

## Schedule

Each wave runs four independent replica jobs in parallel.

| UTC | Local ART | Wave |
|---|---|---|
| 23:30 (1 Oct) | 20:30 (1 Oct) | G1-R1..R4 |
| 00:30 (2 Oct) | 21:30 (1 Oct) | G2-R1..R4 |
| 01:30 (2 Oct) | 22:30 (1 Oct) | G3-R1..R4 |
| 02:30 (2 Oct) | 23:30 (1 Oct) | G4-R1..R4 |
| 03:30 (2 Oct) | 00:30 (2 Oct) | G5-R1..R4 |
| 04:30 (2 Oct) | 01:30 (2 Oct) | G6-R1..R4 |
| 05:30 (2 Oct) | 02:30 (2 Oct) | G7-R1..R4 |
| 06:30 (2 Oct) | 03:30 (2 Oct) | G8-R1..R4 |

## Integrity rules

Each execution gets its own artifact and slot metadata.

A technical failure is recorded as a technical failure, not as an experimental null.

No campaign result is written into the scientific ledger automatically.

No composite consciousness score is produced.

C0.3/C0.4/C0.5 controls are treated as stronger specificity controls for C3/C5/C7 respectively.

G8 is a criterion vector, not a global consciousness score.


## Current status

Verified on 2026-10-02 from GitHub Actions: the restarted campaign has **4/32 executions completed**, all four in **G1**. The successful workflow run is **36955261246** (run #33), with four successful replica jobs and four preserved slot artifacts.

G1 tests **C3 causal self-reference** against the **information-matched state-shuffle** control. The four replicate effects are **0.0625, 0.046875, 0.01953125, and 0.08984375**, with p-values **0.38498075096, 0.49912504375, 0.84995750212, and 0.13454327284** respectively. No G1 replicate crosses p < 0.05.

Descriptive G1 means: effect **0.0546875**, own-gap **0.9921875**, matched-gap **0.9375**. These are descriptive partial-campaign statistics only; **no 32-run composite inference is recorded**.

**Pending:** G2–G8 (28 executions). No scientific conclusion is entered for the full campaign until those executions are actually produced and validated.

The original 32-run campaign is retained as historical evidence with a technical artifact-archival failure.

The restarted campaign uses the artifact-safe workflow and the eight four-job waves listed above. Scientific results are **not** copied into the result ledger automatically. Each produced artifact must first be validated for completeness and provenance.

A technical failure is recorded as a technical failure, never as an experimental null.
