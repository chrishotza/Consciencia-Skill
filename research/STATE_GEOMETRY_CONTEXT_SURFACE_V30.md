<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V30 — Superficie contextual independiente del donante

## Pregunta

¿Cómo cambia la respuesta direccional del state observada en V24–V27 al variar independientemente memory y pressure del receptor, sin depender de la identidad del donante?

## Diseño

- Seis puntos ciegos V12.
- Cuatro pares de historias.
- Seeds independientes 50–59.
- State del receptor fijado al midpoint A/B.
- Memory y pressure del receptor son valores sintéticos, fijos y predeclarados:
  - memory: -0.8, -0.4, 0, 0.4, 0.8
  - pressure: 0, 0.5, 1.0, 1.5, 2.0
- Radio de desviación del state donante: 1.1.
- Ángulos: 30°, 60°, 90°, 120°, 150°.
- Input futuro: exactamente cero.
- Noise: 0.01.

Cada contexto nuisance del receptor es independiente de las historias donantes. Las continuaciones de referencia locales A/B se generan dentro del mismo contexto nuisance.

El ángulo 180° se excluye porque, con el state del receptor fijado exactamente al midpoint A/B, una rotación de 180° mapea matemáticamente el donante A sobre B.

El experimento estudia la interacción contexto × geometría y evita variables nuisance ligadas al donante. No establece consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

# V30 — Donor-Independent Context Surface

## Question
How does the V24–V27 directional state response change as receiver memory and pressure are varied independently of donor identity?

## Design
- Six fixed V12 blind parameter points.
- Four history pairs.
- Independent seeds 50–59.
- Receiver state fixed to the A/B midpoint.
- Receiver memory and pressure are synthetic, fixed, predeclared values:
  - memory: -0.8, -0.4, 0, 0.4, 0.8
  - pressure: 0, 0.5, 1.0, 1.5, 2.0
- Donor state deviation radius: 1.1.
- Angles: 30°, 60°, 90°, 120°, 150°.
- Future input: exactly zero.
- Noise: 0.01.

Each receiver nuisance context is independent of the donor histories. Local A/B reference continuations are generated inside the same nuisance context.

The 180° angle is excluded because, with the receiver state fixed at the exact A/B midpoint, a 180° rotation mathematically maps donor A onto donor B.

The experiment targets the context × geometry interaction and avoids donor-linked nuisance variables. It does not establish consciousness or subjective experience.
