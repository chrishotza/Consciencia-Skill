# I5.26 — Matched-Magnitude Sign-Coupling Control

## Objective

I5.25 established a strong compensatory lag = −shift diagonal for absolute AUC and future-action change.

I5.26 removes the remaining magnitude confound by comparing only cells with equal absolute shift and lag:

- opposite sign: lag = −shift;
- same sign: lag = shift.

The comparison is performed separately for |shift| = 1, 2, 3 and then with max-T across the three magnitudes.

## Frozen-data design

No new trajectories are collected.

Input is the frozen I5.23 replicate × 6-shift × 6-lag surface.

For each magnitude k:

- opposite-sign cells: (−k,+k) and (+k,−k);
- same-sign cells: (−k,−k) and (+k,+k);
- the replicate-level contrast is opposite-sign mean minus same-sign mean.

## Boundaries

A positive result isolates a sign-coupling effect after matching the absolute temporal magnitude. A null result would weaken the interpretation of the compensatory diagonal.

This remains a computational/statistical property of the harness. It does not establish consciousness, subjective experience, or a unique mechanism.


## Resultado verificado / Verified result

## I5.26 — Control matched-magnitude de acoplamiento de signos

Análisis sobre el summary congelado de I5.23; no se recogieron nuevas trayectorias. 24 réplicas, tres magnitudes |shift|=|lag| (1, 2, 3) y 20.000 permutaciones.

Para cada magnitud, se comparó la media de las celdas de signo opuesto (lag=−shift) con la media de las celdas de mismo signo (lag=shift), eliminando la diferencia de magnitud.

- **AUC firmada:** contrastes por magnitud −0.17637, −0.26843 y −0.26521; max-T entre magnitudes p **0.72751**; contraste global p **0.43118**. Nulo.
- **AUC absoluta:** contrastes +2.26314, +4.50633 y +4.35331; max-T por magnitud p **0.01780**, **<0.00005**, **<0.00005**; any-magnitude p **<0.00005**; contraste global p **<0.00005**.
- **Cambio de acción futura:** contrastes +0.22619, +0.46577 y +0.44792; max-T por magnitud p **0.01845**, **<0.00005**, **<0.00005**; any-magnitude p **<0.00005**; contraste global p **<0.00005**.
- El resultado confirma que el patrón compensatorio no depende únicamente de que los lags/shift sean de mayor magnitud: con magnitud emparejada, el signo opuesto conserva una ventaja robusta en AUC absoluta y acción futura.

Interpretación: I5.25 mostró una diagonal lag=−shift enriquecida; I5.26 demuestra que esa ventaja persiste después de igualar |shift| y |lag|. La AUC firmada continúa sin evidencia de este acoplamiento. Esto sigue siendo una propiedad estadística/computacional del arnés y no demuestra consciencia ni experiencia subjetiva.

Verificación: research-lab **37066787603**, artifact **11253435918**; tests **37066787571** y package **37066787624**; todos los checks del código pasaron.

### I6.1 — Cierre causal del self-model

Pasar de controles descriptivos a una intervención arquitectónica: comparar un organismo cuyo self-model participa causalmente en la selección y actualización de trayectoria frente a un control lesionado que recibe la misma información pero no puede usar el self-model para seleccionar su propia trayectoria.

## I5.26 — Matched-magnitude sign-coupling control

Frozen-data analysis of I5.23; no new trajectories were collected. 24 replicates, three matched magnitudes |shift|=|lag| (1, 2, 3), and 20,000 permutations.

For each magnitude, the mean of opposite-sign cells (lag=−shift) was compared with the mean of same-sign cells (lag=shift), eliminating magnitude differences.

- **Signed AUC:** contrasts −0.17637, −0.26843, and −0.26521; max-T across magnitudes p **0.72751**; global contrast p **0.43118**. Null.
- **Absolute AUC:** contrasts +2.26314, +4.50633, +4.35331; max-T per magnitude p **0.01780**, **<0.00005**, **<0.00005**; any-magnitude p **<0.00005**; global contrast p **<0.00005**.
- **Future-action change:** contrasts +0.22619, +0.46577, +0.44792; max-T per magnitude p **0.01845**, **<0.00005**, **<0.00005**; any-magnitude p **<0.00005**; global contrast p **<0.00005**.
- The result shows that the compensatory pattern is not explained only by larger temporal magnitudes: after matching |shift| and |lag|, opposite-sign coupling remains robust for absolute AUC and future-action change.

Interpretation: I5.25 showed enrichment on lag=−shift; I5.26 shows the advantage survives matched-magnitude control. Signed AUC remains unsupported. This remains a statistical/computational property of the harness and does not establish consciousness or subjective experience.

Verification: research-lab **37066787603**, artifact **11253435918**; tests **37066787571** and package **37066787624**; all code checks passed.

### I6.1 — Causal closure of the self-model

Move from descriptive controls to an architectural intervention: compare an organism whose self-model participates causally in trajectory selection and update against a lesioned control that receives the same information but cannot use the self-model to select its own trajectory.
