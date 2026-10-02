# I5.16 — Counterbalanced Pure-Phase Temporal Control

<a id="espanol"></a>

<details>
<summary>ES — abrir</summary>

## Objetivo

I5.15 mostró una fuerte asimetría de magnitud entre lag -1 y +1, pero su rotación finita de siete posiciones mezclaba el corrimiento temporal con efectos de frontera y reordenamiento local. I5.16 reemplaza esa construcción por una secuencia periódica de siete fases y un horizonte más largo, de modo que el lag sea un corrimiento de fase puro.

## Diseño

La secuencia base tiene **15 ciclos** sobre un periodo de siete fases:

`A, B, C, D, E, F, G`

El ciclo 0 permanece fijado en `A`. Los ciclos 1–14 siguen la fase:

`phase(cycle, lag) = (cycle + lag) mod 7`

con:

`lag ∈ {-3,-2,-1,+1,+2,+3}`

Como los ciclos 1–14 contienen exactamente dos periodos completos, todas las condiciones conservan la misma distribución de SELF_MODEL: dos apariciones de cada fase en el tramo desplazado, más la fase A fijada en t0.

## Contrabalanceo semántico

Para evitar que una etiqueta semántica concreta quede asociada a una dirección de lag, las siete asignaciones de significado A–G se rotan entre réplicas. El calendario temporal y la asignación de acciones permanecen iguales dentro de cada réplica emparejada.

## Condiciones

- BASE
- LAG -3
- LAG -2
- LAG -1
- LAG +1
- LAG +2
- LAG +3

Los brazos ±1 también se ejecutan con el bridge del modelo de sí desactivado.

## Endpoints

- cambio de acción futura respecto de BASE en ciclos 1–14;
- AUC absoluta de divergencia de estado;
- AUC firmada BASE → lag;
- diferencia firmada del estado final;
- simetría +k vs -k;
- coincidencia de acción aplicada en t0;
- coincidencia de distribución de SELF_MODEL;
- efecto bridge ON vs OFF en ±1.

## Estadística

Las métricas de magnitud se reportan de forma descriptiva. Los contrastes firmados usan sign-flip de 20.000 permutaciones sobre diferencias emparejadas. Se mantienen 24 réplicas, 24 ciclos de warmup y un checkpoint base idéntico dentro de cada réplica.

## Control metodológico

La ventaja de I5.16 frente a I5.15 es que no rota una cola finita de siete posiciones. Todas las condiciones usan el mismo ciclo periódico interno; el único cambio temporal es la fase inicial del tramo posterior a t0. El horizonte contiene un número entero de periodos posteriores, evitando desbalances de distribución semántica.

## Límite

I5.16 prueba si la asimetría observada en I5.15 sobrevive a una construcción de fase pura y contrabalanceada. No demuestra consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

<details>
<summary>EN — open</summary>

## Objective

I5.15 showed a strong magnitude asymmetry between lag -1 and +1, but its finite seven-position rotation mixed temporal displacement with boundary and local-reordering effects. I5.16 replaces that construction with a longer seven-phase periodic sequence so that lag is implemented as a pure phase shift.

## Design

The base sequence uses **15 cycles** over a seven-phase period:

`A, B, C, D, E, F, G`

Cycle 0 remains fixed at `A`. Cycles 1–14 follow:

`phase(cycle, lag) = (cycle + lag) mod 7`

with:

`lag ∈ {-3,-2,-1,+1,+2,+3}`

Because cycles 1–14 contain exactly two complete periods, every condition preserves the same SELF_MODEL distribution: two occurrences of every phase in the shifted segment, plus the cycle-0 A fixed at t0.

## Semantic counterbalancing

To avoid tying a specific semantic label to a lag direction, the seven A–G semantic assignments are cyclically rotated across replicates. The temporal schedule and action mapping remain paired within each replicate.

## Conditions

- BASE
- LAG -3
- LAG -2
- LAG -1
- LAG +1
- LAG +2
- LAG +3

The ±1 arms also receive bridge-OFF controls.

## Endpoints

- future-action change relative to BASE across cycles 1–14;
- absolute state-divergence AUC;
- signed BASE → lag state-difference AUC;
- signed final-state difference;
- symmetry between +k and -k;
- applied-action match at t0;
- SELF_MODEL distribution match;
- bridge ON vs OFF at ±1.

## Statistics

Magnitude metrics are reported descriptively. Signed paired contrasts use 20,000 sign-flip permutations on paired differences. The design keeps 24 replicates, 24 warmup cycles, and an identical warmup checkpoint within each replicate.

## Methodological control

The key improvement over I5.15 is that I5.16 does not rotate a finite seven-position tail. Every condition uses the same internal periodic cycle; the temporal manipulation is only the initial phase of the post-t0 segment. The post-t0 horizon contains an integer number of periods, preventing semantic-distribution imbalance.

## Boundary

I5.16 tests whether the I5.15 asymmetry survives a pure-phase, counterbalanced construction. It does not demonstrate consciousness or subjective experience.

</details>
