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
- El contenido de los cuatro objetivos se mantiene fuera de la decisión de consulta.

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

## Resultado verificado

Artifact de GitHub Actions:

- workflow run: **36984675391**;
- artifact: **11216743506**;
- commit experimental: **0b857f7c93e5a7112b184840f36994712aed2967**;
- seed: **20261002**;
- episodios: **512**.

Endpoints:

- accuracy FULL: **1.0**;
- FULL − SHUFFLED: **+1.0**, p **4.99975×10⁻⁵**;
- FULL − ZERO: **+0.771484375**, p **4.99975×10⁻⁵**;
- FULL − RANDOM: **+0.7421875**, p **4.99975×10⁻⁵**;
- accuracy después de LESION: **0.236328125**;
- FULL − LESION: **+0.763671875**, p **4.99975×10⁻⁵**;
- tasa de cambio de consulta dependiente del estado: **1.0**.

Interpretación: bajo este arnés sintético, el estado global implementado controló de forma reproducible la selección del siguiente módulo. La caída pronunciada tras la lesión del origen seleccionado aporta una intervención causal dentro del mecanismo probado.

## Límite científico

El resultado verifica un mecanismo computacional independiente para acceso selectivo dependiente del estado.

No demuestra consciencia ni experiencia subjetiva, no valida por sí mismo una arquitectura completa de Global Workspace y no sustituye la integración del mecanismo dentro de `PersistentOrganism`.

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
- Target contents are kept outside the query-selection decision.

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

## Verified result

GitHub Actions artifact:

- workflow run: **36984675391**;
- artifact: **11216743506**;
- experimental commit: **0b857f7c93e5a7112b184840f36994712aed2967**;
- seed: **20261002**;
- episodes: **512**.

Endpoints:

- FULL accuracy: **1.0**;
- FULL − SHUFFLED: **+1.0**, p **4.99975×10⁻⁵**;
- FULL − ZERO: **+0.771484375**, p **4.99975×10⁻⁵**;
- FULL − RANDOM: **+0.7421875**, p **4.99975×10⁻⁵**;
- LESION query accuracy: **0.236328125**;
- FULL − LESION: **+0.763671875**, p **4.99975×10⁻⁵**;
- state-dependent query-change rate: **1.0**.

Interpretation: under this synthetic harness, the implemented global state reproducibly controlled selection of the next module. The large post-lesion drop provides a causal intervention within the tested mechanism.

## Scientific boundary

The result verifies a standalone computational mechanism for state-dependent selective access.

It does not demonstrate consciousness or subjective experience, does not by itself validate a complete Global Workspace architecture, and does not replace integration of the mechanism into `PersistentOrganism`.

</details>
