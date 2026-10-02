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


## Resultado verificado / Verified result

## I5.22 — Control de desplazamiento cíclico semántico

24 réplicas, 24 warmup, 15 ciclos, seis lags, seed **20261022** y 20.000 permutaciones. Los cuatro invariantes del control fueron del **100%**: modelo de sí en t0, acción aplicada en t0, multiconjunto de contenido semántico post-t0 y secuencia de etiquetas de fase.

- AUC firmada: gap global **+0.0280132**, p de sign-flip **0.74476**; interacción lag×especificidad **p=0.20354**; max-T any-lag **p=0.22344**.
- AUC absoluta: gap global **+0.0298333**, p **0.71256**; interacción global **p=0.57192**; max-T any-lag **p=0.76186**.
- Cambio de acción futura: gap global **+0.0064484**, p **0.52927**; interacción global **p=0.51672**; max-T any-lag **p=0.78481**.

Interpretación: bajo el control más estricto, que conserva la secuencia temporal de fases, el multiconjunto semántico y la estructura cíclica de transiciones mientras desplaza el anclaje fase↔contenido, **no se detectó especificidad semántica en ninguno de los tres endpoints**. Esto limita la interpretación de I5.21: su efecto positivo no puede atribuirse únicamente al desacoplamiento fase↔contenido; es compatible con una dependencia adicional de la transformación temporal/estructural introducida por esa permutación.

La corrida inicial de I5.22 se descartó como evidencia porque su indicador de integridad comparaba cadenas completas fase — contenido; la repetición corregida separó explícitamente fase y contenido y obtuvo 100% en los cuatro invariantes. Solo la repetición corregida se considera resultado válido.

Verificación válida: research-lab **37061263630**, artifact **11251161457**; tests **37061263638** y package **37061263624**, todos exitosos.

### I5.23 — Barrido de desplazamientos cíclicos

Repetir el mismo control con los seis desplazamientos no nulos del ciclo de siete fases (−3, −2, −1, +1, +2, +3) para distinguir un nulo específico de +1 de una ausencia robusta de especificidad bajo toda la familia de desplazamientos cíclicos.

## I5.22 — Cyclic semantic phase-shift control

24 replicates, 24 warmup cycles, 15 cycles, six lags, seed **20261022**, and 20,000 permutations. All four control invariants were **100%**: t0 self-model, t0 applied action, post-t0 semantic content multiset, and phase-label sequence.

- Signed AUC: global gap **+0.0280132**, sign-flip p **0.74476**; lag×specificity interaction **p=0.20354**; max-T any-lag **p=0.22344**.
- Absolute AUC: global gap **+0.0298333**, p **0.71256**; global interaction **p=0.57192**; max-T any-lag **p=0.76186**.
- Future-action change: global gap **+0.0064484**, p **0.52927**; global interaction **p=0.51672**; max-T any-lag **p=0.78481**.

Interpretation: under the stricter control, which preserves phase sequence, semantic multiset, and cyclic transition structure while shifting phase↔content anchoring, **no semantic specificity was detected on any of the three endpoints**. This limits the interpretation of I5.21: its positive effect cannot be attributed solely to phase↔content decoupling and is compatible with an additional dependence on the temporal/structural transformation introduced by that permutation.

The initial I5.22 run was discarded as evidence because its integrity metric compared complete phase — content strings; the corrected repeat explicitly separated phase and content and achieved 100% on all four invariants. Only the corrected repeat is treated as valid.

Valid verification: research-lab **37061263630**, artifact **11251161457**; tests **37061263638** and package check **37061263624**, all successful.

### I5.23 — Cyclic shift sweep

Repeat the same control for all six non-zero seven-phase shifts (−3, −2, −1, +1, +2, +3) to distinguish a +1-specific null from a robust absence of specificity across the cyclic-shift family.
