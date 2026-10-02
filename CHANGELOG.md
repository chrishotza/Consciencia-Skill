## 2026-10-02 — I5.26 verificado / I5.26 verified

- Frozen I5.23 analysis; no new trajectories.
- Workflow **37066787603**, artifact **11253435918**; tests **37066787571** and package **37066787624** passed.
- Signed AUC matched-magnitude coupling null: p=0.43118.
- Absolute AUC and future-action matched-magnitude coupling global p<0.00005 each.
- Next: I6.1 causal closure of the self-model.

## 2026-10-02 — I5.25 verificado / I5.25 verified

- Frozen I5.23 analysis; no new trajectories.
- Workflow **37065168288**, artifact **11251708654**; package **37065168296** and tests **37065168323** passed.
- Signed AUC orientation p=0.30128 and diagonal p=0.62617.
- Absolute AUC and future-action orientation/diagonal p=0.00005; Bonferroni 0.00030.
- Next: I5.26 matched-magnitude sign-coupling control.

## 2026-10-02 — I5.24 verificado / I5.24 verified

- Frozen I5.23 analysis; no new trajectories.
- Workflow 37063264401, artifact 11252345042; tests 37063264520 and package check 37063264454 passed.
- Global shift×lag interaction: signed AUC p=0.89461; absolute AUC p=0.00005; future-action change p=0.00005.
- Bonferroni-adjusted p across three endpoints: 1.0, 0.00015, 0.00015 respectively.
- Next: I5.25 shift×lag orientation and symmetry control.

## 2026-10-02 — I5.23 verificado / I5.23 verified

- 24 replicates; seed **20261023**; 24 warmup; 15 cycles; six shifts; six lags; 20,000 permutations.
- Workflow **37062538761**, artifact **11251207688**; tests **37062538733** and package check **37062538712** passed.
- All four structural invariants were preserved across **864 control cells**.
- Signed AUC: no shift survived max-T.
- Absolute AUC and future-action change: five of six shifts survived max-T; +1 was the only null shift.
- The 36-cell shift×lag sweep was significant for absolute AUC and future-action change.
- Next: I5.24 global shift×lag interaction.

