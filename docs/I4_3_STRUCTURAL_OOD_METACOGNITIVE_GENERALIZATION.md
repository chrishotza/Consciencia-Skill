<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# I4.3 — Generalización metacognitiva estructural OOD

## Estado

**Ejecución confirmatoria verificada.**

## Pregunta

¿Un modelo de fiabilidad de segundo orden entrenado con una estructura de perturbación oculta sigue siendo útil cuando cambia la estructura causal de la perturbación, sin reentrenamiento online?

## Entrenamiento

El observador metacognitivo se entrenó únicamente con la familia `linear_action_pressure`, magnitud 0.50 y riesgo oculto `0.04 + 0.09 * |action| + 0.06 * max(pressure, 0)`.

## Familias OOD

El modelo quedó congelado antes de la evaluación y fue desafiado con `quadratic_action`, `pressure_threshold` y `state_coupled`.

## Resultado verificado

Workflow **36974947476** · artifact **11213116686** · commit **d69d04ccc390c36c2e404d405d657426199a8bb5**.

- META−LESION error medio: **−0.0015489972**, p **4.2710×10⁻⁶**
- META−PERMUTED error medio: **−0.0015669273**, p **9.3756×10⁻⁶**
- META−RANDOM error medio: **−0.0065857231**, p **3.6403×10⁻¹⁷**
- META−LESION recovery: **−0.0039470302**, p **0.1505181** (nulo)
- META−PERMUTED prediction MAE: **−0.0015325239**, p **0.0014245**
- serialización exacta: **sí**
- actualizaciones online durante evaluación: **no**

Por familia, `state_coupled` produjo la mayor separación META−LESION en error (**−0.0033318**, p **4.66×10⁻¹⁰**). `pressure_threshold` fue mucho más débil en error (p **0.05010**) y mostró un patrón de recovery distinto.

## Interpretación

I4.3 aporta evidencia de **generalización estructural del componente de predicción de error** frente a perturbaciones no vistas bajo este arnés determinista. La generalización del endpoint de recuperación es mixta y el agregado META−LESION de recovery es nulo.

Esto es una propiedad computacional del mecanismo metacognitivo; no es una puntuación de consciencia ni demuestra experiencia subjetiva.

</details>

<a id="english"></a>
# I4.3 — Structural OOD Metacognitive Generalization

## Status

**Verified confirmatory execution completed.**

## Question

> Does a second-order reliability model trained under one hidden-disturbance structure remain useful when the structure of the disturbance changes, without online retraining?

I4.2 established persistence, serialization/restore, lesion/permutation separation, and rescue under the I4.1 disturbance family. I4.3 attacks the remaining external-validity weakness by changing the causal structure of the hidden disturbance after training.

## Training condition

The metacognitive observer is trained only under:

\`linear_action_pressure\`

with hidden risk:

\`0.04 + 0.09 * |action| + 0.06 * max(pressure, 0)\`

Training magnitude:

\`0.50\`

## OOD disturbance families

The trained observer is frozen before evaluation.

### 1. quadratic_action

\`0.035 + 0.075 * |action|^2 + 0.055 * pressure\`

### 2. pressure_threshold

\`0.025 + 0.03 * |action| + 0.10 * max(pressure - 0.18, 0)\`

The disturbance direction reverses above a fixed pressure threshold for non-zero actions.

### 3. state_coupled

\`0.02 + 0.06 * |action| + 0.08 * |state| * |action| + 0.04 * pressure\`

The disturbance direction depends on the joint sign relationship between state and action.

These structures are not shown during training.

## Conditions

- **META** — restored second-order model controls action selection.
- **LESION** — second-order layer removed; first-order selection remains.
- **PERMUTED** — restored model with targets permuted while retaining the learned feature distribution.
- **RANDOM** — matched candidate actions sampled randomly.

All conditions are paired by family, seed, initial state, perturbation magnitude, and deterministic world seeds.

No online updates occur during evaluation.

## Primary endpoint

Aggregate paired difference in mean prediction error:

\`META - LESION\`

across all OOD families and evaluation episodes.

## Secondary endpoints

- META - PERMUTED mean prediction error;
- META - RANDOM mean prediction error;
- META - LESION recovery;
- META - PERMUTED second-order prediction MAE;
- family-specific paired contrasts;
- policy-shift rate.

## Prespecified interpretation

A positive primary result supports structural OOD generalization of a computational metacognitive reliability mechanism.

A null or negative result is retained as evidence that the mechanism remains too tied to the training disturbance structure and should drive the next redesign.

No result from I4.3 is a consciousness score or evidence of subjective experience by itself.

## Reproducibility

The workflow records the exact commit, run identifier, and artifact. The trained second-order model is serialized and restored before every evaluation batch.

The protocol does not permit online meta-model updates during evaluation.

### Verified execution

Workflow **36974947476** · artifact **11213116686** · commit **d69d04ccc390c36c2e404d405d657426199a8bb5**.

- META−LESION mean error: **−0.0015489972**, p **4.2710×10⁻⁶**
- META−PERMUTED mean error: **−0.0015669273**, p **9.3756×10⁻⁶**
- META−RANDOM mean error: **−0.0065857231**, p **3.6403×10⁻¹⁷**
- META−LESION recovery: **−0.0039470302**, p **0.1505181** (null)
- META−PERMUTED prediction MAE: **−0.0015325239**, p **0.0014245**
- exact serialization: **true**
- online updates during evaluation: **false**

Interpretation: I4.3 supports structural OOD generalization of the second-order prediction-error component under the deterministic protocol, while the aggregate recovery endpoint remains mixed/null. It does not establish consciousness or subjective experience.