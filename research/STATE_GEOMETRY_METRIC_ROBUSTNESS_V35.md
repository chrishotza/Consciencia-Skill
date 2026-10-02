<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V35 — Robustez de métrica / null angular por clusters

V35 replica independientemente el diseño V34 usando history-seeds 100–109 y seeds disjuntas para referencias y continuaciones de prueba.

El diseño mantiene fijos los seis puntos paramétricos V34, cuatro estratos history-pair, nueve contextos sintéticos memory/pressure, radio 1.1, ángulos 30° y 150° e input futuro exactamente cero.

El objetivo es probar si el contraste direccional 30°→150° depende específicamente de la fórmula de signed-affinity usada en V33/V34.

Se calculan tres readouts a partir de las mismas trayectorias:

1. **signed_affinity**: score de distancia euclídea normalizada usado en V34.
2. **distance_margin**: diferencia de distancia euclídea bruta, db − da, después de corrección de signo consistente con el donante.
3. **cosine_delta**: diferencia de similitud coseno respecto de las dos firmas independientes de continuación de referencia, después de corrección de signo consistente con el donante.

La inferencia se realiza en el mismo nivel de bloque history-seed que V34: las celdas repetidas de parámetro/contexto se promedian dentro de cada uno de los 40 bloques history-seed. El contraste primario es 30° menos 150°.

El null es una permutación sign-flip estratificada dentro de los cuatro estratos history-pair (20.000 permutaciones). Un bootstrap estratificado entre bloques history-seed (10.000 remuestras) proporciona un intervalo del 95%.

La interpretación se restringe a geometría/dinámica computacional. Un resultado positivo no establece consciencia, experiencia subjetiva, sentiencia ni realización física fuera del simulador implementado.

</details>

<a id="english"></a>

# V35 — Metric Robustness / Angular Cluster Null

V35 is an independent replication of the V34 design using history seeds 100–109 and disjoint reference/test continuation seeds.

The simulation design is held fixed at the six V34 parameter points, four history-pair strata, nine synthetic memory/pressure contexts, radius 1.1, angles 30° and 150°, and exactly zero future input.

The purpose is to test whether the observed 30°→150° directional contrast depends specifically on the signed-affinity formula used in V33/V34.

Three readouts are computed from the same trajectories:

1. **signed_affinity**: normalized Euclidean distance score used in V34.
2. **distance_margin**: raw Euclidean distance difference, db − da, after donor-consistent sign correction.
3. **cosine_delta**: difference in cosine similarity to the two independent reference continuation signatures, after donor-consistent sign correction.

Inference is performed at the same history-seed block level as V34: repeated parameter/context cells are averaged inside each of the 40 history-seed blocks. The primary contrast is 30° minus 150°.

The null is a stratified sign-flip permutation within each of the four history-pair strata (20,000 permutations). A stratified bootstrap across history-seed blocks (10,000 resamples) provides a 95% interval.

Interpretation is restricted to computational geometry/dynamics. A positive result does not establish consciousness, subjective experience, sentience, or any physical realization outside the implemented simulator.
