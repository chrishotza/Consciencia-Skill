<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Evidencia V61 — Self-model metacognitivo

## Hipótesis

Un organismo persistente con self-model de primer orden debería poder aprender un modelo de segundo orden del error de predicción de ese modelo y utilizar la fiabilidad estimada de sus propias predicciones como parte de la selección de trayectoria.

## Diseño experimental

Cada réplica:

1. construye una trayectoria warmup emparejada;
2. persiste snapshots del self-observer de primer orden;
3. inicializa un MetaSelfObserver de segundo orden a partir de errores históricos de predicción de primer orden;
4. clona el mismo estado en tres brazos;
5. selecciona entre {-1, +1} usando meta-self-model, self-model de primer orden o control random;
6. puntúa la trayectoria elegida contra un oracle post hoc;
7. reconstruye los errores reales de predicción de primer orden para ambas trayectorias candidatas;
8. compara esos errores con los errores predichos por el modelo de segundo orden.

## Comparación primaria

regret_self_model - regret_meta_self_model

es la ventaja emparejada del meta-self-model.

## Comparación metacognitiva secundaria

Para cada candidato:

abs(predicted_error - actual_prediction_error)

se compara con el error de un baseline de error medio constante.

## Limitaciones

El simulador es determinista salvo por su proceso de ruido seedado y el provider es sintético. El protocolo mide comportamiento computacional de modelo-de-modelo, no fenomenología.

</details>

<a id="english"></a>

# Evidence V61 — Metacognitive self-model

## Hypothesis

A persistent organism with a first-order self-model should be able to learn a second-order model of that model's prediction error and use the estimated reliability of its own predictions as part of trajectory selection.

## Experimental design

Each replicate:

1. builds a matched warmup trajectory;
2. persists first-order self-observer snapshots;
3. initializes a second-order MetaSelfObserver from historical first-order prediction errors;
4. clones the same state into three arms;
5. selects among {-1, +1} using meta-self-model, first-order self-model, or random control;
6. scores the chosen trajectory against a post-hoc oracle;
7. reconstructs actual first-order prediction errors for both candidate trajectories;
8. compares those errors with the second-order model's predicted errors.

## Primary comparison

regret_self_model - regret_meta_self_model

is the paired meta-self-model advantage.

## Secondary metacognitive comparison

For every candidate:

abs(predicted_error - actual_prediction_error)

is compared against the error of a constant mean-error baseline.

## Limitations

The simulator is deterministic apart from its seeded noise process and the provider is synthetic. The protocol measures computational model-of-model behavior, not phenomenology.