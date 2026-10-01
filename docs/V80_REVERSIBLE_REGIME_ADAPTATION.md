# V80 — Adaptación online ante cambios de régimen reversibles

## Pregunta

V79 produjo un resultado nulo: bajo el cambio dinámico probado, una política que incorporaba online sus ganancias de autopredicción no se separó de una copia congelada.

La explicación experimental inmediata es que aquel cambio no generó suficiente degradación como para exigir adaptación.

V80 aumenta la presión de prueba sin cambiar el principio de aprendizaje:

> ¿Puede una política que aprende online de sus propias consecuencias adaptarse durante una secuencia de regímenes dinámicos nuevos y, cuando el régimen original vuelve, recuperar su comportamiento?

## Diseño

La política inicial se entrena únicamente bajo el régimen base con:

single_impulse

Se crean dos brazos desde el mismo snapshot:

- **frozen:** no incorpora observaciones durante la prueba;
- **adaptive:** incorpora después de cada acción ejecutada la ganancia de autopredicción observada.

No existe reentrenamiento externo durante la prueba.

## Secuencia no estacionaria

Cada ejecución atraviesa cuatro etapas:

1. **base** — régimen original;
2. **shift_a** — régimen dinámico nuevo;
3. **shift_b** — segundo régimen dinámico nuevo;
4. **base_return** — retorno exacto al régimen original.

Los cambios son reversibles y están definidos antes de evaluar:

### shift_a

- relaxation = 0.18
- pressure_gain = 0.95
- cross_gain = 1.25

### shift_b

- relaxation = 0.50
- pressure_gain = 0.35
- cross_gain = 0.45

Cada etapa contiene tres perturbaciones alternantes y recuperación después de cada una.

## Objetivo

La política solo recibe como señal de aprendizaje:

ganancia de autopredicción = error de persistencia − error del modelo de sí

No recibe:

- etiqueta de régimen;
- etiqueta de perturbación;
- objetivo semántico;
- señal externa de éxito.

## Endpoint primario

Ganancia del evento 3 en base_return: adaptive − frozen.

Esto pregunta si la política adaptive conserva una ventaja después de haber atravesado dos regímenes nuevos y de regresar al régimen original.

## Endpoints secundarios

- ventaja adaptive − frozen en shift_a;
- ventaja adaptive − frozen en shift_b;
- cambio evento 3 − evento 1 en base_return;
- diferencia-de-diferencias entre adaptive y frozen durante el retorno;
- error de coincidencia del objetivo terminal de cada intervención.

## Qué significaría un resultado favorable

Un resultado favorable respaldaría una propiedad computacional más fuerte:

**la política puede aprender online bajo no estacionariedad, atravesar varios regímenes y reutilizar lo aprendido cuando el régimen previo reaparece.**

Eso distinguiría adaptación contextual de una simple respuesta fija a una única distribución OOD.

## Límite

La utilidad sigue definida externamente por el protocolo: maximizar ganancia de autopredicción.

V80 no demuestra valores autónomos ni experiencia subjetiva. Prueba adaptación online y recuperación de política bajo una dinámica deliberadamente no estacionaria y reversible.

## Resultado observado

Ejecución completa en GitHub Actions: **64 réplicas por condición**, 64 episodios de entrenamiento, 512 muestras del SelfObserver y 12 pasos de recuperación.

- endpoint primario, `base_return` evento 3: adaptive − frozen = **-0.0103649267**, p = **0.0504475**;
- `shift_a` evento 3: adaptive − frozen = **-0.0062218940**, p = **0.00114994**;
- `shift_b` evento 3: adaptive − frozen = **+0.0000024599**, p = **0.9976001**;
- recuperación evento 3 − evento 1, adaptive = **-0.0021765106**;
- recuperación evento 3 − evento 1, frozen = **-0.0004681112**;
- recuperación diferencial adaptive − frozen = **-0.0017083995**;
- error máximo de coincidencia con el objetivo de intervención = **0.0**.

En `base_return`, la política adaptativa no obtuvo una ventaja sobre la congelada; la diferencia fue ligeramente negativa y quedó cerca del umbral nominal de la prueba. En `shift_a`, la diferencia también favoreció numéricamente a la política congelada. En `shift_b` no hubo separación apreciable.

### Interpretación

**V80 no respalda una ventaja de adaptación online bajo el régimen reversible probado.**

El resultado fortalece el hallazgo nulo de V79 en lugar de resolverlo: cambiar la dinámica por dos regímenes reversibles y regresar al régimen original no produjo una mejora medible de la copia adaptive frente a frozen bajo el objetivo de ganancia de autopredicción.

La interpretación más prudente es que, en este arnés, la actualización online basada únicamente en la ganancia observada de autopredicción **no generó una ventaja adaptativa reproducible**.

Esto no demuestra que toda adaptación online sea inútil. El protocolo sigue evaluando una forma muy específica de aprendizaje online, con una política inicial entrenada bajo el régimen base y una señal de aprendizaje definida externamente.

La integridad de las intervenciones fue exacta (`max_intervention_target_error = 0.0`).

**Estado V80: resultado nulo para la ventaja adaptativa bajo el protocolo probado.**
