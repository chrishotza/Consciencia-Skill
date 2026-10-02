# Laboratorio GitHub

El laboratorio principal del proyecto se ejecuta mediante GitHub Actions. Colab queda como entorno auxiliar para análisis interactivo, visualización o experimentos que requieran intervención manual.

## Flujo reproducible

```
commit
  ↓
GitHub Actions
  ↓
pruebas
  ↓
experimentos
  ↓
results/*.json
  ↓
artefacto de evidencia
```

## Laboratorio de investigación

Workflow:

`.github/workflows/research.yml`

Se ejecuta en `push` sobre código relevante y también mediante `workflow_dispatch`.

Ejecuta:

1. pruebas del repositorio;
2. baseline dinámico;
3. validación de continuidad;
4. prueba de estrés longitudinal;
5. ablación del sueño;
6. recuperación de memoria;
7. manifiesto de ejecución;
8. publicación de artefactos.

Cada ejecución conserva el SHA del commit y los resultados producidos por ese código.

## Pruebas

Workflow:

`.github/workflows/tests.yml`

Se utiliza como verificación de pull requests.

## Protocolo C0.18 — segundo orden autónomo

Workflow:

`.github/workflows/organism-c0-18-autonomous-second-order.yml`

Ejecuta el test de esquema y una campaña de 24 réplicas emparejadas. Publica `summary.json`, `replicates.json`, las bases SQLite de las réplicas y un manifiesto de ejecución. El ledger científico no se actualiza automáticamente: el artifact se valida primero.

## Prueba manual con proveedor en vivo

Workflow:

`.github/workflows/live-provider-smoke.yml`

Es manual porque requiere secretos de un proveedor compatible con OpenAI:

- `ONTTO_API_KEY`
- `ONTTO_MODEL`
- `ONTTO_API_BASE_URL` (opcional; por defecto `https://api.openai.com/v1`)

Esta prueba no pretende demostrar consciencia. Comprueba que un modelo real puede funcionar como componente cognitivo del organismo y que este conserva trayectoria, memoria y transición VIGILIA/SUEÑO después de cerrar y reabrir el almacenamiento.

## Regla de interpretación

Los workflows pueden demostrar que un comportamiento computacional ocurrió bajo un protocolo reproducible.

No convierten automáticamente ese comportamiento en una afirmación de experiencia subjetiva. Esa distinción se mantiene explícita en los resultados.


<details>
<summary>🇺🇸 English — open</summary>

# GitHub Laboratory

The project's main laboratory runs through GitHub Actions. Colab remains an auxiliary environment for interactive analysis, visualization, or experiments that require manual intervention.

## Reproducible flow

```
commit
  ↓
GitHub Actions
  ↓
tests
  ↓
experiments
  ↓
results/*.json
  ↓
evidence artifact
```

## Research laboratory

Workflow:

`.github/workflows/research.yml`

It runs on `push` for relevant code and can also be launched with `workflow_dispatch`.

It executes:

1. repository tests;
2. dynamic baseline;
3. continuity validation;
4. longitudinal stress test;
5. sleep ablation;
6. memory recovery;
7. execution manifest;
8. artifact publication.

Each run preserves the commit SHA and the results produced by that code.

## Tests

Workflow:

`.github/workflows/tests.yml`

Used as pull-request verification.

## C0.18 — autonomous second order

Workflow:

`.github/workflows/organism-c0-18-autonomous-second-order.yml`

Runs the schema test and a 24-replica paired campaign. It publishes `summary.json`, `replicates.json`, replica SQLite databases, and a run manifest. The scientific ledger is not updated automatically: the artifact is validated first.

## Manual live-provider smoke test

Workflow:

`.github/workflows/live-provider-smoke.yml`

It is manual because it requires secrets for an OpenAI-compatible provider:

- `ONTTO_API_KEY`
- `ONTTO_MODEL`
- `ONTTO_API_BASE_URL` (optional; defaults to `https://api.openai.com/v1`)

This test does not attempt to demonstrate consciousness. It checks whether a real model can act as the organism's cognitive provider while the runtime preserves trajectory, memory, and WAKE/SLEEP transition after closing and reopening storage.

## Interpretation rule

Workflows can demonstrate that a computational behavior occurred under a reproducible protocol.

They do not automatically convert that behavior into a claim of subjective experience. That distinction remains explicit in the results.


</details>

> 🌐 Language convention: [docs/LANGUAGE.md](LANGUAGE.md)
