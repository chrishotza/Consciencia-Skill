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
