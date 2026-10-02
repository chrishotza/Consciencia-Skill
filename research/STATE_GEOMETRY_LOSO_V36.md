<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V36 — Validación por exclusión de un history-pair

V36 es una réplica nueva usando history-seeds 110–119.

El diseño completo coincide con V34/V35: seis puntos ciegos, cuatro estratos history-pair, nueve contextos memory/pressure, radio 1.1, ángulos 30° y 150°, input futuro exactamente cero y seeds disjuntas de referencia/prueba.

El análisis primario se realiza a nivel de bloque history-seed. Las celdas repetidas de parámetro/contexto se promedian primero dentro de cada bloque.

Además del análisis completo de 40 bloques, V36 realiza cuatro análisis leave-one-history-pair-out. Cada uno pregunta si el contraste agregado 30°−150° permanece positivo después de eliminar uno de los cuatro estratos históricos.

Para cada métrica, la inferencia utiliza un null sign-flip estratificado sobre los estratos history-pair restantes y un bootstrap sobre bloques history-seed.

Readouts:

- signed_affinity
- distance_margin
- cosine_delta

El experimento prueba robustez frente a dominancia de un estrato histórico. No establece consciencia, experiencia subjetiva, sentiencia ni propiedades fuera del sistema computacional implementado.

</details>

<a id="english"></a>

# V36 — Leave-One-History-Pair-Out Cluster Validation

V36 is a fresh replication using history seeds 110–119.

The full design matches V34/V35: six blind parameter points, four history-pair strata, nine memory/pressure contexts, radius 1.1, angles 30° and 150°, exactly zero future input, and disjoint reference/test continuation seeds.

The primary analysis is performed at the history-seed block level. Repeated parameter/context cells are first averaged inside each history-seed block.

In addition to the full 40-block analysis, V36 performs four leave-one-history-pair-out analyses. Each asks whether the aggregate 30°−150° contrast remains positive after removing one of the four historical strata.

For each metric, inference uses a stratified sign-flip null over the remaining history-pair strata and a bootstrap over history-seed blocks.

Readouts:
- signed_affinity
- distance_margin
- cosine_delta

The experiment tests robustness to historical-stratum dominance. It does not establish consciousness, subjective experience, sentience, or any property outside the implemented computational system.
