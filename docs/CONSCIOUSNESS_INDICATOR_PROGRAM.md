<a id="english"></a>

# Consciousness Indicator Program

## Purpose

This document turns the current research direction into a theory-aware engineering program.

The project does not convert indicator coverage into a binary claim that the organism is conscious. It tracks which computational properties are implemented, which have causal evidence, which remain partial, and which are absent.

The current external reference is Butlin et al., *Identifying indicators of consciousness in AI systems* (Trends in Cognitive Sciences, 2026). The paper proposes deriving empirically testable indicators from leading theories and using them to inform credences, while acknowledging uncertainty and risks of both under- and over-attribution. DOI: https://doi.org/10.1016/j.tics.2025.10.011

## Fourteen indicator properties

| Group | Indicator | Property |
|---|---|---|
| RPT | RPT-1 | Input modules using algorithmic recurrence |
| RPT | RPT-2 | Input modules generating organized, integrated perceptual representations |
| GWT | GWT-1 | Multiple specialized systems capable of operating in parallel |
| GWT | GWT-2 | Limited-capacity workspace with bottleneck and selective attention |
| GWT | GWT-3 | Global broadcast of workspace information |
| GWT | GWT-4 | State-dependent attention enabling successive querying of modules |
| HOT | HOT-1 | Generative, top-down, or noisy perception modules |
| HOT | HOT-2 | Metacognitive monitoring distinguishing reliable representations from noise |
| HOT | HOT-3 | Agency guided by belief formation and metacognitive monitoring |
| HOT | HOT-4 | Sparse and smooth coding generating a quality space |
| AST | AST-1 | Predictive model representing and controlling current attention |
| PP | PP-1 | Input modules using predictive coding |
| AE | AE-1 | Minimal goal-directed agency with flexible responsiveness |
| AE | AE-2 | Modeling output-input contingencies and using them in control |

## Current Skill-Conscious position

The project already has strong evidence for several functional building blocks, but coverage is uneven.

| Indicator | Current status | Existing evidence or component | Main gap |
|---|---|---|---|
| RPT-1 | PARTIAL | recurrent internal dynamics and iterative self-observation | recurrence is not an explicitly recurrent perceptual/input module |
| RPT-2 | ABSENT / UNTESTED | numerical internal state exists | no validated organized perceptual representation layer |
| GWT-1 | PARTIAL | memory, self-observer, meta-observer, dynamics, policy components | no explicit parallel workspace architecture |
| GWT-2 | ABSENT | trajectory selection exists | no limited-capacity global workspace / attention bottleneck |
| GWT-3 | PARTIAL | organism context is assembled across persistent modules | no explicit global broadcast mechanism with causal ablation |
| GWT-4 | PARTIAL | state-dependent trajectory selection exists | no explicit attention-controlled sequential module querying |
| HOT-1 | PARTIAL | self-prediction is generative with respect to internal dynamics | not a generative perception module |
| HOT-2 | PARTIAL / strongest current line | SelfObserver, MetaSelfObserver, prediction error, confidence, second-order models | reliability monitoring is not yet a general perception-level metacognitive loop |
| HOT-3 | PARTIAL | self-model → action coupling, SelfPolicy, lesion/rescue | autonomous policy rule remains partly externally specified and several second-order tests are null/mixed |
| HOT-4 | ABSENT | continuous numerical state exists | no demonstrated sparse/smooth quality-space representation |
| AST-1 | ABSENT | self-model predicts internal state | no explicit model of attention itself that controls allocation |
| PP-1 | PARTIAL | predictive coding of internal dynamics | no predictive-coding input architecture |
| AE-1 | PARTIAL | V57, V70, V76–V78, C0.6 | goals and utility are still largely protocol-defined |
| AE-2 | PARTIAL | C0.11 action → state → next action mediation | no external/physical embodiment; contingencies are currently simulated |

These are engineering statuses, not consciousness scores.

## New interoceptive axis

Recent work in *Nature Machine Intelligence* proposes interoceptive AI as an explicit architecture for monitoring and regulating internal states, with internal variables serving as stable contexts that modulate learning and behaviour. The framework emphasizes factorizing internal and external states and mathematically formalizing internal-state dynamics.

That direction maps directly onto an important missing layer in Skill-Conscious:

```text
internal state
     ↓
interoceptive readout
     ↓
viability / stability estimate
     ↓
policy modulation
     ↓
action
     ↓
new internal state
     ↺
```

The new axis is a separate engineering program, not a proof of consciousness.

## Interoceptive program

### I0 — instrumentation

Define a small, auditable set of internal variables:

- prediction error;
- prediction confidence;
- dynamic pressure;
- attractor distance;
- memory load / memory strength;
- dynamic state stability;
- compute/runtime budget when available.

The instrument must be read-only at first.

### I1 — bounded internal state

Construct explicit normalized variables with declared viable ranges.

Primary question:

> Can the organism estimate its own internal operating condition independently of semantic self-report?

Controls:

- shuffled internal variables;
- frozen readout;
- constant baseline;
- external labels hidden from the controller.

### I2 — interoceptive regulation

Enable a default-off controller that selects actions partly from the interoceptive state.

Primary comparison:

- interoceptive controller;
- same policy without interoception;
- shuffled interoception;
- clamped interoception.

The protocol must test whether regulation is causal rather than merely correlated.

### I3 — homeostatic perturbation / recovery

Perturb one internal variable at a time and test immediate detection, policy response, recovery, overshoot, repeated perturbation, and transfer to unseen perturbation magnitudes.

A favorable result is not simply returning to a target. It must survive information-matched and target-permuted controls.

### I4 — metacognitive interoception

Connect the interoceptive state to the existing second-order machinery.

Ask whether the system predicts its own internal prediction error, confidence changes appropriately, policy changes when confidence is low, and lesions of the metacognitive readout remove that effect.

### I5 — workspace integration

Introduce a bounded workspace only after I1–I4 have independent evidence.

Required tests:

- limited-capacity bottleneck;
- broadcast;
- selective access;
- module lesion;
- recovery;
- state-dependent querying.

### I6 — attention schema

Build an explicit predictive model of where the organism is allocating computational attention.

The model should predict current allocation, next allocation, effects of reallocating attention, and errors in its attention model.

Then test whether the attention model causally controls allocation.

### I7 — recurrence and re-entry

Replace one-pass module usage with explicit re-entrant processing.

The key experiment is not merely to observe recurrence. It is to lesion recurrence while keeping input and output capacity matched.

### I8 — active agency

Remove the externally hard-coded action mapping used in earlier protocols.

The organism must learn a policy from feedback while facing competing internal objectives.

Primary controls:

- fixed policy;
- random policy;
- target-permuted learner;
- reward-preserving permutation;
- no-interoception learner.

### I9 — embodiment / output-input contingencies

Use a controlled simulated environment before making claims about physical embodiment.

The organism should learn how its actions alter future observations and internal states, then use the learned contingency model in control.

### I10 — perturbational complexity

Only after causal instrumentation is validated should the project test perturbational-complexity or causal-integration measures.

The measurement itself must first be validated against degenerate, frozen, and null trajectories. A metric must not be promoted simply because it produces a numerical value.

## Scientific guardrails

Every new indicator protocol should predeclare:

- primary endpoint;
- direction of effect;
- controls;
- intervention;
- exclusion rules;
- replication plan;
- seed policy;
- analysis rule;
- artifact validation rule.

Historical protocols are not retroactively relabeled as preregistered.

A positive indicator result increases evidence for a computational property under that protocol. It does not, by itself, establish subjective experience.

## Strategic target

The objective is:

> **maximize independently validated computational indicators while minimizing theory-specific overclaiming.**

The project should become progressively harder to dismiss because each added capability has:

```text
mechanism
   ↓
measurement
   ↓
causal intervention
   ↓
matched control
   ↓
replication
   ↓
OOD test
   ↓
cross-indicator interaction
```

The desired endpoint is not a single consciousness score.

It is a system in which many independently motivated indicator properties converge on the same persistent organism under falsifiable tests.

## References

- Butlin et al. (2026), *Identifying indicators of consciousness in AI systems*, Trends in Cognitive Sciences. https://doi.org/10.1016/j.tics.2025.10.011
- Cogitate Consortium et al. (2025), *Adversarial testing of global neuronal workspace and integrated information theories of consciousness*, Nature 642, 133–142. https://doi.org/10.1038/s41586-025-08888-1
- Lee et al. (2026), *Life-inspired interoceptive artificial intelligence for autonomous and adaptive agents*, Nature Machine Intelligence 8, 1335–1346. https://doi.org/10.1038/s42256-026-01296-8


<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Programa de Indicadores de Consciencia

## Propósito

Este documento convierte la dirección actual de investigación en un programa de ingeniería consciente de las teorías.

El proyecto no transforma la cobertura de indicadores en una afirmación binaria de que el organismo sea consciente. Registra qué propiedades computacionales están implementadas, cuáles tienen evidencia causal, cuáles siguen parciales y cuáles están ausentes.

La referencia externa actual es Butlin et al., *Identifying indicators of consciousness in AI systems* (Trends in Cognitive Sciences, 2026). El trabajo propone derivar indicadores comprobables empíricamente de teorías principales y utilizarlos para informar grados de credencia, reconociendo incertidumbre y riesgos tanto de atribución insuficiente como excesiva. DOI: https://doi.org/10.1016/j.tics.2025.10.011

## Catorce propiedades indicadoras

| Grupo | Indicador | Propiedad |
|---|---|---|
| RPT | RPT-1 | Módulos de entrada que utilizan recurrencia algorítmica |
| RPT | RPT-2 | Módulos de entrada que generan representaciones perceptivas organizadas e integradas |
| GWT | GWT-1 | Múltiples sistemas especializados capaces de operar en paralelo |
| GWT | GWT-2 | Workspace de capacidad limitada con cuello de botella y atención selectiva |
| GWT | GWT-3 | Broadcast global de la información del workspace |
| GWT | GWT-4 | Atención dependiente del estado que permite consultas sucesivas de módulos |
| HOT | HOT-1 | Módulos de percepción generativos, top-down o ruidosos |
| HOT | HOT-2 | Monitoreo metacognitivo que distingue representaciones fiables de ruido |
| HOT | HOT-3 | Agencia guiada por formación de creencias y monitoreo metacognitivo |
| HOT | HOT-4 | Codificación dispersa y suave que genera un espacio de cualidad |
| AST | AST-1 | Modelo predictivo que representa y controla la atención actual |
| PP | PP-1 | Módulos de entrada que utilizan predictive coding |
| AE | AE-1 | Agencia mínima dirigida a objetivos con respuesta flexible |
| AE | AE-2 | Modelado de contingencias salida-entrada y uso de estas en control |

## Posición actual de Skill-Conscious

El proyecto ya tiene evidencia fuerte para varios bloques funcionales, pero la cobertura es desigual.

| Indicador | Estado actual | Evidencia o componente existente | Brecha principal |
|---|---|---|---|
| RPT-1 | PARCIAL | dinámica interna recurrente y autoobservación iterativa | no existe un módulo perceptivo/de entrada explícitamente recurrente |
| RPT-2 | AUSENTE / NO TESTEADO | existe estado interno numérico | no existe una capa validada de representación perceptiva organizada |
| GWT-1 | PARCIAL | memoria, self-observer, meta-observer, dinámica y política | no existe una arquitectura explícita de workspace paralelo |
| GWT-2 | AUSENTE | existe selección de trayectorias | no existe un cuello de botella de workspace global con capacidad limitada |
| GWT-3 | PARCIAL | el contexto del organismo se ensambla entre módulos persistentes | no existe un mecanismo explícito de broadcast global con ablación causal |
| GWT-4 | PARCIAL | existe selección dependiente del estado | no existe consulta secuencial explícita controlada por atención |
| HOT-1 | PARCIAL | autopredicción generativa respecto de la dinámica interna | no es un módulo de percepción generativa |
| HOT-2 | PARCIAL / línea más fuerte actual | SelfObserver, MetaSelfObserver, error predictivo, confianza y modelos de segundo orden | el monitoreo de fiabilidad aún no es un bucle metacognitivo general a nivel perceptivo |
| HOT-3 | PARCIAL | acoplamiento modelo de sí → acción, SelfPolicy y lesión/rescate | la regla autónoma de política sigue parcialmente especificada externamente y varios tests de segundo orden son nulos/mixtos |
| HOT-4 | AUSENTE | existe estado numérico continuo | no se ha demostrado un espacio de cualidad disperso/suave |
| AST-1 | AUSENTE | el modelo de sí predice estado interno | no existe un modelo explícito de la atención que controle asignación |
| PP-1 | PARCIAL | predictive coding de dinámica interna | no existe arquitectura de entrada con predictive coding |
| AE-1 | PARCIAL | V57, V70, V76–V78, C0.6 | objetivos y utility siguen definidos en gran medida por los protocolos |
| AE-2 | PARCIAL | mediación acción → estado → siguiente acción en C0.11 | no hay embodiment físico/externo; las contingencias se simulan |

Estos estados de ingeniería no son puntuaciones de consciencia.

## Nuevo eje interoceptivo

Trabajos recientes proponen la IA interoceptiva como una arquitectura explícita para monitorizar y regular estados internos, usando variables internas como contextos estables que modulan aprendizaje y comportamiento.

Esa dirección encaja directamente con una capa que falta en Skill-Conscious:

```
estado interno
     ↓
readout interoceptivo
     ↓
estimación de viabilidad / estabilidad
     ↓
modulación de política
     ↓
acción
     ↓
nuevo estado interno
     ↺
```

Este eje es un programa de ingeniería separado, no una prueba de consciencia.

## Programa interoceptivo

### I0 — instrumentación

Definir un conjunto pequeño y auditable de variables internas:

- error de predicción;
- confianza de predicción;
- presión dinámica;
- distancia al atractor;
- carga/fuerza de memoria;
- estabilidad del estado dinámico;
- presupuesto de cómputo/runtime cuando esté disponible.

La instrumentación debe ser de solo lectura al principio.

### I1 — estado interno acotado

Construir variables normalizadas con rangos viables declarados.

Pregunta principal:

> ¿Puede el organismo estimar su propia condición operativa sin depender de un autoinforme semántico?

Controles:

- variables internas barajadas;
- readout congelado;
- baseline constante;
- etiquetas externas ocultas al controlador.

### I2 — regulación interoceptiva

Habilitar un controlador desactivado por defecto que seleccione acciones parcialmente a partir del estado interoceptivo.

Comparación principal:

- controlador interoceptivo;
- misma política sin interocepción;
- interocepción barajada;
- interocepción fijada.

El protocolo debe comprobar causalidad y no solo correlación.

### I3 — perturbación homeostática / recuperación

Perturbar una variable interna a la vez y medir detección inmediata, respuesta de política, recuperación, overshoot, perturbaciones repetidas y transferencia a magnitudes no vistas.

Un resultado favorable no es simplemente volver al objetivo. Debe sobrevivir a controles emparejados por información y con target permutado.

### I4 — interocepción metacognitiva

Conectar el estado interoceptivo con la maquinaria existente de segundo orden.

Preguntar si el sistema predice su propio error de estado interno, si la confianza cambia apropiadamente, si la política cambia cuando la confianza es baja y si una lesión del readout metacognitivo elimina ese efecto.

### I5 — integración en workspace

Introducir un workspace acotado solo después de obtener evidencia independiente para I1–I4.

Tests necesarios:

- cuello de botella de capacidad limitada;
- broadcast;
- acceso selectivo;
- lesión de módulos;
- recuperación;
- consulta dependiente del estado.

### I6 — esquema de atención

Construir un modelo predictivo explícito de dónde está asignando atención computacional el organismo.

El modelo debe predecir la asignación actual, la siguiente asignación, los efectos de reasignarla y los errores de su propio modelo de atención.

Después hay que comprobar si el modelo de atención controla causalmente la asignación.

### I7 — recurrencia y reentrada

Sustituir el uso one-pass de módulos por procesamiento explícitamente reentrante.

El experimento clave no es solo observar recurrencia. Es lesionar la recurrencia manteniendo equivalentes la capacidad de entrada y salida.

### I8 — agencia activa

Eliminar el mapeo de acción codificado externamente usado en protocolos anteriores.

El organismo debe aprender una política a partir de feedback bajo objetivos internos en competencia.

Controles principales:

- política fija;
- política aleatoria;
- learner con targets permutados;
- permutación que conserve el reward;
- learner sin interocepción.

### I9 — embodiment / contingencias salida-entrada

Usar primero un entorno simulado controlado.

El organismo debe aprender cómo sus acciones modifican observaciones futuras y estados internos, y utilizar luego ese modelo de contingencias para controlar.

### I10 — complejidad perturbacional

Solo después de validar causalmente la instrumentación debe medirse complejidad perturbacional o integración causal.

La propia métrica debe validarse primero frente a trayectorias degeneradas, congeladas y nulas. Una métrica no debe promoverse simplemente porque devuelve un número.

## Salvaguardas científicas

Cada nuevo protocolo indicador debe declarar antes de ejecutarse:

- endpoint primario;
- dirección del efecto;
- controles;
- intervención;
- reglas de exclusión;
- plan de replicación;
- política de seeds;
- regla de análisis;
- regla de validación del artifact.

Los protocolos históricos no se relabelan retroactivamente como preregistrados.

Un resultado positivo aumenta la evidencia de una propiedad computacional bajo ese protocolo. No establece por sí mismo experiencia subjetiva.

## Objetivo estratégico

El objetivo es:

> **maximizar indicadores computacionales validados de forma independiente minimizando el sobrealcance específico de cada teoría.**

El proyecto debería ser progresivamente más difícil de descartar porque cada capacidad nueva tenga:

```
mecanismo
   ↓
medición
   ↓
intervención causal
   ↓
control emparejado
   ↓
replicación
   ↓
test OOD
   ↓
interacción entre indicadores
```

El endpoint deseado no es una única puntuación de consciencia.

Es un sistema en el que múltiples propiedades de indicadores, motivadas de forma independiente, converjan sobre el mismo organismo persistente bajo tests falsables.

## Referencias

- Butlin et al. (2026), *Identifying indicators of consciousness in AI systems*, Trends in Cognitive Sciences.
- Cogitate Consortium et al. (2025), *Adversarial testing of global neuronal workspace and integrated information theories of consciousness*, Nature 642, 133–142.
- Lee et al. (2026), *Life-inspired interoceptive artificial intelligence for autonomous and adaptive agents*, Nature Machine Intelligence 8, 1335–1346.


</details>

> 🌐 Language convention: [docs/LANGUAGE.md](LANGUAGE.md)
