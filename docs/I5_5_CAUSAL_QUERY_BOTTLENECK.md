# I5.5 — Causal Query Bottleneck

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.5 rediseña el punto débil observado en I5.4: la consulta dependiente del estado era observable dentro de `PersistentOrganism`, pero no era funcionalmente necesaria para la conducta bajo el mapeo probado.

La nueva hipótesis es explícita:

`estado global → consulta → cuello de botella de acceso → atención → lectura → acción`

La información de módulos no seleccionados debe quedar fuera del readout cuando el bottleneck está activo.

## Diseño

Cuatro módulos objetivo (2–5) contienen señales de acción. Un código bidimensional identifica cuál módulo es relevante. Los otros módulos son distractores con la señal opuesta.

El mecanismo usa:

- `StateDependentQuery` para seleccionar el módulo;
- `AttentionSchema` para asignar recursos;
- un bottleneck que enmascara módulos no consultados;
- un readout de acción basado únicamente en la información accesible.

## Controles

- **FULL** — query real + atención real + bottleneck;
- **SHUFFLED_QUERY**;
- **ZERO_QUERY**;
- **RANDOM_QUERY**;
- **SHUFFLED_ATTENTION**;
- **LESION_TARGET** — lesión funcional del contenido objetivo;
- **NO_BOTTLENECK** — acceso a todos los módulos.

## Endpoint primario

FULL menos SHUFFLED_QUERY en accuracy de acción.

Endpoints secundarios:

- FULL menos ZERO_QUERY;
- FULL menos RANDOM_QUERY;
- FULL menos SHUFFLED_ATTENTION;
- FULL menos LESION_TARGET;
- FULL menos NO_BOTTLENECK;
- accuracy de consulta FULL;
- masa de atención sobre el objetivo.

Se usan 512 episodios y 20.000 permutaciones sign-flip.

## Límite científico

Este protocolo prueba un mecanismo combinado de consulta dependiente del estado y cuello de botella atencional.

No demuestra consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

## Objective

I5.5 redesigns the weakness identified in I5.4: state-dependent querying was observable inside `PersistentOrganism`, but was not functionally necessary for behavior under the tested mapping.

The new hypothesis is explicit:

`global state → query → access bottleneck → attention → readout → action`

Information from non-selected modules must be excluded from the readout when the bottleneck is active.

## Design

Four target modules (2–5) contain action signals. A two-dimensional code identifies the relevant module. The other modules are distractors carrying the opposite signal.

The mechanism uses:

- `StateDependentQuery` for module selection;
- `AttentionSchema` for resource allocation;
- a bottleneck masking non-queried modules;
- an action readout based only on accessible information.

## Controls

- **FULL** — real query + real attention + bottleneck;
- **SHUFFLED_QUERY**;
- **ZERO_QUERY**;
- **RANDOM_QUERY**;
- **SHUFFLED_ATTENTION**;
- **LESION_TARGET** — functional lesion of the target content;
- **NO_BOTTLENECK** — access to all modules.

## Primary endpoint

FULL minus SHUFFLED_QUERY action accuracy.

Secondary endpoints:

- FULL minus ZERO_QUERY;
- FULL minus RANDOM_QUERY;
- FULL minus SHUFFLED_ATTENTION;
- FULL minus LESION_TARGET;
- FULL minus NO_BOTTLENECK;
- FULL query accuracy;
- target attention mass.

512 episodes and 20,000 sign-flip permutations are used.

## Scientific boundary

This protocol tests a combined state-dependent query and attention-bottleneck mechanism.

It does not demonstrate consciousness or subjective experience.

</details>
