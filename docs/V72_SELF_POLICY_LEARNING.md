<a id="espanol"></a>

# V72 — Aprendizaje de la política desde el propio modelo de sí

## Pregunta

V70 dejó identificado un cuello de botella: la conversión de la lectura del modelo de sí en acción todavía estaba definida explícitamente por el protocolo.

V71 llevó el lector persistente hacia el ciclo autónomo.

V72 da el siguiente paso:

> ¿Puede una política aprender a utilizar el propio modelo de sí para seleccionar trayectorias, en lugar de recibir de antemano la regla de selección?

## Diseño

El protocolo aprende una función numérica de utilidad a partir de características producidas por el SelfObserver:

- estado actual;
- distancia al atractor;
- estado siguiente predicho;
- desplazamiento predicho;
- señal candidata.

La política se persiste, se recarga sin reentrenamiento y después se prueba sin entrada semántica.

## Comparaciones

La evaluación incluye:

1. política aprendida con estado propio;
2. la misma política con el estado cegado;
3. política fija actual del selector;
4. selección aleatoria.

La comparación principal es la diferencia entre la política aprendida con acceso al estado propio y la misma política con estado cegado.

## Límite científico

La función de utilidad es externa al sistema.

Por tanto, V72 no afirma que el organismo descubra por sí mismo qué debe valorar. La pregunta es más acotada:

> ¿Puede aprender a utilizar una representación numérica de sí mismo para seleccionar trayectorias bajo un objetivo definido externamente?

Ese límite permanece aunque el resultado sea positivo.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V72 — Learning a Policy from the Self-Model

## Question

V70 identified a bottleneck: conversion of self-model readout into action was still explicitly defined by the protocol.

V71 moved the persistent reader into the autonomous cycle.

V72 takes the next step:

> Can a policy learn to use the self-model to select trajectories instead of receiving the selection rule in advance?

## Design

The protocol learns a numerical utility function from SelfObserver features:

- current state;
- attractor distance;
- predicted next state;
- predicted displacement;
- candidate signal.

The policy is persisted, reloaded without retraining, and then tested without semantic input.

## Comparisons

Evaluation includes:

1. learned policy with self-state access;
2. the same policy with state blinded;
3. the current fixed selector policy;
4. random selection.

The primary comparison is learned-policy performance with self-state access versus the same policy with state blinded.

## Scientific boundary

The utility function remains external to the system.

Therefore V72 does not claim that the organism discovers what it should value by itself. The narrower question is:

> Can it learn to use a numerical representation of itself to select trajectories under an externally defined objective?

That boundary remains even if the result is positive.

</details>