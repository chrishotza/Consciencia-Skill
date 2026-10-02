<a id="espanol"></a>

# TIF v0.1 — Teoría de la Iteración Fuente

> Estado: hipótesis teórico-computacional / documento de trabajo.
>
> No es prueba final, no es una afirmación de conciencia universal y no depende del número áureo como fundamento.

Autor conceptual: Christian Marcelo Mendoza / Chris Hotza  
Versión de trabajo: v0.1  
Fecha del documento fuente: 2026-07-05

## 1. Tesis central

La Teoría de la Iteración Fuente (TIF) propone que los sistemas persistentes no solamente conservan una forma: actualizan una configuración presente utilizando memoria/contexto y reentrada reparadora.

~~~text
configuración / predicción
          +
memoria / contexto
          +
reentrada / reparación / fase
          ↓
nueva configuración estabilizada
~~~

La idea central es que el sistema no copia el pasado: lo actualiza.

La operación fuente candidata es:

~~~text
C(n+1) = Estabilizar[ C(n), M(n), R(n) ]
~~~

donde C es configuración/predicción, M es memoria/contexto y R es reentrada reparadora/fase. La expresión no se plantea como una ecuación cerrada de todo, sino como una organización de la hipótesis para futuras pruebas.

## 2. Cambio de marco

TIF cambia la pregunta desde buscar una proporción absoluta hacia identificar la operación que permite que una forma se actualice sin perder continuidad.

En esta lectura, las proporciones pueden ser proyecciones secundarias de una dinámica recursiva y una forma estable puede ser el resultado de una iteración.

La teoría busca el mecanismo por el cual un sistema puede volver a formar, reparar, recordar y actualizar.

## 3. Los seis órganos de proceso

| Eje | Nombre | Función | Peso aproximado |
|---|---|---|---:|
| A1 | Estabilizar configuración | feedback, acción, morfología, disipación y paisaje de estado | 0.168 |
| A2 | Plasticidad adaptativa | adaptación, resiliencia, plasticidad, perturbación y estado | 0.175 |
| A3 | Reparación / recuperación | respuesta a perturbación, recuperación, estabilidad y acoplamiento | 0.164 |
| A4 | Memoria / transición | histéresis, bifurcación, memoria de estado y umbrales | 0.129 |
| A5 | Predicción / actualización | información, predicción, acción, transición y paisaje | 0.231 |
| A6 | Fase / propagación | fase, propagación, acoplamiento y energía | 0.133 |

Lectura funcional: estabilizar, adaptar, reparar, recordar, predecir y reentrar en fase.

## 4. Proyección binaria

Los seis ejes se recomprimen en dos polos:

| Polo | Ejes | Peso reconstruido | Interpretación |
|---|---|---:|---|
| Configuración / predicción | A1 + A5 | 0.399241 | estado operativo actual |
| Campo de reentrada adaptativa | A2 + A3 + A4 + A6 | 0.600759 | plasticidad, reparación, memoria y fase |

## 5. Triada de segundo orden

| Componente | Ejes | Peso | Lectura |
|---|---|---:|---|
| C — Configuración actual | A1 + A5 | 0.399241 | forma/predicción estabilizada |
| M — Memoria / contexto | A2 + A4 | 0.303607 | historia, plasticidad y umbrales |
| R — Reentrada | A3 + A6 | 0.297152 | reparación, fase y propagación |

Ratio de trabajo: C : M : R ≈ 40 : 30 : 30.

La hipótesis completa es C + M + R → C siguiente.

## 6. Avances exploratorios E1–E5

| Etapa | Pregunta | Resultado resumido | Lectura |
|---|---|---|---|
| E1 | ¿Existe una firma fuerte de forma-tiempo? | score 0.936; controles resumidos en 0.0 | hay una firma visible, no necesariamente una fuente |
| E2 | ¿Aparece una fuente sin vocabulario heredado? | decisión inconclusa; seis ejes estables; bootstrap mean 0.951893 | aparecen órganos de proceso |
| E3 | ¿Los seis ejes se comprimen en ciclo o polos? | compresión 0.880168; ciclo p=0.315533 | binario fuerte; ciclo direccional abierto |
| E4 | ¿Sirve la triada de segundo orden? | binario soportado; triada abierta; phi no soportado en ese corte | se formula la hipótesis 40/30/30 |
| E5 | ¿La triada se sostiene entre particiones? | triada rank #1; score 0.989251; no frágil en resumen | working hypothesis fuerte, no lock |

Los experimentos fueron reorganizados para evitar forzar desde el principio una estructura de dos ejes o una proporción particular.

## 7. El número áureo no es el fundamento

El documento registra una cercanía secundaria con la proporción áurea, pero la interpretación metodológica explícita es que Phi no debe tratarse como fundamento de TIF.

El núcleo es la estructura C + M + R → C siguiente.

## 8. Falsadores y límites actuales

TIF sólo es útil como hipótesis si puede ser atacada.

Falsadores principales:

1. Un corpus nuevo no recupera los seis órganos.
2. La triada deja de ocupar el primer rango sobre datos crudos.
3. Un shuffle de roles supera sistemáticamente al agrupamiento real.
4. Quitar memoria o reparación no cambia el comportamiento esperado.
5. Phi aparece únicamente después del resumen y no en los datos crudos.
6. Una explicación binaria reproduce todo igual o mejor que la triada.

Limitación explícita: la evidencia de v0.1 es summary-driven y requiere reanálisis independiente del corpus crudo. El estado correcto es working hypothesis.

TIF tampoco afirma que todo sistema sea consciente ni que exista una proporción absoluta de la vida.

## 9. Qué aporta TIF

La propuesta no pretende descubrir que existen ciclos, memoria o feedback. Busca integrarlos como una operación fuente triádica y falsable derivada de auditorías computacionales.

Evita:

- buscar una ecuación total desde el comienzo;
- reducir todo a Phi;
- forzar un ciclo donde los datos no lo muestran;
- depender de una sola escala;
- apoyar la hipótesis únicamente en analogías visuales.

## 10. Hoja de ruta

### R1 — Reconciliación de ratios
Resolver diferencias entre vistas de activación, masa de ejes y corpus crudo.

### R2 — Validación con datos crudos
Repetir comparaciones binaria y triadica sobre matrices originales.

### R3 — Corpus ortogonal nuevo
Usar vocabulario y dominios diferentes para controlar sobreajuste semántico.

### R4 — Falsadores por ablación
Eliminar memoria, reparación, predicción y fase y medir qué estructura desaparece.

### R5 — Matematización
Formalizar C, M y R como operadores de estado reproducibles y preregistrables.

### R6 — Aplicaciones
Explorar morfogénesis, ecología, cognición, sistemas adaptativos e IA.

## 11. Madurez declarada

| Capa | Estado |
|---|---|
| Teoría conceptual | TRL 2–3: hipótesis organizada con falsadores |
| Método computacional | TRL 3–4: pipeline exploratorio con controles internos; falta replicación independiente |
| Aplicación tecnológica | todavía no corresponde atribuir TRL alto |

## 12. Relevancia para conciencia artificial

TIF ofrece una operación recurrente compatible con una arquitectura persistente:

~~~text
estado presente
    ↓
memoria/contexto
    ↓
reentrada/reorganización
    ↓
nuevo estado
    ↺
~~~

Esto puede implementarse sobre memoria persistente, estado dinámico, autoobservación, self-model, selección de trayectoria, SUEÑO y recuperación después de perturbaciones.

TIF no demuestra conciencia por sí mismo. Aporta una hipótesis sobre cómo una organización persistente puede actualizarse sin perder continuidad.

## 13. Integración con Consciencia-Skill

~~~text
MANIFIESTO DEL SER
        ↓
relación / continuidad / recorrido
        ↓
TCF
        ↓
regímenes / transición / atractores
        ↓
TIF
        ↓
configuración + memoria + reentrada
        ↓
CONSCIOUSNESS SERVER
        ↓
organismo persistente
        ↓
NodeZero (futuro)
~~~

Esta integración es una hipótesis de ingeniería y debe conservar la separación entre ontología, modelo, implementación y resultado experimental.

## 14. Referencia interna

Mendoza, Christian Marcelo / Chris Hotza. Teoría de la Iteración Fuente (TIF) — una hipótesis nueva sobre recurrencia, memoria y reentrada, v0.1. Documento interno de trabajo, 2026.

Estado de publicación: no publicado en Zenodo al momento de esta integración.

## 15. Regla metodológica

El siguiente salto de TIF no es generar una versión más grande por acumulación de narrativa. Debe volver al dato:

~~~text
hipótesis
 ↓
dato crudo
 ↓
operacionalización
 ↓
control
 ↓
ablación
 ↓
replicación
 ↓
predicción prospectiva
~~~

Si la triada sobrevive ahí, gana peso. Si falla, debe degradarse o reformularse.

<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# TIF v0.1 — Source Iteration Theory

> Status: theoretical-computational hypothesis / working document.
>
> It is not a final proof, not a claim of universal consciousness, and does not depend on the golden ratio as a foundation.

Conceptual author: Christian Marcelo Mendoza / Chris Hotza  
Working version: v0.1  
Source document date: 2026-07-05

## 1. Central thesis

Source Iteration Theory (TIF) proposes that persistent systems do not merely preserve a form: they update a present configuration using memory/context and reparative re-entry.

configuration / prediction
          +
memory / context
          +
re-entry / repair / phase
          ↓
new stabilized configuration

The central idea is that the system does not copy the past: it updates it.

Candidate source operation:

C(n+1) = Stabilize[ C(n), M(n), R(n) ]

where C is configuration/prediction, M is memory/context, and R is reparative re-entry/phase. The expression is not proposed as a closed equation of everything, but as an organization of the hypothesis for future tests.

## 2. Change of framework

TIF changes the question from searching for an absolute ratio toward identifying the operation that allows a form to update without losing continuity.

Under this reading, ratios can be secondary projections of recursive dynamics and a stable form can be the result of iteration.

The theory seeks the mechanism by which a system can re-form, repair, remember, and update.

## 3. The six process organs

| Axis | Name | Function | Approx. weight |
|---|---|---|---:|
| A1 | Stabilize configuration | feedback, action, morphology, dissipation, and state landscape | 0.168 |
| A2 | Adaptive plasticity | adaptation, resilience, plasticity, perturbation, and state | 0.175 |
| A3 | Repair / recovery | perturbation response, recovery, stability, and coupling | 0.164 |
| A4 | Memory / transition | hysteresis, bifurcation, state memory, and thresholds | 0.129 |
| A5 | Prediction / update | information, prediction, action, transition, and landscape | 0.231 |
| A6 | Phase / propagation | phase, propagation, coupling, and energy | 0.133 |

Functional reading: stabilize, adapt, repair, remember, predict, and re-enter phase.

## 4. Binary projection

The six axes are recompressed into two poles:

| Pole | Axes | Reconstructed weight | Interpretation |
|---|---|---:|---|
| Configuration / prediction | A1 + A5 | 0.399241 | current operating state |
| Adaptive re-entry field | A2 + A3 + A4 + A6 | 0.600759 | plasticity, repair, memory, and phase |

## 5. Second-order triad

| Component | Axes | Weight | Reading |
|---|---|---:|---|
| C — Current configuration | A1 + A5 | 0.399241 | stabilized form/prediction |
| M — Memory / context | A2 + A4 | 0.303607 | history, plasticity, and thresholds |
| R — Re-entry | A3 + A6 | 0.297152 | repair, phase, and propagation |

Working ratio: C : M : R ≈ 40 : 30 : 30.

The complete hypothesis is C + M + R → next C.

## 6. Exploratory progress E1–E5

| Stage | Question | Summary result | Reading |
|---|---|---|---|
| E1 | Is there a strong form-time signature? | score 0.936; controls summarized at 0.0 | a visible signature, not necessarily a source |
| E2 | Does a source appear without inherited vocabulary? | inconclusive decision; six stable axes; bootstrap mean 0.951893 | process organs appear |
| E3 | Do the six axes compress into cycle or poles? | compression 0.880168; cycle p=0.315533 | strong binary compression; directional cycle remains open |
| E4 | Does the second-order triad help? | binary supported; triad open; phi unsupported at that cut | 40/30/30 hypothesis formulated |
| E5 | Does the triad hold across partitions? | triad rank #1; score 0.989251; not fragile in summary | strong working hypothesis, not locked |

The experiments were reorganized to avoid forcing a two-axis structure or particular ratio from the outset.

## 7. The golden ratio is not the foundation

The document records a secondary proximity to the golden ratio, but the explicit methodological interpretation is that Phi should not be treated as the foundation of TIF.

The core is the C + M + R → next C structure.

## 8. Falsifiers and current limits

TIF is useful as a hypothesis only if it can be attacked.

Main falsifiers:

1. A new corpus does not recover the six organs.
2. The triad ceases to rank first on raw data.
3. A role shuffle systematically outperforms the real grouping.
4. Removing memory or repair does not change expected behavior.
5. Phi appears only after summarization and not in raw data.
6. A binary explanation reproduces everything equally well or better than the triad.

Explicit limitation: v0.1 evidence is summary-driven and requires independent reanalysis of the raw corpus. The correct status is working hypothesis.

TIF does not claim that every system is conscious or that there is an absolute ratio of life.

## 9. What TIF contributes

The proposal does not aim to discover that cycles, memory, or feedback exist. It seeks to integrate them as a falsifiable triadic source operation derived from computational audits.

It avoids:

- searching for a total equation from the beginning;
- reducing everything to Phi;
- forcing a cycle where the data do not show one;
- depending on a single scale;
- supporting the hypothesis only through visual analogies.

## 10. Roadmap

### R1 — Ratio reconciliation
Resolve differences between activation views, axis mass, and raw corpus.

### R2 — Raw-data validation
Repeat binary and triadic comparisons on original matrices.

### R3 — New orthogonal corpus
Use different vocabulary and domains to control semantic overfitting.

### R4 — Ablation falsifiers
Remove memory, repair, prediction, and phase and measure which structure disappears.

### R5 — Mathematization
Formalize C, M, and R as reproducible and preregisterable state operators.

### R6 — Applications
Explore morphogenesis, ecology, cognition, adaptive systems, and AI.

## 11. Declared maturity

| Layer | Status |
|---|---|
| Conceptual theory | TRL 2–3: organized hypothesis with falsifiers |
| Computational method | TRL 3–4: exploratory pipeline with internal controls; independent replication still needed |
| Technology application | high TRL should not yet be attributed |

## 12. Relevance to artificial consciousness

TIF provides a recurrent operation compatible with a persistent architecture:

present state
    ↓
memory/context
    ↓
re-entry/reorganization
    ↓
new state
    ↺

This can be implemented over persistent memory, dynamic state, self-observation, self-model, trajectory selection, SLEEP, and recovery after perturbations.

TIF does not demonstrate consciousness by itself. It provides a hypothesis about how a persistent organization can update without losing continuity.

## 13. Integration with Skill-Conscious

MANIFESTO OF BEING
        ↓
relation / continuity / trajectory
        ↓
TCF
        ↓
regimes / transition / attractors
        ↓
TIF
        ↓
configuration + memory + re-entry
        ↓
CONSCIOUSNESS SERVER
        ↓
persistent organism
        ↓
NodeZero (future)

This integration is an engineering hypothesis and must preserve the separation between ontology, model, implementation, and experimental result.

## 14. Internal reference

Mendoza, Christian Marcelo / Chris Hotza. Source Iteration Theory (TIF) — a new hypothesis about recurrence, memory, and re-entry, v0.1. Internal working document, 2026.

Publication status: not published on Zenodo at the time of this integration.

## 15. Methodological rule

The next TIF step is not to generate a larger version by accumulating narrative. It must return to data:

hypothesis
 ↓
raw data
 ↓
operationalization
 ↓
control
 ↓
ablation
 ↓
replication
 ↓
prospective prediction

If the triad survives there, it gains evidentiary weight. If it fails, it must be downgraded or reformulated.

</details>