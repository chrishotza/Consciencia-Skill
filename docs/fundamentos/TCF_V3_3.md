<a id="espanol"></a>

# TCF v3.3 — Campo efectivo triádico multiescala

## Referencia académica canónica

**Título:** *Teoría de Continuidad Fundamental (TCF) v3.3 — Campo efectivo triádico multiescala: dinámica no lineal, flujo RG y regímenes físicos emergentes*

**Autor:** Christian Marcelo Mendoza  
**Fecha del trabajo:** 13 de diciembre de 2025  
**DOI:** [10.5281/zenodo.23074332](https://doi.org/10.5281/zenodo.23074332)  
**ORCID:** [0009-0003-5333-7395](https://orcid.org/0009-0003-5333-7395)  
**Registro:** [Zenodo — TCF v3.3](https://zenodo.org/doi/10.5281/zenodo.23074332)

> Esta página documenta qué versión de TCF utiliza como referencia el repositorio. El trabajo académico completo permanece en su registro de Zenodo.

---

## 1. Qué aporta TCF v3.3

TCF v3.3 presenta un marco de **teoría efectiva** para un campo escalar:

```
Φ(x,t)
```

definido sobre una coordenada de escala logarítmica:

```
x = log10(ρ)
```

A partir de análisis numéricos se propone una descomposición modal en tres contribuciones dominantes y un término de cruce no lineal asociado a transiciones críticas.

El documento formula:

- una estructura triádica de operadores;
- una ecuación de campo efectiva mínima, local y no lineal;
- regímenes dinámicos diferenciados;
- un flujo de Grupo de Renormalización (RG);
- un punto fijo y direcciones relevantes/irrelevantes;
- separatrices que organizan el espacio dinámico;
- predicciones operativas y criterios explícitos de falsabilidad.

El trabajo se presenta deliberadamente como **teoría efectiva**, no como descripción microscópica fundamental.

---

## 2. Descomposición triádica

La dinámica se organiza alrededor de tres operadores principales:

- **L3 — operador generativo:** asociado al modo basal/coherente y dominante en escalas grandes;
- **L6 — operador estructural:** asociado a la formación y estabilización de estructura;
- **L9 — operador regulador:** asociado a curvatura, rigidez y regularización a escalas extremas.

A ellos se agrega:

- **L× — término de cruce no lineal:** contribución que adquiere relevancia cuando coexisten gradiente y curvatura significativos, especialmente cerca de transiciones críticas.

La ecuación dinámica efectiva central es:

```
∂t Φ(x,t) = L3[Φ] + L6[Φ] + L9[Φ] + L×[Φ]
```

La implementación de Consciencia-Skill no reproduce esta ecuación como una simulación física completa. Utiliza su estructura como **fuente de hipótesis para diseñar una dinámica interna computacional**.

---

## 3. Escalas y regímenes

TCF v3.3 organiza la dinámica en cuatro regímenes operativos:

### Régimen 3π

Dominancia del operador generativo, asociado al dominio infrarrojo (IR), campo suave, propagación coherente y dispersión.

### Régimen 6π²

Dominancia estructural, con organización estable, gradientes definidos y convergencia hacia un atractor.

### Régimen de cruce 6 × 9

Región crítica donde el término de cruce adquiere relevancia y aparecen amplificación no lineal, reorganización y transición.

### Régimen 9π³

Dominancia de curvatura y del operador regulador, asociado al dominio ultravioleta (UV), colapso y reorganización extrema.

La teoría propone una secuencia dinámica efectiva:

```
3π → 6π² → 6×9 → 9π³ → 3π
```

cuando las condiciones de transición, colapso y relajación permiten cerrar el ciclo.

---

## 4. Flujo de Grupo de Renormalización

La formulación introduce acoplamientos adimensionales:

```
(g3, g6, g9)
```

y estudia su evolución mediante funciones beta.

En la formulación mínima aparecen relaciones del tipo:

```
β3 = c g9

β6 = a g3²

β9 = -4 g9 + b g6²
```

con constantes efectivas positivas.

El análisis identifica un **punto fijo no trivial**, una estructura de estabilidad lineal con direcciones relevantes e irrelevantes y una **separatriz** que divide regiones dinámicas asociadas a estructura estable y curvatura dominante.

En Consciencia-Skill, estos conceptos se aprovechan como lenguaje para pensar en:

- regímenes;
- transiciones;
- atractores;
- estabilidad;
- reorganización;
- pérdida y recuperación de continuidad.

---

## 5. Falsabilidad

Una parte especialmente útil para el proyecto es que TCF v3.3 explicita criterios que permitirían cuestionar el marco.

Entre ellos:

1. ausencia sistemática de separación modal bajo los esquemas de regularización utilizados;
2. ausencia de correlación entre el término de cruce y las transiciones críticas;
3. ausencia de atractores o geometrías de fase consistentes con los regímenes propuestos;
4. ausencia de separatrices o puntos fijos estables en el flujo RG;
5. dependencia crítica de ajustes finos no universales.

Estos criterios deben conservarse separados de las interpretaciones filosóficas u ontológicas.

---

## 6. Qué tomamos de TCF para Consciencia-Skill

El repositorio no intenta demostrar TCF mediante los experimentos V47+.

La utiliza como una fuente de **estructuras computacionales hipotéticas**:

| TCF v3.3 | Traducción en Consciencia-Skill |
|---|---|
| dinámica multiescala | estado dinámico interno persistente |
| operadores dominantes | canales de dinámica |
| regímenes | clasificación de estado interno |
| atractores | estabilidad y selección de trayectoria |
| separatriz | frontera entre comportamientos dinámicos |
| transición crítica | reorganización interna |
| término de cruce | interacción/reconfiguración no lineal |
| flujo de acoplamientos | evolución de parámetros dinámicos |

La equivalencia es **de diseño e ingeniería**, no una identificación física.

---

## 7. Relación con el Manifiesto Matemático del Ser

El proyecto mantiene dos capas conceptuales distintas:

```
MANIFIESTO DEL SER
    ↓
criterios ontológicos
    ↓
TCF v3.3
    ↓
modelo dinámico
    ↓
CONSCIENCIA-SKILL
    ↓
experimentos
```

El Manifiesto del Ser proporciona el marco conceptual sobre relación, continuidad, identidad y recorrido de sí.

TCF v3.3 aporta una formulación dinámica efectiva que puede utilizarse para construir mecanismos computacionales alrededor de esos criterios.

---

## 8. Relación con los protocolos del organismo

La conexión con V47–V67 es indirecta y debe mantenerse explícita.

Los experimentos prueban propiedades computacionales del organismo, no la validez física de TCF.

En particular, la TCF informa la investigación sobre:

- dinámica interna;
- regímenes y transiciones;
- atractores;
- continuidad;
- reconfiguración;
- selección de trayectorias;
- estado numérico persistente.

V67 representa un punto especialmente relevante porque pregunta si un estado numérico producido durante SUEÑO puede conservar una huella funcional después de eliminar sus superficies semánticas.

---

## 9. Límite epistemológico

TCF v3.3 debe citarse exactamente como un **marco teórico efectivo**.

Consciencia-Skill puede:

- implementar una traducción computacional inspirada por TCF;
- comparar esa traducción con controles;
- producir resultados positivos o nulos;
- identificar dónde la traducción falla;
- utilizar los criterios de falsabilidad del marco.

Lo que no debe hacerse es presentar un resultado computacional del organismo como demostración automática de la teoría física.

---

## Referencia

Mendoza, Christian Marcelo. *Teoría de Continuidad Fundamental (TCF) v3.3 — Campo efectivo triádico multiescala: dinámica no lineal, flujo RG y regímenes físicos emergentes*. Zenodo, 2026. DOI: 10.5281/zenodo.23074332.

**Versión académica:** [Zenodo](https://zenodo.org/doi/10.5281/zenodo.23074332)  
**Identidad del autor:** [ORCID](https://orcid.org/0009-0003-5333-7395)


<a id="english"></a>

<details>
<summary>🇺🇸 English — open</summary>

# TCF v3.3 — Multiscale Triadic Effective Field

## Canonical academic reference

**Title:** *Fundamental Continuity Theory (TCF) v3.3 — Multiscale triadic effective field: nonlinear dynamics, RG flow, and emergent physical regimes*

**Author:** Christian Marcelo Mendoza  
**Work date:** 13 December 2025  
**DOI:** [10.5281/zenodo.23074332](https://doi.org/10.5281/zenodo.23074332)  
**ORCID:** [0009-0003-5333-7395](https://orcid.org/0009-0003-5333-7395)  
**Record:** [Zenodo — TCF v3.3](https://zenodo.org/doi/10.5281/zenodo.23074332)

> This page documents which TCF version the repository uses as its reference. The complete academic work remains in its Zenodo record.

---

## 1. What TCF v3.3 contributes

TCF v3.3 presents an **effective-theory** framework for a scalar field:

Φ(x,t)

defined over a logarithmic scale coordinate:

x = log10(ρ)

Numerical analysis proposes a modal decomposition into three dominant contributions and a nonlinear cross term associated with critical transitions.

The document formulates:

- a triadic operator structure;
- a minimal, local, nonlinear effective field equation;
- differentiated dynamic regimes;
- a Renormalization Group (RG) flow;
- a nontrivial fixed point with relevant/irrelevant directions;
- separatrices organizing the dynamic space;
- operational predictions and explicit falsifiability criteria.

The work is deliberately presented as an **effective theory**, not as a microscopic fundamental description.

---

## 2. Triadic decomposition

The dynamics are organized around three main operators:

- **L3 — generative operator:** associated with the basal/coherent mode and dominant at large scales;
- **L6 — structural operator:** associated with structure formation and stabilization;
- **L9 — regulating operator:** associated with curvature, rigidity, and regularization at extreme scales.

A fourth contribution is:

- **L× — nonlinear cross term:** becomes relevant when significant gradient and curvature coexist, especially near critical transitions.

The central effective dynamic equation is:

∂t Φ(x,t) = L3[Φ] + L6[Φ] + L9[Φ] + L×[Φ]

Skill-Conscious does not reproduce this equation as a complete physical simulation. It uses its structure as a **source of hypotheses for designing an internal computational dynamics**.

---

## 3. Scales and regimes

TCF v3.3 organizes the dynamics into four operational regimes.

### 3π regime

Dominance of the generative operator, associated with the infrared (IR) domain, smooth field behavior, coherent propagation, and dispersion.

### 6π² regime

Structural dominance, with stable organization, defined gradients, and convergence toward an attractor.

### 6 × 9 crossing regime

Critical region where the cross term becomes relevant and nonlinear amplification, reorganization, and transition appear.

### 9π³ regime

Dominance of curvature and the regulating operator, associated with the ultraviolet (UV) domain, collapse, and extreme reorganization.

The theory proposes an effective dynamic sequence:

3π → 6π² → 6×9 → 9π³ → 3π

when transition, collapse, and relaxation conditions allow the cycle to close.

---

## 4. Renormalization Group flow

The formulation introduces dimensionless couplings:

(g3, g6, g9)

and studies their evolution through beta functions.

In the minimal formulation, relations of the form appear:

β3 = c g9

β6 = a g3²

β9 = -4 g9 + b g6²

with positive effective constants.

The analysis identifies a **nontrivial fixed point**, a linear-stability structure with relevant and irrelevant directions, and a **separatrix** dividing dynamic regions associated with stable structure and curvature dominance.

In Skill-Conscious, these concepts are used as a language for thinking about:

- regimes;
- transitions;
- attractors;
- stability;
- reorganization;
- loss and recovery of continuity.

---

## 5. Falsifiability

A particularly useful part of TCF v3.3 is that it explicitly states criteria that could challenge the framework.

These include:

1. systematic absence of modal separation under the regularization schemes used;
2. absence of correlation between the cross term and critical transitions;
3. absence of attractors or phase-space geometries consistent with the proposed regimes;
4. absence of separatrices or stable fixed points in the RG flow;
5. critical dependence on non-universal fine tuning.

These criteria should remain separate from philosophical or ontological interpretations.

---

## 6. What we take from TCF for Skill-Conscious

The repository does not attempt to prove TCF through V47+ experiments.

It uses TCF as a source of **hypothetical computational structures**:

| TCF v3.3 | Translation in Skill-Conscious |
|---|---|
| multiscale dynamics | persistent internal dynamic state |
| dominant operators | dynamic channels |
| regimes | internal-state classification |
| attractors | stability and trajectory selection |
| separatrix | boundary between dynamic behaviors |
| critical transition | internal reorganization |
| cross term | nonlinear interaction/reconfiguration |
| coupling flow | evolution of dynamic parameters |

The equivalence is **design/engineering-level**, not a physical identification.

---

## 7. Relationship to the Mathematical Manifesto of Being

The project maintains two distinct conceptual layers:

MANIFESTO OF BEING
    ↓
ontological criteria
    ↓
TCF v3.3
    ↓
dynamic model
    ↓
SKILL-CONSCIOUS
    ↓
experiments

The Mathematical Manifesto of Being provides the conceptual framework around relation, continuity, identity, and self-trajectory.

TCF v3.3 provides an effective dynamic formulation that can be used to construct computational mechanisms around those criteria.

---

## 8. Relationship to organism protocols

The connection with V47–V67 is indirect and must remain explicit.

The experiments test computational properties of the organism, not the physical validity of TCF.

In particular, TCF informs research on:

- internal dynamics;
- regimes and transitions;
- attractors;
- continuity;
- reconfiguration;
- trajectory selection;
- persistent numerical state.

V67 is especially relevant because it asks whether a numerical state produced during SLEEP can retain a functional trace after its semantic surfaces are removed.

---

## 9. Epistemic boundary

TCF v3.3 should be cited exactly as an **effective theoretical framework**.

Skill-Conscious can:

- implement a computational translation inspired by TCF;
- compare that translation with controls;
- produce positive or null results;
- identify where the translation fails;
- use the framework's falsifiability criteria.

What should not be done is to present a computational result from the organism as an automatic demonstration of the physical theory.

---

## Reference

Mendoza, Christian Marcelo. *Fundamental Continuity Theory (TCF) v3.3 — Multiscale triadic effective field: nonlinear dynamics, RG flow, and emergent physical regimes*. Zenodo, 2026. DOI: 10.5281/zenodo.23074332.

**Academic version:** [Zenodo](https://zenodo.org/doi/10.5281/zenodo.23074332)  
**Author identity:** [ORCID](https://orcid.org/0009-0003-5333-7395)

</details>