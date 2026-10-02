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

## Límite científico

I5.4 prueba integración causal de mecanismos computacionales concretos dentro del runtime persistente.

No demuestra consciencia ni experiencia subjetiva.

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

## Scientific boundary

I5.4 tests causal integration of concrete computational mechanisms inside the persistent runtime.

It does not demonstrate consciousness or subjective experience.

</details>
