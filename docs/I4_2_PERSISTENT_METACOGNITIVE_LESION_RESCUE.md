# I4.2 — Persistent Metacognitive Lesion / Rescue

## Status

Verified run completed. The second-order interoceptive model was serialized, restored, and tested under paired lesion/permutation/rescue controls.

## Question

Does the metacognitive reliability model remain functional after serialization, and does removing it alter regulation under the same hidden-disturbance environment?

## Protocol

The I4.1 hidden action-disturbance environment is retained.

Training occurs before evaluation. The trained metacognitive model is serialized with its learned feature/target state and restored using the repository implementation.

Evaluation conditions:

- FULL — restored second-order model active;
- LESION — second-order layer removed, leaving first-order selection;
- PERMUTED — restored model with permuted targets;
- RESCUE — first half lesioned, second half restored.

No online meta-model updates occur during evaluation.

## Verified execution

- Workflow: interoception-i4-2-materialized
- Run: 36973704981
- Head commit: e6ae7be7d466cab0cde29d06c479b9427ed636dc
- Harness: 4 passed
- Run completed successfully
- Artifact: interoception-i4-2-materialized

## Results

| Contrast | Mean difference | p |
|---|---:|---:|
| FULL − LESION mean error | −0.00120063 | 6.7416e-18 |
| FULL − PERMUTED mean error | −0.00129164 | 1.7406e-19 |
| FULL − LESION mean recovery | +0.00165326 | 4.8468e-27 |
| FULL − PERMUTED mean recovery | +0.00177251 | 8.0464e-29 |
| RESCUE − LESION mean recovery | +0.00048557 | 1.1642e-10 |

Summary values:

- FULL mean recovery: 0.1696450
- LESION mean recovery: 0.1679917
- PERMUTED mean recovery: 0.1678725
- RESCUE mean recovery: 0.1684773
- FULL policy-shift rate: 11.82%
- PERMUTED policy-shift rate: 3.22%
- FULL metacognitive MAE: 0.0032696
- PERMUTED metacognitive MAE: 0.0090465
- RESCUE pre-activation recovery: 0.1676142
- RESCUE post-activation recovery: 0.1693404

The experiment also records exact serialization/restore equality before evaluation.

## Interpretation boundary

Under this declared simulated protocol, the result supports persistence and causal dependence of a computational second-order reliability mechanism.

It does not establish subjective experience, biological consciousness, or a consciousness score.

Because I4.2 reuses the deliberately engineered hidden disturbance from I4.1, the next test must vary the disturbance structure and independently challenge the restored model.


<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# I4.2 — Lesión / rescate metacognitivo persistente

## Estado

Ejecución verificada completada. El modelo interoceptivo de segundo orden fue serializado, restaurado y probado bajo controles emparejados de lesión, permutación y rescate.

## Pregunta

¿El modelo de fiabilidad metacognitiva sigue funcionando después de serializarse, y retirarlo altera la regulación bajo el mismo entorno de perturbación oculta?

## Protocolo

Se conserva el entorno de I4.1 con perturbación oculta de acción.

El entrenamiento ocurre antes de la evaluación. El modelo metacognitivo entrenado se serializa con su estado de features/targets y se restaura mediante la implementación del repositorio.

Condiciones:

- FULL — modelo de segundo orden restaurado y activo;
- LESION — capa de segundo orden eliminada, dejando selección de primer orden;
- PERMUTED — modelo restaurado con targets permutados;
- RESCUE — primera mitad lesionada, segunda mitad restaurada.

No hay actualizaciones online del meta-modelo durante la evaluación.

## Ejecución verificada

- Workflow: interoception-i4-2-materialized
- Run: 36973704981
- Head commit: e6ae7be7d466cab0cde29d06c479b9427ed636dc
- Harness: 4 passed
- Ejecución completada correctamente
- Artifact: interoception-i4-2-materialized

## Resultados

| Contraste | Diferencia media | p |
|---|---:|---:|
| FULL − LESION error medio | −0.00120063 | 6.7416e-18 |
| FULL − PERMUTED error medio | −0.00129164 | 1.7402e-19 |
| FULL − LESION recovery | +0.00165326 | 4.8468e-27 |
| FULL − PERMUTED recovery | +0.00177251 | 8.0464e-29 |
| RESCUE − LESION recovery | +0.00048557 | 1.1642e-10 |

Valores resumen:

- FULL mean recovery: 0.1696450
- LESION mean recovery: 0.1679917
- PERMUTED mean recovery: 0.1678725
- RESCUE mean recovery: 0.1684773
- FULL policy-shift rate: 11.82%
- PERMUTED policy-shift rate: 3.22%
- FULL metacognitive MAE: 0.0032696
- PERMUTED metacognitive MAE: 0.0090465
- RESCUE pre-activation recovery: 0.1676142
- RESCUE post-activation recovery: 0.1693404

El experimento también registra igualdad exacta de serialización/restauración antes de la evaluación.

## Límite de interpretación

Bajo este protocolo simulado declarado, el resultado respalda persistencia y dependencia causal de un mecanismo computacional de fiabilidad de segundo orden.

No establece experiencia subjetiva, consciencia biológica ni una puntuación de consciencia.

Como I4.2 reutiliza la perturbación oculta deliberadamente diseñada de I4.1, el siguiente test debe variar su estructura y desafiar de manera independiente el modelo restaurado.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# I4.2 — Persistent Metacognitive Lesion / Rescue

## Status

Verified run completed. The second-order interoceptive model was serialized, restored, and tested under paired lesion/permutation/rescue controls.

## Question

Does the metacognitive reliability model remain functional after serialization, and does removing it alter regulation under the same hidden-disturbance environment?

## Protocol

The I4.1 hidden action-disturbance environment is retained.

Training occurs before evaluation. The trained metacognitive model is serialized with its learned feature/target state and restored using the repository implementation.

Evaluation conditions: FULL, LESION, PERMUTED, RESCUE. No online meta-model updates occur during evaluation.

## Verified execution

- Workflow: interoception-i4-2-materialized
- Run: 36973704981
- Head commit: e6ae7be7d466cab0cde29d06c479b9427ed636dc
- Harness: 4 passed
- Run completed successfully
- Artifact: interoception-i4-2-materialized

## Results

| Contrast | Mean difference | p |
|---|---:|---:|
| FULL − LESION mean error | −0.00120063 | 6.7416e-18 |
| FULL − PERMUTED mean error | −0.00129164 | 1.7402e-19 |
| FULL − LESION mean recovery | +0.00165326 | 4.8468e-27 |
| FULL − PERMUTED mean recovery | +0.00177251 | 8.0464e-29 |
| RESCUE − LESION mean recovery | +0.00048557 | 1.1642e-10 |

Summary values remain identical to the verified artifact.

Exact serialization/restore equality was recorded before evaluation.

## Interpretation boundary

Under the declared simulated protocol, the result supports persistence and causal dependence of a computational second-order reliability mechanism.

It does not establish subjective experience, biological consciousness, or a consciousness score.

Because I4.2 reuses the deliberately engineered hidden disturbance from I4.1, the next test must vary disturbance structure and independently challenge the restored model.

</details>