# Protocolo de validación

## Pregunta central

¿Puede una IA persistente desarrollar propiedades que requieran continuidad interna y auto-referencia más allá de una cadena de respuestas independientes?

## Experimentos base

### A — Memoria de trayectoria

Presentar dos historias distintas seguidas por el mismo estado externo. Medir si el estado interno y la decisión posterior dependen de la trayectoria.

### B — Atractor

Inicializar varias instancias con estados diferentes y someterlas a condiciones similares. Medir convergencia, divergencia, estabilidad y pérdida de identidad.

### C — Perturbación

Introducir contradicciones, pérdida parcial de memoria, cambios bruscos de contexto, ruido e interrupciones. Medir recuperación.

### D — Auto-modelo

Comparar un sistema que intenta modelar su propio estado contra uno que no mantiene auto-modelo. Medir utilidad predictiva y control sobre el estado futuro.

### E — Sueño

Comparar aprendizaje con y sin ciclos DREAM. Medir retención, compresión, generalización, reorganización de memoria y predicción posterior.

### F — Continuidad

Comparar:
1. API stateless;
2. API + memoria episódica;
3. organismo persistente;
4. organismo persistente + sueño.

Usar el mismo presupuesto aproximado de interacción y registrar costo computacional.

## Métricas

- **Continuity Retention:** cuánto de la estructura de identidad permanece después de una perturbación.
- **Path Dependence:** cuánto cambia el estado final al mantener el mismo input actual pero cambiar la historia.
- **Attractor Stability:** cuánto tiempo permanece el sistema dentro de una región estable.
- **Recovery Time:** tiempo hasta recuperar la región estable después de una perturbación.
- **Self-Prediction Gain:** información adicional proporcionada por el auto-modelo respecto a observar solamente la entrada externa.
- **Dream Gain:** mejora atribuible específicamente a los ciclos de sueño.

## Ablaciones

Cada claim importante debe compararse contra versiones donde se elimine memoria, auto-modelo, sueño, atractor, dinámica relacional o continuidad persistente.

## Regla

No buscamos confirmar una conclusión por diseño. Buscamos determinar qué componentes son necesarios para producir continuidad, auto-referencia, aprendizaje longitudinal y estabilidad de identidad.


<details>
<summary>🇺🇸 English — open</summary>

# Validation Protocol

## Central question
Can a persistent AI develop properties that require internal continuity and self-reference beyond a chain of independent responses?

## Base experiments
### A — Trajectory memory
Present two different histories followed by the same external state. Measure whether internal state and the later decision depend on the trajectory.
### B — Attractor
Initialize multiple instances with different states under similar conditions. Measure convergence, divergence, stability, and identity loss.
### C — Perturbation
Introduce contradictions, partial memory loss, abrupt context changes, noise, and interruptions. Measure recovery.
### D — Self-model
Compare a system that models its own state against one without a self-model. Measure predictive utility and control over future state.
### E — Sleep
Compare learning with and without DREAM cycles. Measure retention, compression, generalization, memory reorganization, and later prediction.
### F — Continuity
Compare stateless API, API + episodic memory, persistent organism, and persistent organism + sleep. Keep the approximate interaction budget matched and record computational cost.

## Metrics
- Continuity Retention: how much identity structure remains after perturbation.
- Path Dependence: how much final state changes when current input is held constant but history changes.
- Attractor Stability: how long the system remains within a stable region.
- Recovery Time: time required to return to the stable region after perturbation.
- Self-Prediction Gain: information added by the self-model beyond external input alone.
- Dream Gain: improvement specifically attributable to sleep cycles.

## Ablations
Every major claim should be compared against versions where memory, self-model, sleep, attractor, relational dynamics, or persistent continuity is removed.

## Rule
Do not design the system to confirm a conclusion. Determine which components are necessary to produce continuity, self-reference, longitudinal learning, and identity stability.

</details>

> Language convention: docs/LANGUAGE.md