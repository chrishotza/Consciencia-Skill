# I5.17 — Phase-Resolved Bridge Mediation Map

<a id="espanol"></a>

<details>
<summary>ES — abrir</summary>

## Objetivo

I5.16 reprodujo la asimetría de magnitud entre lag -1 y +1 con una construcción de fase pura y contrabalanceada. I5.17 pregunta si el efecto del puente del modelo de sí es específico de una fase o si aparece de forma general a lo largo del mapa temporal.

## Diseño

Se conserva exactamente el arnés de I5.16:

- 15 ciclos;
- periodo semántico de siete fases `A…G`;
- ciclo 0 fijado en A;
- lags `{-3,-2,-1,+1,+2,+3}`;
- dos periodos completos en los ciclos 1–14;
- siete rotaciones cíclicas de las asignaciones semánticas entre réplicas;
- 24 réplicas emparejadas y 24 ciclos de warmup.

Para **cada lag** se ejecutan dos condiciones emparejadas:

- bridge ON;
- bridge OFF.

BASE se mantiene con bridge ON y sirve como referencia común para los endpoints de trayectoria.

## Endpoints

Para cada lag y estado del bridge:

- cambio de acción futura respecto de BASE;
- AUC absoluta de divergencia de estado;
- AUC firmada BASE → condición;
- diferencia firmada del estado final;
- coincidencia de acción aplicada en t0;
- coincidencia de distribución de SELF_MODEL.

Para el efecto específico del bridge se calculan:

- ON − OFF en AUC absoluta;
- ON − OFF en AUC firmada;
- ON − OFF en cambio de acción futura;
- simetría del efecto bridge entre +k y -k.

## Estadística

Los contrastes por lag usan sign-flip de 20.000 permutaciones sobre diferencias emparejadas. La pregunta es de localización de fase: los p-valores se reportan por lag y no se convierten en una afirmación global de significación sin una corrección adicional.

## Control

El t0 permanece emparejado y el calendario semántico es idéntico entre ON y OFF. El único factor manipulado entre esas dos condiciones es el puente del modelo de sí.

## Límite

I5.17 prueba si el efecto del bridge observado en +1 es local a una fase temporal o forma un perfil más general. No demuestra consciencia ni experiencia subjetiva.


## Resultado verificado

Workflow: **37047719727** (run **801**); artifact **11244733803**; commit **578802962b4f37066db95d46567245dcbb9ac83b**; seed **20261017**; **24** réplicas; **24** ciclos de warmup; **15** ciclos experimentales; **180 tests** pasaron.

Controles de identidad del protocolo:
- coincidencia de acción aplicada en t0: **100%** en todos los lags y estados del bridge;
- coincidencia de distribución de SELF_MODEL: **100%** en todos los lags y estados del bridge.

Resumen por lag, bridge ON:
- lag -3: AUC absoluta media **4.188494**; AUC firmada media **-0.167807**; cambio de acción futura **44.05%**.
- lag -2: AUC absoluta **4.290030**; AUC firmada **-0.455736**; cambio de acción **45.54%**.
- lag -1: AUC absoluta **4.720667**; AUC firmada **-0.710849**; cambio de acción **50.89%**.
- lag +1: AUC absoluta **4.180806**; AUC firmada **-0.405803**; cambio de acción **42.86%**.
- lag +2: AUC absoluta **4.526839**; AUC firmada **-0.169213**; cambio de acción **49.70%**.
- lag +3: AUC absoluta **4.359548**; AUC firmada **-0.066147**; cambio de acción **45.24%**.

Efecto bridge ON − OFF, por lag:
- **-3:** AUC absoluta **-0.715123**, p **0.000900**; AUC firmada **-1.218683**, p **0.002000**; cambio de acción **-0.110119**, p **0.001550**.
- **-2:** AUC absoluta **-0.613587**, p **0.069047**; AUC firmada **-1.506611**, p **0.000600**; cambio de acción **-0.095238**, p **0.045798**.
- **-1:** AUC absoluta **-0.182950**, p **0.529124**; AUC firmada **-1.761724**, p **<0.00005**; cambio de acción **-0.041667**, p **0.287986**.
- **+1:** AUC absoluta **-0.722811**, p **0.003450**; AUC firmada **-1.456679**, p **0.001500**; cambio de acción **-0.122024**, p **0.000300**.
- **+2:** AUC absoluta **-0.376779**, p **0.099395**; AUC firmada **-1.220088**, p **0.002050**; cambio de acción **-0.053571**, p **0.116394**.
- **+3:** AUC absoluta **-0.544069**, p **0.057997**; AUC firmada **-1.117023**, p **0.003450**; cambio de acción **-0.098214**, p **0.005850**.

Simetría absoluta del efecto bridge +k vs -k:
- k=1: diferencia media **-0.539861**, p **0.129994**;
- k=2: diferencia media **+0.236808**, p **0.565822**;
- k=3: diferencia media **+0.171054**, p **0.440678**.

Interpretación: el efecto del bridge **no queda restringido al lag +1** bajo este arnés; aparecen contrastes por lag en múltiples endpoints. Sin embargo, las comparaciones absolutas +k vs -k no separaron significativamente ninguna de las tres parejas. Los p-valores fueron calculados por lag con 20.000 permutaciones sign-flip y no deben interpretarse como una afirmación global sin corrección por multiplicidad. I5.17 por tanto caracteriza un **perfil fase-dependiente del bridge**, pero no identifica todavía una fase única ni establece una explicación causal de orden superior.

No demuestra consciencia ni experiencia subjetiva.
</details>

<a id="english"></a>

<details>
<summary>EN — open</summary>

## Objective

I5.16 reproduced the -1/+1 magnitude asymmetry under a pure-phase, counterbalanced construction. I5.17 asks whether the self-model bridge effect is specific to one temporal phase or appears broadly across the temporal map.

## Design

I5.17 preserves the I5.16 harness exactly:

- 15 cycles;
- seven-phase semantic period `A…G`;
- cycle 0 fixed at A;
- lags `{-3,-2,-1,+1,+2,+3}`;
- two complete periods across cycles 1–14;
- seven cyclic semantic-assignment rotations across replicates;
- 24 paired replicates and 24 warmup cycles.

For **every lag**, two paired conditions are run:

- bridge ON;
- bridge OFF.

BASE remains bridge ON and is the common trajectory reference.

## Endpoints

For each lag and bridge state:

- future-action change relative to BASE;
- absolute state-divergence AUC;
- signed BASE → condition state AUC;
- signed final-state difference;
- applied-action match at t0;
- SELF_MODEL distribution match.

For the bridge-specific effect:

- ON − OFF absolute-AUC difference;
- ON − OFF signed-AUC difference;
- ON − OFF future-action-change difference;
- bridge-effect symmetry between +k and -k.

## Statistics

Per-lag paired contrasts use 20,000 sign-flip permutations on paired differences. This is a phase-localization question: p-values are reported per lag and are not treated as a global significance claim without an additional multiplicity correction.

## Control

t0 remains paired and the semantic calendar is identical between ON and OFF. The bridge is the only manipulated factor between those conditions.

## Boundary

I5.17 tests whether the +1 bridge effect is localized to a temporal phase or forms a broader response profile. It does not demonstrate consciousness or subjective experience.


## Verified result

Workflow: **37047719727** (run **801**); artifact **11244733803**; commit **578802962b4f37066db95d46567245dcbb9ac83b**; seed **20261017**; **24** replicates; **24** warmup cycles; **15** experimental cycles; **180 tests** passed.

Protocol identity controls:
- applied-action match at t0: **100%** across all lags and bridge states;
- SELF_MODEL distribution match: **100%** across all lags and bridge states.

Bridge ON summary by lag:
- lag -3: mean absolute AUC **4.188494**; signed AUC **-0.167807**; future-action change **44.05%**.
- lag -2: mean absolute AUC **4.290030**; signed AUC **-0.455736**; future-action change **45.54%**.
- lag -1: mean absolute AUC **4.720667**; signed AUC **-0.710849**; future-action change **50.89%**.
- lag +1: mean absolute AUC **4.180806**; signed AUC **-0.405803**; future-action change **42.86%**.
- lag +2: mean absolute AUC **4.526839**; signed AUC **-0.169213**; future-action change **49.70%**.
- lag +3: mean absolute AUC **4.359548**; signed AUC **-0.066147**; future-action change **45.24%**.

Bridge effect ON − OFF by lag:
- **-3:** absolute AUC **-0.715123**, p **0.000900**; signed AUC **-1.218683**, p **0.002000**; future-action change **-0.110119**, p **0.001550**.
- **-2:** absolute AUC **-0.613587**, p **0.069047**; signed AUC **-1.506611**, p **0.000600**; future-action change **-0.095238**, p **0.045798**.
- **-1:** absolute AUC **-0.182950**, p **0.529124**; signed AUC **-1.761724**, p **<0.00005**; future-action change **-0.041667**, p **0.287986**.
- **+1:** absolute AUC **-0.722811**, p **0.003450**; signed AUC **-1.456679**, p **0.001500**; future-action change **-0.122024**, p **0.000300**.
- **+2:** absolute AUC **-0.376779**, p **0.099395**; signed AUC **-1.220088**, p **0.002050**; future-action change **-0.053571**, p **0.116394**.
- **+3:** absolute AUC **-0.544069**, p **0.057997**; signed AUC **-1.117023**, p **0.003450**; future-action change **-0.098214**, p **0.005850**.

Absolute bridge-effect symmetry +k vs -k:
- k=1: mean difference **-0.539861**, p **0.129994**;
- k=2: mean difference **+0.236808**, p **0.565822**;
- k=3: mean difference **+0.171054**, p **0.440678**.

Interpretation: the bridge effect is **not restricted to lag +1** under this harness; multiple lags show bridge-related contrasts across endpoints. However, none of the three absolute +k vs -k symmetry contrasts separated significantly. P-values are per-lag 20,000-permutation sign-flip tests and should not be treated as a global claim without multiplicity correction. I5.17 therefore characterizes a **phase-dependent bridge response profile**, but does not identify a unique phase or establish a higher-order causal explanation.

It does not demonstrate consciousness or subjective experience.
</details>
