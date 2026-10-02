<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V25 — Réplica confirmatoria de la superficie polar del estado

## Propósito

V25 es el seguimiento confirmatorio de V24.

V24 mapeó una superficie radio × ángulo usando seeds 0–9. V25 conserva los seis puntos ciegos V12 y el análisis exacto de affinity/identidad, pero utiliza seeds disjuntas 10–19 y una grilla más fina predeclarada.

## Hipótesis

Si el efecto direccional del estado de V24 es reproducible, una réplica con seeds independientes debería recuperar:

1. baja discriminación de identidad cerca de radio cero;
2. mayor discriminación en radios no nulos;
3. máximo direccional cerca de la orientación original de la desviación;
4. inversión antipodal cerca de 180°;
5. ganancia radial no monótona en lugar de una relación basada solo en magnitud.

## Diseño

- Puntos paramétricos: p1–p6 exactamente como V24.
- Pares de historias: 4.
- Seeds independientes: 10–19.
- Input futuro: exactamente cero.
- Memory y pressure del receptor: midpoint A/B común.
- Radios: 0.50 a 1.30 en incrementos de 0.10.
- Ángulos: 0° a 350° en incrementos de 10°.
- Métrica primaria: accuracy de identidad usando la misma regla de affinity de continuación que V24.

## Disciplina de confirmación

Los puntos paramétricos y la regla de análisis no cambian respecto de V24. Las seeds aleatorias son disjuntas. La grilla más fina está fijada en el script antes de observar resultados V25.

V25 está pensado como réplica, no como nueva pasada de optimización. Cualquier zoom local o selección de parámetros posterior debe tratarse como experimento exploratorio separado.

## Límite de interpretación

Una réplica exitosa respaldaría que este modelo computacional contiene una representación interna reproducible, manipulable causalmente y sensible a la geometría.

No establecería consciencia, experiencia subjetiva ni sentiencia.

</details>

<a id="english"></a>

# V25 — Confirmatory State Polar Replication

## Purpose
V25 is the confirmatory follow-up to V24.

V24 mapped a radius × angle surface using seeds 0–9. V25 keeps the six fixed V12 blind parameter points and the exact affinity/identity analysis, but uses disjoint seeds 10–19 and a finer predeclared grid.

## Hypothesis
If the V24 directional state effect is reproducible, an independently seeded replication should recover:
1. low identity discrimination near zero radius,
2. increased discrimination at nonzero radius,
3. a directional maximum near the original state-deviation orientation,
4. an antipodal reversal near 180°,
5. non-monotonic radial gain rather than a simple magnitude-only relationship.

## Design
- Parameter points: p1–p6 exactly as V24.
- History pairs: 4.
- Independent seeds: 10–19.
- Future input: exactly zero.
- Receiver memory and pressure: common A/B midpoint.
- Radii: 0.50 to 1.30 in 0.10 increments.
- Angles: 0° to 350° in 10° increments.
- Primary metric: identity accuracy using the same continuation-affinity rule as V24.

## Confirmation discipline
The parameter points and analysis rule are unchanged from V24. The random seeds are disjoint. The finer grid is fixed in the script before observing V25 outcomes.

V25 is intended as replication, not as a new optimization pass. Any later local zoom or parameter selection should be treated as a separate exploratory experiment.

## Interpretation boundary
A successful replication would support the claim that this computational model contains a reproducible, causally manipulable, geometry-sensitive internal state representation.

It would not establish consciousness, subjective experience, or sentience.
