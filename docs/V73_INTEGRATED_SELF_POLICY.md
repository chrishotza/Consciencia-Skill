<a id="espanol"></a>

# V73 — Política propia integrada en el organismo persistente

## Pregunta

V72 mostró que una política puede aprender a utilizar variables del modelo de sí bajo un objetivo de continuidad definido externamente.

V71 llevó el lector persistente hacia el ciclo autónomo.

V73 mueve esa política desde el experimento aislado hacia el organismo persistente.

> ¿Puede el organismo guardar su propia política junto a su modelo de sí, reiniciarse, entrar en SUEÑO y utilizar automáticamente esa política para seleccionar una trayectoria después de una ablación semántica?

## Cambio arquitectónico

El organismo ahora dispone de una capa opcional SelfPolicy:

- persistida en SQLite;
- recuperada durante el arranque;
- evaluada durante autonomous_wake_cycle();
- seleccionada antes que la política fija cuando self_policy_enabled=True.

La funcionalidad queda desactivada por defecto para no alterar los protocolos anteriores.

## Protocolo

Cada réplica:

1. entrena un SelfObserver;
2. entrena una SelfPolicy sobre características del propio modelo;
3. guarda ambos modelos dentro del SQLite del organismo;
4. introduce dos estados dinámicos controlados;
5. elimina las superficies semánticas;
6. reinicia el organismo;
7. recupera automáticamente modelo y política;
8. entra en SUEÑO;
9. ejecuta selección autónoma con SelfPolicy;
10. repite la prueba con el estado dinámico cegado;
11. intercambia el núcleo dinámico entre condiciones.

## Criterio

El endpoint principal es de integración funcional:

modelo de sí persistido + política persistida
→ reinicio
→ SUEÑO
→ ablación semántica
→ selección autónoma

Controles:

- estado dinámico cegado;
- intercambio causal del núcleo;
- política fija;
- ausencia de entrada semántica durante la sonda.

## Límite

El objetivo de utilidad continúa siendo externo al organismo.

Por tanto, un resultado positivo demostraría integración computacional de modelo de sí + política persistente + SUEÑO + selección, pero no que el sistema haya descubierto autónomamente sus propios valores ni que exista experiencia subjetiva.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V73 — Self-Policy Integrated into the Persistent Organism

## Question

V72 showed that a policy can learn to use self-model variables under an externally defined continuity objective.

V71 moved the persistent reader into the autonomous cycle.

V73 moves the policy from an isolated experiment into the persistent organism.

> Can the organism store its own policy alongside its self-model, restart, enter SLEEP, and automatically use that policy to select a trajectory after semantic ablation?

## Architectural change

The organism now has an optional SelfPolicy layer:

- persisted in SQLite;
- recovered during startup;
- evaluated during autonomous_wake_cycle();
- selected ahead of the fixed policy when self_policy_enabled=True.

The capability remains disabled by default so previous protocols are not altered.

## Protocol

Each replicate:

1. trains a SelfObserver;
2. trains a SelfPolicy on features of that self-model;
3. stores both models in the organism SQLite database;
4. introduces two controlled dynamic states;
5. removes semantic surfaces;
6. restarts the organism;
7. automatically recovers model and policy;
8. enters SLEEP;
9. performs autonomous selection with SelfPolicy;
10. repeats the test with blinded dynamic state;
11. exchanges the dynamic core between conditions.

## Criterion

The primary endpoint is functional integration:

persisted self-model + persisted policy
→ restart
→ SLEEP
→ semantic ablation
→ autonomous selection

Controls:

- blinded dynamic state;
- causal core exchange;
- fixed policy;
- no semantic input during the probe.

## Evidence boundary

The utility objective remains external to the organism.

A positive result would therefore demonstrate computational integration of self-model + persistent policy + SLEEP + selection, but not that the system autonomously discovered its own values or that subjective experience exists.

</details>