# I5.21 — Phase-Local Semantic Permutation

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.20 encontró especificidad semántica para AUC absoluta y cambio de acción futura, pero su permutación invertía globalmente la secuencia temporal después de t0. I5.21 prueba si la especificidad persiste cuando esa ruptura se limita al interior de cada período de siete fases.

Después de t0, la condición localmente permutada contiene exactamente los mismos strings SELF_MODEL que la condición matched. La diferencia es una permutación derangement fija aplicada por separado a cada bloque de siete fases.

Esto conserva:

- t0;
- el multiconjunto semántico global;
- el multiconjunto semántico dentro de cada período;
- la estructura periódica de siete fases.

Y rompe:

- la correspondencia específica entre fase y contenido SELF_MODEL.

## Protocolo congelado

- 24 réplicas;
- 24 warmup;
- 15 ciclos;
- lags −3, −2, −1, +1, +2, +3;
- siete rotaciones semánticas;
- permutación local fija [1,0,3,4,5,6,2];
- 20.000 permutaciones estadísticas;
- misma corrección max-T y prueba global de interacción de I5.18/I5.20.

## Pregunta

El endpoint primario es matched_on − phase_local_permuted_on, equivalente a la diferencia entre sus efectos bridge frente a OFF.

Si el efecto de I5.20 dependía de la correspondencia fase-contenido y no simplemente del orden temporal global, debería permanecer bajo este control más conservador.

## Límite

I5.21 prueba especificidad computacional de la correspondencia semántica dentro de la estructura periódica local. No demuestra consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

<details>
<summary>EN — open</summary>

## Objective

I5.20 found semantic specificity for absolute AUC and future-action change, but its permutation globally reversed the post-t0 temporal sequence. I5.21 tests whether specificity persists when the disruption is restricted within each seven-phase period.

After t0, the locally permuted condition contains exactly the same SELF_MODEL strings as the matched condition. The difference is a fixed derangement applied separately to each seven-phase block.

This preserves:

- t0;
- the global semantic multiset;
- the semantic multiset within each period;
- the seven-phase periodic structure.

And breaks:

- the specific phase-to-SELF_MODEL correspondence.

## Frozen protocol

- 24 replicates;
- 24 warmup cycles;
- 15 cycles;
- lags −3, −2, −1, +1, +2, +3;
- seven semantic rotations;
- fixed local permutation [1,0,3,4,5,6,2];
- 20,000 statistical permutations;
- same max-T correction and global interaction test as I5.18/I5.20.

## Question

The primary endpoint is matched_on − phase_local_permuted_on, equivalent to the difference between their bridge effects against OFF.

If the I5.20 effect depended on phase-content correspondence rather than only global temporal disruption, it should persist under this more conservative control.

## Boundary

I5.21 tests computational specificity of semantic correspondence within the local periodic structure. It does not establish consciousness or subjective experience.

</details>


## Resultado verificado / Verified result

### I5.21 — Control de permutación semántica local por fase

24 réplicas, 24 warmup, 15 ciclos, seis lags, semilla **20261021** y 20.000 permutaciones. Los invariantes se cumplieron al **100%**: acción aplicada en t0, multiconjunto semántico global y multiconjunto semántico dentro de cada período de siete fases.

- AUC firmada: gap global **+0.0215510**, p **0.85726**; interacción global lag×especificidad **p=0.29069**; max-T any-lag **p=0.35483**.
- AUC absoluta: gap global **+0.4473984**, p **0.00010**; interacción global **p=0.00030**; max-T any-lag **p=0.00065**.
- Cambio de acción futura: gap global **+0.0466270**, p **0.00100**; interacción global **p<0.00005**; max-T any-lag **p=0.00100**.
- En AUC absoluta, los contrastes max-T por lag que sobreviven son **−1: p=0.00905** y **+2: p=0.00065**.
- En cambio de acción futura, sobreviven **−1: p=0.00100** y **+2: p=0.00680**.
- La AUC firmada permanece nula bajo el mismo control.

Interpretación: la especificidad semántica observada en I5.20 **persiste cuando la ruptura temporal se restringe a cada ciclo local de siete fases** y, para AUC absoluta y cambio de acción futura, aparece además una modulación estadísticamente detectable según el lag. Esto separa el resultado de una explicación basada únicamente en haber destruido el orden temporal global. El efecto sigue siendo una propiedad computacional del arnés; no demuestra consciencia ni experiencia subjetiva.

Verificación: research-lab **37059465725**, artifact **11249378346**; tests **37059465807** y package **37059465643**, todos exitosos.

### I5.21 — Phase-local semantic permutation control

24 replicates, 24 warmup cycles, 15 cycles, six lags, seed **20261021**, and 20,000 permutations. All invariants were preserved at **100%**: applied t0 action, global semantic multiset, and within-period seven-phase semantic multiset.

- Signed AUC: global gap **+0.0215510**, p **0.85726**; global lag×specificity interaction **p=0.29069**; max-T any-lag **p=0.35483**.
- Absolute AUC: global gap **+0.4473984**, p **0.00010**; global interaction **p=0.00030**; max-T any-lag **p=0.00065**.
- Future-action change: global gap **+0.0466270**, p **0.00100**; global interaction **p<0.00005**; max-T any-lag **p=0.00100**.
- For absolute AUC, max-T-adjusted lag contrasts surviving were **−1: p=0.00905** and **+2: p=0.00065**.
- For future-action change, surviving contrasts were **−1: p=0.00100** and **+2: p=0.00680**.
- Signed AUC remained null under the same control.

Interpretation: the semantic specificity observed in I5.20 **persists when temporal disruption is restricted within each seven-phase local cycle**, and for absolute AUC and future-action change there is also a statistically detectable lag modulation. This separates the result from an explanation based only on destroying global temporal order. The effect remains a computational property of the harness; it does not establish consciousness or subjective experience.

Verification: research-lab **37059465725**, artifact **11249378346**; tests **37059465807** and package check **37059465643**, all successful.

### I5.22 / Next

### I5.22 — Control de desplazamiento cíclico semántico

Preservar la estructura de transiciones semánticas dentro de cada período de siete fases mediante un desplazamiento cíclico de las etiquetas SELF_MODEL, rompiendo solo el anclaje entre contenido y fase. El objetivo es separar la especificidad fase↔contenido de una explicación basada en cambios de adyacencia u orden local.

### I5.22 — Cyclic semantic phase-shift control

Preserve the within-period semantic transition structure by cyclically shifting SELF_MODEL labels, breaking only the content-to-phase anchoring. The goal is to separate phase-content specificity from explanations based on changed local adjacency or order.
