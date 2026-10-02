<a id="espanol"></a>

# V36 — Leave-One-History-Pair-Out Cluster Evidence

## Estado

**OFICIAL — GitHub Actions run #2, corregido.**

V36 replica el diseño de V34 con historia-seeds 110–119 y realiza inferencia a nivel de bloque history-seed. Una auditoría detectó y corrigió un error de indexado en el bootstrap de la primera ejecución.

## Resultado primario

En 40 bloques históricos:

- signed-affinity, contraste 30°−150°: **0.353882**
- null estratificado, media: **0.000256**
- null 95%: **0.096306**
- permutation p: **0.00005**
- bootstrap 95%: **[0.336407, 0.368998]**

Los cuatro análisis leave-one-history-pair-out permanecen positivos:

- excluir pair 0: **0.316763**, IC [0.293816, 0.336578]
- excluir pair 1: **0.372603**, IC [0.349371, 0.392401]
- excluir pair 2: **0.381222**, IC [0.371967, 0.390492]
- excluir pair 3: **0.344938**, IC [0.322435, 0.364593]

Las métricas alternativas también permanecen positivas en el análisis completo:

- distance-margin: **1.807406**, IC [1.708954, 1.897006]
- cosine-delta: **1.005377**, IC [0.943086, 1.065470]

## Lectura

La señal observada en V34 no depende de un único tipo de historia dentro de este protocolo y sobrevive el análisis cluster-level corregido.

Esto demuestra robustez interna del fenómeno computacional bajo estas condiciones; no demuestra conciencia ni experiencia subjetiva.

## Reproducibilidad

Run: **36791582866**

Artifact: **11131824269**

Código corregido: **2b7e7c35467c5d044e88903c66a7b42844f72576**

La ejecución #1 queda conservada en el registro de auditoría y no se usa para los intervalos finales.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V36 — Leave-One-History-Pair-Out Cluster Evidence

## Status

**OFFICIAL — GitHub Actions run #2, corrected.**

V36 replicates V34 with history-seeds 110–119 and performs history-seed block-level inference. An audit detected and corrected an indexing error in bootstrap in the first execution.

## Primary result

Across 40 history blocks:

- signed-affinity, 30°−150° contrast: **0.353882**
- stratified null mean: **0.000256**
- 95th null: **0.096306**
- permutation p: **0.00005**
- bootstrap 95% CI: **[0.336407, 0.368998]**

All four leave-one-history-pair-out analyses remain positive:

- exclude pair 0: **0.316763**, CI [0.293816, 0.336578]
- exclude pair 1: **0.372603**, CI [0.349371, 0.392401]
- exclude pair 2: **0.381222**, CI [0.371967, 0.390492]
- exclude pair 3: **0.344938**, CI [0.322435, 0.364593]

Alternative metrics also remain positive in the complete analysis:

- distance-margin: **1.807406**, CI [1.708954, 1.897006]
- cosine-delta: **1.005377**, CI [0.943086, 1.065470]

## Interpretation

The signal observed in V34 does not depend on one history type within this protocol and survives the corrected cluster-level analysis.

This demonstrates internal robustness of the computational phenomenon under these conditions; it does not demonstrate consciousness or subjective experience.

## Reproducibility

Run: **36791582866**

Artifact: **11131824269**

Corrected code: **2b7e7c35467c5d044e88903c66a7b42844f72576**

Execution #1 remains preserved in the audit record and is not used for final intervals.

</details>