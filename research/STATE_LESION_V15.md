<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V15 — Lesión del estado / necesidad causal

## Pregunta

V14 mostró que el estado recurrente agrega información predictiva en los regímenes critical, holdout-critical y persistence bajo dimensionalidad de features emparejada. V15 formula la pregunta causal más fuerte:

> Cuando existe identidad histórica, ¿borrar selectivamente el estado recurrente degrada la identidad más que borrar memory o pressure explícitos?

## Diseño experimental

Se prueban cuatro regímenes: critical, holdout_critical, persistence y baseline.

Cada régimen utiliza cuatro protocolos de pares de historias y 20 seeds de ruido emparejados por protocolo. El input de continuación es exactamente cero.

En la frontera de historia, A y B generan contextos donantes distintos. Su midpoint aritmético es el contexto común.

Para cada donante, un componente de contexto se lesiona selectivamente hacia el contexto común con dosis 0, .05, .10, .20, .40, .60, .80 y 1.0.

- Lesión state: ambos slots recurrentes (state_prev y state) se interpolan hacia el state común.
- Lesión memory: solo memory explícita se interpola.
- Lesión pressure: solo pressure se interpola.

Todos los demás componentes permanecen específicos del donante y se usa el mismo seed de continuación en cada intervención.

## Readouts

La identidad se mide mediante affinity respecto de las trayectorias de referencia A y B intactas durante los primeros 60 pasos futuros. La accuracy de identidad es la fracción clasificada como el donante correcto.

El MAE de predicción mide la divergencia respecto de la continuación intacta del donante en la misma ventana.

## Regla de interpretación

Una respuesta dosis-efecto específica del state, replicada, mayor que los controles memory/pressure y presente en el régimen holdout, respaldaría que el estado recurrente es un portador causalmente importante de información histórica en este modelo.

Es un resultado dinámico computacional. No establece consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

# V15 — State Lesion / Causal Necessity

## Question

V14 showed that the recurrent state adds predictive information in the critical, holdout-critical, and persistence regimes under matched feature dimensionality. V15 asks the stronger causal question:

> When historical identity is present, does selectively erasing the recurrent state degrade identity more strongly than erasing explicit memory or pressure?

## Experimental design

Four regimes are tested: critical, holdout_critical, persistence, and baseline.

Each regime uses four history-pair protocols and 20 matched-noise seeds per protocol. The continuation input is exactly zero.

At the history boundary, A and B generate distinct donor contexts. Their arithmetic midpoint is the common context.

For each donor, one context component is selectively lesioned toward the common context at doses 0, .05, .10, .20, .40, .60, .80, and 1.0.

- State lesion: both recurrent state slots (state_prev and state) are interpolated toward the common state.
- Memory lesion: only explicit memory is interpolated.
- Pressure lesion: only pressure is interpolated.

All other components remain donor-specific, and the same continuation seed is used for every intervention.

## Readouts

Identity is measured by affinity to the intact A and B reference trajectories over the first 60 future steps. Identity accuracy is the fraction classified as the correct donor.

Prediction MAE measures divergence from the intact donor continuation over the same window.

## Interpretation rule

A replicated state-specific dose-response, larger than memory and pressure controls and present in the holdout regime, would support the claim that the recurrent state is a causally important carrier of historical information in this model.

This is a computational dynamical result. It does not establish consciousness or subjective experience.