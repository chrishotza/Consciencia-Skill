<a id="espanol"></a>

# V36 — Leave-One-History-Pair-Out Pre-validation

## Estado

**PRE-VALIDACIÓN LOCAL.** No sustituye un artefacto oficial de GitHub Actions.

V36 usa historia-seeds 110–119, seis puntos paramétricos, cuatro pares históricos, nueve contextos memoria×presión, radio 1.1, ángulos 30°/150°, entrada futura exactamente cero y semillas de referencia/prueba disjuntas.

La inferencia se hace sobre 40 bloques history-seed. Además del análisis completo, se repite el análisis excluyendo por turno cada uno de los cuatro estratos históricos.

## Resultado completo

| Métrica | Contraste 30°−150° | Null 95% | p | IC bootstrap 95% |
|---|---:|---:|---:|---:|
| signed_affinity | **0.230534** | 0.066905 | **0.00005** | **[0.214425, 0.244982]** |
| distance_margin | **1.063146** | 0.305978 | **0.00005** | **[0.975905, 1.142971]** |
| cosine_delta | **0.621432** | 0.177109 | **0.00005** | **[0.564808, 0.674366]** |

## Leave-one-history-pair-out

### signed_affinity

| Estrato excluido | Bloques restantes | Contraste | IC bootstrap 95% | p |
|---|---:|---:|---:|---:|
| pair 0 | 30 | **0.223621** | [0.202800, 0.241968] | 0.00005 |
| pair 1 | 30 | **0.264073** | [0.243639, 0.281566] | 0.00005 |
| pair 2 | 30 | **0.255732** | [0.245654, 0.266448] | 0.00005 |
| pair 3 | 30 | **0.178710** | [0.157421, 0.196991] | 0.00005 |

### distance_margin

| Estrato excluido | Contraste | IC bootstrap 95% | p |
|---|---:|---:|---:|
| pair 0 | **0.968864** | [0.855367, 1.072804] | 0.00005 |
| pair 1 | **1.214922** | [1.104086, 1.314602] | 0.00005 |
| pair 2 | **1.172020** | [1.124854, 1.221802] | 0.00005 |
| pair 3 | **0.896778** | [0.781633, 0.998760] | 0.00005 |

### cosine_delta

| Estrato excluido | Contraste | IC bootstrap 95% | p |
|---|---:|---:|---:|
| pair 0 | **0.532765** | [0.458779, 0.600840] | 0.00005 |
| pair 1 | **0.684747** | [0.612339, 0.751167] | 0.00005 |
| pair 2 | **0.687590** | [0.657316, 0.719280] | 0.00005 |
| pair 3 | **0.580628** | [0.504860, 0.649384] | 0.00005 |

## Lectura

Las tres métricas conservan el contraste 30°−150° cuando cualquiera de los cuatro tipos de historia se elimina del análisis. En esta pre-validación no aparece un único estrato cuya ausencia destruya la señal.

Esto es evidencia de robustez interna del fenómeno computacional bajo los protocolos definidos, no evidencia de conciencia ni de experiencia subjetiva.

La resolución del test de permutación es 1/(20,000+1), por lo que p=0.00005 debe leerse como un límite de resolución del procedimiento, no como una precisión adicional.

## Reproducibilidad

Código V36: 55b2d98c2f73e7121f7fee764cd1cdb82f6728dc

Workflow V36: 2c2e9e3d305f4adcb1b626090296a10855149fba

La pre-validación local mantuvo las ecuaciones del simulador y el esquema de semillas/ruido del protocolo; el objetivo fue comprobar la estructura de inferencia antes de la lectura del artefacto oficial de Actions.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V36 — Leave-One-History-Pair-Out Pre-validation

## Status

**LOCAL PRE-VALIDATION.** It does not replace an official GitHub Actions artifact.

V36 uses history-seeds 110–119, six parameter points, four history pairs, nine memory×pressure contexts, radius 1.1, angles 30°/150°, exactly zero future input, and disjoint reference/test seeds.

Inference uses 40 history-seed blocks. The protocol also repeats the analysis while excluding each of the four history strata in turn.

## Complete result

| Metric | 30°−150° contrast | Null 95% | p | Bootstrap 95% CI |
|---|---:|---:|---:|---:|
| signed_affinity | **0.230534** | 0.066905 | **0.00005** | **[0.214425, 0.244982]** |
| distance_margin | **1.063146** | 0.305978 | **0.00005** | **[0.975905, 1.142971]** |
| cosine_delta | **0.621432** | 0.177109 | **0.00005** | **[0.564808, 0.674366]** |

## Leave-one-history-pair-out

### signed_affinity

| Excluded stratum | Remaining blocks | Contrast | Bootstrap 95% CI | p |
|---|---:|---:|---:|---:|
| pair 0 | 30 | **0.223621** | [0.202800, 0.241968] | 0.00005 |
| pair 1 | 30 | **0.264073** | [0.243639, 0.281566] | 0.00005 |
| pair 2 | 30 | **0.255732** | [0.245654, 0.266448] | 0.00005 |
| pair 3 | 30 | **0.178710** | [0.157421, 0.196991] | 0.00005 |

### distance_margin

| Excluded stratum | Contrast | Bootstrap 95% CI | p |
|---|---:|---:|---:|
| pair 0 | **0.968864** | [0.855367, 1.072804] | 0.00005 |
| pair 1 | **1.214922** | [1.104086, 1.314602] | 0.00005 |
| pair 2 | **1.172020** | [1.124854, 1.221802] | 0.00005 |
| pair 3 | **0.896778** | [0.781633, 0.998760] | 0.00005 |

### cosine_delta

| Excluded stratum | Contrast | Bootstrap 95% CI | p |
|---|---:|---:|---:|
| pair 0 | **0.532765** | [0.458779, 0.600840] | 0.00005 |
| pair 1 | **0.684747** | [0.612339, 0.751167] | 0.00005 |
| pair 2 | **0.687590** | [0.657316, 0.719280] | 0.00005 |
| pair 3 | **0.580628** | [0.504860, 0.649384] | 0.00005 |

## Interpretation

All three metrics preserve the 30°−150° contrast when any of the four history types is removed. No single stratum destroys the signal in this pre-validation.

This is evidence of internal robustness of the computational phenomenon under the defined protocols, not evidence of consciousness or subjective experience.

The permutation-test resolution is 1/(20,000+1), so p=0.00005 is a resolution floor rather than extra precision.

## Reproducibility

V36 code: 55b2d98c2f73e7121f7fee764cd1cdb82f6728dc

V36 workflow: 2c2e9e3d305f4adcb1b626090296a10855149fba

Local pre-validation preserved the simulator equations and seed/noise scheme of the protocol; the goal was to verify inference structure before reading the official Actions artifact.

</details>