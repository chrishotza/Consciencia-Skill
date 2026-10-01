# C0 Campaign — 32 scheduled executions

## Window

Local time: Buenos Aires / ART (UTC−03:00)

Restarted campaign window: **20:30 → 03:30 ART**, 1–2 October 2026.

Frequency: **4 executions per hour**, implemented as four parallel replica jobs in each hourly group wave.

GitHub Actions cron is expressed in UTC. The eight scheduled waves are **23:30 UTC (1 Oct) → 06:30 UTC (2 Oct)**.

The historical 32-run campaign is retained as executed evidence. The restarted campaign uses eight hourly schedule entries with a four-job matrix and validates result files before artifact upload.

## Groups

| Group | Local time | Criterion / question | Control |
|---|---|---|---|
| G1 | 06:15–07:00 | C3 causal self-reference | information-matched state shuffle |
| G2 | 07:15–08:00 | C5 intrinsic dynamics | information-matched action replay |
| G3 | 08:15–09:00 | C7 recurrent closure | information-matched action-chain shuffle |
| G4 | 09:15–10:00 | C4 trajectory continuity | FULL − NO_PERSISTENCE |
| G5 | 10:15–11:00 | C1 own-state persistence | FULL − NO_PERSISTENCE |
| G6 | 11:15–12:00 | C2 self/environment differentiation | FULL − STATE_BLIND |
| G7 | 12:15–13:00 | C6 reorganization | FULL − STATE_BLIND |
| G8 | 13:15–14:00 | C0 confirmatory battery | strong controls for C3/C5/C7 + matched controls for C1/C2/C4/C6 |

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
