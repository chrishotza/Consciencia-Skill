<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V32 — Geometría contextual de referencia ensemble

V32 es el reemplazo robusto de V31.

El state del receptor permanece en el midpoint común A/B. Memory y pressure del receptor son valores sintéticos independientes del donante. El state donante se trasplanta con radio 1.1 y ángulos 30°, 60°, 90°, 120° y 150°.

Para cada contexto, las firmas A/B de referencia son las medias de cinco simulaciones independientes de ruido de continuación utilizando states donantes sin rotar (0°).

Las continuaciones de prueba utilizan seeds de ruido independientes y se puntúan frente a las dos firmas ensemble mediante distancia temporal euclídea sobre la trayectoria del estado muestreada cada cinco pasos.

Esto evita la cancelación con mismo ruido y evita comparar una prueba rotada directamente contra una referencia generada con la misma rotación.

El objetivo es caracterizar robustamente la interacción contexto × geometría. No establece consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

# V32 — Ensemble Reference Context Geometry

V32 is the robust replacement for V31.

The receiver state remains the common A/B midpoint. Receiver memory and pressure are donor-independent synthetic values. The donor state is transplanted at radius 1.1 and test angles 30°, 60°, 90°, 120°, 150°.

For each context, the A/B reference signatures are the means of five independent continuation-noise simulations using the unrotated (0°) donor states.

Test continuations use independent noise seeds and are scored against the two ensemble reference signatures using Euclidean temporal distance over the state trajectory sampled every five steps.

This avoids same-noise cancellation and avoids comparing a rotated test directly against a reference generated with the same rotation.

The objective is to characterize context × geometry interaction robustly. It does not establish consciousness or subjective experience.
