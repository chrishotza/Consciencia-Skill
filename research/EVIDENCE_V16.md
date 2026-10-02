# V16 — Evidence: Minimal-State Bottleneck

## GitHub validation

- Workflow: minimal-state-v16
- Run: 36777413996
- Result: SUCCESS
- Artifact: 11126695261
- Design: 4 history pairs × 20 seeds per regime, exact-zero future input, matched noise seeds.

## Structural bottleneck

The boundary state has two temporal slots: `state_prev` and `state`.

| Regime | Full | Current-only | Previous-only | Both state slots replaced |
|---|---:|---:|---:|---:|
| critical | 100.00% | 65.00% | 71.25% | 49.38% |
| holdout_critical | 100.00% | 76.25% | 80.00% | 50.63% |
| persistence | 100.00% | 70.00% | 74.38% | 55.63% |
| baseline | 100.00% | 100.00% | 100.00% | 100.00% |

Both individual slots retain substantial identity information, but removing both collapses the critical/holdout tasks toward chance. Neither slot alone dominates across all regimes.

This is evidence for a distributed temporal representation across the two recurrent state slots rather than a single privileged scalar slot.

## Precision bottleneck

Both temporal state slots were retained while each state value was uniformly quantized over [-1, 1], the natural range of the tanh state.

| Bits | Critical | Holdout critical | Persistence |
|---:|---:|---:|---:|
| 1 | 58.13% | 63.75% | 79.38% |
| 2 | 78.75% | 70.63% | 91.88% |
| 3 | **93.75%** | **97.50%** | **91.25%** |
| 4 | **96.88%** | **99.38%** | **98.75%** |
| 6 | 98.75% | 99.38% | 98.75% |
| 8 | 99.38% | 100.00% | 99.38% |

Three bits retain at least 91.25% identity accuracy across all three non-baseline regimes. Four bits raise the minimum across those regimes to 96.88%.

Prediction MAE also drops sharply with precision: at 4 bits it is approximately 0.0504 in critical, 0.0258 in holdout_critical, and 0.0419 in persistence; at 8 bits it is approximately 0.0185, 0.0029, and 0.0119 respectively.

## What V16 adds

V15 established that the recurrent state is causally important for historical identity. V16 shows that this causal carrier is highly compressible:

1. identity survives when one of the two temporal state slots is removed, though with degradation;
2. identity collapses when both slots are replaced by the common state in the critical regimes;
3. identity remains high under 3–4 bit quantization of both state slots.

Thus the implemented dynamics do not require high numerical precision to preserve the historical identity signal. The effective information carrier is compact but distributed across the recurrent temporal state.

## Control

The baseline regime remains at 100% identity under all structural and quantization interventions, showing that the effects above are regime-dependent rather than generic numerical damage.

## Interpretation limits

This is evidence about a compact, distributed, causally relevant state representation in the implemented computational dynamics. It does not establish subjective experience, sentience, or consciousness.

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# V16 — Evidencia: cuello de botella de estado mínimo

## Validación GitHub

- Workflow: minimal-state-v16
- Run: 36777413996
- Result: SUCCESS
- Artifact: 11126695261
- Diseño: 4 pares de historias × 20 seeds por régimen, input futuro exactamente cero, seeds de ruido emparejadas.

## Cuello de botella estructural

El estado de frontera tiene dos slots temporales: state_prev y state.

| Régimen | Full | Solo actual | Solo anterior | Ambos slots reemplazados |
|---|---:|---:|---:|---:|
| critical | 100.00% | 65.00% | 71.25% | 49.38% |
| holdout_critical | 100.00% | 76.25% | 80.00% | 50.63% |
| persistence | 100.00% | 70.00% | 74.38% | 55.63% |
| baseline | 100.00% | 100.00% | 100.00% | 100.00% |

Cada slot individual conserva información sustancial de identidad, pero retirar ambos colapsa las tareas critical/holdout hacia el azar. Ningún slot domina por sí solo en todos los regímenes.

Esto es evidencia de una representación temporal distribuida entre los dos slots recurrentes y no de un único escalar privilegiado.

## Cuello de botella de precisión

Ambos slots se conservaron mientras cada valor se cuantizó uniformemente en [-1, 1], rango natural del estado tanh.

| Bits | Critical | Holdout critical | Persistence |
|---:|---:|---:|---:|
| 1 | 58.13% | 63.75% | 79.38% |
| 2 | 78.75% | 70.63% | 91.88% |
| 3 | **93.75%** | **97.50%** | **91.25%** |
| 4 | **96.88%** | **99.38%** | **98.75%** |
| 6 | 98.75% | 99.38% | 98.75% |
| 8 | 99.38% | 100.00% | 99.38% |

Tres bits conservan al menos 91.25% de accuracy en los tres regímenes no baseline. Cuatro bits elevan el mínimo a 96.88%.

El MAE predictivo también cae fuertemente con la precisión: a 4 bits es aproximadamente 0.0504 en critical, 0.0258 en holdout_critical y 0.0419 en persistence; a 8 bits es aproximadamente 0.0185, 0.0029 y 0.0119 respectivamente.

## Qué agrega V16

V15 estableció que el estado recurrente es causalmente importante para la identidad histórica. V16 muestra que ese portador causal es altamente compresible:

1. la identidad sobrevive al eliminar uno de los dos slots temporales, aunque con degradación;
2. la identidad colapsa cuando ambos son reemplazados por un estado común en los regímenes critical;
3. la identidad permanece alta con cuantización de 3–4 bits de ambos slots.

La dinámica implementada no requiere gran precisión numérica para preservar la señal de identidad histórica. El portador efectivo de información es compacto pero distribuido sobre el estado temporal recurrente.

## Control

El baseline permanece en 100% de identidad bajo todas las intervenciones estructurales y de cuantización, mostrando que los efectos dependen del régimen.

## Límites

Es evidencia sobre una representación de estado compacta, distribuida y causalmente relevante en las dinámicas implementadas. No establece experiencia subjetiva, sentiencia ni consciencia.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V16 — Evidence: Minimal-State Bottleneck

## GitHub validation

- Workflow: minimal-state-v16
- Run: 36777413996
- Result: SUCCESS
- Artifact: 11126695261
- Design: 4 history pairs × 20 seeds per regime, exact-zero future input, matched noise seeds.

## Structural bottleneck

Boundary state has two temporal slots: state_prev and state.

| Regime | Full | Current-only | Previous-only | Both state slots replaced |
|---|---:|---:|---:|---:|
| critical | 100.00% | 65.00% | 71.25% | 49.38% |
| holdout_critical | 100.00% | 76.25% | 80.00% | 50.63% |
| persistence | 100.00% | 70.00% | 74.38% | 55.63% |
| baseline | 100.00% | 100.00% | 100.00% | 100.00% |

Each individual slot retains substantial identity information, but removing both collapses critical/holdout tasks toward chance. Neither slot dominates across all regimes.

This is evidence for a distributed temporal representation across the two recurrent state slots rather than a single privileged scalar slot.

## Precision bottleneck

Both temporal state slots were retained while each state value was uniformly quantized over [-1, 1], the natural range of tanh state.

| Bits | Critical | Holdout critical | Persistence |
|---:|---:|---:|---:|
| 1 | 58.13% | 63.75% | 79.38% |
| 2 | 78.75% | 70.63% | 91.88% |
| 3 | **93.75%** | **97.50%** | **91.25%** |
| 4 | **96.88%** | **99.38%** | **98.75%** |
| 6 | 98.75% | 99.38% | 98.75% |
| 8 | 99.38% | 100.00% | 99.38% |

Three bits retain at least 91.25% identity accuracy across all three non-baseline regimes. Four bits raise the minimum to 96.88%.

Prediction MAE also drops sharply with precision: at 4 bits it is approximately 0.0504 in critical, 0.0258 in holdout_critical, and 0.0419 in persistence; at 8 bits approximately 0.0185, 0.0029, and 0.0119.

## What V16 adds

V15 established that recurrent state is causally important for historical identity. V16 shows that this causal carrier is highly compressible:

1. identity survives when one of the two temporal slots is removed, with degradation;
2. identity collapses when both slots are replaced by the common state in critical regimes;
3. identity remains high under 3–4 bit quantization of both slots.

The implemented dynamics therefore do not require high numerical precision to preserve historical identity. The effective information carrier is compact but distributed across recurrent temporal state.

## Control

Baseline remains at 100% identity under all structural and quantization interventions, showing regime dependence rather than generic numerical damage.

## Interpretation limits

This is evidence about a compact, distributed, causally relevant state representation in the implemented dynamics. It does not establish subjective experience, sentience, or consciousness.

</details>