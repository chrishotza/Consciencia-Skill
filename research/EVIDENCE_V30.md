# V30 — Donor-Independent Context Surface Evidence

## Status
**SUCCESS** — GitHub Actions run `36787348410`.

## Question
Does the directional state response depend on receiver memory and pressure when those variables are independent of donor identity?

## Design
- 6 fixed V12 blind parameter points.
- 4 history pairs.
- independent seeds 50–59.
- receiver state fixed to the A/B midpoint.
- synthetic receiver memory: -0.8, -0.4, 0, 0.4, 0.8.
- synthetic receiver pressure: 0, 0.5, 1.0, 1.5, 2.0.
- state-deviation radius fixed at 1.1.
- angles: 30°, 60°, 90°, 120°, 150°.
- future input exactly zero.
- noise_std = 0.01.
- local A/B reference continuations are generated within each exact receiver context.

## Main result
The geometry remains highly directional across the context surface, but the strength and angular profile depend on receiver context.

Examples:
- At memory = -0.8, pressure = 0, identity accuracy ranges from **92.92% at 30°** to **3.75% at 150°**.
- At memory = -0.4, pressure = 2.0, the corresponding range is **88.75% → 7.29%**.
- At memory = 0.8, pressure = 0, it is **81.04% → 1.88%**.
- At memory = 0.8, pressure = 2.0, it is **91.67% → 8.13%**.

The context interaction is large. Across the 25 context cells, the pooled identity ranges are:

| Angle | Min accuracy | Max accuracy | Range |
|---:|---:|---:|---:|
| 30° | 69.38% | 92.92% | 23.54 pp |
| 60° | 65.00% | 86.46% | 21.46 pp |
| 90° | 38.33% | 70.21% | 31.88 pp |
| 120° | 13.13% | 42.08% | 28.96 pp |
| 150° | 1.88% | 27.29% | 25.42 pp |

The largest signed-affinity context range occurs at 30° (0.557), followed closely by 150° (0.538).

## Mechanistic interpretation
V30 supports a constrained statement:

> The donor-state geometry is not an unconditional context-free code. Its downstream identity expression is jointly determined by the transplanted state geometry and the receiver's auxiliary memory/pressure context.

Because the synthetic contexts are donor-independent, the context effect cannot be explained simply by copying a donor-specific memory or pressure trace into the receiver.

## Boundary
V30 does not establish consciousness, subjective experience, or sentience. It establishes a reproducible context × state-geometry interaction in the implemented dynamics.

## Next
V31 will convert this surface into paired causal effect estimates, using the same state geometry while varying one context variable at a time. The primary endpoint will be within-seed change in signed affinity, separating memory main effects, pressure main effects, and their interaction.


<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V30 — Evidencia de superficie de contexto independiente del donante

## Estado
**SUCCESS** — GitHub Actions run 36787348410.

## Pregunta
¿La respuesta direccional del estado depende de memory y pressure del receptor cuando esas variables son independientes de la identidad del donante?

## Diseño
- 6 puntos ciegos V12.
- 4 pares de historias.
- seeds independientes 50–59.
- state del receptor fijado en midpoint A/B.
- memory sintética del receptor: -0.8, -0.4, 0, 0.4, 0.8.
- pressure sintética: 0, 0.5, 1.0, 1.5, 2.0.
- radio de desviación de state fijado en 1.1.
- ángulos: 30°, 60°, 90°, 120°, 150°.
- input futuro exactamente cero.
- noise_std = 0.01.
- referencias locales A/B generadas dentro de cada contexto exacto del receptor.

## Resultado principal
La geometría sigue siendo fuertemente direccional en toda la superficie de contextos, pero su intensidad y perfil angular dependen del contexto receptor.

Ejemplos:
- memory = -0.8, pressure = 0: accuracy **92.92% a 30°** a **3.75% a 150°**.
- memory = -0.4, pressure = 2.0: **88.75% → 7.29%**.
- memory = 0.8, pressure = 0: **81.04% → 1.88%**.
- memory = 0.8, pressure = 2.0: **91.67% → 8.13%**.

La interacción con contexto es grande:

| Angle | Min accuracy | Max accuracy | Range |
|---:|---:|---:|---:|
| 30° | 69.38% | 92.92% | 23.54 pp |
| 60° | 65.00% | 86.46% | 21.46 pp |
| 90° | 38.33% | 70.21% | 31.88 pp |
| 120° | 13.13% | 42.08% | 28.96 pp |
| 150° | 1.88% | 27.29% | 25.42 pp |

El mayor rango de affinity firmado ocurre a 30° (0.557), seguido de cerca por 150° (0.538).

## Interpretación mecanística
V30 permite una afirmación acotada:

> La geometría del estado donante no es un código incondicional libre de contexto. Su expresión posterior de identidad está determinada conjuntamente por la geometría trasplantada del estado y el contexto auxiliar memory/pressure del receptor.

Como los contextos sintéticos son independientes del donante, el efecto de contexto no puede explicarse simplemente copiando una traza de memory o pressure específica del donante en el receptor.

## Límite
V30 no establece consciencia, experiencia subjetiva ni sentiencia. Establece una interacción reproducible contexto × geometría de estado en las dinámicas implementadas.

## Próximo
V31 convertirá esta superficie en estimaciones causales emparejadas, usando la misma geometría de estado mientras se modifica una variable de contexto a la vez. El endpoint primario será el cambio dentro de seed en affinity firmado, separando efectos principales de memory, pressure e interacción.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V30 — Donor-Independent Context Surface Evidence

## Status
**SUCCESS** — GitHub Actions run 36787348410.

## Question
Does directional state response depend on receiver memory and pressure when those variables are independent of donor identity?

## Design
- 6 fixed V12 blind parameter points.
- 4 history pairs.
- independent seeds 50–59.
- receiver state fixed to A/B midpoint.
- synthetic receiver memory: -0.8, -0.4, 0, 0.4, 0.8.
- synthetic receiver pressure: 0, 0.5, 1.0, 1.5, 2.0.
- state-deviation radius fixed at 1.1.
- angles: 30°, 60°, 90°, 120°, 150°.
- future input exactly zero.
- noise_std = 0.01.
- local A/B references generated within each exact receiver context.

## Main result
Geometry remains highly directional across the context surface, but strength and angular profile depend on receiver context.

Examples:
- memory = -0.8, pressure = 0: **92.92% at 30°** to **3.75% at 150°**.
- memory = -0.4, pressure = 2.0: **88.75% → 7.29%**.
- memory = 0.8, pressure = 0: **81.04% → 1.88%**.
- memory = 0.8, pressure = 2.0: **91.67% → 8.13%**.

Across 25 context cells:

| Angle | Min accuracy | Max accuracy | Range |
|---:|---:|---:|---:|
| 30° | 69.38% | 92.92% | 23.54 pp |
| 60° | 65.00% | 86.46% | 21.46 pp |
| 90° | 38.33% | 70.21% | 31.88 pp |
| 120° | 13.13% | 42.08% | 28.96 pp |
| 150° | 1.88% | 27.29% | 25.42 pp |

Largest signed-affinity context range occurs at 30° (0.557), followed by 150° (0.538).

## Mechanistic interpretation
V30 supports a constrained statement:

> Donor-state geometry is not an unconditional context-free code. Its downstream identity expression is jointly determined by transplanted state geometry and receiver memory/pressure context.

Because synthetic contexts are donor-independent, context effects cannot simply be explained by copying donor-specific memory or pressure into the receiver.

## Boundary
V30 does not establish consciousness, subjective experience, or sentience. It establishes a reproducible context × state-geometry interaction in the implemented dynamics.

## Next
V31 will convert this surface into paired causal effect estimates, holding the same state geometry while varying one context variable at a time. The primary endpoint will be within-seed signed-affinity change, separating memory main effects, pressure main effects, and interaction.

</details>