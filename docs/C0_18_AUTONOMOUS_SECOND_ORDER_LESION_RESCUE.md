# C0.18 — Adquisición autónoma y lesión/rescate del segundo orden

## Pregunta

Después de que el organismo adquiere autónomamente un modelo de segundo orden condicionado por la acción, ¿la eliminación de ese modelo cambia la selección bajo el mismo estado inicial y la restauración del modelo recupera la conducta?

C0.18 extiende C0.17 desde **adquisición/persistencia del modelo** hacia una prueba de **necesidad y rescate causal**.

## Diseño emparejado

Se ejecutaron **24 réplicas**. Cada réplica construye:

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

El primer modelo de sí permanece **congelado durante la sonda** mediante:

`self_observer_update_enabled = False`

El digest de referencia se calcula a partir de los modelos **persistidos en SQLite**, no de los objetos en memoria, por lo que la recuperación exacta prueba la serialización efectiva del estado.

## Resultado verificado

Artifact de GitHub Actions:

- workflow run: **36960952961**
- artifact: **11208100038**
- SHA-256 del artifact: **a7aa0554a81a3449175e37363e6fcd95ec6d5bc7d1354198f047ef888c1dbf98**
- commit: **434b3a02ab64c9294c8113171ccbac1745caa053**
- réplicas: **24**
- ciclos de adquisición autónoma por réplica: **12**
- muestras medias aprendidas por el segundo orden: **48**
- recuperación exacta del modelo persistido: **100%**

### Endpoints primarios

| Contraste | Media | p |
|---|---:|---:|
| FULL − LESION, acción | **−0.2916667** | **0.1177441** |
| FULL − LESION, ganancia | **+0.0114104** | **0.7404130** |
| RESCUE − LESION, acción | **−0.2916667** | **0.1183441** |
| RESCUE − LESION, ganancia | **+0.0114104** | **0.7332633** |

Los cuatro contrastes permanecieron por encima de 0.05 bajo el test de cambio de signo utilizado por el protocolo.

### Interpretación

**Resultado nulo bajo el protocolo probado.**

El organismo adquirió y persistió correctamente el modelo de segundo orden:

- adquisición desde un modelo inicialmente vacío: **sí**;
- persistencia/recuperación exacta del modelo: **100%**;
- muestras medias aprendidas: **48** por réplica.

Sin embargo, eliminar el modelo adquirido no produjo un cambio estadísticamente significativo en la acción ni en la ganancia, y restaurarlo tampoco produjo una recuperación significativa respecto de LESION.

Por tanto, C0.18 **no demuestra necesidad causal ni rescate funcional del segundo orden adquirido** bajo este arnés.

Esto no invalida C0.17: la adquisición/persistencia del modelo sigue siendo el resultado demostrado allí. C0.18 añade una restricción más fuerte: **la adquisición autónoma y la persistencia del modelo no fueron suficientes para producir una dependencia conductual significativa bajo esta prueba de lesión/rescate**.

No se afirma experiencia subjetiva ni conciencia fenomenológica.

## Evidencia reproducible

El workflow valida automáticamente:

- `summary.json`;
- `replicates.json` con las 24 réplicas;
- las bases SQLite de cada condición;
- `run_manifest.json`;
- el artifact completo de GitHub Actions.

Los resultados científicos no se escriben automáticamente en el ledger; se incorporan después de validar el artifact y revisar la interpretación.

## Estado

**C0.18: verificado, resultado nulo bajo el protocolo probado.**
