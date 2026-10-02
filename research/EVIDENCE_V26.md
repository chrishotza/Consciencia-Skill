# V26 — Temporal Persistence Evidence

## Status
**SUCCESS** — GitHub Actions run `36784768598`.

## Question
Does the directional state code observed in V24/V25 remain causally expressed after transplantation as the common zero-input continuation unfolds?

## Design
- 6 fixed blind V12 parameter points.
- 4 history pairs.
- Independent seeds 10–19.
- Future input exactly zero.
- Receiver memory and pressure fixed to the common A/B midpoint.
- State geometry conditions:
  - radius 0.0: null control,
  - radius 0.5 at 0°, 90°, 180°,
  - radius 1.1 at 0°, 90°, 180°.
- Eight consecutive windows of 15 steps.
- Primary metric: identity accuracy in each window, using the same continuation-affinity rule as V24/V25.

## Result

### Null control
Radius 0.0 remains exactly **50.0%** in all eight windows for all tested angles.

### Radius 0.5
At 0°:
- first window: **80.0%**
- eighth window: **64.17%**
- mean across windows: **66.90%**

At 180°:
- first window: **20.0%**
- eighth window: **35.83%**
- mean: **33.10%**

At 90°:
- first window: **60.63%**
- eighth window: **51.88%**
- mean: **53.20%**

### Radius 1.1
At 0°:
- first window: **94.79%**
- eighth window: **85.42%**
- mean across windows: **88.02%**

At 180°:
- first window: **5.21%**
- eighth window: **14.58%**
- mean: **11.98%**

At 90°:
- first window: **38.96%**
- eighth window: **42.29%**
- mean: **41.35%**

The 0° and 180° conditions retain a strong antipodal separation throughout the entire 120-step zero-input continuation.

## Interpretation
V26 supports a temporal extension of the V24/V25 result:

> The compact two-slot state geometry remains causally expressed across successive zero-input continuation windows rather than functioning only as an instantaneous readout.

At the established radius 1.1, the directional code weakens modestly from the first to the last window at 0°, but remains far from the 50% null baseline. The antipodal 180° condition remains correspondingly biased toward the opposite identity.

The 90° condition is substantially closer to chance, consistent with the angular structure already observed in V23–V25.

## Limits
This is a computational dynamical result for the implemented model. It does not establish consciousness, subjective experience, or sentience.

## Next
V27 should test robustness to controlled increases in dynamical noise while keeping the same state geometry, parameter points, and zero-input continuation. This separates a reproducible geometric code from a phenomenon that exists only at the baseline noise level.


<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V26 — Evidencia de persistencia temporal

## Estado
**SUCCESS** — GitHub Actions run 36784768598.

## Pregunta
¿El código direccional de estado observado en V24/V25 sigue expresándose causalmente después del trasplante mientras se desarrolla la continuación común sin input?

## Diseño
- 6 puntos ciegos V12 fijos.
- 4 pares de historias.
- Seeds independientes 10–19.
- Input futuro exactamente cero.
- Memory y pressure del receptor fijados al midpoint común A/B.
- Condiciones geométricas:
  - radius 0.0: control nulo;
  - radius 0.5 a 0°, 90°, 180°;
  - radius 1.1 a 0°, 90°, 180°.
- Ocho ventanas consecutivas de 15 pasos.
- Métrica primaria: accuracy de identidad en cada ventana usando la misma regla de affinity que V24/V25.

## Resultado

### Control nulo
Radius 0.0 permanece exactamente en **50.0%** en las ocho ventanas para todos los ángulos.

### Radius 0.5

A 0°:
- primera ventana: **80.0%**
- octava: **64.17%**
- media: **66.90%**

A 180°:
- primera: **20.0%**
- octava: **35.83%**
- media: **33.10%**

A 90°:
- primera: **60.63%**
- octava: **51.88%**
- media: **53.20%**

### Radius 1.1

A 0°:
- primera ventana: **94.79%**
- octava: **85.42%**
- media: **88.02%**

A 180°:
- primera: **5.21%**
- octava: **14.58%**
- media: **11.98%**

A 90°:
- primera: **38.96%**
- octava: **42.29%**
- media: **41.35%**

Las condiciones 0° y 180° conservan una separación antipodal fuerte durante toda la continuación de 120 pasos sin input.

## Interpretación

V26 extiende temporalmente V24/V25:

> La geometría compacta de dos slots del estado sigue expresándose causalmente en ventanas sucesivas de continuación sin input, en lugar de funcionar solo como readout instantáneo.

En radius 1.1, la señal 0° se debilita modestamente entre la primera y última ventana, pero permanece lejos del baseline nulo de 50%. La condición antipodal 180° conserva el sesgo correspondiente hacia la identidad opuesta.

La condición 90° está mucho más cerca del azar, consistente con la estructura angular observada en V23–V25.

## Límites
Es un resultado dinámico computacional del modelo implementado. No establece consciencia, experiencia subjetiva ni sentiencia.

## Próximo
V27 debe probar robustez ante aumentos controlados del ruido dinámico conservando la misma geometría de estado, puntos paramétricos y continuación sin input.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V26 — Temporal Persistence Evidence

## Status
**SUCCESS** — GitHub Actions run 36784768598.

## Question
Does the directional state code observed in V24/V25 remain causally expressed after transplantation as the common zero-input continuation unfolds?

## Design
- 6 fixed blind V12 parameter points.
- 4 history pairs.
- Independent seeds 10–19.
- Future input exactly zero.
- Receiver memory and pressure fixed to common A/B midpoint.
- Geometry conditions: radius 0.0 null, radius 0.5 at 0°/90°/180°, radius 1.1 at 0°/90°/180°.
- Eight consecutive windows of 15 steps.
- Primary metric: identity accuracy in each window using the V24/V25 continuation-affinity rule.

## Result

### Null control
Radius 0.0 remains exactly **50.0%** in all eight windows for all angles.

### Radius 0.5
At 0°: first window **80.0%**, eighth **64.17%**, mean **66.90%**.
At 180°: first **20.0%**, eighth **35.83%**, mean **33.10%**.
At 90°: first **60.63%**, eighth **51.88%**, mean **53.20%**.

### Radius 1.1
At 0°: first **94.79%**, eighth **85.42%**, mean **88.02%**.
At 180°: first **5.21%**, eighth **14.58%**, mean **11.98%**.
At 90°: first **38.96%**, eighth **42.29%**, mean **41.35%**.

The 0° and 180° conditions retain strong antipodal separation throughout the full 120-step zero-input continuation.

## Interpretation

V26 temporally extends the V24/V25 result:

> Compact two-slot state geometry remains causally expressed across successive zero-input continuation windows rather than functioning only as an instantaneous readout.

At established radius 1.1, directional code weakens modestly from first to last window at 0° but remains far from the 50% null baseline. Antipodal 180° remains correspondingly biased toward opposite identity.

The 90° condition is closer to chance, consistent with V23–V25 angular structure.

## Limits

This is a computational dynamical result for the implemented model. It does not establish consciousness, subjective experience, or sentience.

## Next

V27 should test robustness to controlled increases in dynamical noise while keeping the same state geometry, parameter points, and zero-input continuation.

</details>