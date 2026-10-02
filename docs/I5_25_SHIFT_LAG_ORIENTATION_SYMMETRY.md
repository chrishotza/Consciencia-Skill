# I5.25 — Shift × Lag Orientation and Symmetry Control

## Objective

I5.24 established a global non-additive shift×lag interaction for absolute AUC and future-action change on frozen I5.23 data.

I5.25 separates two possibilities:

1. orientation asymmetry: the surface changes when both shift and lag signs are reversed;
2. compensatory alignment: cells on lag = −shift are enriched relative to the other 30 cells.

## Frozen-data design

No new trajectories are collected.

For each endpoint, the analysis uses the frozen replicate × 6-shift × 6-lag I5.23 surface.

Orientation symmetry:
- pair each cell (shift, lag) with (−shift, −lag);
- compute the 18 paired differences;
- max-T control across the 18 orientation pairs;
- global any-pair test by replicate-level sign flips.

Compensatory diagonal:
- average the six cells satisfying lag = −shift;
- compare that average with the mean of the remaining 30 cells within each replicate;
- sign-flip test across replicates.

Bonferroni correction is applied across the six primary endpoint-family tests.

## Boundary

I5.25 characterizes the geometry of the frozen computational surface. It does not establish consciousness, subjective experience, or a unique causal mechanism.


## Resultado verificado / Verified result

## I5.25 — Control de orientación y simetría shift×lag

Análisis sobre el summary congelado de I5.23; no se recogieron nuevas trayectorias. 24 réplicas, seis shifts, seis lags y 20.000 permutaciones.

- **AUC firmada:** asimetría global por inversión simultánea de signos p=**0.30128**; contraste diagonal lag=−shift p=**0.62617**. Bonferroni de seis pruebas: **1.0** y **1.0**.
- **AUC absoluta:** asimetría global p=**0.00005**; diagonal lag=−shift vs resto p=**0.00005**. Bonferroni: **0.00030** en ambos contrastes.
- **Cambio de acción futura:** asimetría global p=**0.00005**; diagonal lag=−shift vs resto p=**0.00005**. Bonferroni: **0.00030** en ambos contrastes.
- El control de orientación empareja las 36 celdas en 18 pares bajo (shift,lag) ↔ (−shift,−lag) y aplica max-T entre esos pares.
- El contraste diagonal compara, dentro de cada réplica, la media de las seis celdas lag=−shift frente a las 30 celdas restantes.
- En AUC absoluta y acción futura, el resultado confirma que la superficie no es simétrica bajo inversión de signos y que la diagonal compensatoria está enriquecida; esto caracteriza la geometría estadística del arnés, no un mecanismo causal único.
- AUC firmada no muestra ninguna de esas dos estructuras globales.

Verificación: research-lab **37065168288**, artifact **11251708654**; package **37065168296** y tests **37065168323** exitosos.

### I5.26 — Control matched-magnitude de acoplamiento de signos

Comparar, para cada |shift|=|lag|, las celdas con shift×lag<0 frente a las celdas con shift×lag>0, eliminando la diferencia de magnitud y aislando el signo de la relación shift-lag.

## I5.25 — Shift×lag orientation and symmetry control

Analysis of the frozen I5.23 summary; no new trajectories were collected. 24 replicates, six shifts, six lags, and 20,000 permutations.

- **Signed AUC:** global simultaneous-sign-reversal asymmetry p=**0.30128**; compensatory diagonal lag=−shift p=**0.62617**. Six-test Bonferroni: **1.0** and **1.0**.
- **Absolute AUC:** global orientation asymmetry p=**0.00005**; lag=−shift diagonal versus remainder p=**0.00005**. Bonferroni: **0.00030** for both.
- **Future-action change:** global orientation asymmetry p=**0.00005**; lag=−shift diagonal versus remainder p=**0.00005**. Bonferroni: **0.00030** for both.
- The orientation control pairs the 36 cells into 18 (shift,lag) ↔ (−shift,−lag) pairs and applies max-T across those pairs.
- The diagonal contrast compares, within each replicate, the mean of the six lag=−shift cells against the remaining 30 cells.
- For absolute AUC and future action, the surface is therefore not symmetric under sign reversal and the compensatory diagonal is enriched; this characterizes the statistical geometry of the harness rather than a unique causal mechanism.
- Signed AUC shows neither global structure.

Verification: research-lab **37065168288**, artifact **11251708654**; package **37065168296** and tests **37065168323** successful.

### I5.26 — Matched-magnitude sign-coupling control

Compare, for each |shift|=|lag|, cells with shift×lag<0 against cells with shift×lag>0, removing magnitude differences and isolating the sign relationship between shift and lag.
