# C0.18 — Adquisición autónoma y lesión/rescate del segundo orden

## Pregunta

Después de que el organismo adquiere autónomamente un modelo de segundo orden condicionado por la acción, ¿la eliminación de ese modelo cambia la selección bajo el mismo estado inicial y la restauración del modelo recupera la conducta?

C0.18 extiende C0.17 desde **adquisición/persistencia del modelo** hacia una prueba de **necesidad y rescate causal**.

## Diseño emparejado

Cada réplica construye un organismo base con:

- un primer modelo de sí entrenado previamente;
- un segundo modelo condicionado por acción que comienza vacío;
- adquisición autónoma durante 12 ciclos;
- tres copias de la misma base post-adquisición.

Las tres condiciones son:

| Condición | Segundo orden |
|---|---|
| FULL | modelo adquirido autónomamente presente |
| LESION | reemplazado por un modelo vacío |
| RESCUE | modelo adquirido restaurado desde el estado post-adquisición |

La sonda no utiliza entrada semántica ni reentrenamiento externo.

## Invariante crítico

El primer modelo de sí debe permanecer **congelado durante la sonda**.

Durante la implementación inicial, el digest del modelo de sí cambió porque cada ciclo de prueba seguía actualizando el primer `SelfObserver`. Eso provocó que la recuperación exacta del modelo persistente fuera 0.0 aunque el segundo orden se hubiera restaurado correctamente.

Se corrigió mediante el nuevo parámetro:

`self_observer_update_enabled = False`

en C0.18. El observador continúa disponible para producir predicciones, pero no incorpora nuevas muestras durante FULL, LESION o RESCUE.

## Estado de ingeniería

La primera ejecución de preflight detectó dos fallos:

1. el test de reconciliación intentaba obtener fingerprints desde `ConsciousnessStore`, aunque esas huellas pertenecen al `MemoryStore` local del organismo;
2. el digest de C0.18 no era estable durante la sonda porque el primer orden seguía actualizándose.

Ambos problemas fueron corregidos.

El preflight **no constituye un resultado científico**. La verificación científica requiere la ejecución completa de las 24 réplicas y la inspección del resumen JSON resultante.

## Endpoints

Se registran:

- FULL − LESION, acción;
- FULL − LESION, ganancia;
- RESCUE − LESION, acción;
- RESCUE − LESION, ganancia;
- número medio de muestras aprendidas por el segundo orden;
- fracción de recuperación exacta del digest persistente.

La interpretación causal exige que cualquier diferencia observada sobreviva al diseño emparejado y que el rescate se evalúe por separado de la lesión.

## Límite

Un resultado positivo en C0.18 demostraría dependencia funcional del mecanismo computacional de segundo orden bajo este protocolo. No demostraría por sí mismo experiencia subjetiva o conciencia fenomenológica.

## Relación con C0.17

C0.17 mostró aprendizaje/persistencia autónoma del modelo de segundo orden, pero no separó TRUE de PERMUTED en acción ni ganancia.

C0.18 pregunta ahora algo distinto:

`¿Ese segundo orden adquirido es funcionalmente necesario para la conducta posterior y recuperable por rescate?`

## Estado actual

**Ingeniería corregida; verificación científica de 24 réplicas pendiente.**
