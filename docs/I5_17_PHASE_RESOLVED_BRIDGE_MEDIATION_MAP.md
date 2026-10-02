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

</details>
