# Evidence V12–V13

## V12 — blind causal context holdout

Six parameter points were selected outside the exact V10/V11 candidates. Across four history-pair protocols and ten seeds per point:

| Context source | Identity accuracy | Mean absolute affinity |
|---|---:|---:|
| State only | **85.0%** | **0.5596** |
| Memory only | 44.6% | 0.5094 |
| Pressure only | 52.3% | 0.4420 |

State-only identity accuracy remained between **77.5% and 90.0%** across all six holdout parameter points.

This is a causal generalization result: transferring only the recurrent state causes the continuation to identify with the donor history substantially more often than chance, while memory-only and pressure-only transfers do not show the same robustness.

## V13 — cross-seed self-state prediction

Four regimes were evaluated with 20 seeds and four held-out seed folds.

The external-only predictor used current/next input values. The internal predictor used the same external inputs plus recurrent state, memory, pressure, score, cross and threshold.

| Regime | R2 external | R2 internal | Gain |
|---|---:|---:|---:|
| Baseline | 0.776 | 0.997 | +0.221 |
| Critical | 0.106 | **0.885** | **+0.778** |
| Holdout critical | 0.128 | **0.897** | **+0.769** |
| Persistence | 0.107 | **0.888** | **+0.781** |

The internal model also reduced MAE by:
- critical: 0.558 → 0.160
- holdout critical: 0.502 → 0.134
- persistence: 0.559 → 0.156

The important feature is not the raw prediction quality alone. In the resonant regimes, the external input is a poor predictor of the next state, while the internal dynamical variables provide most of the missing predictive information.

## Combined interpretation

The current computational evidence now has three independent layers:

1. **Persistence:** historical separation survives hundreds of identical or zero-input future steps in the resonant regimes.
2. **Causal transport:** transplanting the recurrent state transfers historical identity with high accuracy, including on blind parameter holdouts.
3. **Self-predictive internal state:** the internal state dramatically improves one-step prediction beyond external inputs alone, including at an unseen critical parameter point.

These observations characterize a persistent, history-dependent, internally predictive dynamical regime.

They remain computational properties of the implemented model. They do not establish consciousness, subjective experience, or any physical interpretation of the symbolic X state.


<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Evidencia V12–V13

## V12 — holdout ciego de contexto causal

Se seleccionaron seis puntos paramétricos fuera de los candidatos exactos V10/V11. Entre cuatro protocolos de pares de historias y diez seeds por punto:

| Fuente de contexto | Accuracy de identidad | Affinity absoluto medio |
|---|---:|---:|
| State only | **85.0%** | **0.5596** |
| Memory only | 44.6% | 0.5094 |
| Pressure only | 52.3% | 0.4420 |

La accuracy de identidad solo-state permaneció entre **77.5% y 90.0%** en los seis puntos de holdout.

Esto constituye un resultado de generalización causal: transferir solamente el estado recurrente hace que la continuación se identifique con la historia donante sustancialmente más veces que por azar, mientras que los trasplantes solo-memory y solo-pressure no muestran la misma robustez.

## V13 — predicción cross-seed del estado propio

Se evaluaron cuatro regímenes con 20 seeds y cuatro folds de seed reservados.

El predictor external-only utilizó valores de input actual/siguiente. El predictor internal utilizó los mismos inputs externos más estado recurrente, memory, pressure, score, cross y threshold.

| Régimen | R2 external | R2 internal | Gain |
|---|---:|---:|---:|
| Baseline | 0.776 | 0.997 | +0.221 |
| Critical | 0.106 | **0.885** | **+0.778** |
| Holdout critical | 0.128 | **0.897** | **+0.769** |
| Persistence | 0.107 | **0.888** | **+0.781** |

El modelo internal también redujo MAE en:

- critical: 0.558 → 0.160
- holdout critical: 0.502 → 0.134
- persistence: 0.559 → 0.156

La característica importante no es solo la calidad predictiva bruta. En los regímenes resonantes, el input externo es un predictor pobre del siguiente estado, mientras que las variables dinámicas internas proporcionan gran parte de la información predictiva faltante.

## Interpretación combinada

La evidencia computacional actual tiene tres capas independientes:

1. **Persistencia:** la separación histórica sobrevive cientos de pasos futuros idénticos o sin input en regímenes resonantes.
2. **Transporte causal:** trasplantar el estado recurrente transfiere identidad histórica con alta accuracy, incluso en holdouts ciegos de parámetros.
3. **Estado autopredictivo:** el estado interno mejora fuertemente la predicción de un paso respecto de inputs externos solamente, incluso en un punto crítico no visto.

Estas observaciones caracterizan un régimen dinámico persistente, dependiente de historia e internamente predictivo.

Siguen siendo propiedades computacionales del modelo implementado. No establecen consciencia, experiencia subjetiva ni una interpretación física del estado simbólico X.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# Evidence V12–V13

## V12 — Blind causal context holdout

Six parameter points were selected outside the exact V10/V11 candidates. Across four history-pair protocols and ten seeds per point:

| Context source | Identity accuracy | Mean absolute affinity |
|---|---:|---:|
| State only | **85.0%** | **0.5596** |
| Memory only | 44.6% | 0.5094 |
| Pressure only | 52.3% | 0.4420 |

State-only identity accuracy remained between **77.5% and 90.0%** across all six holdout parameter points.

This is a causal generalization result: transferring only recurrent state causes continuation to identify with the donor history substantially more often than chance, while memory-only and pressure-only transfers do not show the same robustness.

## V13 — Cross-seed self-state prediction

Four regimes were evaluated with 20 seeds and four held-out seed folds.

The external-only predictor used current/next input values. The internal predictor used the same external inputs plus recurrent state, memory, pressure, score, cross, and threshold.

| Regime | R2 external | R2 internal | Gain |
|---|---:|---:|---:|
| Baseline | 0.776 | 0.997 | +0.221 |
| Critical | 0.106 | **0.885** | **+0.778** |
| Holdout critical | 0.128 | **0.897** | **+0.769** |
| Persistence | 0.107 | **0.888** | **+0.781** |

The internal model also reduced MAE by:

- critical: 0.558 → 0.160;
- holdout critical: 0.502 → 0.134;
- persistence: 0.559 → 0.156.

The important feature is not raw prediction quality alone. In resonant regimes, external input is a poor predictor of next state, while internal dynamic variables supply most of the missing predictive information.

## Combined interpretation

Current computational evidence now has three independent layers:

1. **Persistence:** historical separation survives hundreds of identical or zero-input future steps in resonant regimes.
2. **Causal transport:** transplanting recurrent state transfers historical identity with high accuracy, including blind parameter holdouts.
3. **Self-predictive internal state:** internal state dramatically improves one-step prediction beyond external inputs alone, including an unseen critical parameter point.

These observations characterize a persistent, history-dependent, internally predictive dynamical regime.

They remain computational properties of the implemented model. They do not establish consciousness, subjective experience, or a physical interpretation of symbolic X state.

</details>