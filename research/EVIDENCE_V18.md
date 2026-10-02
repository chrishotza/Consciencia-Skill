# V18 — Evidence: State Source / Permutation Control

## GitHub validation

- Workflow: state-source-permutation-v18
- Run: 36778479908
- Result: SUCCESS
- Artifact: 11126596868
- Six V12 blind parameter points, 3 source histories, 10 matched-noise seeds per point.
- Receiver memory and pressure were common across the three histories.
- Future input was exactly zero.

## Source classification

| State precision | Source identity accuracy |
|---|---:|
| Full precision | 75.00% |
| 3 bits | **78.33%** |
| 4 bits | **78.33%** |
| 6 bits | 73.33% |

At the six blind parameter points, 3-bit source classification was:

| Point | Accuracy |
|---|---:|
| p1 | 100.0% |
| p2 | 76.7% |
| p3 | 80.0% |
| p4 | 86.7% |
| p5 | 60.0% |
| p6 | 66.7% |

The effect varies by parameter point, so the result should be treated as a robust source-following tendency rather than perfect transfer.

## Permutation control

At 3 bits, the nominal receiver label was changed across all three receiver positions while the donor state was held fixed.

| State source | Receiver label 0 | Receiver label 1 | Receiver label 2 |
|---|---:|---:|---:|
| Source 0 | 90% | 90% | 90% |
| Source 1 | 80% | 80% | 80% |
| Source 2 | 65% | 65% | 65% |

The exact invariance across receiver labels is the clean control: changing the nominal receiver does not change the classification. The classification follows the state source.

## Main finding

V17 showed that donor state can transfer identity when memory and pressure are common. V18 adds source specificity: under a three-history receiver control, the transferred identity follows the state source independently of the nominal receiver label.

This strengthens the narrower computational claim that the recurrent state is not merely a passive contextual correlate; its encoded history can be transported as a causal state variable.

## Interpretation limits

The source-following effect is not perfect at every parameter point and precision. The experiment therefore supports a graded causal-transfer interpretation, not a claim of a discrete or universal identity channel.

This remains a computational dynamical result and does not establish subjective experience, sentience, or consciousness.

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V18 — Evidencia: control de fuente/permutación del estado

## Validación GitHub

- Workflow: state-source-permutation-v18
- Run: 36778479908
- Result: SUCCESS
- Artifact: 11126596868
- Seis puntos ciegos V12, 3 historias fuente, 10 seeds de ruido emparejados por punto.
- Memory y pressure del receptor comunes a las tres historias.
- Input futuro exactamente cero.

## Clasificación de fuente

| Precisión de state | Accuracy de fuente |
|---|---:|
| Full precision | 75.00% |
| 3 bits | **78.33%** |
| 4 bits | **78.33%** |
| 6 bits | 73.33% |

En los seis puntos ciegos, la clasificación de fuente a 3 bits fue:

| Punto | Accuracy |
|---|---:|
| p1 | 100.0% |
| p2 | 76.7% |
| p3 | 80.0% |
| p4 | 86.7% |
| p5 | 60.0% |
| p6 | 66.7% |

El efecto varía por punto, por lo que debe tratarse como una tendencia robusta de seguimiento de fuente y no como transferencia perfecta.

## Control de permutación

A 3 bits se cambió la etiqueta nominal del receptor entre las tres posiciones, manteniendo fijo el state donante.

| Fuente de state | Etiqueta receptor 0 | Etiqueta receptor 1 | Etiqueta receptor 2 |
|---|---:|---:|---:|
| Source 0 | 90% | 90% | 90% |
| Source 1 | 80% | 80% | 80% |
| Source 2 | 65% | 65% | 65% |

La invariancia exacta entre etiquetas es el control limpio: cambiar el receptor nominal no cambia la clasificación. La clasificación sigue la fuente del estado.

## Hallazgo principal

V17 mostró que el estado donante puede transferir identidad cuando memory y pressure son comunes. V18 añade especificidad de fuente: en un control receptor de tres historias, la identidad transferida sigue la fuente de state independientemente de la etiqueta nominal del receptor.

Esto fortalece la afirmación computacional más estrecha de que el estado recurrente no es solamente un correlato contextual pasivo; su historia codificada puede transportarse como variable de estado causal.

## Límites

El seguimiento de fuente no es perfecto en todos los puntos y precisiones. El experimento respalda una interpretación gradual de transferencia causal y no un canal de identidad discreto o universal.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V18 — Evidence: State Source / Permutation Control

## GitHub validation

- Workflow: state-source-permutation-v18
- Run: 36778479908
- Result: SUCCESS
- Artifact: 11126596868
- Six V12 blind parameter points, 3 source histories, 10 matched-noise seeds per point.
- Receiver memory and pressure were common across the three histories.
- Future input was exactly zero.

## Source classification

| State precision | Source identity accuracy |
|---|---:|
| Full precision | 75.00% |
| 3 bits | **78.33%** |
| 4 bits | **78.33%** |
| 6 bits | 73.33% |

At the six blind parameter points, 3-bit source classification was p1 100.0%, p2 76.7%, p3 80.0%, p4 86.7%, p5 60.0%, p6 66.7%.

The effect varies by parameter point and should be treated as a robust source-following tendency rather than perfect transfer.

## Permutation control

At 3 bits, the nominal receiver label was changed across all three positions while donor state was fixed.

| State source | Receiver label 0 | Receiver label 1 | Receiver label 2 |
|---|---:|---:|---:|
| Source 0 | 90% | 90% | 90% |
| Source 1 | 80% | 80% | 80% |
| Source 2 | 65% | 65% | 65% |

Exact invariance across receiver labels is the clean control: classification follows the state source.

## Main finding

V17 showed donor-state identity transfer when memory and pressure are common. V18 adds source specificity: transferred identity follows state source independently of nominal receiver label.

This strengthens the narrower computational claim that recurrent state is not merely a passive contextual correlate; encoded history can be transported as a causal state variable.

## Interpretation limits

The source-following effect is not perfect at every parameter point and precision. The experiment therefore supports graded causal-transfer interpretation, not a discrete or universal identity channel.

</details>