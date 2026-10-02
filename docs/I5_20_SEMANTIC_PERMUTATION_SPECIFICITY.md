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
