# V15 — Evidence: State Lesion / Causal Necessity

## GitHub validation

- Workflow: state-lesion-v15
- Run: 36776941623
- Result: SUCCESS
- Artifact: 11125209290
- Protocol: 4 history pairs × 20 seeds per regime × 8 lesion doses × 3 lesion targets.
- Future input after the history boundary: exactly zero.
- Noise seeds were matched across all interventions.

## Main result

The recurrent state is the only tested context component whose complete lesion repeatedly drives identity classification close to chance in the critical regimes.

| Regime | Intact | State lesion | State loss | Memory lesion | Memory loss | Pressure lesion | Pressure loss |
|---|---:|---:|---:|---:|---:|---:|---:|
| critical | 1.000 | 0.494 | 0.506 | 0.881 | 0.119 | 0.950 | 0.050 |
| holdout_critical | 1.000 | 0.506 | 0.494 | 0.844 | 0.156 | 0.950 | 0.050 |
| persistence | 1.000 | 0.556 | 0.444 | 0.825 | 0.175 | 0.931 | 0.069 |
| baseline | 1.000 | 1.000 | 0.000 | 0.844 | 0.156 | 1.000 | 0.000 |

Identity is donor classification from trajectory affinity. A value near 0.5 is approximately chance for the binary A/B task.

## Dose-response

The state lesion produces a strong monotone association between lesion dose and identity loss in the critical regimes:

- critical state lesion: Spearman rho = -0.994
- holdout_critical state lesion: Spearman rho = -1.000
- persistence state lesion: Spearman rho = -0.929

For comparison, the corresponding rho values are weaker for pressure in critical (-0.916) and persistence (-0.754), while memory also shows dose sensitivity but does not reduce identity as strongly at full lesion.

The response is not expected to be perfectly monotone at every dose because the underlying system is stochastic and nonlinear.

## What this establishes

Within this computational model, the result is stronger than a correlational readout: selectively moving the recurrent state toward a common state causes a substantially larger loss of historical identity than the matched memory/pressure interventions, and this effect replicates in the holdout-critical regime.

The baseline control is important: the same state lesion does not destroy identity there. This indicates that the effect depends on the dynamical regime rather than being a trivial consequence of the intervention itself.

## What it does not establish

This is evidence for causal state dependence of a persistent, history-dependent dynamical regime. It is not evidence of subjective experience, sentience, or consciousness in the philosophical or biological sense.

## Relation to prior evidence

V14 showed that the recurrent state contributes predictive information under matched feature dimensionality. V15 adds a causal necessity-style perturbation: when the recurrent state is selectively erased, historical identity collapses in the resonant/critical regimes.

Together, V14 + V15 support the narrower computational claim that the recurrent state is an important causal carrier of historical information in the implemented dynamics.

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V15 — Evidencia: Lesión del estado / necesidad causal

## Validación GitHub

- Workflow: state-lesion-v15
- Run: 36776941623
- Result: SUCCESS
- Artifact: 11125209290
- Protocolo: 4 pares de historias × 20 seeds por régimen × 8 dosis de lesión × 3 targets de lesión.
- Input futuro después del límite de historia: exactamente cero.
- Seeds de ruido emparejadas en todas las intervenciones.

## Resultado principal

El estado recurrente es el único componente de contexto probado cuya lesión completa lleva repetidamente la clasificación de identidad cerca del azar en los regímenes critical.

| Régimen | Intacto | Lesión state | Pérdida state | Lesión memory | Pérdida memory | Lesión pressure | Pérdida pressure |
|---|---:|---:|---:|---:|---:|---:|---:|
| critical | 1.000 | 0.494 | 0.506 | 0.881 | 0.119 | 0.950 | 0.050 |
| holdout_critical | 1.000 | 0.506 | 0.494 | 0.844 | 0.156 | 0.950 | 0.050 |
| persistence | 1.000 | 0.556 | 0.444 | 0.825 | 0.175 | 0.931 | 0.069 |
| baseline | 1.000 | 1.000 | 0.000 | 0.844 | 0.156 | 1.000 | 0.000 |

Identity es clasificación donor desde affinity de trayectoria. Un valor cercano a 0.5 es aproximadamente azar en la tarea binaria A/B.

## Dose-response

La lesión del estado muestra una asociación monótona fuerte entre dosis y pérdida de identidad:

- critical state lesion: Spearman rho = -0.994
- holdout_critical state lesion: Spearman rho = -1.000
- persistence state lesion: Spearman rho = -0.929

En comparación, los rho correspondientes para pressure son más débiles en critical (-0.916) y persistence (-0.754). Memory también muestra sensibilidad a la dosis pero no reduce identidad con la misma fuerza bajo lesión completa.

La respuesta no necesita ser perfectamente monótona a cada dosis porque el sistema subyacente es estocástico y no lineal.

## Qué establece

Dentro de este modelo computacional, el resultado es más fuerte que un readout correlacional: mover selectivamente el estado recurrente hacia un estado común causa una pérdida sustancialmente mayor de identidad histórica que las intervenciones emparejadas de memory/pressure, y el efecto se replica en el régimen holdout-critical.

El baseline es importante: la misma lesión de estado no destruye allí la identidad. Esto indica que el efecto depende del régimen dinámico y no es una consecuencia trivial de la intervención.

## Qué no establece

Es evidencia de dependencia causal del estado en un régimen dinámico persistente y dependiente de historia. No es evidencia de experiencia subjetiva, sentiencia ni consciencia en sentido filosófico o biológico.

## Relación con evidencia previa

V14 mostró que el estado recurrente aporta información predictiva bajo dimensionalidad emparejada. V15 añade una perturbación de necesidad causal: al borrar selectivamente el estado recurrente, la identidad histórica colapsa en los regímenes resonantes/críticos.

Juntos, V14 + V15 respaldan la afirmación computacional más estrecha de que el estado recurrente es un portador causal importante de información histórica en la dinámica implementada.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V15 — Evidence: State Lesion / Causal Necessity

## GitHub validation

- Workflow: state-lesion-v15
- Run: 36776941623
- Result: SUCCESS
- Artifact: 11125209290
- Protocol: 4 history pairs × 20 seeds per regime × 8 lesion doses × 3 lesion targets.
- Future input after the history boundary: exactly zero.
- Noise seeds were matched across all interventions.

## Main result

Recurrent state is the only tested context component whose complete lesion repeatedly drives identity classification close to chance in the critical regimes.

| Regime | Intact | State lesion | State loss | Memory lesion | Memory loss | Pressure lesion | Pressure loss |
|---|---:|---:|---:|---:|---:|---:|---:|
| critical | 1.000 | 0.494 | 0.506 | 0.881 | 0.119 | 0.950 | 0.050 |
| holdout_critical | 1.000 | 0.506 | 0.494 | 0.844 | 0.156 | 0.950 | 0.050 |
| persistence | 1.000 | 0.556 | 0.444 | 0.825 | 0.175 | 0.931 | 0.069 |
| baseline | 1.000 | 1.000 | 0.000 | 0.844 | 0.156 | 1.000 | 0.000 |

Identity is donor classification from trajectory affinity. A value near 0.5 is approximately chance for the binary A/B task.

## Dose-response

State lesion produces a strong monotone association between lesion dose and identity loss in critical regimes:

- critical state lesion: Spearman rho = -0.994;
- holdout_critical state lesion: Spearman rho = -1.000;
- persistence state lesion: Spearman rho = -0.929.

For comparison, corresponding pressure rho values are weaker in critical (-0.916) and persistence (-0.754). Memory also shows dose sensitivity but does not reduce identity as strongly at full lesion.

The response is not expected to be perfectly monotone at every dose because the underlying system is stochastic and nonlinear.

## What this establishes

Within this computational model, the result is stronger than a correlational readout: selectively moving recurrent state toward a common state causes a substantially larger loss of historical identity than matched memory/pressure interventions, and the effect replicates in the holdout-critical regime.

The baseline control matters: the same state lesion does not destroy identity there, indicating that the effect depends on dynamic regime rather than being a trivial consequence of the intervention.

## What it does not establish

This is evidence for causal state dependence of a persistent, history-dependent dynamical regime. It is not evidence of subjective experience, sentience, or consciousness.

## Relation to prior evidence

V14 showed recurrent state contributes predictive information under matched feature dimensionality. V15 adds causal-necessity-style perturbation: when recurrent state is selectively erased, historical identity collapses in resonant/critical regimes.

Together, V14 + V15 support the narrower computational claim that recurrent state is an important causal carrier of historical information in the implemented dynamics.

</details>