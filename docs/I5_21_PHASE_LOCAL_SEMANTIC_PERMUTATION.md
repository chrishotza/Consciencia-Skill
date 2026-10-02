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
