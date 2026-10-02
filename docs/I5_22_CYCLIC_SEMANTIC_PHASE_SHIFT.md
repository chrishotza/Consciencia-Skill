# I5.22 — Cyclic Semantic Phase-Shift Control

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.21 mostró que la especificidad semántica persiste bajo permutación local y que aparece una modulación por lag. I5.22 hace el control más estricto: conserva la misma secuencia temporal de fases y la misma estructura cíclica del contenido, pero desplaza el mapeo contenido→fase una posición después de t0.

La condición shifted conserva:

- t0;
- la secuencia de etiquetas de fase;
- el multiconjunto semántico post-t0;
- la estructura cíclica del contenido.

Y rompe:

- la correspondencia entre fase y contenido SELF_MODEL.

## Protocolo congelado

- 24 réplicas;
- 24 warmup;
- 15 ciclos;
- lags −3, −2, −1, +1, +2, +3;
- siete rotaciones semánticas;
- desplazamiento cíclico fijo +1 después de t0;
- 20.000 permutaciones;
- mismo análisis global, interacción lag×especificidad y corrección max-T.

## Pregunta

El endpoint es matched_on − cyclic_shifted_on, equivalente a la diferencia entre sus efectos bridge frente a OFF.

Este control busca separar el anclaje fase↔contenido de cualquier explicación basada en cambios de adyacencia u orden local.

## Límite

I5.22 prueba especificidad computacional del anclaje semántico a fase. No demuestra consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

<details>
<summary>EN — open</summary>

## Objective

I5.21 showed that semantic specificity survives local permutation and that lag modulation becomes detectable. I5.22 makes the control stricter: it preserves the same temporal phase sequence and cyclic content structure, but shifts the content-to-phase mapping by one position after t0.

The shifted condition preserves:

- t0;
- phase-label sequence;
- post-t0 semantic multiset;
- cyclic content structure.

And breaks:

- phase-to-SELF_MODEL correspondence.

## Frozen protocol

- 24 replicates;
- 24 warmup cycles;
- 15 cycles;
- lags −3, −2, −1, +1, +2, +3;
- seven semantic rotations;
- fixed +1 cyclic shift after t0;
- 20,000 permutations;
- same global analysis, lag×specificity interaction, and max-T correction.

## Question

The endpoint is matched_on − cyclic_shifted_on, equivalent to the difference between their bridge effects against OFF.

This control separates phase-content anchoring from explanations based on altered local adjacency or temporal order.

## Boundary

I5.22 tests computational specificity of semantic phase anchoring. It does not establish consciousness or subjective experience.

</details>
