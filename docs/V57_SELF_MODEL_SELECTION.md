<a id="espanol"></a>

# V57 — Selección mediante modelo de sí comparada con un oráculo

## Pregunta

¿El modelo de sí aprendido por el organismo selecciona futuras trayectorias mejor que una política aleatoria emparejada después de la misma historia de calibración?

## Diseño

Cada réplica comienza desde una trayectoria de calentamiento emparejada.

Se permiten dos señales candidatas:

- `-1.0`;
- `+1.0`.

El brazo con modelo de sí puntúa ambos estados siguientes contrafactuales y elige la señal con mejor puntuación de coherencia declarada.

El brazo aleatorio elige una de las mismas candidatas mediante una política aleatoria determinista con semilla.

Después de la elección se ejecuta la transición real.

Por separado, un oráculo evalúa directamente ambas transiciones candidatas desde el mismo estado previo utilizando la dinámica numérica congelada. El oráculo se utiliza solamente después de la intervención para calcular regret; nunca se expone al selector del organismo.

## Observables principales

- regret del modelo de sí;
- regret del control aleatorio;
- ventaja emparejada de regret;
- tasa de aciertos del oráculo;
- valor p de permutación emparejada por cambio de signo.

## Interpretación

Si el brazo con modelo de sí presenta sistemáticamente menor regret que el brazo aleatorio emparejado, el modelo interno de sí mismo del organismo no es meramente descriptivo: resulta funcionalmente útil para seleccionar entre trayectorias futuras.

Esto sigue siendo un resultado computacional sobre un modelo de sí, no una demostración de consciencia fenomenológica.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V57 — Self-Model Selection Compared with an Oracle

## Question

Does the organism's learned self-model select future trajectories better than a matched random policy after the same calibration history?

## Design

Each replicate starts from a matched warm-up trajectory.

Two candidate signals are allowed:

- -1.0;
- +1.0.

The self-model arm scores both counterfactual next states and selects the signal with the better declared coherence score.

The random arm chooses one of the same candidates using a deterministic seeded random policy.

The actual transition is executed after selection.

Separately, an oracle evaluates both candidate transitions directly from the same prior state using frozen numerical dynamics. The oracle is used only after intervention to calculate regret; it is never exposed to the organism selector.

## Primary observables

- self-model regret;
- random-control regret;
- paired regret advantage;
- oracle hit rate;
- paired sign-flip permutation p-value.

## Interpretation

If the self-model arm systematically shows lower regret than the matched random arm, the organism's internal self-model is not merely descriptive: it is functionally useful for selecting among future trajectories.

This remains a computational result about a self-model, not a demonstration of phenomenal consciousness.

</details>