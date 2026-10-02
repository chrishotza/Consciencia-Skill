# Context Factorial — V9

V9 decomposes the historical persistence after a 300-step history followed by 500 zero-input steps. Both branches use identical noise seeds.

Interventions synchronize selected context variables at the history/future boundary while preserving the others.

## End-gap retention relative to the full historical context

| Regime | State+Memory reset | State+Pressure reset | Memory+Pressure reset |
|---|---:|---:|---:|
| baseline | ~0 | ~0 | effectively baseline numerical residual |
| critical | **0.250** | **0.551** | **0.832** |
| persistence | **0.274** | **1.004** | **0.962** |

Interpretation of columns:
- State+Memory reset: pressure is the only branch-specific variable retained.
- State+Pressure reset: memory is the only branch-specific variable retained.
- Memory+Pressure reset: state is the only branch-specific variable retained.

## Main finding

The critical ridge retains approximately 83% of the full end-gap when only the recurrent state difference is preserved, and approximately 55% when only the explicit memory difference is preserved.

The persistence ridge is even more state-dominated: preserving only the state retains approximately 96% of the full effect, while preserving only memory retains approximately 100% in this protocol.

Pressure alone does not account for the persistence: resetting pressure while retaining state and memory leaves the high-persistence effect essentially unchanged.

The strongest operational description is therefore **distributed context persistence**: the system stores history across interacting dynamical variables rather than in one explicit memory scalar.

This is a property of the implemented computational model. It does not establish consciousness, subjective experience, or a physical interpretation of the model's symbolic states.

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Factorial de contexto — V9

V9 descompone la persistencia histórica después de una historia de 300 pasos seguida por 500 pasos sin input. Ambas ramas utilizan seeds de ruido idénticas.

Las intervenciones sincronizan variables de contexto seleccionadas en el límite historia/futuro y conservan las demás.

## Retención del end-gap respecto del contexto histórico completo

| Régimen | Reset state+memory | Reset state+pressure | Reset memory+pressure |
|---|---:|---:|---:|
| baseline | ~0 | ~0 | residual numérico de baseline |
| critical | **0.250** | **0.551** | **0.832** |
| persistence | **0.274** | **1.004** | **0.962** |

Interpretación de las columnas:

- state+memory reset: pressure es la única variable específica de la rama que permanece;
- state+pressure reset: memory es la única variable específica de la rama;
- memory+pressure reset: state es la única variable específica de la rama.

## Hallazgo principal

La cresta crítica conserva aproximadamente 83% del end-gap completo cuando solo se conserva la diferencia de estado recurrente y aproximadamente 55% cuando solo se conserva la diferencia explícita de memoria.

La cresta de persistence está aún más dominada por el estado: conservar solo state retiene aproximadamente 96% del efecto completo, mientras conservar solo memory retiene aproximadamente 100% en este protocolo.

Pressure por sí solo no explica la persistencia: resetear pressure manteniendo state y memory deja el efecto de alta persistencia prácticamente sin cambios.

La descripción operacional más fuerte es **persistencia de contexto distribuida**: el sistema conserva la historia a través de variables dinámicas que interactúan, no en un único escalar de memoria explícita.

Esta es una propiedad del modelo computacional implementado. No establece consciencia, experiencia subjetiva ni una interpretación física de los estados simbólicos.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# Context Factorial — V9

V9 decomposes historical persistence after a 300-step history followed by 500 zero-input steps. Both branches use identical noise seeds.

Interventions synchronize selected context variables at the history/future boundary while preserving the others.

## End-gap retention relative to the full historical context

| Regime | State+Memory reset | State+Pressure reset | Memory+Pressure reset |
|---|---:|---:|---:|
| baseline | ~0 | ~0 | effectively baseline numerical residual |
| critical | **0.250** | **0.551** | **0.832** |
| persistence | **0.274** | **1.004** | **0.962** |

Column interpretation:

- State+Memory reset: pressure is the only branch-specific variable retained.
- State+Pressure reset: memory is the only branch-specific variable retained.
- Memory+Pressure reset: state is the only branch-specific variable retained.

## Main finding

The critical ridge retains approximately 83% of the full end-gap when only the recurrent state difference is preserved, and approximately 55% when only the explicit memory difference is preserved.

The persistence ridge is even more state-dominated: preserving only state retains approximately 96% of the full effect, while preserving only memory retains approximately 100% in this protocol.

Pressure alone does not account for persistence: resetting pressure while retaining state and memory leaves the high-persistence effect essentially unchanged.

The strongest operational description is therefore **distributed context persistence**: the system stores history across interacting dynamical variables rather than in one explicit memory scalar.

This is a property of the implemented computational model. It does not establish consciousness, subjective experience, or a physical interpretation of the model's symbolic states.

</details>