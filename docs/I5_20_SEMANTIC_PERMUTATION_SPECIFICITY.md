# I5.20 — Semantic Permutation Specificity Control

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.19 reprodujo el efecto medio del bridge con una semilla independiente. I5.20 prueba ahora si ese efecto depende de la correspondencia temporal específica del contenido semántico.

El control no cambia qué información semántica aparece. Después de t0, la condición permuted_on contiene exactamente los mismos strings SELF_MODEL que matched_on, pero en un orden temporal diferente.

Así se separan tres condiciones por lag:

- matched_on: bridge activo + correspondencia semántica original;
- permuted_on: bridge activo + mismo multiconjunto semántico, pero correspondencia temporal rota;
- off: bridge desactivado.

El endpoint primario es la diferencia matched_on − permuted_on, que equivale a la diferencia entre los respectivos efectos bridge frente a off.

## Controles invariantes

- 24 réplicas;
- 24 ciclos de warmup;
- 15 ciclos;
- lags −3, −2, −1, +1, +2, +3;
- siete rotaciones semánticas entre réplicas;
- misma dinámica, semillas de réplica y configuración del organismo entre condiciones;
- mismo multiconjunto exacto de SELF_MODEL después de t0;
- misma acción aplicada en t0;
- 20.000 permutaciones estadísticas;
- misma corrección max-T y prueba global de interacción de I5.18.

La única intervención adicional es la permutación temporal del contenido semántico después de t0.

## Análisis estadístico

Para cada endpoint se calcula una matriz réplica × lag del gap de especificidad:

(matched_on − off) − (permuted_on − off).

Se reportan:

1. efecto global de especificidad agregado a través de los seis lags;
2. interacción global lag × especificidad;
3. p-valores por lag;
4. p-valores corregidos max-T a través de los seis lags.

## Límite

I5.20 evalúa especificidad computacional de la correspondencia semántica dentro del puente. No demuestra consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

<details>
<summary>EN — open</summary>

## Objective

I5.19 independently replicated the average bridge effect. I5.20 now tests whether that effect depends on the specific temporal correspondence of semantic content.

The control does not change which semantic information appears. After t0, permuted_on contains exactly the same SELF_MODEL strings as matched_on, but in a different temporal order.

This creates three conditions per lag:

- matched_on: bridge active + original semantic correspondence;
- permuted_on: bridge active + same semantic multiset, but disrupted temporal correspondence;
- off: bridge disabled.

The primary endpoint is matched_on − permuted_on, equal to the difference between the respective bridge effects against off.

## Control invariants

- 24 replicates;
- 24 warmup cycles;
- 15 cycles;
- lags −3, −2, −1, +1, +2, +3;
- seven semantic rotations across replicates;
- same dynamics, replicate seeds, and organism configuration across conditions;
- exact same SELF_MODEL multiset after t0;
- same t0 applied action;
- 20,000 statistical permutations;
- same max-T correction and global interaction test as I5.18.

The only added intervention is temporal permutation of semantic content after t0.

## Statistical analysis

For each endpoint, compute a replicate × lag semantic-specificity gap:

(matched_on − off) − (permuted_on − off).

Report:

1. global specificity effect across all six lags;
2. global lag × specificity interaction;
3. per-lag p-values;
4. max-T adjusted p-values across the six lags.

## Boundary

I5.20 tests computational specificity of semantic correspondence within the bridge. It does not establish consciousness or subjective experience.

</details>


## Resultado verificado / Verified result

### I5.20 — Control de especificidad por permutación semántica

24 réplicas, 24 ciclos de warmup, 15 ciclos, seis lags y 20.000 permutaciones estadísticas. Semilla **20261020**. El control preservó al **100%** la acción aplicada en t0 y al **100%** el multiconjunto exacto de SELF_MODEL después de t0.

El endpoint primario fue el gap de especificidad matched−permuted, equivalente a la diferencia entre los efectos bridge frente a OFF.

- AUC firmada: gap global **-0.1036703**, p de sign-flip **0.24169**; interacción global lag×especificidad **p=0.43558**.
- AUC absoluta: gap global **+0.7145935**, p **0.00005**; interacción global **p=0.36903**.
- Cambio de acción futura: gap global **+0.0729167**, p **0.00005**; interacción global **p=0.24484**.
- Con max-T entre los seis lags, el contraste global any-lag fue significativo para AUC absoluta (**p=0.01060**) y cambio de acción futura (**p=0.01110**), mientras que AUC firmada permaneció nula (**p=0.65022**).
- En ambos endpoints positivos, el contraste max-T corregido más extremo correspondió a lag **-3** (AUC absoluta p=0.01060; acción p=0.01110), pero la interacción global por lag no fue significativa, por lo que no se interpreta como una localización causal específica en fase.

Interpretación: bajo este arnés, el efecto medio del bridge no depende solo de que el bridge esté encendido. La correspondencia temporal del contenido SELF_MODEL aporta una diferencia reproducible en la magnitud absoluta del estado y en el cambio de acción futura. El endpoint de AUC firmada no mostró esa separación. Esto es evidencia de **especificidad computacional de la correspondencia semántica**, no evidencia de consciencia o experiencia subjetiva.

Verificación: research-lab **37058932661**, artifact **11249457646**; tests **37058932554** y package **37058932500**, todos exitosos.

### I5.20 — Semantic permutation specificity control

24 replicates, 24 warmup cycles, 15 cycles, six lags, and 20,000 statistical permutations. Seed **20261020**. The control preserved the applied t0 action at **100%** and the exact post-t0 SELF_MODEL multiset at **100%**.

The primary endpoint was the matched−permuted specificity gap, equivalent to the difference between the respective bridge effects against OFF.

- Signed AUC: global gap **-0.1036703**, sign-flip p **0.24169**; global lag×specificity interaction **p=0.43558**.
- Absolute AUC: global gap **+0.7145935**, p **0.00005**; global interaction **p=0.36903**.
- Future-action change: global gap **+0.0729167**, p **0.00005**; global interaction **p=0.24484**.
- With max-T across the six lags, the global any-lag contrast was significant for absolute AUC (**p=0.01060**) and future-action change (**p=0.01110**), while signed AUC remained null (**p=0.65022**).
- For both positive endpoints, the most extreme max-T corrected lag was **-3** (absolute AUC p=0.01060; action p=0.01110), but the global lag interaction was non-significant, so this is not interpreted as causal phase localization.

Interpretation: under this harness, the average bridge effect is not explained solely by bridge activation. Temporal correspondence of SELF_MODEL content contributes a reproducible difference in absolute state magnitude and future action change. Signed AUC did not separate under the same control. This is evidence for **computational specificity of semantic correspondence**, not evidence of consciousness or subjective experience.

Verification: research-lab **37058932661**, artifact **11249457646**; tests **37058932554** and package check **37058932500**, all successful.

### I5.21 / Next

### I5.21 — Permutación semántica local por período

Mantener la misma información semántica y el mismo t0, pero sustituir la permutación global de I5.20 por una permutación derangement dentro de cada período de siete fases, preservando la estructura cíclica local. El objetivo es separar dependencia de correspondencia fase-contenido de un efecto más general de ruptura del orden temporal.

### I5.21 — Phase-local semantic permutation

Keep the same semantic information and t0, but replace I5.20's global reversal with a derangement applied within each seven-phase period, preserving local cyclic structure. The goal is to separate phase-content correspondence from a more general effect of disrupting temporal order.
