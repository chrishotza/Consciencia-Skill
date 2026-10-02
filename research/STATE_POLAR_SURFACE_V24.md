<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V24 — Superficie polar del estado

## Pregunta

V23 estableció una dependencia angular fuerte a norma fija de desviación del estado. V24 separa dos factores: **radius** (distancia del estado respecto del contexto común) y **angle** (orientación).

## Protocolo

Seis puntos ciegos V12, cuatro pares de historias, diez seeds de ruido emparejados por par, input futuro exactamente cero y memory/pressure comunes del receptor.

La desviación de state de dos slots del donante se escala por radios 0, .25, .5, .75, 1 y 1.25 y se rota mediante 12 ángulos separados 30°.

Radius y angle se varían independientemente. La identidad se clasifica por affinity frente a referencias de continuación A/B intactas durante los primeros 60 pasos futuros.

## Interpretación

La superficie radius × angle permite distinguir:

- efectos de magnitud del estado;
- efectos de orientación del estado;
- interacciones entre magnitud y orientación.

Una región localizada de alta identidad en la orientación del donante y alta identidad opuesta cerca de 180° proporcionaría una superficie de respuesta bidimensional en lugar de un fenómeno de un único parámetro.

Es una caracterización computacional de la geometría del estado recurrente y no establece consciencia subjetiva.

</details>

<a id="english"></a>

# V24 — State Polar Surface

## Question

V23 established strong angular dependence at fixed state-deviation norm. V24 separates two factors: **radius** (how far the state is from the common context) and **angle** (orientation).

## Protocol

Six V12 blind parameter points, four history pairs, ten matched-noise seeds per pair, exact-zero future input, and common receiver memory/pressure.

The donor two-slot state deviation is scaled by radius 0, .25, .5, .75, 1, and 1.25 and rotated through 12 angles at 30-degree spacing.

Radius and angle are varied independently. Identity is classified by affinity to intact A/B continuation references over the first 60 future steps.

## Interpretation

The resulting radius × angle surface distinguishes:
- effects of state magnitude;
- effects of state orientation;
- interactions between magnitude and orientation.

A localized region of high identity at the donor orientation and high opposite identity near 180 degrees would provide a two-dimensional response surface rather than a single-parameter phenomenon.

This is a computational characterization of the recurrent state geometry and does not establish subjective consciousness.