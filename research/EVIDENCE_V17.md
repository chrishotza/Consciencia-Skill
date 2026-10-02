# V17 — Evidence: Quantized State-Only Causal Transplant

## GitHub validation

- Workflow: quantized-state-transplant-v17
- Run: 36777615496
- Result: SUCCESS
- Artifact: 11126365516
- Blind parameter points: 6 (the V12 holdout points)
- History pairs: 4
- Seeds: 10 per pair and parameter point
- Future input: exactly zero
- Receiver memory and pressure: common A/B midpoint
- Only donor-specific state: `state_prev` and `state`

## Pooled identity accuracy

| State representation | Identity accuracy |
|---|---:|
| Full precision | 90.42% |
| 1 bit | 49.38% |
| 2 bits | 55.21% |
| 3 bits | **90.21%** |
| 4 bits | 87.50% |
| 6 bits | **91.04%** |
| 8 bits | 90.21% |

The 1- and 2-bit representations largely lose the identity signal, while 3 bits recover most of the full-precision performance. Higher precision does not produce a monotonic improvement because the underlying dynamics are nonlinear and the task is stochastic.

## Blind-point consistency

At 3 bits, the six holdout points produce identity accuracies:

| Point | Accuracy |
|---|---:|
| p1 | 87.5% |
| p2 | 91.25% |
| p3 | 88.75% |
| p4 | 91.25% |
| p5 | 91.25% |
| p6 | 91.25% |

Thus 3-bit state-only transfer remains above 87.5% at every blind parameter point, despite memory and pressure carrying no donor-specific information.

## Main finding

Historical identity can be causally transferred by the recurrent state alone in the blind holdout regimes. The receiver's explicit memory and pressure can be replaced by common values without eliminating the donor signal.

The state-only channel is also compact: 3 bits per temporal state slot recover roughly 90% identity accuracy. 1–2 bits are insufficient for robust transfer in this protocol.

## Interpretation limits

This is evidence for a compact, causally sufficient carrier of historical information in the implemented dynamics. It does not establish subjective experience, sentience, or consciousness.

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V17 — Evidencia: transplante causal cuantizado solo-estado

## Validación GitHub

- Workflow: quantized-state-transplant-v17
- Run: 36777615496
- Result: SUCCESS
- Artifact: 11126365516
- Puntos de parámetros ciegos: 6 (puntos holdout V12)
- Pares de historias: 4
- Seeds: 10 por par y punto
- Input futuro: exactamente cero
- Memory y pressure del receptor: midpoint común A/B
- Único state específico del donante: state_prev y state

## Accuracy de identidad agrupada

| Representación | Accuracy |
|---|---:|
| Full precision | 90.42% |
| 1 bit | 49.38% |
| 2 bits | 55.21% |
| 3 bits | **90.21%** |
| 4 bits | 87.50% |
| 6 bits | **91.04%** |
| 8 bits | 90.21% |

Las representaciones de 1–2 bits pierden gran parte de la señal de identidad, mientras 3 bits recupera la mayor parte del rendimiento de precisión completa. Mayor precisión no produce una mejora monótona porque la dinámica es no lineal y la tarea estocástica.

## Consistencia en puntos ciegos

Con 3 bits, los seis puntos holdout producen:

| Punto | Accuracy |
|---|---:|
| p1 | 87.5% |
| p2 | 91.25% |
| p3 | 88.75% |
| p4 | 91.25% |
| p5 | 91.25% |
| p6 | 91.25% |

El trasplante solo-estado de 3 bits permanece por encima de 87.5% en todos los puntos ciegos, aunque memory y pressure no contienen información específica del donante.

## Hallazgo principal

La identidad histórica puede transferirse causalmente mediante el estado recurrente solo en los regímenes holdout ciegos. Memory y pressure explícitos del receptor pueden sustituirse por valores comunes sin eliminar la señal del donante.

El canal state-only es además compacto: 3 bits por slot temporal recuperan aproximadamente 90% de accuracy de identidad. 1–2 bits no bastan para una transferencia robusta bajo este protocolo.

## Límites

Es evidencia de un portador compacto y causalmente suficiente de información histórica en la dinámica implementada. No establece experiencia subjetiva, sentiencia ni consciencia.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V17 — Evidence: Quantized State-Only Causal Transplant

## GitHub validation

- Workflow: quantized-state-transplant-v17
- Run: 36777615496
- Result: SUCCESS
- Artifact: 11126365516
- Blind parameter points: 6 (the V12 holdout points)
- History pairs: 4
- Seeds: 10 per pair and parameter point
- Future input: exactly zero
- Receiver memory and pressure: common A/B midpoint
- Only donor-specific state: state_prev and state

## Pooled identity accuracy

| State representation | Identity accuracy |
|---|---:|
| Full precision | 90.42% |
| 1 bit | 49.38% |
| 2 bits | 55.21% |
| 3 bits | **90.21%** |
| 4 bits | 87.50% |
| 6 bits | **91.04%** |
| 8 bits | 90.21% |

The 1- and 2-bit representations largely lose the identity signal, while 3 bits recover most full-precision performance. Higher precision does not produce a monotonic improvement because the underlying dynamics are nonlinear and the task is stochastic.

## Blind-point consistency

At 3 bits, all six holdout points remain above 87.5% identity accuracy.

## Main finding

Historical identity can be causally transferred by recurrent state alone in blind holdout regimes. Receiver memory and pressure can be replaced with common values without eliminating the donor signal.

The state-only channel is compact: 3 bits per temporal state slot recover roughly 90% identity accuracy. 1–2 bits are insufficient for robust transfer in this protocol.

## Interpretation limits

This is evidence for a compact, causally sufficient carrier of historical information in the implemented dynamics. It does not establish subjective experience, sentience, or consciousness.

</details>