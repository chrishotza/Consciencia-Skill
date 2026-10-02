<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V16 — Cuello de botella de estado mínimo

## Pregunta

V15 mostró que borrar selectivamente el estado recurrente causa una pérdida fuerte de identidad histórica en los regímenes critical. V16 pregunta cuánto de ese estado es realmente necesario.

## Cuello de botella estructural

En el límite de historia, el contexto completo del donante contiene dos slots recurrentes: state_prev y state.

Comparamos:

- full: ambos slots conservados;
- current_only: se conserva current state y previous state se reemplaza por el valor común A/B;
- previous_only: se conserva previous state y current state se reemplaza por el valor común;
- state_zero: ambos slots se reemplazan por el valor común.

Las otras variables de contexto permanecen específicas del donante.

## Cuello de botella de precisión

Ambos slots se conservan, pero sus valores se cuantizan uniformemente sobre el rango natural tanh [-1, 1] a 1, 2, 3, 4, 6 y 8 bits.

El input de continuación es exactamente cero y el noise seed se mantiene emparejado entre intervenciones.

## Readout

La identidad se clasifica a partir de affinity de trayectoria respecto de las referencias de continuación A/B intactas durante los primeros 60 pasos futuros. El MAE de predicción se mide contra la trayectoria intacta del donante.

## Interpretación

Si current_only conserva la mayor parte de la señal de identidad mientras previous_only no, el estado recurrente actual sería el portador temporal dominante en la frontera. Si la cuantización de pocos bits conserva identidad, el mecanismo tiene una representación de estado efectiva compacta.

El experimento caracteriza las dinámicas computacionales implementadas. No establece experiencia subjetiva ni consciencia.

</details>

<a id="english"></a>

# V16 — Minimal-State Bottleneck

## Question

V15 showed that selectively erasing the recurrent state causes a strong loss of historical identity in the critical regimes. V16 asks how much of that state is actually necessary.

## Structural bottleneck

At the history boundary, the full donor context contains two recurrent state slots: `state_prev` and `state`.

We compare:
- `full`: both state slots retained.
- `current_only`: current state retained, previous state replaced by the A/B common value.
- `previous_only`: previous state retained, current state replaced by the common value.
- `state_zero`: both state slots replaced by the common value.

The other context variables remain donor-specific.

## Precision bottleneck

Both state slots are retained, but their values are uniformly quantized over the natural tanh range [-1, 1] at 1, 2, 3, 4, 6, and 8 bits.

The continuation input is exactly zero and the noise seed is matched across interventions.

## Readout

Identity is classified from trajectory affinity to the intact A/B continuation references over the first 60 future steps. Prediction MAE is measured against the intact donor trajectory.

## Interpretation

If `current_only` retains most of the identity signal while `previous_only` does not, the current recurrent state is the dominant temporal carrier at the boundary. If low-bit quantization retains identity, the mechanism has a compact effective state representation.

This experiment characterizes the implemented computational dynamics. It does not establish subjective experience or consciousness.