# I0 — Interoceptive Instrumentation

## Status

**Instrumentation implemented; causal regulation not yet enabled.**

I0 is intentionally read-only. It does not change organism state, policy, rewards, or trajectory selection.

## Instrumented variables

The current probe exposes bounded internal signals derived from the persistent organism state:

| Signal | Source |
|---|---|
| prediction_error | `self_prediction_error` |
| prediction_confidence | `self_prediction_confidence` |
| dynamic_pressure | `dynamic_pressure` |
| attractor_distance | `dynamic_attractor_distance` |
| memory_load | memory count / configured memory limit |
| dynamic_activity | magnitude of dynamic state + dynamic memory |
| state_change | absolute current-vs-previous dynamic state |
| operating_condition | declared weighted aggregate of the above signals |

The aggregate is an engineering diagnostic, not a biological claim and not a consciousness score.

## Invariance requirements

The probe must:

- be deterministic for identical state inputs;
- leave the supplied `OntologicalState` unchanged;
- keep readout variables in the declared [0,1] range;
- expose each component separately so the aggregate can be audited;
- remain independent of semantic self-report.

These requirements are covered by unit tests.

## Next confirmatory step

I1 should preregister the viability ranges and test whether the organism can estimate its internal operating condition after controlled perturbations without semantic labels.

Before enabling any interoceptive controller, the protocol should specify:

- primary endpoint;
- perturbation distribution;
- viability bounds;
- recovery horizon;
- matched controls;
- target-permuted controls;
- lesion of the interoceptive readout;
- replication count and seed policy;
- analysis rule;
- artifact validation.

Only after I1 passes should the interoceptive signal be permitted to modulate policy.

## External motivation

Lee et al. (2026) propose interoceptive AI as an architecture in which artificial systems explicitly factor internal and external states and use mathematically represented internal states to modulate adaptive behaviour. The Skill-Conscious I0 layer is a narrower instrumentation step toward testing such mechanisms.

Reference: Lee et al. (2026), *Life-inspired interoceptive artificial intelligence for autonomous and adaptive agents*, Nature Machine Intelligence 8, 1335–1346.

https://doi.org/10.1038/s42256-026-01296-8


<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# I0 — Instrumentación interoceptiva

## Estado

**Instrumentación implementada; regulación causal todavía no habilitada.**

I0 es deliberadamente de solo lectura. No modifica el estado del organismo, la política, las recompensas ni la selección de trayectorias.

## Variables instrumentadas

La sonda actual expone señales internas acotadas derivadas del estado persistente:

| Señal | Fuente |
|---|---|
| prediction_error | self_prediction_error |
| prediction_confidence | self_prediction_confidence |
| dynamic_pressure | dynamic_pressure |
| attractor_distance | dynamic_attractor_distance |
| memory_load | cantidad de memorias / límite configurado |
| dynamic_activity | magnitud del estado dinámico + memoria dinámica |
| state_change | valor absoluto del estado dinámico actual frente al anterior |
| operating_condition | agregado ponderado declarado de las señales anteriores |

El agregado es un diagnóstico de ingeniería, no una afirmación biológica ni una puntuación de consciencia.

## Requisitos de invariancia

La sonda debe:

- ser determinista para entradas de estado idénticas;
- dejar sin cambios el OntologicalState recibido;
- mantener las variables de lectura dentro del rango declarado [0,1];
- exponer cada componente por separado para permitir auditoría;
- mantenerse independiente del autoinforme semántico.

Estos requisitos están cubiertos por tests unitarios.

## Próximo paso confirmatorio

I1 debe predefinir los rangos de viabilidad y probar si el organismo puede estimar su condición operativa interna después de perturbaciones controladas sin etiquetas semánticas.

Antes de habilitar cualquier controlador interoceptivo, el protocolo debe fijar endpoint primario, distribución de perturbaciones, límites de viabilidad, horizonte de recuperación, controles emparejados, controles con targets permutados, lesión del readout interoceptivo, cantidad de réplicas y política de seeds, regla de análisis y validación del artifact.

Solo después de que I1 supere ese umbral debe permitirse que la señal interoceptiva module la política.

## Motivación externa

Lee et al. (2026) proponen una IA interoceptiva como arquitectura donde sistemas artificiales representan explícitamente estados internos y externos y utilizan esos estados matemáticamente representados para modular comportamiento adaptativo. La capa I0 de Skill-Conscious es un paso instrumental más acotado para probar mecanismos de ese tipo.

Referencia: Lee et al. (2026), *Life-inspired interoceptive artificial intelligence for autonomous and adaptive agents*, Nature Machine Intelligence 8, 1335–1346.

https://doi.org/10.1038/s42256-026-01296-8

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# I0 — Interoceptive Instrumentation

## Status

**Instrumentation implemented; causal regulation not yet enabled.**

I0 is intentionally read-only. It does not change organism state, policy, rewards, or trajectory selection.

## Instrumented variables

The current probe exposes bounded internal signals derived from persistent organism state:

| Signal | Source |
|---|---|
| prediction_error | self_prediction_error |
| prediction_confidence | self_prediction_confidence |
| dynamic_pressure | dynamic_pressure |
| attractor_distance | dynamic_attractor_distance |
| memory_load | memory count / configured memory limit |
| dynamic_activity | magnitude of dynamic state + dynamic memory |
| state_change | absolute current-vs-previous dynamic state |
| operating_condition | declared weighted aggregate of the signals above |

The aggregate is an engineering diagnostic, not a biological claim and not a consciousness score.

## Invariance requirements

The probe must be deterministic for identical state inputs, leave the supplied OntologicalState unchanged, keep readout variables in the declared [0,1] range, expose each component separately for auditing, and remain independent of semantic self-report.

These requirements are covered by unit tests.

## Next confirmatory step

I1 should preregister viability ranges and test whether the organism can estimate its internal operating condition after controlled perturbations without semantic labels.

Before enabling any interoceptive controller, the protocol should freeze the primary endpoint, perturbation distribution, viability bounds, recovery horizon, matched controls, target-permuted controls, interoceptive-readout lesion, replication count and seed policy, analysis rule, and artifact validation.

Only after I1 passes should the interoceptive signal be permitted to modulate policy.

## External motivation

Lee et al. (2026) propose interoceptive AI as an architecture in which artificial systems explicitly represent internal and external states and use mathematically represented internal states to modulate adaptive behaviour. Skill-Conscious I0 is a narrower instrumentation step toward testing such mechanisms.

Reference: Lee et al. (2026), *Life-inspired interoceptive artificial intelligence for autonomous and adaptive agents*, Nature Machine Intelligence 8, 1335–1346.

https://doi.org/10.1038/s42256-026-01296-8

</details>