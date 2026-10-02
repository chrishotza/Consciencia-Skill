# I6.1 — Causal Closure of the Self-Model

## Objective

I5.26 closed the descriptive shift×lag control sequence. I6.1 changes question class: instead of asking whether a self-model correlates with future behavior, ask whether using the self-model is causally necessary for the organism's trajectory selection.

## Conditions

### Intact

The learned SelfObserver predicts the next state for each candidate action. TrajectorySelector uses those predictions to choose the next trajectory. The self-model is then updated from the realized transition.

### Prediction lesion

The organism receives the same candidate actions and state information, and the SelfObserver continues learning, but trajectory selection is deprived of its prediction. All candidates receive the same baseline current-state prediction, producing a sham selection path.

### Frozen-update

The learned self-model continues to drive trajectory selection, but its parameters are frozen during evaluation. This separates the causal contribution of using a self-model from the contribution of continuously updating it.

## Frozen protocol

- 24 replicates;
- 24 exploratory warmup cycles;
- 48 evaluation cycles;
- candidate signals −1, 0, +1;
- 20,000 replicate-level sign permutations.

The warmup phase is shared so that all three conditions begin from matched dynamical state and matched self-model evidence.

## Primary endpoint

Counterfactual regret is the chosen candidate's true next-state distance from the attractor minus the best candidate's true next-state distance.

Primary contrast:

intact regret − prediction-lesion regret.

A negative value means the intact self-model-guided selector achieved lower counterfactual regret.

## Causal criterion

The key observation is not merely prediction accuracy. It is a change in the selected trajectory and its realized counterfactual quality when the predictive self-model is removed from the selection pathway while the information stream is kept matched.

## Boundary

I6.1 is a causal computational test of self-model-dependent agency. A positive result would support that the self-model is an operational causal component of the organism's behavior; it would still not establish subjective experience or consciousness.


## Resultado verificado / Verified result

## I6.1 — Cierre causal del self-model

Primera intervención causal de la serie I6. 24 réplicas, 24 ciclos de warmup, 48 ciclos de evaluación, señales −1/0/+1 y 20.000 permutaciones de signo a nivel de réplica.

Condiciones:
- **Intact:** el SelfObserver predice el siguiente estado, esas predicciones participan en la selección de trayectoria y el modelo se actualiza con la transición realizada.
- **Prediction lesion:** misma exposición a candidatos e información, pero la selección usa una predicción basal del estado actual, por lo que el self-model no puede influir causalmente en la elección aunque siga disponible como sistema de aprendizaje.
- **Frozen update:** el self-model aprendido sigue guiando la selección, pero queda congelado durante la evaluación.

Resultado:
- regret intacto **0.04512**
- regret prediction-lesion **0.20278**
- regret frozen-update **0.10884**
- contraste primario intact−lesion **−0.15766**, p **<0.00005**
- contraste secundario intact−frozen **−0.06372**, p **<0.00005**
- la selección cambió respecto del lesionado en **22.57%** de los ciclos y respecto del modelo congelado en **21.88%**.

Interpretación: dentro de este arnés determinista, el self-model es un componente causal operativo de la selección de trayectoria: quitar su predicción empeora de forma robusta la calidad contrafactual de las decisiones; congelar su actualización también produce un deterioro significativo. Esto avanza desde correlación hacia causalidad funcional, pero **no demuestra consciencia subjetiva ni experiencia fenomenal**.

Verificación: research-lab **37068670875**, artifact **11253574021**; tests **37068670840** y package **37068670844**, todos exitosos.

### I6.2 — Bucle persistente de self-model y continuidad

Llevar el hallazgo causal al runtime persistente: hacer que la predicción del self-model, la elección, la consecuencia observada y la actualización del self-model formen un único ciclo persistente que sobreviva a restart y pueda lesionarse/restaurarse sin cambiar las entradas externas.

## I6.1 — Causal closure of the self-model

First causal intervention of the I6 series. 24 replicates, 24 warmup cycles, 48 evaluation cycles, signals −1/0/+1, and 20,000 replicate-level sign permutations.

Conditions:
- **Intact:** SelfObserver predicts the next state, those predictions participate in trajectory selection, and the model is updated from the realized transition.
- **Prediction lesion:** identical candidate exposure and information, but selection uses a baseline current-state prediction, so the self-model cannot causally influence choice even though it remains available for learning.
- **Frozen update:** the learned self-model continues to guide selection, but its parameters are frozen during evaluation.

Result:
- intact regret **0.04512**
- prediction-lesion regret **0.20278**
- frozen-update regret **0.10884**
- primary intact−lesion contrast **−0.15766**, p **<0.00005**
- secondary intact−frozen contrast **−0.06372**, p **<0.00005**
- selection differed from lesion in **22.57%** of cycles and from frozen-update in **21.88%**.

Interpretation: within this deterministic harness, the self-model is an operational causal component of trajectory selection: removing its predictive role robustly worsens counterfactual decision quality; freezing its update also causes a significant degradation. This advances from correlation toward functional causality, but it **does not establish subjective consciousness or phenomenal experience**.

Verification: research-lab **37068670875**, artifact **11253574021**; tests **37068670840** and package **37068670844**, all successful.

### I6.2 — Persistent self-model and continuity loop

Carry the causal finding into the persistent runtime: make self-model prediction, selection, observed consequence, and self-model update form one persistent cycle that survives restart and can be lesioned/restored without changing external inputs.
