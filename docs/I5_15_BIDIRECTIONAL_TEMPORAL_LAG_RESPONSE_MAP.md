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

## Resultado verificado

Workflow: **37044533566** (run **784**); artifact **11243557588**; commit verificado **09e57c8a9592a300f8ed0f7f2590ab55f57fe10c**; seed **20261015**; **24** réplicas; **24** ciclos de warmup; **8** ciclos experimentales.

- coincidencia de acción aplicada en t0: **100%** en todos los lags;
- coincidencia de distribución de SELF_MODEL: **100%** en todos los lags;
- cambio medio de acción futura: **32.74%** (-3), **58.93%** (-2), **51.19%** (-1), **11.31%** (+1), **55.36%** (+2), **30.36%** (+3);
- AUC absoluta media de divergencia: **1.383681** (-3), **2.363792** (-2), **2.240213** (-1), **0.262091** (+1), **2.129393** (+2), **1.200861** (+3);
- contrastes firmados BASE → lag: **p=0.04740** para -2 y **p=0.04430** para +2; los demás lags no fueron significativos bajo este endpoint;
- simetría firmada +k vs -k: **p=0.84616** (+1), **0.80236** (+2), **0.63342** (+3);
- simetría por magnitud absoluta: +1 vs -1 produjo una diferencia de **-1.978122**, p **4.99975×10⁻⁵**; +2 vs -2: p **0.11349**; +3 vs -3: p **0.12099**;
- bridge +1 ON vs OFF: **0.262091** vs **2.019521**, diferencia ON−OFF **-1.757430**, p **4.99975×10⁻⁵**;
- bridge -1 ON vs OFF: **2.240213** vs **2.019521**, diferencia ON−OFF **+0.220692**, p **0.24834**.

Interpretación: el mapa revela una asimetría muy marcada de **magnitud** entre los lags -1 y +1, mientras que los contrastes firmados y la simetría firmada no establecen una separación direccional robusta. El efecto de bridge también fue específico de la dirección en este protocolo, pero el brazo +1 cambió la magnitud en sentido de reducción, no de incremento. Por tanto, I5.15 caracteriza una respuesta dependiente del desplazamiento temporal, pero no aísla todavía una explicación puramente de fase frente a efectos de frontera y reordenamiento local introducidos por la rotación finita de la cola. La siguiente prueba debe usar una secuencia periódica más larga y contrabalanceada, con el corrimiento aplicado como fase pura y sin la frontera artificial de la rotación de 7 posiciones.

## Verified result

Workflow: **37044533566** (run **784**); artifact **11243557588**; verified commit **09e57c8a9592a300f8ed0f7f2590ab55f57fe10c**; seed **20261015**; **24** replicates; **24** warmup cycles; **8** experimental cycles.

- applied-action match at t0: **100%** across all lags;
- SELF_MODEL distribution match: **100%** across all lags;
- mean future-action change: **32.74%** (-3), **58.93%** (-2), **51.19%** (-1), **11.31%** (+1), **55.36%** (+2), **30.36%** (+3);
- mean absolute state-divergence AUC: **1.383681** (-3), **2.363792** (-2), **2.240213** (-1), **0.262091** (+1), **2.129393** (+2), **1.200861** (+3);
- signed BASE → lag contrasts: **p=0.04740** for -2 and **p=0.04430** for +2; the other lags were not significant for this endpoint;
- signed +k vs -k symmetry: **p=0.84616** (+1), **0.80236** (+2), **0.63342** (+3);
- absolute-magnitude symmetry: +1 vs -1 differed by **-1.978122**, p **4.99975×10⁻⁵**; +2 vs -2: p **0.11349**; +3 vs -3: p **0.12099**;
- +1 bridge ON vs OFF: **0.262091** vs **2.019521**, ON−OFF **-1.757430**, p **4.99975×10⁻⁵**;
- -1 bridge ON vs OFF: **2.240213** vs **2.019521**, ON−OFF **+0.220692**, p **0.24834**.

Interpretation: the map reveals a strong **magnitude** asymmetry between lags -1 and +1, while the signed contrasts and signed symmetry tests do not establish a robust directional separation. The bridge effect was also direction-specific in this protocol, but the +1 arm changed magnitude by reducing it rather than increasing it. I5.15 therefore characterizes a displacement-dependent response, but it does not yet isolate a pure phase explanation from boundary and local-reordering effects introduced by the finite 7-position tail rotation. The next test should use a longer counterbalanced periodic sequence, with lag implemented as a pure phase shift and without the artificial boundary created by tail rotation.
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
