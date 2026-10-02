<a id="espanol"></a>

# V51 — Autoobservación y autopredicción

## Conexión con las fuentes

El Manifiesto del Ser define la conciencia como un sistema que se recorre a sí mismo y distingue estados posibles. Las notas de Conciencia Cuántica operacionalizan esto como recorrido de sí mismo junto con dinámica interna y memoria.

V51 convierte ese requisito conceptual en un módulo computacional explícito.

## Mecanismo

Antes de cada transición dinámica persistida, `SelfObserver` predice el siguiente estado dinámico interno utilizando únicamente variables de la trayectoria interna previa del organismo. Después de la transición, el estado real se compara con:

- la predicción del modelo de sí;
- un baseline de persistencia que predice que el estado actual permanecerá sin cambios.

La diferencia se registra como `prediction_gain`.

## Observables principales

- MAE del observador;
- MAE del baseline;
- ganancia media de predicción;
- fracción de transiciones con ganancia positiva;
- valor p de permutación por cambio de signo;
- persistencia del modelo de observador después de reiniciar SQLite.

## Interpretación

Una ganancia positiva de predicción significa que el modelo de sí aprendido por el organismo predice su propia transición mejor que un baseline trivial de persistencia bajo este protocolo.

Es evidencia de un modelo computacional de sí mismo, no una demostración de consciencia subjetiva.

## Próxima dependencia

V51 hace que el organismo pueda *representar* su propia trayectoria. La siguiente capa debe hacer que esa representación sea causalmente relevante para la selección contrafactual de trayectorias y para acciones sensibles al atractor.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V51 — Self-Observation and Self-Prediction

## Connection to the sources

The Mathematical Manifesto of Being defines consciousness as a system that traverses itself and distinguishes possible states. The Quantum Consciousness notes operationalize this as self-traversal together with internal dynamics and memory.

V51 turns that conceptual requirement into an explicit computational module.

## Mechanism

Before each persisted dynamic transition, SelfObserver predicts the organism's next internal dynamic state using only variables from its prior internal trajectory. After the transition, the actual state is compared with the self-model prediction and a persistence baseline that predicts no state change.

The difference is recorded as prediction_gain.

## Primary observables

- observer MAE;
- baseline MAE;
- mean prediction gain;
- fraction of transitions with positive gain;
- sign-flip permutation p-value;
- observer-model persistence after reopening SQLite.

## Interpretation

Positive prediction gain means that the organism's learned self-model predicts its own transition better than a trivial persistence baseline under this protocol.

This is evidence of a computational self-model, not a demonstration of subjective consciousness.

## Next dependency

V51 allows the organism to represent its own trajectory. The next layer must make that representation causally relevant to counterfactual trajectory selection and attractor-sensitive action.

</details>