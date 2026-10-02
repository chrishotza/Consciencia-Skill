# V25 — Confirmatory State Polar Replication Evidence

## Status
**SUCCESS** — GitHub Actions run `36783982639`.

## Design
V25 replicated V24 using independent seeds 10–19, while preserving:
- the same six blind V12 parameter points,
- the same four history-pair constructions,
- the same common receiver memory/pressure midpoint,
- exactly zero future input,
- the same continuation-affinity and identity-classification rule.

The radius grid was refined to 0.50–1.30 in 0.10 increments and the angular grid to 10° increments.

Each pooled cell contains 480 donor instances (6 parameters × 4 pairs × 10 seeds × 2 donors).

## Primary result
The V24 directional surface replicates.

V25 radial directional contrast (max identity accuracy − min identity accuracy):

| Radius | Max | Min | Contrast |
|---:|---:|---:|---:|
| 0.50 | 71.67% | 28.33% | 43.33 pp |
| 0.60 | 79.38% | 20.63% | 58.75 pp |
| 0.70 | 82.71% | 17.29% | 65.42 pp |
| 0.80 | 88.75% | 11.25% | 77.50 pp |
| 0.90 | 87.71% | 12.29% | 75.42 pp |
| 1.00 | 89.58% | 10.42% | 79.17 pp |
| **1.10** | **90.83%** | **9.17%** | **81.67 pp** |
| 1.20 | 89.58% | 10.42% | 79.17 pp |
| 1.30 | 90.63% | 9.38% | 81.25 pp |

The V25 global maximum is 90.83% at radius 1.10, angle 0°. The corresponding antipodal condition at 180° is 9.17%.

At radius 1.10, the pooled angular profile is strongly directional: 0° = 90.83%, 90° = 40.21%, 180° = 9.17%.

## Independent replication against V24
For the directly overlapping V24 grid (radii 0.50 and 1.00; angles 0–350° in the V25 data), V24 and V25 identity surfaces have:
- Pearson correlation: **0.99268**
- mean absolute difference: **1.79 percentage points**
- RMSE: **2.46 percentage points**

V25 therefore reproduces the geometry observed in V24 on disjoint seeds rather than merely reproducing a single peak.

## Parameter-level robustness
At radius 1.10, the six blind parameter points each retain a strong directional profile. Their peak identity accuracies range from 90.0% to 97.5%, while minima range from 7.5% to 12.5%. Peak orientation remains near the original 0° axis (with the 10° grid resolving some peaks at 340°).

## Statistical reference
At the pooled 1.10/0° cell, 90.83% identity corresponds to an approximate binomial 95% interval of 88.25–93.41% under the simple independent-trial approximation. At 1.10/180°, 9.17% corresponds to 6.59–11.75%. These intervals are descriptive; the repeated dynamical simulations are not necessarily independent experimental subjects.

## Interpretation
V25 supports a reproducible computational result:

> Under a common receiver memory/pressure context and zero future input, identity classification depends strongly on the orientation and magnitude of a compact two-slot state deviation.

The agreement between independent V24 and V25 surfaces makes this less consistent with a seed-specific artifact.

## Boundary
This establishes a property of the implemented computational dynamics. It does **not** establish consciousness, subjective experience, or sentience.

## Next experiment
V26 should move from spatial structure to temporal structure: measure identity accuracy in successive continuation windows after state transplantation. This tests whether the directional state code is merely an immediate perturbation or remains causally expressed as the common zero-input trajectory unfolds.


<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V25 — Evidencia de réplica confirmatoria de la superficie polar

## Estado
**SUCCESS** — GitHub Actions run 36783982639.

## Diseño
V25 replica V24 con seeds independientes 10–19, conservando:
- los mismos seis puntos paramétricos ciegos V12;
- las mismas cuatro construcciones de pares de historias;
- el mismo midpoint común de memory/pressure del receptor;
- input futuro exactamente cero;
- la misma regla de affinity de continuación y clasificación de identidad.

La grilla de radius se refinó a 0.50–1.30 en pasos de 0.10 y la angular a pasos de 10°.

Cada celda agrupada contiene 480 instancias donantes (6 parámetros × 4 pares × 10 seeds × 2 donantes).

## Resultado primario
La superficie direccional de V24 se replica.

| Radius | Max | Min | Contraste |
|---:|---:|---:|---:|
| 0.50 | 71.67% | 28.33% | 43.33 pp |
| 0.60 | 79.38% | 20.63% | 58.75 pp |
| 0.70 | 82.71% | 17.29% | 65.42 pp |
| 0.80 | 88.75% | 11.25% | 77.50 pp |
| 0.90 | 87.71% | 12.29% | 75.42 pp |
| 1.00 | 89.58% | 10.42% | 79.17 pp |
| **1.10** | **90.83%** | **9.17%** | **81.67 pp** |
| 1.20 | 89.58% | 10.42% | 79.17 pp |
| 1.30 | 90.63% | 9.38% | 81.25 pp |

El máximo global V25 es 90.83% en radius 1.10, angle 0°. La condición antipodal a 180° es 9.17%.

En radius 1.10, el perfil angular agrupado es fuertemente direccional: 0° = 90.83%, 90° = 40.21%, 180° = 9.17%.

## Réplica independiente frente a V24

Para la grilla directamente superpuesta de V24, las superficies V24/V25 tienen:
- correlación de Pearson: **0.99268**;
- diferencia absoluta media: **1.79 puntos porcentuales**;
- RMSE: **2.46 puntos porcentuales**.

V25 reproduce la geometría observada en V24 con seeds disjuntas, no solo un pico aislado.

## Robustez paramétrica

En radius 1.10, los seis puntos ciegos conservan un perfil direccional fuerte. Sus accuracies máximas van de 90.0% a 97.5%, mientras los mínimos van de 7.5% a 12.5%. La orientación máxima permanece cerca del eje original 0°; la grilla de 10° resuelve algunos picos en 340°.

## Referencia estadística

En la celda agrupada 1.10/0°, 90.83% de identidad corresponde aproximadamente a un intervalo binomial 95% de 88.25–93.41% bajo la aproximación simple de trials independientes. En 1.10/180°, 9.17% corresponde a 6.59–11.75%. Estos intervalos son descriptivos; las simulaciones dinámicas repetidas no son necesariamente sujetos experimentales independientes.

## Interpretación

V25 respalda un resultado computacional reproducible:

> Bajo contexto común de memory/pressure y input futuro cero, la clasificación de identidad depende fuertemente de la orientación y magnitud de una desviación de estado compacta de dos slots.

La concordancia entre las superficies V24 y V25 independientes es menos compatible con un artefacto específico de seed.

## Límite

Establece una propiedad de las dinámicas computacionales implementadas. No establece consciencia, experiencia subjetiva ni sentiencia.

## Próximo experimento

V26 debe pasar de estructura espacial a estructura temporal: medir accuracy de identidad en ventanas sucesivas de continuación después del trasplante de estado. Esto prueba si el código direccional es una perturbación inmediata o si continúa causalmente expresándose mientras avanza la trayectoria común sin input.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V25 — Confirmatory State Polar Replication Evidence

## Status
**SUCCESS** — GitHub Actions run 36783982639.

## Design
V25 replicated V24 using independent seeds 10–19, preserving the same six blind V12 parameter points, four history-pair constructions, common receiver memory/pressure midpoint, zero future input, and continuation-affinity identity rule.

Radius grid was refined to 0.50–1.30 in 0.10 increments; angle grid to 10° increments.

Each pooled cell contains 480 donor instances.

## Primary result
The V24 directional surface replicates.

| Radius | Max | Min | Contrast |
|---:|---:|---:|---:|
| 0.50 | 71.67% | 28.33% | 43.33 pp |
| 0.60 | 79.38% | 20.63% | 58.75 pp |
| 0.70 | 82.71% | 17.29% | 65.42 pp |
| 0.80 | 88.75% | 11.25% | 77.50 pp |
| 0.90 | 87.71% | 12.29% | 75.42 pp |
| 1.00 | 89.58% | 10.42% | 79.17 pp |
| **1.10** | **90.83%** | **9.17%** | **81.67 pp** |
| 1.20 | 89.58% | 10.42% | 79.17 pp |
| 1.30 | 90.63% | 9.38% | 81.25 pp |

The global maximum is 90.83% at radius 1.10, angle 0°. The corresponding antipodal 180° condition is 9.17%.

At radius 1.10, pooled angular profile is strongly directional: 0° = 90.83%, 90° = 40.21%, 180° = 9.17%.

## Independent replication against V24

On the directly overlapping V24 grid, V24 and V25 identity surfaces have Pearson correlation **0.99268**, mean absolute difference **1.79 percentage points**, and RMSE **2.46 percentage points**.

V25 therefore reproduces V24 geometry on disjoint seeds rather than merely reproducing one peak.

## Parameter robustness

At radius 1.10, all six blind parameter points retain a strong directional profile. Peak identity accuracies range 90.0%–97.5%; minima range 7.5%–12.5%. Peak orientation remains near the original 0° axis, with some peaks resolved at 340° by the 10° grid.

## Statistical reference

At pooled 1.10/0°, 90.83% identity corresponds to an approximate binomial 95% interval of 88.25–93.41% under a simple independent-trial approximation. At 1.10/180°, 9.17% corresponds to 6.59–11.75%. These intervals are descriptive; repeated dynamical simulations are not necessarily independent experimental subjects.

## Interpretation

V25 supports a reproducible computational result:

> Under common receiver memory/pressure context and zero future input, identity classification depends strongly on the orientation and magnitude of a compact two-slot state deviation.

Agreement between independent V24 and V25 surfaces is less consistent with a seed-specific artifact.

## Boundary

This establishes a property of the implemented computational dynamics. It does not establish consciousness, subjective experience, or sentience.

## Next experiment

V26 should move from spatial structure to temporal structure by measuring identity accuracy in successive continuation windows after state transplantation.

</details>