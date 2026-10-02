# I5.23 — Cyclic Shift Sweep

## Objetivo

I5.22 probó un único desplazamiento cíclico (+1) y obtuvo un resultado nulo bajo un control con invariantes preservados al 100%. I5.23 elimina la arbitrariedad del desplazamiento elegido y barre los seis shifts no nulos de un ciclo de siete fases: −3, −2, −1, +1, +2, +3.

La condición desplazada conserva exactamente t0, la secuencia de etiquetas de fase y el multiconjunto de contenido semántico post-t0. Solo cambia el anclaje entre fase y contenido.

## Protocolo

24 réplicas; 24 warmup; 15 ciclos; seis lags; seis shifts; siete rotaciones semánticas; 20.000 permutaciones.

Matched y OFF se ejecutan una sola vez por réplica×lag. Las seis condiciones shifted reutilizan esas referencias.

Se reportan efectos por shift, interacción lag×especificidad por shift, max-T entre lags, max-T entre shifts y un max-T global entre los 36 pares shift×lag.

## Endpoint primario

Para cada shift y lag: matched_on − shifted_on sobre AUC firmada, AUC absoluta y cambio de acción futura.

## Invariantes

La ejecución aborta si una celda viola t0, acción t0, multiconjunto exacto de contenido semántico post-t0 o secuencia de etiquetas de fase.

## Límite

I5.23 evalúa robustez computacional de la especificidad frente a toda la familia de shifts cíclicos. No demuestra consciencia, experiencia subjetiva ni una interpretación mecanística única.

## English

I5.23 replaces the single +1 shift with the complete family of six non-zero seven-phase cyclic shifts. It preserves t0, the phase-label sequence, and the post-t0 semantic content multiset. Multiplicity is controlled at shift, lag, and full 36-cell sweep levels. It tests computational specificity only.


## Resultado verificado / Verified result

## I5.23 — Barrido de desplazamientos cíclicos semánticos

24 réplicas, 24 warmup, 15 ciclos, seis lags, seis shifts no nulos (−3, −2, −1, +1, +2, +3), siete rotaciones semánticas y 20.000 permutaciones. Los cuatro invariantes estructurales fueron **100% en las 864 celdas de control**.

Resultados agregados por shift con max-T entre los seis shifts:

- **AUC firmada:** ningún shift fue significativo tras max-T; perfil global p=**0.14534**.
- **AUC absoluta:** shifts **−3, −2, −1, +2 y +3** fueron significativos tras max-T (p≤0.00010); shift **+1** fue nulo (p=**0.91345**). El contraste any-shift global fue p=**0.00005**.
- **Cambio de acción futura:** shifts **−3, −2, −1, +2 y +3** fueron significativos tras max-T (p≤0.00025); shift **+1** fue nulo (p=**0.90245**). Any-shift global p=**0.00005**.
- Las interacciones globales lag×especificidad fueron significativas para AUC absoluta y acción futura en los shifts −3, −2, −1, +2 y +3 (p<0.00005 en cada caso), pero no en +1 ni en AUC firmada.
- En el max-T global de los 36 pares shift×lag, los contrastes más extremos para AUC absoluta y acción futura se concentraron en combinaciones donde el lag contrarresta el shift (por ejemplo −3/+3, −2/+2, −1/+1, +2/−2, +3/−3). Esto se reporta como patrón descriptivo de la superficie 2D, no como explicación causal.

Interpretación: **I5.22 (+1) fue un nulo específico, no un nulo de toda la familia de desplazamientos**. Bajo este arnés, la especificidad semántica aparece de forma robusta para cinco de los seis shifts en AUC absoluta y cambio de acción futura, mientras la AUC firmada permanece sin evidencia global. El siguiente análisis debe formalizar la interacción bidimensional shift×lag antes de atribuir significado mecanístico al patrón observado.

Verificación: research-lab **37062538761**, artifact **11251207688**; tests **37062538733** y package **37062538712**, todos exitosos.

### I5.24 — Interacción global shift×lag

Construir una prueba global bidimensional sobre la matriz réplica × shift × lag, preservando los valores internos de cada réplica y permutando independientemente las etiquetas de shift y lag para separar efectos principales de la interacción específica de su emparejamiento.

## I5.23 — Cyclic semantic shift sweep

24 replicates, 24 warmup cycles, 15 cycles, six non-zero shifts (−3, −2, −1, +1, +2, +3), seven semantic rotations, and 20,000 permutations. All four structural invariants were **100% across 864 control cells**.

Shift-level results with max-T across the six shifts:

- **Signed AUC:** no shift was significant after max-T; global any-shift p=**0.14534**.
- **Absolute AUC:** shifts **−3, −2, −1, +2, +3** remained significant after max-T (p≤0.00010); shift **+1** was null (p=**0.91345**). Global any-shift p=**0.00005**.
- **Future-action change:** shifts **−3, −2, −1, +2, +3** remained significant after max-T (p≤0.00025); shift **+1** was null (p=**0.90245**). Global any-shift p=**0.00005**.
- Global lag×specificity interaction was significant for absolute AUC and future-action change for shifts −3, −2, −1, +2, +3 (p<0.00005 in each case), but not for +1 or signed AUC.
- In the global max-T sweep over all 36 shift×lag cells, the most extreme contrasts for absolute AUC and future-action change clustered where lag counteracted shift (e.g. −3/+3, −2/+2, −1/+1, +2/−2, +3/−3). This is reported as a descriptive 2D-surface pattern, not a causal explanation.

Interpretation: **I5.22 (+1) was a shift-specific null, not a family-wide null**. Under this harness, semantic specificity is robust for five of six shifts on absolute AUC and future-action change, while signed AUC remains globally unsupported. The next analysis should formalize the two-dimensional shift×lag interaction before assigning mechanistic meaning to the observed pattern.

Verification: research-lab **37062538761**, artifact **11251207688**; tests **37062538733** and package check **37062538712**, all successful.

### I5.24 — Global shift×lag interaction

Run a global two-dimensional interaction test on the replicate × shift × lag matrix, preserving each replicate's 6×6 values and independently permuting shift and lag labels to distinguish main effects from interaction-specific pairing.
