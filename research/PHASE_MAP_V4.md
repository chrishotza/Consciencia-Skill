<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Mapa de fase dinámica — V4

El barrido completo de frontera V4 evaluó beta_memory de 0.9950 a 0.9995 en 181 puntos y 20 seeds.

## Observación principal

El régimen no es un único umbral beta monótono.

Path-gap ya es alto en beta=0.995 y permanece elevado durante el intervalo explorado. Lo que cambia fuertemente es el tiempo de persistencia de la separación histórica.

| beta | path_gap | critical_lift | recovery_to_10pct |
|---:|---:|---:|---:|
| 0.9950 | 0.576 | 0.794 | 64.7 |
| 0.9965 | 0.580 | 0.814 | 183.6 |
| 0.9970 | 0.583 | 0.826 | 198.7 |
| 0.99735 | 0.624 | 0.812 | 210.6 |
| 0.99750 | 0.590 | 0.841 | 217.4 |
| 0.99775 | 0.599 | 0.867 | 207.5 |
| 0.9980 | 0.554 | 0.826 | 117.8 |
| 0.9985 | 0.583 | 0.841 | 20.7 |
| 0.9990 | 0.571 | 0.818 | 88.9 |
| 0.9995 | 0.554 | 0.806 | 155.7 |

## Cresta conjunta

Una región conjunta definida por recovery_to_10pct >= 180 y critical_lift >= 0.80 contiene 51 puntos beta, aproximadamente 0.99650 <= beta <= 0.997825.

Dentro de esa región:

- path-gap medio = 0.5902
- critical-lift medio = 0.8277
- recovery medio = 201.1 pasos

Un score conjunto simple path_gap × critical_lift × recovery_time alcanza su máximo cerca de beta ≈ 0.997475:

- path-gap = 0.6038
- critical-lift = 0.8395
- recovery = 215.8 pasos

Los máximos separados están desplazados:

- máximo path-gap: beta ≈ 0.99735
- máximo critical-lift: beta ≈ 0.99775
- máximo score conjunto: beta ≈ 0.997475

Este desplazamiento es importante: sugiere que el sistema tiene varios observables acoplados en lugar de un único parámetro de orden escalar.

## Interpretación

La descripción computacional actual más fuerte es una banda amplia de persistencia-criticalidad en lugar de un único beta crítico.

Es una caracterización operacional de las dinámicas del modelo. No establece consciencia, experiencia subjetiva ni una interpretación física del estado simbólico X.

</details>

<a id="english"></a>

# Dynamic Phase Map — V4

The completed V4 boundary sweep evaluated beta_memory from 0.9950 to 0.9995 at 181 points and 20 seeds.

## Main observation

The regime is not a single monotonic beta threshold.

Path-gap is already high at beta=0.995 and remains elevated through the scanned interval. What changes strongly is the persistence time of the historical separation.

| beta | path_gap | critical_lift | recovery_to_10pct |
|---:|---:|---:|---:|
| 0.9950 | 0.576 | 0.794 | 64.7 |
| 0.9965 | 0.580 | 0.814 | 183.6 |
| 0.9970 | 0.583 | 0.826 | 198.7 |
| 0.99735 | 0.624 | 0.812 | 210.6 |
| 0.99750 | 0.590 | 0.841 | 217.4 |
| 0.99775 | 0.599 | 0.867 | 207.5 |
| 0.9980 | 0.554 | 0.826 | 117.8 |
| 0.9985 | 0.583 | 0.841 | 20.7 |
| 0.9990 | 0.571 | 0.818 | 88.9 |
| 0.9995 | 0.554 | 0.806 | 155.7 |

## Joint ridge

A practical joint region defined by recovery_to_10pct >= 180 and critical_lift >= 0.80 contains 51 beta points spanning approximately 0.99650 <= beta <= 0.997825.

Within that region:
- mean path-gap = 0.5902
- mean critical-lift = 0.8277
- mean recovery time = 201.1 steps

A simple joint score path_gap × critical_lift × recovery_time peaks around beta ≈ 0.997475:
- path-gap = 0.6038
- critical-lift = 0.8395
- recovery = 215.8 steps

The separate maxima are offset:
- path-gap maximum: beta ≈ 0.99735
- critical-lift maximum: beta ≈ 0.99775
- joint score maximum: beta ≈ 0.997475

This offset is important: it suggests the system has multiple coupled observables rather than one scalar order parameter.

## Interpretation

The strongest current computational description is a broad persistence-criticality band rather than a single critical beta.

This is an operational characterization of the model dynamics. It does not establish consciousness, subjective experience, or any physical interpretation of the symbolic X state.