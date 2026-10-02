# I5.6 — Persistent Query-Task Integration

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.6 lleva la cadena query+atención a un task interno del `PersistentOrganism` para responder directamente al resultado nulo de I5.4.

El objetivo no es introducir una nueva capacidad semántica, sino comprobar si una señal de acceso selectivo puede modificar la **acción real del organismo** cuando la tarea depende de información interna que debe ser consultada.

`estado persistente → target interno → query → atención → acceso → acción`

## Tarea interna

El controlador genera el target a partir del estado dinámico persistente:

- el módulo objetivo se deriva de `dynamic_steps` y memoria dinámica;
- la acción objetivo se deriva de presión/estado dinámicos y el paso;
- el routing code del target se construye con el codebook de I5.2 y perturbaciones derivadas del estado;
- módulos no objetivo contienen distractores con la acción opuesta.

El organismo no recibe el target desde el experimentador como una etiqueta externa.

## Controles

- **FULL** — query + atención + bottleneck;
- **SHUFFLED_QUERY**;
- **ZERO_QUERY**;
- **RANDOM_QUERY**;
- **SHUFFLED_ATTENTION**;
- **LESION_TARGET**;
- **NO_BOTTLENECK**.

## Endpoint primario

Accuracy de la acción real elegida por `PersistentOrganism`, FULL menos SHUFFLED_QUERY.

Endpoints secundarios:

- FULL menos ZERO_QUERY;
- FULL menos RANDOM_QUERY;
- FULL menos SHUFFLED_ATTENTION;
- FULL menos LESION_TARGET;
- FULL menos NO_BOTTLENECK;
- accuracy interna de query;
- masa de atención;
- persistencia exacta de los observables de la tarea tras reinicio.

Se declaran 24 réplicas, 24 warmup y 20.000 permutaciones sign-flip por contraste.

## Límite científico

Es una tarea instrumental interna para probar integración causal de query+atención dentro del runtime persistente.

No demuestra consciencia ni experiencia subjetiva, y el target generado por reglas internas no equivale a una meta emergente.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

## Objective

I5.6 brings the query+attention chain into an internal task of `PersistentOrganism` to directly address the null integration result from I5.4.

The goal is not a new semantic capability, but to test whether selective access can change the **actual organism action** when the task depends on internally generated information that must be queried.

`persistent state → internal target → query → attention → access → action`

## Internal task

The controller generates the target from persistent dynamic state:

- target module is derived from `dynamic_steps` and dynamic memory;
- target action is derived from dynamic pressure/state and step;
- target routing code is built from the I5.2 codebook plus state-derived perturbations;
- non-target modules contain distractors carrying the opposite action.

The organism is not handed the target as an external label by the experimenter.

## Controls

- **FULL** — query + attention + bottleneck;
- **SHUFFLED_QUERY**;
- **ZERO_QUERY**;
- **RANDOM_QUERY**;
- **SHUFFLED_ATTENTION**;
- **LESION_TARGET**;
- **NO_BOTTLENECK**.

## Primary endpoint

Actual `PersistentOrganism` action accuracy, FULL minus SHUFFLED_QUERY.

Secondary endpoints:

- FULL minus ZERO_QUERY;
- FULL minus RANDOM_QUERY;
- FULL minus SHUFFLED_ATTENTION;
- FULL minus LESION_TARGET;
- FULL minus NO_BOTTLENECK;
- internal query accuracy;
- attention mass;
- exact persistence of task observables after restart.

The protocol declares 24 replicates, 24 warmup cycles, and 20,000 sign-flip permutations per contrast.

## Scientific boundary

This is an instrumental internal task for testing causal query+attention integration inside the persistent runtime.

It does not demonstrate consciousness or subjective experience, and the rule-generated target is not an emergent goal.

</details>
