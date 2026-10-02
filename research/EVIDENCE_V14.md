# Evidence V14 — Matched-Dimension Self-Prediction

V14 controls the feature-count objection in V13. Every predictor uses exactly two inputs.

- external = [u(t), u(t-1)]
- state = [u(t), r(t)]
- memory = [u(t), m(t)]
- pressure = [u(t), p(t)]

Cross-seed evaluation uses 20 seeds and four held-out folds.

| Regime | External R2 | Input+State R2 | State gain | Input+Memory R2 | Memory gain | Input+Pressure R2 | Pressure gain |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline | 0.776 | 0.990 | +0.214 | 0.912 | +0.136 | 0.853 | +0.077 |
| Critical | 0.106 | **0.292** | **+0.186** | 0.082 | -0.024 | 0.084 | -0.023 |
| Holdout critical | 0.128 | **0.295** | **+0.167** | 0.104 | -0.024 | 0.103 | -0.026 |
| Persistence | 0.107 | **0.289** | **+0.182** | 0.087 | -0.020 | 0.086 | -0.021 |

## Main conclusion

In the resonant regimes, adding the recurrent state as a single matched-dimensional feature improves next-state prediction by approximately 0.17–0.19 R2, while replacing that state with the explicit memory or pressure scalar does not improve prediction.

This strengthens the interpretation that the recurrent state itself carries the most useful predictive information about the system's subsequent trajectory.

This remains a computational property of the model and does not by itself establish consciousness or subjective experience.

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Evidencia V14 — Autopredicción con dimensión emparejada

V14 controla la objeción sobre la cantidad de features planteada en V13. Cada predictor utiliza exactamente dos entradas.

- external = [u(t), u(t-1)]
- state = [u(t), r(t)]
- memory = [u(t), m(t)]
- pressure = [u(t), p(t)]

La evaluación cross-seed utiliza 20 seeds y cuatro folds reservados.

| Régimen | R2 externo | R2 input+state | Ganancia state | R2 input+memory | Ganancia memory | R2 input+pressure | Ganancia pressure |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline | 0.776 | 0.990 | +0.214 | 0.912 | +0.136 | 0.853 | +0.077 |
| Critical | 0.106 | **0.292** | **+0.186** | 0.082 | -0.024 | 0.084 | -0.023 |
| Holdout critical | 0.128 | **0.295** | **+0.167** | 0.104 | -0.024 | 0.103 | -0.026 |
| Persistence | 0.107 | **0.289** | **+0.182** | 0.087 | -0.020 | 0.086 | -0.021 |

## Conclusión principal

En los regímenes resonantes, agregar el estado recurrente como feature único de dimensión emparejada mejora la predicción del estado siguiente aproximadamente 0.17–0.19 R2, mientras que reemplazarlo por memory o pressure explícitos no mejora la predicción.

Esto refuerza la interpretación de que el propio estado recurrente contiene la información predictiva más útil sobre la trayectoria posterior del sistema.

Sigue siendo una propiedad computacional del modelo y no establece por sí sola consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V14 — Evidence: Matched-Dimension Self-Prediction

V14 controls the feature-count objection in V13. Every predictor uses exactly two inputs.

- external = [u(t), u(t-1)]
- state = [u(t), r(t)]
- memory = [u(t), m(t)]
- pressure = [u(t), p(t)]

Cross-seed evaluation uses 20 seeds and four held-out folds.

| Regime | External R2 | Input+State R2 | State gain | Input+Memory R2 | Memory gain | Input+Pressure R2 | Pressure gain |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline | 0.776 | 0.990 | +0.214 | 0.912 | +0.136 | 0.853 | +0.077 |
| Critical | 0.106 | **0.292** | **+0.186** | 0.082 | -0.024 | 0.084 | -0.023 |
| Holdout critical | 0.128 | **0.295** | **+0.167** | 0.104 | -0.024 | 0.103 | -0.026 |
| Persistence | 0.107 | **0.289** | **+0.182** | 0.087 | -0.020 | 0.086 | -0.021 |

## Main conclusion

In resonant regimes, adding recurrent state as a single matched-dimensional feature improves next-state prediction by approximately 0.17–0.19 R2, while replacing that state with explicit memory or pressure does not improve prediction.

This strengthens the interpretation that recurrent state itself carries the most useful predictive information about subsequent trajectory.

This remains a computational property of the model and does not by itself establish consciousness or subjective experience.

</details>