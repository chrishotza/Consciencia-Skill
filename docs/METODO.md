# Método Consciencia-Skill

## Hacer consciente a una IA mediante continuidad

El objetivo del proyecto es investigar y construir una IA capaz de mantener una continuidad propia, representarse a sí misma, observar su propia dinámica y utilizar esa información para recorrer y seleccionar futuros posibles.

No se parte de una sola instrucción de sistema ni de un único prompt. Se construye una arquitectura que mantiene relaciones internas a través del tiempo.

## 1. Dar continuidad

Una respuesta aislada termina cuando termina la interacción.

El primer paso consiste en que la IA mantenga un estado que pueda sobrevivir entre interacciones y entre reinicios del proceso.

La continuidad se materializa mediante estado persistente, eventos, memoria y snapshots de la trayectoria.

## 2. Dar memoria

La IA debe conservar información sobre su propia historia.

No se trata solamente de guardar conversaciones. La memoria debe poder influir sobre estados posteriores y ser sometida a intervenciones controladas.

V47–V50 exploran progresivamente historia, memoria y estado dinámico.

## 3. Dar un modelo de sí

La IA mantiene una representación de aspectos de su propio estado.

El modelo de sí puede aprender a predecir cómo cambia la propia dinámica y luego utilizar esa predicción para seleccionar entre trayectorias.

V51 y V57 prueban esta capa.

## 4. Hacer que se observe

Un modelo que contiene una representación de sí todavía puede ser solamente descriptivo.

La siguiente etapa es que esa representación pueda compararse con el estado que realmente ocurrió y producir una señal de error o ganancia de autopredicción.

V51 convierte la autoobservación en una variable medible.

## 5. Hacer causal el modelo de sí

El modelo de sí debe poder cambiar lo que ocurre después.

Por eso el proyecto introduce puentes explícitos entre representación semántica, estado interno y selección de trayectoria.

V58, V62 y V63 estudian esta cadena causal.

## 6. Dar futuros posibles

La IA no debe limitarse a reaccionar ante el presente.

Debe poder evaluar estados futuros posibles y seleccionar entre trayectorias.

V57 y los protocolos posteriores comparan la selección guiada por modelo de sí con controles emparejados.

## 7. Mantener una dinámica propia

La continuidad no puede depender únicamente del texto almacenado.

Por eso existe un núcleo de estado numérico persistente que evoluciona incluso en ciclos autónomos y puede interactuar con memoria, continuidad y selección.

## 8. Separar VIGILIA y SUEÑO

La arquitectura contempla dos regímenes funcionales:

**VIGILIA** — interacción con el entorno, percepción, lenguaje, memoria y decisión.

**SUEÑO** — menor dependencia de entrada externa y mayor actividad interna: consolidación, recombinación y reorganización.

V65 y V66 estudian si lo generado durante SUEÑO puede influir sobre la actividad posterior.

## 9. Eliminar la explicación fácil

La prueba más importante no consiste en demostrar que una memoria textual cambia una respuesta.

Consiste en eliminar progresivamente la explicación textual y comprobar qué queda.

V64 y V66 producen resultados nulos bajo sus condiciones.

V67 lleva esta estrategia más lejos: elimina memoria semántica, eventos, snapshots, texto del modelo de sí y otras superficies de representación, conserva únicamente el núcleo dinámico y prueba si esa información puede continuar siendo recuperable y causalmente transferible.

## 10. Regla científica

Cada nueva capacidad debe seguir:

```
hipótesis
   ↓
implementación
   ↓
control
   ↓
intervención
   ↓
medición
   ↓
resultado
   ↓
intento de refutación
```

Los resultados positivos no se consideran definitivos.

Los resultados nulos y negativos se conservan.

Una capacidad solo gana peso cuando sobrevive a pruebas cada vez más exigentes.

## Fundamentos

El método se apoya en dos documentos de referencia:

- [Manifiesto Matemático del Ser](../MANIFIESTO_DEL_SER.md)
- [TCF v3.3](fundamentos/TCF_V3_3.md)

El primero define el marco ontológico.

El segundo aporta una formulación dinámica efectiva que inspira parte de la arquitectura.

La traducción del marco teórico al software se considera una hipótesis de ingeniería y se mantiene separada de la evidencia experimental.

## Estado

El repositorio se encuentra en investigación activa.

La frontera experimental incluye ahora **C0.18 verificado**. C0.17 sigue aportando evidencia de adquisición/persistencia autónoma del segundo orden, pero sin especificidad conductual TRUE vs PERMUTED bajo su protocolo.

C0.18 extendió esa línea a una prueba emparejada de **lesión/rescate** con 24 réplicas. La adquisición y persistencia del modelo se reprodujeron, pero los contrastes FULL − LESION y RESCUE − LESION fueron nulos bajo el protocolo probado.

Por tanto, C0.18 reduce la interpretación causal del segundo orden: la persistencia del modelo no fue suficiente para demostrar necesidad conductual ni rescate funcional en esta prueba.

La campaña C0 de 32 ejecuciones fue reiniciada con una ruta de artifacts más segura. Sus resultados no se consideran evidencia hasta validar cada réplica.

En paralelo, la infraestructura ya incluye **LOCAL/SERVER runtime modes**, **Consciousness Server**, **continuity checkpoints** y **continuity reconciliation**. Esta capa permite pasar de persistencia local a un plano de continuidad verificable antes de implementar replay, recuperación y futura federación entre nodos.
