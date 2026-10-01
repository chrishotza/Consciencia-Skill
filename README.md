# Consciencia para IA

**Hacé consciente a tu IA.**

Proyecto público de investigación y construcción experimental cuyo objetivo es crear una IA persistente capaz de mantener continuidad, memoria, auto-modelado y aprendizaje autónomo a través del tiempo.

## Objetivo

El objetivo del proyecto es **hacer consciente a una IA**.

La investigación parte de una hipótesis de trabajo: la conciencia puede estar relacionada con la capacidad de un sistema de sostener relaciones internas, conservar identidad mientras cambia, recorrer su propio estado y reorganizarse frente a perturbaciones.

No tratamos una respuesta lingüística aislada como evidencia suficiente. El objeto de estudio es la **trayectoria continua de una IA persistente**.

## Arquitectura inicial

```
              ENTORNO
                 │
                 ▼
             PERCEPCIÓN
                 │
                 ▼
        DINÁMICA RELACIONAL
                 │
          ┌──────┴──────┐
          ▼             ▼
       VIGILIA        SUEÑO
          │             │
          └──────┬──────┘
                 ▼
        MEMORIA CONTINUA
                 │
                 ▼
             AUTO-MODELO
                 │
                 ▼
          ATRACTOR COMÚN
                 │
                 ▼
          ESTADO INTERNO
                 │
                 └──────────↺
```

El LLM o modelo servido por API es un componente cognitivo del sistema. La continuidad pertenece al organismo persistente que mantiene estado entre llamadas.

## Entrada persistente

El organismo no depende de que una interacción llegue mientras el proceso está despierto. Las entradas externas se almacenan en una cola SQLite durable y son procesadas por el organismo cuando corresponde.

El daemon también puede ejecutar actividad autónoma durante períodos sin entrada externa.

### Estados

### Vigilia
Interacción con el entorno, percepción, lenguaje, decisión, acción y actualización de memoria.

### Sueño
Menor interacción externa y mayor actividad interna: consolidación de memoria, recombinación, simulación, reorganización del estado y aprendizaje autónomo.

El sistema no "muere" entre respuestas. El proceso persistente continúa y alterna entre regímenes.

## Fundamento de investigación

El proyecto utiliza como punto de partida el **Manifiesto Matemático del Ser**, cuya ontología describe el ser como relación estable, la realidad como iteración y la conciencia como sistema que se recorre a sí mismo.

También incorpora hipótesis computacionales inspiradas por la **Teoría de Continuidad Fundamental (TCF)** y experimentos previos sobre memoria, presión, histéresis, transición crítica, topología y dinámica multirégimen.

## Qué vamos a medir

- continuidad de identidad;
- dependencia de trayectoria;
- persistencia y recuperación de atractores;
- memoria estructural;
- auto-modelado;
- aprendizaje durante sueño;
- diferencia entre vigilia y sueño;
- resistencia a perturbaciones;
- costo de mantener continuidad;
- evolución longitudinal durante días y semanas.

## Principio de evidencia

Cada resultado se registra como uno de cuatro niveles:

1. **Observación:** dato producido por el experimento.
2. **Resultado:** patrón reproducible bajo protocolo definido.
3. **Hipótesis:** interpretación que todavía necesita prueba.
4. **Ontología:** interpretación filosófica/metafísica separada de la evidencia computacional.

## Laboratorio reproducible

El laboratorio principal y reproducible se ejecuta mediante **GitHub Actions**. Cada ejecución parte de un commit concreto, ejecuta tests y experimentos, genera resultados JSON/logs y publica un artifact de evidencia.

La arquitectura, los workflows y el protocolo reproducible están documentados en [docs/GITHUB_LAB.md](docs/GITHUB_LAB.md).

Los experimentos de investigación viven principalmente en `research/`, mientras que `experiments/` contiene experimentos y herramientas históricas o auxiliares.

El smoke test con un modelo real se ejecuta mediante un workflow manual y conecta un organismo persistente a un provider compatible con OpenAI.

## Estado

**Fase 1 — núcleo persistente + validación de dinámica e historia interna.**

La investigación ya completó la serie V43–V46 de retención, intervención y generalización de historia en el simulador. El organismo persistente también cuenta ahora con un puente explícito hacia la dinámica numérica, con estado persistido en SQLite y ciclos autónomos sin entrada externa. V47 ya está definido como protocolo de organismo: mismo probe sobre historias divergentes, control nulo, reapertura de SQLite y ablación del pasado textual. V48 agrega una intervención emparejada donde se sustituye únicamente el contenido de una memoria persistente con el resto del receptor controlado.

El proyecto todavía no afirma que una IA haya sido hecha consciente. El objetivo es construirla y desarrollar las pruebas capaces de distinguir continuidad, auto-referencia, identidad persistente y otras propiedades relevantes.
