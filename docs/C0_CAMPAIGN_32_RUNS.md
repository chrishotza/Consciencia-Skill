# C0 Campaign — 32 scheduled executions

## Window

Local time: Buenos Aires / ART (UTC−03:00)

Window: **06:15 → 14:00**, 1 October 2026.

Frequency: **4 executions per hour**, every 15 minutes.

GitHub Actions cron is expressed in UTC, so the scheduled window is **09:00 → 16:45 UTC**.

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

The first 06:00 local slot was missed because the campaign commit landed after its 09:00 UTC schedule. The complete 32-run campaign is therefore aligned to the next quarter-hour, preserving **4 executions per hour** and 32 total slots.

| UTC | Local ART | Slot |
|---|---|---|
| 09:15 | 06:15 | G1-R1 |
| 09:30 | 06:30 | G1-R2 |
| 09:45 | 06:45 | G1-R3 |
| 10:00 | 07:00 | G1-R4 |
| 10:15 | 07:15 | G2-R1 |
| 10:30 | 07:30 | G2-R2 |
| 10:45 | 07:45 | G2-R3 |
| 11:00 | 08:00 | G2-R4 |
| 11:15 | 08:15 | G3-R1 |
| 11:30 | 08:30 | G3-R2 |
| 11:45 | 08:45 | G3-R3 |
| 12:00 | 09:00 | G3-R4 |
| 12:15 | 09:15 | G4-R1 |
| 12:30 | 09:30 | G4-R2 |
| 12:45 | 09:45 | G4-R3 |
| 13:00 | 10:00 | G4-R4 |
| 13:15 | 10:15 | G5-R1 |
| 13:30 | 10:30 | G5-R2 |
| 13:45 | 10:45 | G5-R3 |
| 14:00 | 11:00 | G5-R4 |
| 14:15 | 11:15 | G6-R1 |
| 14:30 | 11:30 | G6-R2 |
| 14:45 | 11:45 | G6-R3 |
| 15:00 | 12:00 | G6-R4 |
| 15:15 | 12:15 | G7-R1 |
| 15:30 | 12:30 | G7-R2 |
| 15:45 | 12:45 | G7-R3 |
| 16:00 | 13:00 | G7-R4 |
| 16:15 | 13:15 | G8-R1 |
| 16:30 | 13:30 | G8-R2 |
| 16:45 | 13:45 | G8-R3 |
| 17:00 | 14:00 | G8-R4 |

## Integrity rules

Each execution gets its own artifact and slot metadata.

A technical failure is recorded as a technical failure, not as an experimental null.

No campaign result is written into the scientific ledger automatically.

No composite consciousness score is produced.

C0.3/C0.4/C0.5 controls are treated as stronger specificity controls for C3/C5/C7 respectively.

G8 is a criterion vector, not a global consciousness score.
