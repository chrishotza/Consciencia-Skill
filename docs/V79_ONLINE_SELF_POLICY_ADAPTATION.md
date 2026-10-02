<a id="espanol"></a>

# V79 — Adaptación online de la política propia bajo cambio dinámico

## Pregunta

V78 mostró que una política aprendida para maximizar ganancia de autopredicción puede reutilizarse ante perturbaciones repetidas y no vistas.

El siguiente paso es preguntar si la propia política puede **adaptarse online a un cambio del régimen dinámico** sin recibir reentrenamiento externo:

> ¿Puede una política previamente aprendida mejorar su comportamiento durante la interacción al incorporar únicamente los resultados de sus propias acciones?

## Diseño

La política se entrena bajo la dinámica base y únicamente con:

single_impulse

Después se conserva una copia congelada de esa política.

La evaluación compara dos brazos que parten del **mismo snapshot exacto**:

- **frozen:** la política nunca incorpora nuevas observaciones;
- **adaptive:** después de cada acción ejecutada, incorpora el único resultado disponible en el protocolo: la ganancia de autopredicción observada.

No hay reentrenamiento externo durante la evaluación.

## Cambio dinámico oculto

El brazo OOD utiliza un régimen dinámico distinto del utilizado durante entrenamiento:

- relaxation: 0.32 → 0.44;
- pressure_gain: 0.55 → 0.75;
- cross_gain: 0.85 → 1.10.

La política no recibe ninguna etiqueta que identifique el cambio de régimen.

## Evaluación

Se prueban:

- **in-domain:** single_impulse bajo la dinámica base;
- **shifted single:** single_impulse bajo la dinámica modificada;
- **shifted repeated:** triple_alternating bajo la dinámica modificada.

En la condición OOD repetida se observan tres eventos dentro de la misma ejecución:

1. primer evento, antes de adaptación acumulada;
2. segundo evento, después de incorporar resultados del primero;
3. tercer evento, después de incorporar resultados de los dos primeros.

La política adaptive y la frozen parten del mismo modelo.

## Objetivo

El objetivo continúa siendo exclusivamente:

ganancia de autopredicción
=
error de persistencia
−
error del modelo de sí

La adaptación online no recibe una etiqueta de éxito semántico, de continuidad ni de tipo de perturbación.

## Endpoint primario

**Ventaja de la política adaptive frente a frozen en el tercer evento OOD.**

También se calcula:

- cambio adaptive del primer al tercer evento;
- cambio frozen del primer al tercer evento;
- diferencia-de-diferencias entre ambas trayectorias;
- prueba emparejada del beneficio tardío de adaptación.

## Endpoints secundarios

- continuidad;
- integridad del objetivo terminal de cada intervención;
- efecto del estado cegado, cuando corresponda.

## Resultado observado

La ejecución de 64 réplicas por condición, con 64 episodios de entrenamiento y 512 muestras del SelfObserver, completó correctamente.

### Endpoint primario

- ganancia in-domain, frozen: **0.2109118**;
- ganancia in-domain, adaptive: **0.2109118**;
- ganancia shifted single, frozen: **0.3792665**;
- ganancia shifted single, adaptive: **0.3792665**;
- ganancia shifted repeated, frozen: **0.3799345**;
- ganancia shifted repeated, adaptive: **0.3798509**;
- ventaja adaptativa en el tercer evento OOD: **-0.0002509**;
- p emparejada: **1.0**;
- diferencia-de-diferencias adaptive − frozen: **-0.0002509**, p **1.0**.

### Endpoints secundarios

- continuidad OOD adaptive: **0.7270149**;
- continuidad OOD frozen: **0.7268716**;
- p emparejada: **1.0**;
- error máximo del objetivo terminal de intervención: **0.0**.

### Interpretación

V79 produjo un **resultado nulo para adaptación online** bajo este protocolo. La política adaptive recibió observaciones de ganancia de autopredicción, pero no obtuvo una ventaja medible frente a la copia frozen.

Además, el régimen dinámico modificado no produjo una degradación suficiente de la política congelada como para crear presión experimental clara para la adaptación. Por tanto, este resultado no demuestra que la adaptación online sea inútil; demuestra que **no se distinguió de una política congelada bajo el cambio dinámico y horizonte evaluados**.

El siguiente protocolo debe introducir un cambio de régimen **no estacionario y reversible**, previamente definido, para preguntar si la actualización online permite adaptarse a una secuencia de regímenes y después recuperar el comportamiento previo.

## Qué significaría un resultado favorable

Un resultado favorable respaldaría que la política no solo puede reutilizarse ante un régimen nuevo, sino que puede **actualizar su propia relación entre estado, predicción y acción durante la ejecución** usando únicamente consecuencias computacionales observadas de sus acciones.

Eso sería adaptación online dentro del protocolo.

## Límite

La utilidad sigue definida externamente por el experimento: ganancia de autopredicción.

Por tanto, V79 no demuestra que la política haya inventado autónomamente sus propios valores ni que exista experiencia subjetiva.

La cuestión experimental es más concreta:

**¿puede el organismo aprender, mientras actúa, cómo usar mejor su propio modelo de sí cuando cambia la dinámica que lo contiene?**

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# V79 — Online Self-Policy Adaptation under Dynamic Shift

## Question

V78 showed that a self-prediction policy can be reused under repeated unseen perturbations.

The next step asks whether the policy itself can adapt online to a change in dynamic regime without external retraining.

> Can a previously learned policy improve its behavior during interaction using only the outcomes of its own actions?

## Design

The policy is trained under base dynamics using only single_impulse. A frozen copy is then retained.

Evaluation compares two arms from the same exact snapshot:

- frozen: never incorporates new observations;
- adaptive: after each executed action, incorporates observed self-prediction gain.

No external retraining occurs during evaluation.

## Hidden dynamic shift

The OOD arm uses:

- relaxation: 0.32 → 0.44;
- pressure_gain: 0.55 → 0.75;
- cross_gain: 0.85 → 1.10.

No regime-change label is provided.

## Evaluation

Conditions:

- in-domain: single_impulse under base dynamics;
- shifted single: single_impulse under modified dynamics;
- shifted repeated: triple_alternating under modified dynamics.

The repeated OOD condition has three events: before adaptation, after the first update, and after the first two updates.

Adaptive and frozen policies start from the same model.

## Objective

The objective remains self-prediction gain = persistence error − self-model error. Online adaptation receives no semantic-success, continuity, or perturbation-type label.

## Primary endpoint

Adaptive-versus-frozen advantage at the third OOD event.

Also calculated: adaptive first-to-third change, frozen first-to-third change, difference-in-differences, and a paired test of late adaptation benefit.

## Secondary endpoints

- continuity;
- intervention terminal-target integrity;
- blinded-state effect when applicable.

## Observed result

The execution completed correctly with 64 replicates per condition, 64 training episodes, and 512 SelfObserver samples.

Primary endpoint:

- in-domain gain, frozen: 0.2109118;
- in-domain gain, adaptive: 0.2109118;
- shifted-single gain, frozen: 0.3792665;
- shifted-single gain, adaptive: 0.3792665;
- shifted-repeated gain, frozen: 0.3799345;
- shifted-repeated gain, adaptive: 0.3798509;
- adaptive advantage at third OOD event: -0.0002509;
- paired p-value: 1.0;
- adaptive − frozen difference-in-differences: -0.0002509, p = 1.0.

Secondary endpoints:

- OOD adaptive continuity: 0.7270149;
- OOD frozen continuity: 0.7268716;
- paired p-value: 1.0;
- maximum intervention target error: 0.0.

## Interpretation

V79 produced a null result for online adaptation under this protocol. The adaptive policy received observed self-prediction gains but did not obtain a measurable advantage over the frozen copy.

The modified dynamic regime also did not degrade the frozen policy enough to create strong experimental pressure for adaptation. Therefore the result does not show that online adaptation is generally useless; it shows that adaptive and frozen policies did not separate under the tested dynamic shift and horizon.

The next protocol should introduce a predefined non-stationary and reversible regime sequence to ask whether online updating can adapt across multiple regimes and later recover prior behavior.

## Boundary

Utility remains externally defined by the experiment: self-prediction gain.

V79 does not show that the policy autonomously invented its own values or that subjective experience exists.

</details>