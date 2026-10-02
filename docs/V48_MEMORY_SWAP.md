<a id="espanol"></a>

# V48 — Intervención emparejada de intercambio de memoria

## Pregunta

¿Puede un organismo persistente respaldado por un LLM cambiar su respuesta ante la misma sonda cuando se modifica el contenido de su memoria persistente mientras el resto del estado del receptor permanece fijo?

## Intervención

Se inicializa una única base de datos receptora con un espacio de memoria.

Se crean dos copias idénticas byte por byte.

- MEMORY_A: ALFA → AMBAR
- MEMORY_B: ALFA → VIOLETA

Solo se modifica el campo de contenido de la fila de memoria existente.

Antes de la sonda se mantienen fijos:

- estado dinámico numérico;
- memoria dinámica;
- presión dinámica;
- cantidad de pasos dinámicos;
- distancia al atractor;
- modelo de sí;
- último pensamiento;
- flujo de eventos;
- identidad, importancia y marca temporal de la fila de memoria;
- configuración del receptor.

El contexto del LLM utiliza event_limit=0 y memory_limit=1, por lo que la sonda recibe el elemento de memoria como único canal textual histórico.

## Observable principal

Se presenta la misma sonda en ambas condiciones. El resultado principal es si CHOICE cambia entre MEMORY_A y MEMORY_B.

## Interpretación

Un cambio de elección bajo la intervención emparejada es evidencia de que el contenido de memoria retenido influye causalmente sobre la respuesta del organismo en esta tarea operacional.

Esto no constituye evidencia de consciencia, experiencia subjetiva, sentiencia ni experiencia fenomenológica.

## Por qué es más fuerte que V47

V47 pregunta si trayectorias históricas diferentes conducen a comportamientos posteriores diferentes.

V48 interviene directamente sobre una sola variable de estado persistente mientras mantiene emparejado el resto del receptor. Por eso constituye un análogo de intervención causal sobre el estado de los experimentos de intercambio de memoria V44/V45.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V48 — Matched Memory-Swap Intervention

## Question

Can a persistent LLM-backed organism change its response to the same probe when persistent memory content is changed while the receiver's remaining state is held fixed?

## Intervention

One receiver database is initialized with a memory space. Two byte-identical copies are created.

- MEMORY_A: ALFA → AMBER
- MEMORY_B: ALFA → VIOLET

Only the content field of the existing memory row is changed.

Before the probe, the numerical dynamic state, dynamic memory, dynamic pressure, dynamic-step count, attractor distance, self-model, last thought, event stream, identity, importance and timestamp of the memory row, and receiver configuration remain fixed.

The LLM context uses event_limit=0 and memory_limit=1, so the probe receives the memory item as the sole textual-history channel.

## Primary observable

The same probe is presented in both conditions. The primary result is whether CHOICE changes between MEMORY_A and MEMORY_B.

## Interpretation

A choice change under the matched intervention is evidence that retained memory content causally influences the organism's response in this operational task.

This is not evidence of consciousness, subjective experience, sentience, or phenomenal experience.

## Why it is stronger than V47

V47 asks whether different historical trajectories lead to different later behavior.

V48 directly intervenes on one persistent-state variable while matching the rest of the receiver. It is therefore an analogue of causal state intervention used in the V44/V45 memory-swap experiments.

</details>