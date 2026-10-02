# V32 — Ensemble Context Geometry Evidence

## Status
**SUCCESS** — GitHub Actions run `36788862121`.

## Method
V32 replaced the invalid V31 comparator with independent continuation ensembles.

For every receiver context:
- the receiver state is the A/B midpoint;
- memory and pressure are synthetic and donor-independent;
- A and B reference signatures are means of five independent zero-input continuations using the unrotated donor states;
- test continuations use independent noise seeds;
- identity is scored from Euclidean distance between the test temporal state signature and the two ensemble reference signatures.

## Results

At radius 1.1, pooled identity accuracy across all contexts:

| Angle | Mean identity | Context range |
|---:|---:|---:|
| 30° | **87.27%** | 21.63 pp |
| 60° | 64.36% | 32.42 pp |
| 90° | 46.46% | 24.00 pp |
| 120° | 18.44% | 33.33 pp |
| 150° | **9.24%** | 29.67 pp |

The corresponding mean signed affinity changes from **+0.343 at 30°** through approximately zero at 90° to **−0.504 at 150°**.

Across the tested context surface, the directional response is therefore preserved while its magnitude is modulated by memory and pressure.

Examples:
- memory −0.8 / pressure 0.0: 30° = 99.13%, 150° = 0.42%;
- memory 0.8 / pressure 2.0: 30° = 86.08%, 150° = 21.21%;
- memory 0.0 / pressure 1.0: 30° = 81.83%, 150° = 7.25%.

## Interpretation
V32 supports the following bounded computational statement:

> A compact two-slot state geometry produces a reproducible directional response under donor-independent receiver contexts, while the strength of that response varies with contextual memory and pressure.

The ensemble references and independent continuation noise remove the same-noise cancellation problem of V31.

The effect is not context-free: context changes the magnitude and, in some regions, the angular profile.

## Statistical caution
The pooled context cells contain many repeated simulation trials generated from the same fixed parameter points and history families. Therefore the raw cell counts should not be treated as equivalent to independent experimental subjects.

V33 addresses this by computing matched within-history angular contrasts and an angle-permutation null.

## Boundary
V32 establishes a property of the implemented computational dynamics. It does not establish consciousness, subjective experience, or sentience.


<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V32 — Evidencia de geometría contextual por ensemble

## Estado
**SUCCESS** — GitHub Actions run 36788862121.

## Método
V32 reemplazó el comparador inválido de V31 por ensembles de continuación independientes.

Para cada contexto receptor:
- state del receptor = midpoint A/B;
- memory y pressure sintéticos e independientes del donante;
- firmas A y B de referencia = medias de cinco continuaciones independientes sin input usando los estados donantes sin rotar;
- continuaciones de prueba con seeds de ruido independientes;
- identidad calculada por distancia euclídea entre la firma temporal de prueba y las dos firmas ensemble.

## Resultados

A radius 1.1, accuracy de identidad agrupada en todos los contextos:

| Ángulo | Identidad media | Rango entre contextos |
|---:|---:|---:|
| 30° | **87.27%** | 21.63 pp |
| 60° | 64.36% | 32.42 pp |
| 90° | 46.46% | 24.00 pp |
| 120° | 18.44% | 33.33 pp |
| 150° | **9.24%** | 29.67 pp |

La affinity firmada media cambia de **+0.343 a 30°** a aproximadamente cero a 90° y **−0.504 a 150°**.

En la superficie de contexto probada, la respuesta direccional se conserva mientras su magnitud es modulada por memory y pressure.

Ejemplos:
- memory −0.8 / pressure 0.0: 30° = 99.13%, 150° = 0.42%;
- memory 0.8 / pressure 2.0: 30° = 86.08%, 150° = 21.21%;
- memory 0.0 / pressure 1.0: 30° = 81.83%, 150° = 7.25%.

## Interpretación
V32 permite la siguiente afirmación computacional acotada:

> Una geometría compacta de estado de dos slots produce una respuesta direccional reproducible bajo contextos de receptor independientes del donante, mientras que la fuerza de esa respuesta varía con memory y pressure contextuales.

Las referencias ensemble y los ruidos independientes de continuación eliminan el problema de cancelación con el mismo ruido de V31.

El efecto no es independiente del contexto: el contexto cambia magnitud y, en algunas regiones, el perfil angular.

## Precaución estadística
Las celdas agrupadas contienen muchos trials de simulación repetidos generados a partir de los mismos puntos paramétricos y familias de historia. Los conteos crudos no deben tratarse como sujetos experimentales independientes.

V33 aborda esto calculando contrastes angulares emparejados dentro de historia y un null por permutación de ángulos.

## Límite
V32 establece una propiedad de las dinámicas computacionales implementadas. No establece consciencia, experiencia subjetiva ni sentiencia.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V32 — Ensemble Context Geometry Evidence

## Status
**SUCCESS** — GitHub Actions run 36788862121.

## Method
V32 replaced the invalid V31 comparator with independent continuation ensembles.

For every receiver context:
- receiver state is the A/B midpoint;
- memory and pressure are synthetic and donor-independent;
- A and B reference signatures are means of five independent zero-input continuations using unrotated donor states;
- test continuations use independent noise seeds;
- identity is scored from Euclidean distance between the test temporal-state signature and the two ensemble reference signatures.

## Results

At radius 1.1, pooled identity accuracy across contexts:

| Angle | Mean identity | Context range |
|---:|---:|---:|
| 30° | **87.27%** | 21.63 pp |
| 60° | 64.36% | 32.42 pp |
| 90° | 46.46% | 24.00 pp |
| 120° | 18.44% | 33.33 pp |
| 150° | **9.24%** | 29.67 pp |

Mean signed affinity changes from **+0.343 at 30°** through approximately zero at 90° to **−0.504 at 150°**.

Across the tested context surface, directional response is preserved while its magnitude is modulated by contextual memory and pressure.

Examples:
- memory −0.8 / pressure 0.0: 30° = 99.13%, 150° = 0.42%;
- memory 0.8 / pressure 2.0: 30° = 86.08%, 150° = 21.21%;
- memory 0.0 / pressure 1.0: 30° = 81.83%, 150° = 7.25%.

## Interpretation
V32 supports the following bounded computational statement:

> A compact two-slot state geometry produces a reproducible directional response under donor-independent receiver contexts, while response strength varies with contextual memory and pressure.

Ensemble references and independent continuation noise remove the same-noise cancellation problem of V31.

The effect is not context-free: context changes magnitude and, in some regions, angular profile.

## Statistical caution
Pooled context cells contain many repeated simulation trials generated from the same fixed parameter points and history families. Raw cell counts should not be treated as equivalent to independent experimental subjects.

V33 addresses this by computing matched within-history angular contrasts and an angle-permutation null.

## Boundary
V32 establishes a property of implemented computational dynamics. It does not establish consciousness, subjective experience, or sentience.

</details>