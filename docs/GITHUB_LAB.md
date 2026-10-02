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
