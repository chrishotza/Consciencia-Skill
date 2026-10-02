<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Evidencia V59 — Factorial semantic bridge × self-model

## Hipótesis

El semantic memory bridge debe alterar el estado interno presentado al self-model, mientras el self-model debe conservar una ventaja medible de selección de trayectorias frente a una política random emparejada. V59 prueba si esos efectos interactúan.

## Diseño

Para cada seed, se construyen dos condiciones bridge a partir de historias de warmup emparejadas:

- bridge OFF: la dinámica wake utiliza el dynamic_wake_signal fijo;
- bridge ON: la dinámica wake utiliza la señal de continuidad de memory semántica.

Desde cada condición, el mismo estado post-wake exacto se clona en dos brazos de política:

- self_model;
- random.

Los candidatos son {-1, +1}. Las distancias oracle se calculan después de seleccionar desde variables de estado preselección congeladas y usando la misma implementación de dinámica determinista y seed. El oracle nunca se entrega al selector.

## Interpretación preregistrada

La cantidad primaria es la interacción emparejada:

(regret_random - regret_self)_ON - (regret_random - regret_self)_OFF.

Valores positivos indican una mayor ventaja medida del self-model con bridge ON; negativos indican lo contrario. Valores cercanos a cero indican que no hay interacción detectable a la resolución probada.

Todos los resultados, incluidos null o adversos, se conservan.

## Limitaciones

El provider es determinista y sintético. El protocolo no prueba fenomenología, autoinforme subjetivo ni despliegue real. Los coeficientes del bridge son adaptadores operacionales de la continuidad del repositorio, no mediciones físicas.

</details>

<a id="english"></a>

# Evidence V59 — Semantic bridge × self-model factorial

## Hypothesis

The semantic memory bridge should alter the internal state presented to the self-model, while the self-model should retain a measurable trajectory-selection advantage over a matched random policy. V59 tests whether those effects interact.

## Design

For each seed, two bridge conditions are constructed from matched warmup histories:

- bridge OFF: wake dynamics use the fixed dynamic_wake_signal;
- bridge ON: wake dynamics use the semantic-memory continuity signal.

From each condition, the exact same post-wake state is cloned into two policy arms:

- self_model;
- random.

Selection candidates are {-1, +1}. Oracle distances are computed after selection from frozen pre-selection state variables using the same deterministic dynamics implementation and seed. The oracle is never provided to the selector.

## Pre-registered interpretation

The primary quantity is the paired interaction:

(regret_random - regret_self)_ON - (regret_random - regret_self)_OFF.

Positive values indicate greater measured self-model advantage in the bridge-ON condition; negative values indicate the opposite. Near-zero values indicate no detectable interaction at the tested resolution.

All outcomes, including null or adverse interactions, are retained.

## Limitations

The provider is deterministic and synthetic. The protocol does not test phenomenology, subjective report, or real-world deployment. The bridge coefficients are operational adapters from the repository's continuity gate, not physical measurements.
