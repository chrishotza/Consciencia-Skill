# I5.15 — Bidirectional Temporal-Lag Response Map

<a id="espanol"></a>

<details>
<summary>ES — abrir</summary>

## Objetivo

I5.14 mostró que corrimientos temporales de distinta dirección no producen la misma respuesta. I5.15 amplía ese resultado a un mapa bidireccional de lags para caracterizar cómo cambia la trayectoria cuando la secuencia semántica se desplaza varios ciclos.

## Diseño

La secuencia base de 8 ciclos es:

`A, B, C, A, B, C, A, B`

El ciclo 0 se mantiene fijo en `A` para todas las condiciones y las posiciones 1–7 se permutan por rotaciones de:

`lag ∈ {-3,-2,-1,+1,+2,+3}`

Cada lag conserva exactamente la misma distribución de SELF_MODEL que BASE y la misma acción aplicada en t0.

## Condiciones

- BASE
- LAG -3
- LAG -2
- LAG -1
- LAG +1
- LAG +2
- LAG +3

Para los lags ±1 también se ejecuta el brazo bridge OFF como control de mediación.

## Endpoints

- cambio de acción futura respecto de BASE en ciclos 1–7;
- AUC absoluta de divergencia de estado;
- AUC firmada de divergencia BASE → lag;
- diferencia de estado final firmada;
- simetría entre lag +k y -k;
- coincidencia de acción aplicada en t0;
- coincidencia de distribución de SELF_MODEL;
- efecto bridge ON vs OFF en ±1.

## Estadística

Las métricas de magnitud se presentan como mapa descriptivo. Para inferencia emparejada se utilizan contrastes firmados entre BASE y cada lag y entre lags opuestos; se aplica sign-flip de 20.000 permutaciones sobre esas diferencias firmadas.

- 24 réplicas emparejadas;
- 24 ciclos de warmup;
- 8 ciclos experimentales;
- mismo checkpoint y seed por réplica.

## Límite

I5.15 caracteriza sensibilidad temporal computacional bajo el arnés. No demuestra consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

<details>
<summary>EN — open</summary>

## Objective

I5.14 showed that temporal shifts in opposite directions do not produce the same response. I5.15 expands that result into a bidirectional lag-response map to characterize how the trajectory changes when the semantic sequence is displaced by multiple cycles.

## Design

The 8-cycle base sequence is:

`A, B, C, A, B, C, A, B`

Cycle 0 remains fixed at `A` for every condition, while positions 1–7 are rotated by:

`lag ∈ {-3,-2,-1,+1,+2,+3}`

Every lag therefore preserves exactly the same SELF_MODEL distribution as BASE and the same applied action at t0.

## Conditions

- BASE
- LAG -3
- LAG -2
- LAG -1
- LAG +1
- LAG +2
- LAG +3

The ±1 conditions also receive bridge-OFF controls for mediation.

## Endpoints

- future-action change relative to BASE across cycles 1–7;
- absolute state-divergence AUC;
- signed BASE → lag state-difference AUC;
- signed final-state difference;
- symmetry between lag +k and -k;
- applied-action match at t0;
- SELF_MODEL distribution match;
- bridge ON vs OFF effect at ±1.

## Statistics

Magnitude metrics are reported descriptively. Paired inference uses signed BASE-vs-lag contrasts and signed opposite-lag contrasts; 20,000 sign-flip permutations are applied to those signed differences.

- 24 paired replicates;
- 24 warmup cycles;
- 8 experimental cycles;
- same checkpoint and seed per replicate.

## Boundary

I5.15 characterizes computational temporal sensitivity under the harness. It does not demonstrate consciousness or subjective experience.

</details>
