# I5.4 — Persistent Selective Access Integration

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.4 integra en el **PersistentOrganism** los dos mecanismos aislados recién verificados:

`estado global → consulta dependiente del estado → distribución de atención → acceso selectivo → selección de trayectoria`

La prueba busca determinar si esa cadena puede modificar causalmente la selección de trayectoria dentro del runtime persistente y si sus observables sobreviven a reinicio.

## Qué se integra

- workspace global acotado de I5.0/I5.1;
- consulta dependiente del estado de I5.2;
- distribución de atención de I5.3;
- lectura del valor del módulo consultado;
- modulación de la puntuación de cada trayectoria candidata mediante el acceso selectivo.

La integración es opt-in mediante:

- `workspace_selective_access_enabled`;
- `workspace_selective_access_query_mode`;
- `workspace_selective_access_attention_mode`;
- `workspace_selective_access_weight`.

El comportamiento histórico permanece sin cambios cuando la opción está desactivada.

## Controles

Cada réplica parte del mismo checkpoint calibrado:

- **FULL** — query real + atención real;
- **SHUFFLED_QUERY** — broadcast del query con coordenadas intercambiadas;
- **SHUFFLED_ATTENTION** — atención reordenada;
- **ZERO_QUERY** — broadcast del query fijado a cero;
- **RANDOM_QUERY** — código de consulta aleatorio;
- **LESION_QUERY** — broadcast reconstruido excluyendo el origen lesionado configurado.

## Endpoints

Endpoint primario:

`SHUFFLED_QUERY regret − FULL regret`

Endpoints secundarios:

- costo de regret para SHUFFLED_ATTENTION;
- costo de regret para ZERO_QUERY;
- costo de regret para RANDOM_QUERY;
- costo de regret para LESION_QUERY;
- tasa de cambio de acción frente a FULL;
- persistencia exacta de módulo consultado, distancia, pesos de atención y contador.

Se usan 24 réplicas, 24 ciclos de warmup, señales candidatas `(-1, +1)` y 20.000 permutaciones sign-flip por contraste.

## Resultado verificado

Workflow: **36986823516**; artifact: **11217906875**; commit experimental: **27f08ab3d84633986a609a7981429cf6f3fe0cf5**; seed **20261004**; 24 réplicas; 24 ciclos de warmup.

Endpoints:

- SHUFFLED_QUERY regret cost: **0.0**, p **1.0**; action-change **0%**;
- SHUFFLED_ATTENTION regret cost: **+0.0280384**, p **0.5022**; action-change **20.83%**;
- ZERO_QUERY regret cost: **0.0**, p **1.0**; action-change **0%**;
- RANDOM_QUERY regret cost: **0.0**, p **1.0**; action-change **0%**;
- LESION_QUERY regret cost: **0.0**, p **1.0**; action-change **0%**;
- FULL attention mass mean: **0.69550**;
- FULL selective-access strength mean: **0.30500**;
- exact persistence of I5.4 observables: **100%**.

Interpretación: **resultado nulo/mixto bajo el protocolo probado**. El mecanismo integrado es operativo y sus observables persisten exactamente, pero los controles de consulta no cambiaron la selección de trayectoria ni el regret. La reasignación de atención sí cambió la acción en 20.83% de las réplicas, pero el costo de regret no fue significativo. Por tanto, la cadena completa estado→consulta→atención→acceso→acción no mostró una separación funcional robusta en este harness.

### Límite científico

I5.4 demuestra integración computacional y persistencia de los mecanismos probados, pero no una necesidad funcional de la consulta para la conducta bajo este mapeo. No demuestra consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

## Objective

I5.4 integrates the two newly verified standalone mechanisms into **PersistentOrganism**:

`global state → state-dependent query → attention distribution → selective access → trajectory selection`

The test asks whether this chain can causally modify trajectory selection inside the persistent runtime and whether its observables survive restart.

## Integrated mechanism

- bounded global workspace from I5.0/I5.1;
- state-dependent query from I5.2;
- attention distribution from I5.3;
- readout of the queried module value;
- modulation of candidate-trajectory score by selective access.

The integration is opt-in through:

- `workspace_selective_access_enabled`;
- `workspace_selective_access_query_mode`;
- `workspace_selective_access_attention_mode`;
- `workspace_selective_access_weight`.

Historical behavior remains unchanged when disabled.

## Controls

Each replicate starts from the same calibrated checkpoint:

- **FULL** — real query + real attention;
- **SHUFFLED_QUERY** — query broadcast coordinates exchanged;
- **SHUFFLED_ATTENTION** — attention distribution reordered;
- **ZERO_QUERY** — query broadcast clamped to zero;
- **RANDOM_QUERY** — random query code;
- **LESION_QUERY** — query broadcast rebuilt after excluding the configured lesion source.

## Endpoints

Primary endpoint:

`SHUFFLED_QUERY regret − FULL regret`

Secondary endpoints:

- regret cost for SHUFFLED_ATTENTION;
- regret cost for ZERO_QUERY;
- regret cost for RANDOM_QUERY;
- regret cost for LESION_QUERY;
- action-change rate versus FULL;
- exact persistence of queried module, distance, attention weights, and step count.

The protocol uses 24 replicates, 24 warmup cycles, candidate signals `(-1, +1)`, and 20,000 sign-flip permutations per contrast.

## Verified result

Workflow: **36986823516**; artifact: **11217906875**; experimental commit: **27f08ab3d84633986a609a7981429cf6f3fe0cf5**; seed **20261004**; 24 replicates; 24 warmup cycles.

Endpoints:

- SHUFFLED_QUERY regret cost: **0.0**, p **1.0**; action-change **0%**;
- SHUFFLED_ATTENTION regret cost: **+0.0280384**, p **0.5022**; action-change **20.83%**;
- ZERO_QUERY regret cost: **0.0**, p **1.0**; action-change **0%**;
- RANDOM_QUERY regret cost: **0.0**, p **1.0**; action-change **0%**;
- LESION_QUERY regret cost: **0.0**, p **1.0**; action-change **0%**;
- FULL mean attention mass: **0.69550**;
- FULL mean selective-access strength: **0.30500**;
- exact I5.4 observable persistence: **100%**.

Interpretation: **null/mixed result under the tested protocol**. The integrated mechanism is operational and its observables persist exactly, but query controls did not change trajectory selection or regret. Attention reassignment changed the action in 20.83% of replicates, but regret cost was not significant. Therefore the full state→query→attention→access→action chain did not show a robust functional separation in this harness.

### Scientific boundary

I5.4 demonstrates computational integration and persistence of the tested mechanisms, but not functional necessity of state-dependent querying for behavior under this mapping. It does not demonstrate consciousness or subjective experience.

</details>
