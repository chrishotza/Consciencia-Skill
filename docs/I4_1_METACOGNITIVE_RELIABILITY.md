# I4.1 — Metacognitive Reliability Under Hidden Action Disturbance

## Status

Verified run completed. The result supports a computational metacognitive reliability effect under the declared simulated hidden-disturbance protocol.

## Question

Can a second-order model learn when a first-order interoceptive prediction is likely to be unreliable, and can that estimate alter action selection?

## Protocol

The first-order model predicts the next operating condition for candidate actions.

The executed world contains an additional deterministic hidden disturbance:

risk = 0.04 + 0.09 * |action| + 0.06 * max(pressure, 0)

The first-order model does not receive this disturbance term.

The second-order observer learns:

current interoceptive state + candidate action + first-order prediction
→ observed first-order prediction error

Training uses magnitude 0.50. Evaluation uses held-out magnitudes 0.35, 0.65, and 0.90.

## Conditions

FIRST_ORDER, META, PERMUTED, RANDOM.

All evaluation conditions are paired by seed.

## Verified execution

- Workflow: interoception-i4-1-v02
- Run: 36973517099
- Head commit: ebb8176c615bf71a8f77920b0d9a2e43d8b3be2c
- Harness: 4 passed
- Run completed successfully
- Artifact: interoception-i4-1-v02

## Primary observed contrasts

| Contrast | Mean difference | p |
|---|---:|---:|
| META − FIRST_ORDER mean error | −0.00138238 | 7.0953e-21 |
| META − PERMUTED mean error | −0.00125732 | 3.8474e-18 |
| META − FIRST_ORDER recovery | +0.00166219 | 1.3172e-07 |
| META − PERMUTED recovery | +0.00130404 | 3.6700e-05 |

The metacognitive policy shifted its action choice on 11.04% of evaluation steps versus 2.34% for the permuted control.

Mean metacognitive prediction MAE was 0.0036884 for META versus 0.0090787 for PERMUTED.

## Interpretation boundary

This run provides evidence for a computational metacognitive property in the tested simulated environment: the second-order observer learned information about the reliability of the first-order internal-state prediction, and the resulting estimate was used in action selection.

The result does not establish subjective experience, biological consciousness, or a consciousness score.

The hidden disturbance is deliberately engineered, so external validity remains an open question.

## Scientific next step

The next protocol should increase independence from the hand-designed disturbance:

1. vary hidden disturbance structure without changing the meta objective;
2. introduce regime switches that are not directly encoded by action magnitude;
3. test persistence of the second-order model across restart/sleep;
4. add a lesion/rescue intervention targeting only the metacognitive layer;
5. preserve the first-order/permuted controls.


<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# I4.1 — Fiabilidad metacognitiva bajo perturbación oculta de acción

## Estado

Ejecución verificada completada. El resultado respalda un efecto computacional de fiabilidad metacognitiva bajo el protocolo declarado de perturbación oculta simulada.

## Pregunta

¿Puede un modelo de segundo orden aprender cuándo una predicción interoceptiva de primer orden probablemente será poco fiable, y puede esa estimación alterar la selección de acciones?

## Protocolo

El modelo de primer orden predice la siguiente condición operativa para acciones candidatas.

El mundo ejecutado contiene una perturbación determinista oculta adicional:

risk = 0.04 + 0.09 * |action| + 0.06 * max(pressure, 0)

El modelo de primer orden no recibe ese término.

El observador de segundo orden aprende:

estado interoceptivo actual + acción candidata + predicción de primer orden
→ error de predicción de primer orden observado

El entrenamiento utiliza magnitud 0.50. La evaluación utiliza magnitudes reservadas 0.35, 0.65 y 0.90.

## Condiciones

FIRST_ORDER, META, PERMUTED, RANDOM.

Todas las condiciones de evaluación están emparejadas por seed.

## Ejecución verificada

- Workflow: interoception-i4-1-v02
- Run: 36973517099
- Head commit: ebb8176c615bf71a8f77920b0d9a2e43d8b3be2c
- Harness: 4 passed
- Ejecución completada correctamente
- Artifact: interoception-i4-1-v02

## Contrastes primarios observados

| Contraste | Diferencia media | p |
|---|---:|---:|
| META − FIRST_ORDER error medio | −0.00138238 | 7.0953e-21 |
| META − PERMUTED error medio | −0.00125732 | 3.8474e-18 |
| META − FIRST_ORDER recovery | +0.00166219 | 1.3172e-07 |
| META − PERMUTED recovery | +0.00130404 | 3.6700e-05 |

La política META cambió su elección de acción en 11.04% de los pasos de evaluación frente a 2.34% para el control permutado.

MAE medio de predicción metacognitiva: 0.0036884 para META frente a 0.0090787 para PERMUTED.

## Límite de interpretación

Esta ejecución proporciona evidencia de una propiedad metacognitiva computacional en el entorno simulado probado: el observador de segundo orden aprendió información sobre la fiabilidad de la predicción interoceptiva de primer orden y la estimación resultante fue utilizada en la selección de acciones.

No establece experiencia subjetiva, consciencia biológica ni una puntuación de consciencia.

La perturbación oculta está diseñada deliberadamente, por lo que la validez externa permanece abierta.

## Próximo paso científico

El siguiente protocolo debe aumentar la independencia respecto de la perturbación diseñada manualmente:

1. variar su estructura sin cambiar el objetivo meta;
2. introducir cambios de régimen no codificados directamente por la magnitud de la acción;
3. probar persistencia del modelo de segundo orden tras reinicio/sueño;
4. añadir lesión/rescate dirigida solo a la capa metacognitiva;
5. conservar controles first-order/permuted.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# I4.1 — Metacognitive Reliability Under Hidden Action Disturbance

## Status

Verified run completed. The result supports a computational metacognitive reliability effect under the declared simulated hidden-disturbance protocol.

## Question

Can a second-order model learn when a first-order interoceptive prediction is likely to be unreliable, and can that estimate alter action selection?

## Protocol

The first-order model predicts next operating condition for candidate actions.

The executed world contains an additional deterministic hidden disturbance:

risk = 0.04 + 0.09 * |action| + 0.06 * max(pressure, 0)

The first-order model does not receive this disturbance term.

The second-order observer learns current interoceptive state + candidate action + first-order prediction → observed first-order prediction error.

Training uses magnitude 0.50. Evaluation uses held-out magnitudes 0.35, 0.65, and 0.90.

## Conditions

FIRST_ORDER, META, PERMUTED, RANDOM. All evaluation conditions are paired by seed.

## Verified execution

- Workflow: interoception-i4-1-v02
- Run: 36973517099
- Head commit: ebb8176c615bf71a8f77920b0d9a2e43d8b3be2c
- Harness: 4 passed
- Run completed successfully
- Artifact: interoception-i4-1-v02

## Primary observed contrasts

| Contrast | Mean difference | p |
|---|---:|---:|
| META − FIRST_ORDER mean error | −0.00138238 | 7.0953e-21 |
| META − PERMUTED mean error | −0.00125732 | 3.8474e-18 |
| META − FIRST_ORDER recovery | +0.00166219 | 1.3172e-07 |
| META − PERMUTED recovery | +0.00130404 | 3.6700e-05 |

The metacognitive policy shifted its action choice on 11.04% of evaluation steps versus 2.34% for the permuted control.

Mean metacognitive prediction MAE was 0.0036884 for META versus 0.0090787 for PERMUTED.

## Interpretation boundary

This run provides evidence for a computational metacognitive property in the tested simulated environment: the second-order observer learned information about the reliability of first-order internal-state prediction, and the resulting estimate was used in action selection.

The result does not establish subjective experience, biological consciousness, or a consciousness score.

The hidden disturbance is deliberately engineered, so external validity remains open.

## Scientific next step

The next protocol should vary hidden-disturbance structure without changing the meta objective, introduce regime switches not directly encoded by action magnitude, test second-order persistence across restart/sleep, add a metacognitive-only lesion/rescue, and preserve first-order/permuted controls.

</details>