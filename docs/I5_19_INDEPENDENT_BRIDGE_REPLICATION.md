# I5.19 — Independent Bridge Replication

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.18 mostró un efecto bridge medio distinto de cero a través de los seis lags, mientras que la interacción global fase × bridge no fue significativa. I5.19 convierte ese resultado en una prueba de replicación independiente.

La adquisición vuelve a ejecutar el protocolo I5.17 con una **semilla nueva (20261019)**. Después se aplica exactamente el análisis global de I5.18.

## Protocolo congelado

- 24 réplicas;
- 24 ciclos de warmup;
- 15 ciclos experimentales;
- lags **−3, −2, −1, +1, +2, +3**;
- siete rotaciones semánticas cíclicas, una por réplica modulo el período;
- 20.000 permutaciones para la etapa I5.18;
- mismos tres endpoints: AUC firmada, AUC absoluta y cambio de acción futura;
- misma corrección max-T y misma prueba global de interacción;
- única modificación intencional: **semilla independiente**.

No se cambia el endpoint, el criterio de contraste ni la corrección de multiplicidad después de observar el resultado de I5.19.

## Límite

I5.19 prueba reproducibilidad computacional del efecto bajo el mismo arnés. No demuestra consciencia, experiencia subjetiva ni una interpretación mecanística por sí mismo.

</details>

<a id="english"></a>

<details>
<summary>EN — open</summary>

## Objective

I5.18 showed a non-zero average bridge effect across the six tested lags, while the global phase × bridge interaction was not significant. I5.19 turns that result into an independent replication test.

The acquisition reruns I5.17 with a **new seed (20261019)**. The exact I5.18 global analysis is then applied.

## Frozen protocol

- 24 replicates;
- 24 warmup cycles;
- 15 experimental cycles;
- lags **−3, −2, −1, +1, +2, +3**;
- seven cyclic semantic rotations, one per replicate modulo the period;
- 20,000 permutations for the I5.18 analysis stage;
- same three endpoints: signed AUC, absolute AUC, and future-action change;
- same max-T correction and same global interaction test;
- only intentional change: **independent seed**.

Endpoints, contrast criteria, and multiplicity correction are not changed after seeing the I5.19 result.

## Boundary

I5.19 tests computational reproducibility under the same harness. It does not establish consciousness, subjective experience, or a mechanistic interpretation on its own.

</details>

## Resultado verificado / Verified result

### I5.19 — Independent bridge replication

24 replicates with independent seed **20261019**, 24 warmup cycles, 15 experimental cycles, six lags, and 20,000 permutations for the I5.18 analysis stage. Endpoints and multiplicity procedure were unchanged.

- Signed bridge ON−OFF AUC: global mean **-1.3981897076**, replicate-level sign-flip p **0.00030**.
- Absolute bridge ON−OFF AUC: global mean **-0.7306513110**, p **0.00190**.
- Future-action change bridge ON−OFF: global mean **-0.1180555556**, p **0.00110**.
- Global phase × bridge interaction remained non-significant: signed AUC **p=0.16174**, absolute AUC **p=0.24414**, future-action change **p=0.43353**.
- The direction of the average bridge effect therefore reproduced across an independent seed without changing endpoints or multiplicity control.

Interpretation: I5.19 provides an independent computational replication of the average bridge ON−OFF effect under the frozen protocol. It does not establish temporal phase specificity, consciousness, subjective experience, or a mechanistic interpretation.

Verification: research-lab **37056574657**, artifact **11247979913**; tests **37056574726** and package check **37056574723**, all successful.

The independent seed reproduced the direction of all three global bridge effects while leaving the global phase × bridge interaction non-significant for all endpoints.