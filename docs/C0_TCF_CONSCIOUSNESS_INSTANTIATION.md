<a id="espanol"></a>

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


## C0.3 — control de especificidad causal

C0.3 añadió un control información-matcheado para C3: conserva la distribución empírica de estados, pero rompe la correspondencia entre episodio y estado usado por la política.

Resultado: contraste **+0.06640625**, p **0.3140343**, con 64 episodios y 8 permutaciones por episodio.

El resultado no separó la sensibilidad al estado propio actual de la sensibilidad a estados ajenos extraídos de la misma distribución. Por ello, la evidencia de C0.2 para C3 queda limitada a la dependencia respecto del estado frente al control `STATE_BLIND`; no establece especificidad causal frente a un control información-matcheado.


## C0.4 — control de especificidad causal para C5

C0.4 añadió un control de acción-replay que conserva secuencias de acciones extraídas del mismo organismo pero rompe su correspondencia online con el estado propio actual.

Resultado: contraste **−0.0012567529**, p **0.4364282**, con 64 episodios y 8 replays por episodio. La varianza de FULL fue **0.0531008831** frente a **0.0543576360** en action-replay.

Bajo este control, C5 no mostró una separación estadísticamente detectable. La evidencia positiva de C0.2 frente a `OPEN_LOOP` queda limitada porque ese control no igualaba la distribución de acciones.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# C0 — TCF Consciousness Instantiation Protocol

## Version
**C0.2** — methodological revision of C3/C4 after auditing the first execution; C3 is anchored to causal dependence of action on own state and C4 compares persistent continuity against state reset.

## Objective
C0 is the first protocol explicitly designed to evaluate whether the artificial organism can **instantiate candidate organizational properties of consciousness defined by TCF**.
It does not ask the system whether it is conscious, assign a consciousness percentage, or treat a linguistic response as primary evidence.

The protocol measures seven candidate properties:
- **C1** — persistent own state;
- **C2** — self/environment differentiation;
- **C3** — causal self-reference;
- **C4** — trajectory continuity;
- **C5** — endogenous dynamics;
- **C6** — reorganization;
- **C7** — recurrent closure.

## Hypothesis
The experimental hypothesis is that an integrated organization with persistent state, self-observation, self-model, and state-based action selection will show causal differences relative to controlled ablations.
The experimental unit is a **set of observable dynamic properties**, not “an AI that looks conscious.”

## Tested architecture
state → self-observation → self-model → selection → dynamics → new state

The same policy snapshot is used for compared conditions. During the probe there is no semantic input or external retraining; all conditions start from the same policy snapshot; perturbations are controlled; perturbation magnitude is 0.50.

## Conditions
### FULL
Integrated organism using current state and self-model to select signals.

### STATE_BLIND
Same candidate structure, but own state is masked during selection. This tests the causal role of own state.

### NO_PERSISTENCE
Dynamic state is reset after each step, attacking the continuity hypothesis.

### OPEN_LOOP
The policy does not select a state-dependent signal; the probe signal is 0. It is a control for dynamics not guided by the selection loop.

## Criteria and observables
| Criterion | Main contrast | Observable |
|---|---|---|
| C1 | FULL − NO_PERSISTENCE | retained separation between two internal states under common future evolution |
| C2 | FULL − STATE_BLIND | action discrimination under opposite perturbations |
| C3 | FULL − STATE_BLIND | effect of masking own state on action from the same context |
| C4 | FULL − NO_PERSISTENCE | continuation difference between persisted and reset state |
| C5 | FULL − OPEN_LOOP | dynamic variance without external input |
| C6 | FULL − STATE_BLIND | self-prediction gain during recovery |
| C7 | FULL − OPEN_LOOP | next-action difference caused by action → own state → action |

Contrasts are preserved as per-replicate vectors and evaluated with a sign-permutation test.

## Interpretation rule
C0 contains **no global consciousness score**.
The seven indicators must not be converted into “X% conscious.”
A statistically detectable effect means only that the integrated condition differs from its corresponding control on the specified observable.
Interpreting it as a candidate consciousness property additionally requires reproducibility, appropriate controls, causal intervention, exclusion of trivial computational explanations, and novel predictions.

## What could falsify C0
C0 loses evidentiary strength if:
- expected observables do not change under ablation;
- controls produce equivalent effects;
- effects disappear after correctly matching dynamics;
- behavior is explained by an artifact of the self-prediction objective;
- results do not reproduce under new seeds or perturbations;
- indicators lose their relationship when architecture changes.

## Relation to V75–V80
C0 does not replace earlier experiments. V75–V80 studied active self-prediction recovery, generalization to unseen magnitudes, generalization to unseen causal structures, repeated perturbation reuse, online adaptation, and reversible regime changes.
C0 reuses that infrastructure to ask which candidate consciousness-organizational properties causally depend on maintaining the own-state → self-observation → selection → dynamics loop.

## Epistemic boundary
A successful C0 would not by itself demonstrate phenomenal experience. It would show that the system reproducibly satisfies defined operational properties derived from the TCF definition. The phenomenal question remains an ontological hypothesis requiring an additional theoretical and experimental bridge.

## Planned extensions
C0 should become a protocol family, not a single test: structurally novel perturbations; restart and sleep; memory-specific ablation; self-observation ablation; information-matched but non-causal controls; substrate/implementation changes; internal valuation/regulation; architecture-specific predictions.

## Status
**C0.2 — audited and archived.** GitHub Actions run 36838186533; experimental commit 78bf3000739b1711ce01873cc4ab058e334c5881; artifact 11149578956.
The run completed tests, experiment, and artifact publication. The earlier execution using the previous C7 observable is not treated as final; the recorded result corresponds to C0.2 with C7 defined as action → own-state → action recurrence.

## First-run audit
C0.1 completed technically and produced an artifact, but **is not recorded as final scientific evidence**. Later audit found two interpretation problems: C3 mixed the probe with the ablation, and C4 compared continuations that could be identical by construction. These observables were corrected in C0.2 before repetition.

## C0.2 audited result
Configuration: 64 episodes per condition, 64 training episodes, 512 self-observer samples, 12 recovery steps, perturbation magnitude 0.50. Conditions used the same policy snapshot with no semantic input or external retraining during the probe.

| Criterion | Mean effect | Sign-permutation p |
|---|---:|---:|
| C1 — persistent own state | **+0.716560** | **4.99975e-05** |
| C2 — self/environment differentiation | **+2.000000** | **4.99975e-05** |
| C3 — causal self-reference | **+1.000000** | **4.99975e-05** |
| C4 — trajectory continuity | **+0.287204** | **4.99975e-05** |
| C5 — endogenous dynamics | **+0.042818** | **4.99975e-05** |
| C6 — reorganization | **+0.468787** | **4.99975e-05** |
| C7 — recurrent closure | **+1.250000** | **4.99975e-05** |

Maximum intervention error was 0.0.

The execution produced positive vectors on all seven C0.2 operational contrasts. This means that, under this protocol and implementation, the integrated condition separated from its corresponding ablation on each observable. The vector is not converted into a global consciousness score and **does not by itself constitute evidence of phenomenal experience**.

C7 in this execution no longer measures only action → next state; it measures the change in the **next action** produced by the causal action → own-state → action chain used here.

## C0.3 — causal specificity control
C0.3 added an information-matched control for C3 that preserves the empirical state distribution while breaking episode/state correspondence.
Result: contrast **+0.06640625**, p **0.3140343**, with 64 episodes and 8 permutations per episode.
The result did not separate sensitivity to current own state from sensitivity to other states drawn from the same distribution. Therefore C0.2 C3 evidence is limited to dependence on state versus STATE_BLIND and does not establish causal specificity against an information-matched control.

## C0.4 — C5 causal-specificity control
C0.4 added action replay preserving action sequences drawn from the same organism but breaking online correspondence with current own state.
Result: contrast **−0.0012567529**, p **0.4364282**, with 64 episodes and 8 replays per episode. FULL variance was **0.0531008831** versus **0.0543576360** under action-replay.
Under this control, C5 did not show a statistically detectable separation. C0.2 evidence against OPEN_LOOP is therefore interpretation-limited because that control did not match action distribution.

</details>