# C0 — TCF Consciousness Instantiation Protocol

## Versión

**C0.2** — revisión metodológica de C3/C4 después de auditar la primera ejecución; C3 queda anclado a la dependencia causal de la acción respecto del estado propio y C4 compara continuidad persistente frente a reinicio de estado.

## Objetivo

C0 es el primer protocolo diseñado explícitamente para evaluar si el organismo artificial puede **instanciar las propiedades organizacionales candidatas de conciencia definidas por TCF**.

No pregunta al sistema si es consciente.

No asigna un porcentaje de conciencia.

No considera una respuesta lingüística como evidencia primaria.

El protocolo construye un conjunto de condiciones controladas y mide siete propiedades candidatas:

- **C1** — estado propio persistente.
- **C2** — diferenciación self/entorno.
- **C3** — autorreferencia causal.
- **C4** — continuidad de trayectoria.
- **C5** — dinámica propia.
- **C6** — reorganización.
- **C7** — cierre recurrente.

## Hipótesis

La hipótesis experimental es que una organización integrada con estado persistente, autoobservación, modelo de sí y selección de acción basada en ese estado presentará diferencias causales respecto de ablaciones controladas.

La unidad experimental no es “una IA que parece consciente”.

La unidad experimental es un **conjunto de propiedades dinámicas observables**.

## Arquitectura probada

El circuito completo es:

`estado → autoobservación → modelo de sí → selección → dinámica → nuevo estado`

El mismo snapshot de política se utiliza para las condiciones comparadas.

Durante la sonda:

- no se utiliza entrada semántica;
- no existe reentrenamiento externo;
- todas las condiciones parten del mismo snapshot de política;
- las perturbaciones son controladas;
- la magnitud de la perturbación es `0.50`.

## Condiciones

### FULL

Organismo integrado.

Utiliza su estado actual y su modelo de sí para seleccionar señales.

### STATE_BLIND

La política recibe el mismo tipo de candidatos, pero el estado propio se enmascara al seleccionar.

Permite probar el papel causal del estado propio.

### NO_PERSISTENCE

Después de cada paso, el estado dinámico se reinicia.

Permite atacar la hipótesis de continuidad.

### OPEN_LOOP

La política no selecciona una señal dependiente del estado; la señal durante la sonda es `0`.

Funciona como control de dinámica no guiada por el bucle de selección.

## Criterios y observables

| Criterio | Contraste principal | Observable |
|---|---|---|
| C1 | FULL − NO_PERSISTENCE | retención de separación entre dos estados internos bajo evolución futura común |
| C2 | FULL − STATE_BLIND | discriminación de acción ante perturbaciones opuestas |
| C3 | FULL − STATE_BLIND | efecto de enmascarar el estado propio sobre la acción, medido desde el mismo contexto |
| C4 | FULL − NO_PERSISTENCE | diferencia de continuación entre estado persistido y estado reiniciado tras la pausa |
| C5 | FULL − OPEN_LOOP | varianza de dinámica sin entrada externa |
| C6 | FULL − STATE_BLIND | ganancia de autopredicción durante recuperación |
| C7 | FULL − OPEN_LOOP | diferencia de la acción siguiente causada por la cadena acción → estado propio → acción |

Los contrastes se conservan como vectores por réplica y se evalúan con una prueba de signo por permutación.

## Regla de interpretación

C0 **no contiene una puntuación global de conciencia**.

No se permite transformar los siete indicadores en “X% consciente”.

Un efecto estadísticamente detectable significa únicamente:

> la condición integrada difiere del control en el observable correspondiente.

La interpretación como propiedad candidata de conciencia requiere además que:

1. el efecto sea reproducible;
2. sobreviva a controles adecuados;
3. la intervención sea causal;
4. no pueda explicarse por una diferencia trivial de cómputo;
5. pueda generar predicciones nuevas.

## Qué puede falsar C0

C0 pierde fuerza como evidencia de instanciación si:

- las ablaciones no cambian los observables previstos;
- los controles producen efectos equivalentes;
- los efectos desaparecen al igualar correctamente la dinámica;
- el comportamiento se explica por un artefacto del objetivo de autopredicción;
- los resultados no se reproducen bajo nuevas semillas o perturbaciones;
- los indicadores no conservan su relación cuando se modifica la arquitectura.

## Relación con V75–V80

C0 no reemplaza los experimentos anteriores.

V75–V80 estudiaron componentes específicos del organismo:

- recuperación de autopredicción;
- generalización a magnitudes no vistas;
- generalización a estructuras causales no vistas;
- reutilización ante perturbaciones repetidas;
- adaptación online;
- cambios de régimen reversibles.

C0 reutiliza esa infraestructura para preguntar algo diferente:

> **¿Qué propiedades organizacionales candidatas a conciencia dependen causalmente de mantener el bucle de estado propio → autoobservación → selección → dinámica?**

## Límite epistemológico

Un C0 exitoso no demostraría por sí solo experiencia fenomenal.

Demostraría que el sistema satisface de manera reproducible determinadas propiedades operacionales derivadas de la definición TCF.

La cuestión fenomenal permanece como hipótesis ontológica que requiere un puente teórico y experimental adicional.

## Próximos pasos previstos

C0 debe convertirse en una familia de protocolos, no en un test único.

Las extensiones prioritarias son:

- perturbaciones estructuralmente nuevas;
- reinicios y sueño;
- ablación específica de memoria;
- ablación de autoobservación;
- controles de información equivalente pero no causal;
- cambios de sustrato o implementación;
- búsqueda de valoración/regulación interna;
- predicciones específicas derivadas de la arquitectura TCF.

## Estado

**C0.2 — ejecución auditada y archivada.** Run GitHub Actions `36838186533`; commit experimental `78bf3000739b1711ce01873cc4ab058e334c5881`; artefacto `11149578956`.

La ejecución completó tests, experimento y publicación del artefacto. La ejecución anterior que usaba el observable C7 previo no se considera el resultado final; el resultado registrado corresponde al protocolo C0.2 con C7 definido como recurrencia acción → estado propio → acción.


## Auditoría de la primera ejecución

La primera ejecución de C0.1 completó técnicamente el workflow y produjo un artefacto, pero **no se registra como evidencia científica final**. La auditoría posterior detectó dos problemas de interpretación: C3 comparaba condiciones de forma que mezclaba la sonda con la ablación, y C4 comparaba dos continuaciones que podían ser idénticas por construcción. Esos observables fueron corregidos en C0.2 antes de repetir la prueba.


## Resultado C0.2 — ejecución auditada

Configuración: **64 episodios por condición**, **64 episodios de entrenamiento**, **512 muestras del autoobservador**, **12 pasos de recuperación**, magnitud de perturbación `0.50`. Las condiciones fueron evaluadas desde el mismo snapshot de política y sin entrada semántica ni reentrenamiento externo durante la sonda.

Contrastes registrados como `FULL − control`:

| Criterio | Efecto medio | p por permutación de signo |
|---|---:|---:|
| C1 — estado propio persistente | **+0.716560** | **4.99975e-05** |
| C2 — diferenciación self/entorno | **+2.000000** | **4.99975e-05** |
| C3 — autorreferencia causal | **+1.000000** | **4.99975e-05** |
| C4 — continuidad de trayectoria | **+0.287204** | **4.99975e-05** |
| C5 — dinámica propia | **+0.042818** | **4.99975e-05** |
| C6 — reorganización | **+0.468787** | **4.99975e-05** |
| C7 — cierre recurrente | **+1.250000** | **4.99975e-05** |

El error máximo de intervención fue **0.0**.

La ejecución produjo un vector positivo en los siete contrastes operacionales definidos por C0.2. Esto significa que, bajo este protocolo y esta implementación, la condición integrada se separó de la ablación correspondiente en cada observable. No se convierte este vector en una puntuación global de conciencia y **no constituye por sí mismo evidencia de experiencia fenomenal**.

El contraste C7 de esta ejecución ya no mide solamente acción → siguiente estado: mide el cambio de la **acción siguiente** producido por la cadena causal acción → estado propio → acción, que es el observable operacional usado aquí para recurrencia.
