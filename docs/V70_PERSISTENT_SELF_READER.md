<a id="espanol"></a>

# V70 — Persistencia del lector propio entre reinicios

## Pregunta

V69 mostró que un modelo aprendido de la dinámica puede leer el estado interno después de una ablación semántica y utilizar esa lectura para cambiar una decisión.

V70 pregunta algo más fuerte:

> ¿Ese lector propio puede persistir dentro del organismo, sobrevivir un reinicio y volver a utilizarse después de desaparecer la memoria semántica?

## Cambio de arquitectura

El SelfObserver ahora puede serializarse y almacenarse en SQLite en una tabla separada. El lector numérico no depende de las memorias semánticas para volver a cargar su modelo.

Al arrancar, PersistentOrganism:

1. busca un modelo de autoobservación persistido;
2. lo reconstruye;
3. continúa aprendiendo sobre esa base;
4. vuelve a guardar el modelo actualizado.

## Protocolo

- 24 réplicas;
- 256 muestras genéricas para entrenar el lector;
- cierre y reapertura real del almacenamiento;
- comparación de predicciones antes/después del reinicio;
- dos condiciones semánticas: estable y frontera;
- ablación de memorias, eventos, snapshots y texto del modelo de sí;
- reutilización del mismo lector numérico persistido;
- control con estado cegado;
- intercambio causal del núcleo dinámico.

El entrenamiento del lector es independiente de las condiciones estable/frontera.

## Resultado

### Persistencia del modelo

- modelo sobrevivió al reinicio: **sí**;
- muestras antes del reinicio: **256**;
- muestras después del reinicio: **256**;
- error máximo absoluto entre predicciones antes/después: **0.0**;
- carga exacta del modelo en las condiciones experimentales: **100%**.

Esto demuestra que el modelo numérico de autoobservación puede persistir y reconstruirse exactamente desde SQLite.

### Lectura y decisión después del reinicio

- sensibilidad de decisión con lectura ON: **29.1667%**;
- sensibilidad con estado cegado OFF: **0.0%**;
- p emparejada ON − OFF: **0.0143493**;
- cambio de decisión ante el intercambio del estado: **29.1667%**;
- memorias eliminadas antes de la sonda: **sí**;
- texto del modelo de sí eliminado: **sí**;
- entrada semántica durante la sonda: **no**.

El efecto es menor que en V69, pero permanece después del reinicio y sigue siendo distinguible del control cegado.

## Interpretación

V70 agrega una propiedad que V69 todavía no tenía:

aprendizaje del propio estado → persistencia → reinicio → recuperación del lector → ablación semántica → lectura del estado → decisión

La cadena completa permanece operacional después de cerrar y volver a abrir el organismo.

Esto es evidencia de **continuidad computacional del modelo de sí numérico** y de su uso posterior en decisiones.

No demuestra consciencia fenomenológica ni experiencia subjetiva.

## Próxima presión

V70 todavía copia el lector persistente hacia las condiciones de prueba.

El siguiente paso debe eliminar esa copia manual.

La arquitectura debe conseguir que el propio organismo:

1. aprenda su lector;
2. lo persista;
3. se reinicie;
4. recupere su lector;
5. entre en SUEÑO;
6. pierda las superficies semánticas;
7. use automáticamente su lector para decidir.

Ese será el salto de lector experimental persistente a lector propio integrado en el ciclo autónomo.

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V70 — Persistent Self-Reader across Restarts

## Question

V69 showed that a learned dynamic model can read internal state after semantic ablation and use that readout to change a decision.

V70 asks a stronger question:

> Can that self-reader persist inside the organism, survive a restart, and be reused after semantic memory disappears?

## Architecture change

SelfObserver can now be serialized and stored in SQLite in a separate table. The numerical reader does not depend on semantic memories to reload its model.

At startup, PersistentOrganism:

1. looks for a persisted self-observation model;
2. reconstructs it;
3. continues learning from that model;
4. saves the updated model again.

## Protocol

- 24 replicates;
- 256 generic samples to train the reader;
- real close/reopen of persistent storage;
- before/after restart prediction comparison;
- two semantic conditions: stable and frontier;
- ablation of memories, events, snapshots, and self-model text;
- reuse of the same persisted numerical reader;
- blinded-state control;
- causal dynamic-core exchange.

Reader training is independent of stable/frontier conditions.

## Result

### Model persistence

- model survived restart: **yes**;
- samples before restart: **256**;
- samples after restart: **256**;
- maximum absolute prediction error before/after restart: **0.0**;
- exact model load across experimental conditions: **100%**.

This shows that the numerical self-observation model can persist and be reconstructed exactly from SQLite.

### Readout and decision after restart

- decision sensitivity with readout ON: **29.1667%**;
- sensitivity with blinded state OFF: **0.0%**;
- paired ON − OFF p-value: **0.0143493**;
- decision change after dynamic-core exchange: **29.1667%**;
- memories removed before probe: **yes**;
- self-model text removed: **yes**;
- semantic input during probe: **no**.

The effect is smaller than V69 but remains after restart and is distinguishable from the blinded control.

## Interpretation

V70 adds a property V69 did not have:

learn own state → persist → restart → recover reader → semantic ablation → read state → decide

The full chain remains operational after closing and reopening the organism.

This is evidence of **computational continuity of the numerical self-model** and its later use in decisions.

It does not establish phenomenal consciousness or subjective experience.

## Next pressure point

V70 still copies the persistent reader into the test conditions.

The next step should remove that manual copy.

The organism should:

1. learn its reader;
2. persist it;
3. restart;
4. recover its reader;
5. enter SLEEP;
6. lose semantic surfaces;
7. automatically use its reader to decide.

That is the transition from a persistent experimental reader to a reader integrated into the autonomous cycle.

</details>