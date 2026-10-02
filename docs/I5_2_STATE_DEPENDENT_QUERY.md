# I5.2 — State-Dependent Workspace Query

<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

## Objetivo

I5.2 prueba GWT-4: si el **estado global** de un workspace puede determinar qué módulo debe consultarse a continuación.

La hipótesis ya no es simplemente broadcast → acción. Es:

`estado global → selección de consulta → acceso selectivo → información posterior`

## Diseño

Seis módulos participan.

- El módulo 0 contiene una clave de ruteo ruidosa.
- Los módulos 2–5 contienen cuatro posibles contenidos objetivo.
- El código del módulo 0 determina cuál de los cuatro módulos debe consultarse.
- El contenido de los cuatro objetivos se mantiene oculto hasta la consulta.

El workspace selecciona el módulo 0 y genera un broadcast de dos dimensiones. `StateDependentQuery` compara ese estado contra un codebook fijo y selecciona uno de los cuatro módulos.

## Controles

- **FULL** — consulta guiada por broadcast real.
- **SHUFFLED** — coordenadas del broadcast intercambiadas.
- **ZERO** — broadcast cero.
- **RANDOM** — módulo objetivo aleatorio.
- **LESION** — lesión del origen seleccionado antes de reconstruir el broadcast.

## Endpoint primario

Accuracy de consulta FULL menos SHUFFLED.

Endpoints secundarios:

- FULL menos ZERO;
- FULL menos RANDOM;
- FULL menos LESION;
- tasa de cambio de consulta cuando cambia el estado global.

Se usan 512 episodios emparejados y sign-flip de 20.000 permutaciones.

## Límite científico

Un resultado positivo mostraría que el estado global implementado puede controlar acceso selectivo posterior a módulos.

No demuestra consciencia ni experiencia subjetiva.

</details>

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

## Objective

I5.2 tests GWT-4: whether **global workspace state** can determine which module should be queried next.

The hypothesis is no longer simply broadcast → action. It is:

`global state → query selection → selective access → later information`

## Design

Six modules participate.

- Module 0 contains a noisy routing key.
- Modules 2–5 contain four possible target contents.
- The routing code determines which of the four modules should be queried.
- Target content remains hidden until the query.

The workspace selects module 0 and produces a two-dimensional broadcast. `StateDependentQuery` compares that state to a fixed codebook and selects one of the four target modules.

## Controls

- **FULL** — query guided by the real broadcast.
- **SHUFFLED** — broadcast coordinates swapped.
- **ZERO** — zero broadcast.
- **RANDOM** — random target module.
- **LESION** — lesion the selected source before rebuilding the broadcast.

## Primary endpoint

FULL minus SHUFFLED query accuracy.

Secondary endpoints:

- FULL minus ZERO;
- FULL minus RANDOM;
- FULL minus LESION;
- query-change rate when the global state changes.

512 paired episodes and 20,000 sign-flip permutations are used.

## Scientific boundary

A positive result would show that the implemented global state can control subsequent selective access to modules.

It would not demonstrate consciousness or subjective experience.

</details>