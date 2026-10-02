# I1 — Interoceptive Self-Assessment

## Question

> Can the organism estimate a future internal operating condition from a bounded readout of its own current internal state, without semantic self-report?

I1 is the first step after read-only instrumentation. It does not allow the interoceptive signal to control policy yet.

## Design

The protocol uses the deterministic internal dynamics as the environment.

- training perturbation magnitudes: `0.25, 0.50, 0.75`;
- OOD perturbation magnitudes: `0.35, 0.65, 0.90`;
- snapshot immediately after the controlled perturbation;
- recovery horizon: 8 internal steps;
- no semantic input during the probe;
- no model-provider output is required.

At each snapshot, I0 produces eight bounded internal variables. The hidden target is a future recovery score computed from the subsequent internal trajectory:

```text
recovery = 1 / (1 + |future_state| + future_pressure)
```

The target is never supplied to the organism during the probe.

## Controls

I1 compares four predictors:

| Predictor | Purpose |
|---|---|
| Interoceptive | full bounded internal readout |
| Single-signal | strongest single interoceptive variable baseline used here |
| Target-permuted | tests whether feature→target mapping carries predictive information |
| Constant | predicts the training-set mean recovery |

The primary OOD comparison is the full interoceptive predictor against a single-signal baseline, a target-permuted control, and a constant baseline.

## Primary endpoint

Mean absolute error (MAE) on the held-out OOD perturbations.

Paired sign tests compare per-episode absolute errors between the full interoceptive predictor and each control.

## Why this is not yet regulation

I1 only tests **readability of future internal condition**.

It does not allow the readout to change actions, rewards, or dynamics. A favorable I1 result would therefore support an internal predictive representation, not homeostatic agency.

## Interpretation boundary

A positive result would show that the bounded interoceptive representation contains predictive information about near-future internal recovery under the tested dynamics.

It would not establish subjective experience, consciousness, or biological interoception.

## Preregistration status

This document defines the confirmatory structure before the first dedicated I1 workflow result is published. The historical protocol family is not retroactively treated as globally preregistered.

Before extending I1, the primary endpoint, perturbation distribution, controls, exclusion rules, replication count, and analysis rule should remain frozen for the confirmatory run.

## Next step

I2 can only enable interoceptive policy modulation after I1 has a validated readout. I2 should then compare regulation with full, no-interoception, shuffled, and clamped conditions under the same perturbation schedule.


<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# I1 — Autoevaluación interoceptiva

## Pregunta

> ¿Puede el organismo estimar una futura condición operativa interna a partir de una lectura acotada de su propio estado actual, sin autoinforme semántico?

I1 es el primer paso después de la instrumentación de solo lectura. Todavía no permite que la señal interoceptiva controle la política.

## Diseño

El protocolo utiliza la dinámica interna determinista como entorno.

- magnitudes de perturbación de entrenamiento: 0.25, 0.50, 0.75;
- magnitudes OOD: 0.35, 0.65, 0.90;
- snapshot inmediatamente después de la perturbación;
- horizonte de recuperación: 8 pasos internos;
- sin entrada semántica durante la sonda;
- no se requiere salida del proveedor de modelo.

En cada snapshot, I0 produce ocho variables internas acotadas. El target oculto es un score de recuperación futura calculado a partir de la trayectoria interna posterior:

recovery = 1 / (1 + |future_state| + future_pressure)

El target nunca se entrega al organismo durante la sonda.

## Controles

I1 compara cuatro predictores:

| Predictor | Propósito |
|---|---|
| Interoceptive | lectura interna completa y acotada |
| Single-signal | baseline de la señal interoceptiva individual más fuerte usada aquí |
| Target-permuted | prueba si el mapeo feature → target contiene información predictiva |
| Constant | predice la media de recuperación del conjunto de entrenamiento |

La comparación OOD primaria es el predictor interoceptivo completo frente al baseline de una sola señal, el control con targets permutados y el baseline constante.

## Endpoint primario

Error absoluto medio (MAE) sobre perturbaciones OOD reservadas.

Los tests de signo emparejados comparan los errores absolutos por episodio entre el predictor interoceptivo completo y cada control.

## Por qué todavía no es regulación

I1 prueba únicamente **legibilidad del futuro estado interno**.

No permite que el readout modifique acciones, recompensas ni dinámica. Un resultado favorable apoyaría una representación predictiva interna, no agencia homeostática.

## Límite de interpretación

Un resultado positivo mostraría que la representación interoceptiva acotada contiene información predictiva sobre la recuperación interna próxima bajo la dinámica probada.

No establecería experiencia subjetiva, consciencia ni interocepción biológica.

## Estado de preregistro

Este documento define la estructura confirmatoria antes de publicar el primer resultado del workflow I1. La familia histórica de protocolos no se considera retroactivamente preregistrada de manera global.

Antes de ampliar I1, el endpoint primario, distribución de perturbaciones, controles, reglas de exclusión, cantidad de réplicas y regla de análisis deben permanecer congelados para la ejecución confirmatoria.

## Próximo paso

I2 solo puede habilitar modulación de política por interocepción después de validar el readout I1. Entonces I2 debe comparar regulación con condiciones full, sin interocepción, barajada y fijada bajo el mismo calendario de perturbaciones.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# I1 — Interoceptive Self-Assessment

## Question

> Can the organism estimate a future internal operating condition from a bounded readout of its own current internal state, without semantic self-report?

I1 is the first step after read-only instrumentation. It does not yet allow the interoceptive signal to control policy.

## Design

The protocol uses deterministic internal dynamics as the environment.

- training perturbation magnitudes: 0.25, 0.50, 0.75;
- OOD perturbation magnitudes: 0.35, 0.65, 0.90;
- snapshot immediately after controlled perturbation;
- recovery horizon: 8 internal steps;
- no semantic input during the probe;
- no model-provider output required.

At each snapshot, I0 produces eight bounded internal variables. The hidden target is a future recovery score computed from the subsequent internal trajectory:

recovery = 1 / (1 + |future_state| + future_pressure)

The target is never supplied to the organism during the probe.

## Controls

I1 compares four predictors: Interoceptive, Single-signal, Target-permuted, and Constant. The primary OOD comparison is the full interoceptive predictor against the single-signal baseline, target-permuted control, and constant baseline.

## Primary endpoint

Mean absolute error (MAE) on held-out OOD perturbations.

Paired sign tests compare per-episode absolute errors between the full interoceptive predictor and each control.

## Why this is not yet regulation

I1 only tests **readability of future internal condition**.

It does not allow the readout to change actions, rewards, or dynamics. A favorable result would therefore support an internal predictive representation, not homeostatic agency.

## Interpretation boundary

A positive result would show that the bounded interoceptive representation contains predictive information about near-future internal recovery under the tested dynamics.

It would not establish subjective experience, consciousness, or biological interoception.

## Preregistration status

This document defines the confirmatory structure before the first dedicated I1 workflow result is published. The historical protocol family is not retroactively treated as globally preregistered.

Before extending I1, the primary endpoint, perturbation distribution, controls, exclusion rules, replication count, and analysis rule should remain frozen for the confirmatory run.

## Next step

I2 can only enable interoceptive policy modulation after I1 has a validated readout. I2 should then compare regulation with full, no-interoception, shuffled, and clamped conditions under the same perturbation schedule.

</details>