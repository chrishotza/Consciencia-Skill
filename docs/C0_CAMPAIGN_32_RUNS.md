# C0 Campaign — 32 scheduled executions

## Window

Local time: Buenos Aires / ART (UTC−03:00)

Window: **19:15 → 03:00 ART**, 1–2 October 2026.

Frequency: **4 executions per hour**, every 15 minutes.

GitHub Actions cron is expressed in UTC. The restarted campaign uses **22:15 UTC (1 Oct) → 06:00 UTC (2 Oct)**.

The first 32-run campaign completed its experimental step but failed only during artifact upload because the workflow passed literal shell variables to `actions/upload-artifact`. Those historical runs are retained as execution evidence in GitHub logs. This restarted campaign validates the result files before upload and uploads the complete `results/tcf_campaign` directory.


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

| UTC | Local ART | Slot |
|---|---|---|
| 22:15 UTC | 19:15 ART (1 Oct) | G1-R1 |
| 22:30 UTC | 19:30 ART (1 Oct) | G1-R2 |
| 22:45 UTC | 19:45 ART (1 Oct) | G1-R3 |
| 23:00 UTC | 20:00 ART (1 Oct) | G1-R4 |
| 23:15 UTC | 20:15 ART (1 Oct) | G2-R1 |
| 23:30 UTC | 20:30 ART (1 Oct) | G2-R2 |
| 23:45 UTC | 20:45 ART (1 Oct) | G2-R3 |
| 00:00 UTC | 21:00 ART (2 Oct) | G2-R4 |
| 00:15 UTC | 21:15 ART (2 Oct) | G3-R1 |
| 00:30 UTC | 21:30 ART (2 Oct) | G3-R2 |
| 00:45 UTC | 21:45 ART (2 Oct) | G3-R3 |
| 01:00 UTC | 22:00 ART (2 Oct) | G3-R4 |
| 01:15 UTC | 22:15 ART (2 Oct) | G4-R1 |
| 01:30 UTC | 22:30 ART (2 Oct) | G4-R2 |
| 01:45 UTC | 22:45 ART (2 Oct) | G4-R3 |
| 02:00 UTC | 23:00 ART (2 Oct) | G4-R4 |
| 02:15 UTC | 23:15 ART (2 Oct) | G5-R1 |
| 02:30 UTC | 23:30 ART (2 Oct) | G5-R2 |
| 02:45 UTC | 23:45 ART (2 Oct) | G5-R3 |
| 03:00 UTC | 00:00 ART (2 Oct) | G5-R4 |
| 03:15 UTC | 00:15 ART (2 Oct) | G6-R1 |
| 03:30 UTC | 00:30 ART (2 Oct) | G6-R2 |
| 03:45 UTC | 00:45 ART (2 Oct) | G6-R3 |
| 04:00 UTC | 01:00 ART (2 Oct) | G6-R4 |
| 04:15 UTC | 01:15 ART (2 Oct) | G7-R1 |
| 04:30 UTC | 01:30 ART (2 Oct) | G7-R2 |
| 04:45 UTC | 01:45 ART (2 Oct) | G7-R3 |
| 05:00 UTC | 02:00 ART (2 Oct) | G7-R4 |
| 05:15 UTC | 02:15 ART (2 Oct) | G8-R1 |
| 05:30 UTC | 02:30 ART (2 Oct) | G8-R2 |
| 05:45 UTC | 02:45 ART (2 Oct) | G8-R3 |
| 06:00 UTC | 03:00 ART (2 Oct) | G8-R4 |

## Integrity rules

Each execution gets its own artifact and slot metadata.

A technical failure is recorded as a technical failure, not as an experimental null.

No campaign result is written into the scientific ledger automatically.

No composite consciousness score is produced.

C0.3/C0.4/C0.5 controls are treated as stronger specificity controls for C3/C5/C7 respectively.

G8 is a criterion vector, not a global consciousness score.
