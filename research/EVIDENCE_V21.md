# V21 — Evidence: Temporal Order of Recurrent State

## GitHub validation

- Workflow: state-temporal-order-v21
- Run: 36779475055
- Result: SUCCESS
- Artifact: 11126184798
- Six V12 blind parameter points, four history pairs, ten matched-noise seeds per pair.
- Receiver memory and pressure: common A/B midpoint.
- Future input: exactly zero.

## Pooled identity results

| Intervention | Original identity | Opposite identity |
|---|---:|---:|
| Intact | **90.42%** | 9.58% |
| Swap temporal slots | **82.29%** | 17.71% |
| Flatten both slots to donor mean | **80.63%** | 19.38% |
| Replace by common state | 50.00% | 50.00% |
| Centered temporal reversal | 32.71% | **67.29%** |

The `swap_slots` condition preserves the same two scalar values while exchanging their temporal order. Identity falls from 90.42% to 82.29%, showing that ordering matters but is not the sole determinant.

The `time_reverse_centered` condition reflects the ordered donor deviations around the common state and reverses their order. Its classification shifts strongly toward the opposite donor: 67.29% opposite-identity accuracy versus 9.58% for the intact state.

## Blind-point behavior

Across all six blind parameter points, centered temporal reversal favored the opposite identity:

- p1: 63.75% opposite identity
- p2: 66.25%
- p3: 66.25%
- p4: 70.00%
- p5: 72.50%
- p6: 65.00%

This consistency is important because the test was not tuned to the exact V10/V11 candidate point.

## Main finding

V21 supports a temporal-organization interpretation of the recurrent state. Historical identity is not determined solely by the unordered pair of state values: changing their temporal arrangement alters the identity readout, and the centered reversal systematically pushes the inferred identity toward the opposite history.

## Interpretation limits

This is evidence about temporal information encoded in recurrent state. It does not establish subjective experience, sentience, or consciousness.

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V21 — Evidencia: orden temporal del estado recurrente

## Validación GitHub

- Workflow: state-temporal-order-v21
- Run: 36779475055
- Result: SUCCESS
- Artifact: 11126184798
- Seis puntos ciegos V12, cuatro pares de historias, diez seeds de ruido emparejados por par.
- Memory y pressure del receptor: midpoint común A/B.
- Input futuro: exactamente cero.

## Resultados de identidad agrupados

| Intervención | Identidad original | Identidad opuesta |
|---|---:|---:|
| Intact | **90.42%** | 9.58% |
| Swap temporal slots | **82.29%** | 17.71% |
| Flatten ambos slots a media donante | **80.63%** | 19.38% |
| Reemplazar por estado común | 50.00% | 50.00% |
| Reversión temporal centrada | 32.71% | **67.29%** |

swap_slots conserva los dos valores escalares pero intercambia su orden temporal. La identidad cae de 90.42% a 82.29%, mostrando que el orden importa pero no es el único determinante.

time_reverse_centered refleja las desviaciones ordenadas del donante alrededor del estado común y revierte su orden. La clasificación se desplaza fuertemente al donante opuesto: 67.29% de accuracy de identidad opuesta frente a 9.58% para state intacto.

## Puntos ciegos

En los seis puntos ciegos, la reversión temporal centrada favoreció la identidad opuesta:

- p1: 63.75%
- p2: 66.25%
- p3: 66.25%
- p4: 70.00%
- p5: 72.50%
- p6: 65.00%

La consistencia es importante porque el test no fue ajustado al punto candidato exacto V10/V11.

## Hallazgo principal

V21 respalda una interpretación de organización temporal del estado recurrente. La identidad histórica no está determinada solo por el par no ordenado de valores: modificar su organización temporal altera la lectura de identidad y la reversión centrada desplaza sistemáticamente la identidad inferida hacia la historia opuesta.

## Límites

Es evidencia sobre información temporal codificada en el estado recurrente. No establece experiencia subjetiva, sentiencia ni consciencia.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V21 — Evidence: Temporal Order of Recurrent State

## GitHub validation

- Workflow: state-temporal-order-v21
- Run: 36779475055
- Result: SUCCESS
- Artifact: 11126184798
- Six V12 blind parameter points, four history pairs, ten matched-noise seeds per pair.
- Receiver memory and pressure: common A/B midpoint.
- Future input: exactly zero.

## Pooled identity results

| Intervention | Original identity | Opposite identity |
|---|---:|---:|
| Intact | **90.42%** | 9.58% |
| Swap temporal slots | **82.29%** | 17.71% |
| Flatten both slots to donor mean | **80.63%** | 19.38% |
| Replace by common state | 50.00% | 50.00% |
| Centered temporal reversal | 32.71% | **67.29%** |

swap_slots preserves the same two scalar values while exchanging temporal order. Identity falls from 90.42% to 82.29%, showing ordering matters but is not the sole determinant.

time_reverse_centered reflects ordered donor deviations around common state and reverses their order. Classification shifts strongly toward the opposite donor: 67.29% opposite-identity accuracy versus 9.58% for intact state.

## Blind-point behavior

Across all six blind parameter points, centered temporal reversal favored opposite identity: 63.75%, 66.25%, 66.25%, 70.00%, 72.50%, and 65.00%.

This consistency matters because the test was not tuned to the exact V10/V11 candidate point.

## Main finding

V21 supports a temporal-organization interpretation of recurrent state. Historical identity is not determined solely by the unordered pair of state values: changing temporal arrangement alters identity readout, and centered reversal systematically pushes inferred identity toward the opposite history.

## Interpretation limits

This is evidence about temporal information encoded in recurrent state. It does not establish subjective experience, sentience, or consciousness.

</details>