<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V57 — Registro de resultado

## Run

- workflow: organism-self-model-selection-v57
- run: 36802728735
- artifact: 11135928002
- head: 75791177fdf7cf8c167aae1a051f7def700f4b32

## Resultado

Se ejecutaron 24 réplicas emparejadas después de 32 ciclos de calibración con señales candidatas -1.0 y +1.0.

- self-model mean regret = 0.0230727418
- random-control mean regret = 0.1368546699
- mean regret advantage of self-model = 0.1137819281
- median paired advantage = 0.0
- self-model oracle-hit rate = 70.8333%
- random-control oracle-hit rate = 45.8333%
- oracle-hit rate difference = 25 puntos porcentuales
- paired sign-flip p = 0.00434978

El brazo self-model seleccionó el candidato óptimo post hoc con mayor frecuencia y tuvo un regret sustancialmente menor que el control random emparejado.

## Interpretación

V57 es el primer experimento de esta secuencia en el que el self-model aprendido muestra un efecto conductual causal sobre la selección de futuras trayectorias bajo un control emparejado.

Es evidencia de que el self-model interno es funcionalmente útil para elegir entre trayectorias posibles.

No es evidencia de experiencia subjetiva.

</details>

<a id="english"></a>

# V57 — Result Record

## Run

- workflow: `organism-self-model-selection-v57`
- run: `36802728735`
- artifact: `11135928002`
- head: `75791177fdf7cf8c167aae1a051f7def700f4b32`

## Result

24 paired replicates were run after 32 calibration cycles using candidate signals
`-1.0` and `+1.0`.

- self-model mean regret = 0.0230727418;
- random-control mean regret = 0.1368546699;
- mean regret advantage of self-model = 0.1137819281;
- median paired advantage = 0.0;
- self-model oracle-hit rate = 70.8333%;
- random-control oracle-hit rate = 45.8333%;
- oracle-hit rate difference = 25 percentage points;
- paired sign-flip p = 0.00434978.

The self-model arm therefore selected the post-hoc optimal candidate more often
and incurred substantially lower regret than the matched random control.

## Interpretation

V57 is the first experiment in this ladder where the learned self-model is shown
to have a causal behavioral effect on future trajectory selection under a paired
control.

This is evidence that the internal self-model is functionally useful for choosing
among possible trajectories. It is not evidence of subjective experience.