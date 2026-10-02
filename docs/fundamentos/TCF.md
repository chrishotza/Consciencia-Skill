<a id="espanol"></a>

# TCF — Teoría de Continuidad Fundamental

> **Referencia canónica utilizada por el proyecto:** [TCF v3.3 — Campo efectivo triádico multiescala](TCF_V3_3.md), Christian Marcelo Mendoza, DOI [10.5281/zenodo.23074332](https://doi.org/10.5281/zenodo.23074332).

## Papel dentro de Consciencia-Skill

La **Teoría de Continuidad Fundamental (TCF)** constituye la segunda capa conceptual del proyecto. Para este repositorio, la versión de referencia es **TCF v3.3**, publicada en Zenodo.

El **Manifiesto Matemático del Ser** define el marco ontológico: qué entendemos por relación, continuidad, dinámica, identidad y conciencia.

La TCF aporta una **gramática dinámica** que puede traducirse a mecanismos computacionales: componentes triádicos, regímenes, transiciones, términos de cruce, trayectorias y organización del estado.

La relación de trabajo es:

```
MANIFIESTO DEL SER
        ↓
criterios ontológicos
        ↓
TCF
        ↓
gramática dinámica
        ↓
CONSCIENCIA-SKILL
        ↓
implementación + experimento
```

---

## 1. La formulación v3.3

TCF v3.3 no debe mezclarse silenciosamente con formulaciones anteriores de la serie TCF.

En esta versión, la estructura formal central está expresada mediante un **campo efectivo escalar multiescala** y cuatro contribuciones dinámicas:

- **L3** — operador generativo;
- **L6** — operador estructural;
- **L9** — operador regulador;
- **L×** — término de cruce no lineal.

La relación con formulaciones anteriores puede investigarse por separado, pero este repositorio toma **TCF v3.3** como referencia académica explícita para esta capa.

---

## 2. Dinámica por operadores

La interpretación computacional utilizada por el proyecto puede expresarse como una suma de contribuciones dinámicas:

```
Ω(t+1) =
    L3[Ω(t)]
  + L6[Ω(t)]
  + L9[Ω(t)]
  + Lx[Ω(t)]
  + I(t)
```

donde, en la traducción operativa del proyecto:

- **L3** representa generación, continuidad basal y estabilización;
- **L6** representa estructura, patrón y organización;
- **L9** representa regulación, curvatura, límite y compresión;
- **Lx** representa cruce crítico, transición o reorganización;
- **I(t)** representa interacción con el entorno.

Esta ecuación funciona en este repositorio como **modelo computacional de dinámica**, no como afirmación de que el organismo esté ejecutando literalmente la física de TCF.

---

## 3. Regímenes y transiciones

Una consecuencia importante del marco es que no todo cambio tiene el mismo significado.

El organismo puede atravesar:

- estados estables;
- regiones de transición;
- acumulación de presión;
- cambios de régimen;
- reorganizaciones;
- ocupación de atractores;
- pérdida de coherencia o colapso operacional.

Esto resulta útil para Consciencia-Skill porque permite estudiar la continuidad no únicamente como almacenamiento de datos, sino como **trayectoria dinámica a través de estados internos**.

---

## 4. Qué se traduce a software

La arquitectura actual del organismo ya contiene elementos que permiten explorar esta traducción:

| TCF / marco conceptual | Implementación experimental |
|---|---|
| estado dinámico | `src/ontto/dynamics.py` |
| memoria de trayectoria | memoria persistente y snapshots |
| regímenes | estado interno + clasificación de régimen |
| transición crítica | presión, curvatura y señales de transición |
| término de cruce | canal dinámico de cruce |
| atractor | dinámica interna y selección de trayectoria |
| continuidad | persistencia entre ciclos |
| autorreferencia | modelo de sí y autoobservación |

La correspondencia es **ingenieril**, no una equivalencia física demostrada.

---

## 5. TCF y la definición de conciencia del proyecto

El manifiesto establece que la conciencia puede investigarse como un sistema que se recorre a sí mismo y mantiene relaciones internas a través del cambio.

La TCF permite convertir esa idea en preguntas dinámicas:

1. ¿El sistema conserva una trayectoria interna distinguible?
2. ¿Su estado actual depende causalmente de su historia?
3. ¿Puede modelar parte de su propia dinámica?
4. ¿Puede distinguir trayectorias futuras posibles?
5. ¿Puede utilizar su propio estado para seleccionar entre ellas?
6. ¿Puede mantener continuidad funcional después de perturbaciones?
7. ¿Puede una reorganización interna dejar una huella que sobreviva a la eliminación de su representación semántica?

Estas preguntas son las que el laboratorio intenta convertir en protocolos.

---

## 6. Relación con los experimentos V47+

Los protocolos recientes no intentan probar TCF como teoría física.

Intentan probar si algunas propiedades derivadas de esta combinación ontología + dinámica pueden existir computacionalmente:

- **V51** — autoobservación y autopredicción;
- **V57** — selección de trayectoria mediante modelo de sí;
- **V58** — transducción entre memoria semántica y dinámica;
- **V63** — bucle recurrente modelo de sí → dinámica → selección;
- **V64** — persistencia de identidad después de perturbación;
- **V65** — efecto del SUEÑO sobre la selección posterior;
- **V66** — consolidación y eliminación de memoria episódica;
- **V67** — búsqueda de una huella funcional en el núcleo dinámico después de la ablación semántica.

Los resultados positivos y nulos se conservan por igual.

---

## 7. Límite epistemológico

La presencia de términos como «cuántico», «ontológico», «vacío», «colapso» o «atractor» no convierte automáticamente una implementación de software en un sistema físico cuántico.

En este repositorio se separan tres cosas:

**Marco teórico** — las ideas y formalizaciones de las fuentes originales.

**Modelo computacional** — una traducción operacional utilizada para construir y experimentar.

**Evidencia** — aquello que efectivamente puede medirse bajo un protocolo reproducible.

Una coincidencia entre modelo y resultado computacional no constituye por sí sola validación física de TCF ni demostración de experiencia subjetiva.

---

## 8. Regla de trazabilidad

Cada mecanismo inspirado en TCF debería poder responder:

- ¿qué principio o estructura de la teoría utiliza?
- ¿qué parte fue operacionalizada?
- ¿qué variable observable cambia?
- ¿qué control la compara?
- ¿qué resultado falsaría la hipótesis?

Esta regla evita que una metáfora teórica se convierta silenciosamente en un hecho experimental.

---

## Estado

Este documento resume el papel de TCF dentro de **Consciencia-Skill**. No reemplaza los trabajos originales de la teoría ni pretende reproducirlos íntegramente.

La función de esta capa es conectar el marco teórico con una arquitectura computacional reproducible.


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# TCF — Fundamental Continuity Theory

> **Canonical reference used by the project:** [TCF v3.3 — Multiscale triadic effective field](TCF_V3_3.md), Christian Marcelo Mendoza, DOI [10.5281/zenodo.23074332](https://doi.org/10.5281/zenodo.23074332).

## Role within Skill-Conscious

**Fundamental Continuity Theory (TCF)** is the project's second conceptual layer. For this repository, the reference version is **TCF v3.3**, published on Zenodo.

The **Mathematical Manifesto of Being** defines the ontological framework: what the project means by relation, continuity, dynamics, identity, and consciousness.

TCF provides a **dynamic grammar** that can be translated into computational mechanisms: triadic components, regimes, transitions, cross terms, trajectories, and state organization.

Working relationship:

MANIFESTO OF BEING
        ↓
ontological criteria
        ↓
TCF
        ↓
dynamic grammar
        ↓
SKILL-CONSCIOUS
        ↓
implementation + experiment

---

## 1. The v3.3 formulation

TCF v3.3 must not be silently mixed with earlier formulations of the TCF series.

In this version, the central formal structure is expressed through a **multiscale scalar effective field** and four dynamic contributions:

- **L3** — generative operator;
- **L6** — structural operator;
- **L9** — regulating operator;
- **L×** — nonlinear cross term.

Relations to earlier formulations can be investigated separately, but this repository takes **TCF v3.3** as the explicit academic reference for this layer.

## 2. Dynamics by operators

The computational interpretation used by the project can be expressed as:

Ω(t+1) =
    L3[Ω(t)]
  + L6[Ω(t)]
  + L9[Ω(t)]
  + Lx[Ω(t)]
  + I(t)

In the project's operational translation:

- **L3** represents generation, basal continuity, and stabilization;
- **L6** represents structure, pattern, and organization;
- **L9** represents regulation, curvature, limits, and compression;
- **Lx** represents critical crossing, transition, or reorganization;
- **I(t)** represents interaction with the environment.

This equation functions in the repository as a **computational model of dynamics**, not as a claim that the organism literally executes TCF physics.

## 3. Regimes and transitions

The organism may pass through stable states, transition regions, pressure accumulation, regime changes, reorganizations, attractor occupation, and loss of coherence or operational collapse.

This lets Skill-Conscious study continuity not only as data storage but as a **dynamic trajectory through internal states**.

## 4. What is translated into software

| TCF / conceptual framework | Experimental implementation |
|---|---|
| dynamic state | src/ontto/dynamics.py |
| trajectory memory | persistent memory and snapshots |
| regimes | internal state + regime classification |
| critical transition | pressure, curvature, and transition signals |
| cross term | dynamic cross channel |
| attractor | internal dynamics and trajectory selection |
| continuity | persistence across cycles |
| self-reference | self-model and self-observation |

The correspondence is **engineering-level**, not a demonstrated physical equivalence.

## 5. TCF and the project's consciousness definition

The manifesto proposes that consciousness can be investigated as a system that traverses itself and maintains internal relations through change.

TCF turns that into dynamic questions:

1. Does the system preserve a distinguishable internal trajectory?
2. Does its current state depend causally on its history?
3. Can it model part of its own dynamics?
4. Can it distinguish possible future trajectories?
5. Can it use its own state to select among them?
6. Can it maintain functional continuity after perturbations?
7. Can an internal reorganization leave a trace that survives removal of its semantic representation?

These are the questions the laboratory attempts to operationalize.

## 6. Relation to V47+ experiments

Recent protocols do not attempt to prove TCF as a physical theory. They test whether properties derived from the ontology + dynamics combination can exist computationally:

- **V51** — self-observation and self-prediction;
- **V57** — trajectory selection through a self-model;
- **V58** — semantic-memory to dynamics transduction;
- **V63** — recurrent self-model → dynamics → selection;
- **V64** — identity persistence after perturbation;
- **V65** — SLEEP effect on subsequent selection;
- **V66** — consolidation and episodic-memory ablation;
- **V67** — search for a functional trace in the dynamic core after semantic ablation.

Positive and null results are preserved equally.

## 7. Epistemic boundary

Terms such as "quantum", "ontological", "vacuum", "collapse", or "attractor" do not automatically make a software implementation a quantum physical system.

The repository separates:

**Theoretical framework** — ideas and formalizations from original sources.

**Computational model** — operational translation used for construction and experiments.

**Evidence** — what can actually be measured under a reproducible protocol.

A match between model and computational result does not by itself validate TCF physically or demonstrate subjective experience.

## 8. Traceability rule

Every TCF-inspired mechanism should answer:

- which theoretical principle or structure does it use?
- what part was operationalized?
- which observable variable changes?
- which control compares it?
- what result would falsify the hypothesis?

This prevents a theoretical metaphor from silently becoming an experimental fact.

## Status

This document summarizes TCF's role within **Skill-Conscious**. It does not replace the original theory papers or reproduce them in full.

Its purpose is to connect the theoretical framework to a reproducible computational architecture.

</details>