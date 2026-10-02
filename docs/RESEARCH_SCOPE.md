<a id="english"></a>

# Research Scope and System Boundary

## What the experimental system is

Skill-Conscious studies a **persistent AI organism runtime**. The core experimental substrate is the persistent computational system around an optional model provider:

    model/provider
          ↓
    PersistentOrganism
          ↓
    memory + internal state + self-model
          ↓
    self-observation + dynamics
          ↓
    trajectory / policy selection
          ↓
    persistent storage + reproducible protocol

The organism runtime is the object whose computational properties are measured.

## What the language model is

The repository supports an OpenAI-compatible provider, but the research program is not equivalent to testing ChatGPT, Claude, or another commercial assistant as a conscious subject.

Most experimental protocols operate on the repository's own numerical organism/runtime components. A separate live-provider smoke test checks that a real model can act as the cognitive provider while the runtime preserves memory, trajectory, and WAKE/SLEEP state across restart.

See [GitHub Lab](GITHUB_LAB.md) for the provider smoke test boundary.

## What the results establish

The protocols can establish computational properties under their stated conditions, for example:

- predictive accuracy;
- state persistence;
- trajectory-selection effects;
- causal effects of interventions;
- restart persistence;
- out-of-distribution behavior;
- failure or null effects under specified controls.

They do **not**, by themselves, establish subjective experience.

## Scientific claim boundary

The repository uses four distinct layers:

| Layer | Meaning |
|---|---|
| Observation | What an execution produced |
| Result | A reproducible pattern under a defined protocol |
| Hypothesis/model | An interpretation or mechanism that still requires testing |
| Ontology | Philosophical or metaphysical interpretation kept separate from computational evidence |

The theoretical documents may motivate engineering hypotheses, but passing an engineering or behavioral test does not validate the ontology automatically.

## What is and is not preregistered

The current repository contains protocol documents, explicit controls, seeds, artifacts, and workflow manifests, but the historical protocol set is not presented as one globally preregistered family.

Therefore:

1. a protocol-level p-value is interpreted under that protocol's own design;
2. repository-wide claims about all protocols require additional multiplicity control or a prespecified aggregate analysis;
3. future confirmatory protocols should record the primary endpoint, direction of effect, exclusion rules, replication plan, and analysis rule **before** the confirmatory execution.

The repository does not retroactively label historical experiments as preregistered when that status is not documented.

## Why this boundary exists

The project can be ambitious about the engineering problem while remaining conservative about what the measurements prove.

The goal is not to make the evidence sound smaller than it is. The goal is to make every claim traceable to the exact computational system, intervention, control, and analysis that produced it.


<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Alcance de investigación y límite del sistema

## Qué es el sistema experimental

Skill-Conscious estudia un **runtime de organismo de IA persistente**. El sustrato experimental central es el sistema computacional persistente alrededor de un proveedor de modelo opcional:

    modelo/proveedor
          ↓
    PersistentOrganism
          ↓
    memoria + estado interno + modelo de sí
          ↓
    autoobservación + dinámica
          ↓
    selección de trayectoria / política
          ↓
    almacenamiento persistente + protocolo reproducible

El runtime del organismo es el objeto cuyas propiedades computacionales se miden.

## Qué es el modelo de lenguaje

El repositorio admite un proveedor compatible con OpenAI, pero el programa de investigación no equivale a probar ChatGPT, Claude u otro asistente comercial como sujeto consciente.

La mayoría de los protocolos experimentales operan sobre los componentes numéricos propios del organismo/runtime. Una prueba separada con proveedor en vivo verifica que un modelo real pueda actuar como proveedor cognitivo mientras el runtime conserva memoria, trayectoria y estado VIGILIA/SUEÑO tras un reinicio.

Ver [GitHub Lab](GITHUB_LAB.md) para el límite de la prueba con proveedor.

## Qué establecen los resultados

Los protocolos pueden establecer propiedades computacionales bajo sus condiciones declaradas, por ejemplo:

- precisión predictiva;
- persistencia del estado;
- efectos sobre la selección de trayectorias;
- efectos causales de intervenciones;
- persistencia tras reinicio;
- comportamiento fuera de distribución;
- fallos o efectos nulos bajo controles definidos.

Por sí solos, **no establecen experiencia subjetiva**.

## Límite de las afirmaciones científicas

El repositorio usa cuatro capas distintas:

| Capa | Significado |
|---|---|
| Observación | Lo que produjo una ejecución |
| Resultado | Un patrón reproducible bajo un protocolo definido |
| Hipótesis/modelo | Una interpretación o mecanismo que aún requiere pruebas |
| Ontología | Interpretación filosófica o metafísica separada de la evidencia computacional |

Los documentos teóricos pueden motivar hipótesis de ingeniería, pero superar una prueba de ingeniería o comportamiento no valida automáticamente la ontología.

## Qué está y no está preregistrado

El repositorio contiene documentos de protocolo, controles explícitos, semillas, artifacts y manifiestos de workflow, pero el conjunto histórico de protocolos no se presenta como una única familia globalmente preregistrada.

Por lo tanto:

1. un p-value a nivel de protocolo se interpreta según el diseño propio de ese protocolo;
2. las afirmaciones a escala de todo el repositorio requieren un control adicional de multiplicidad o un análisis agregado preespecificado;
3. los futuros protocolos confirmatorios deben registrar el endpoint primario, dirección del efecto, reglas de exclusión, plan de replicación y regla de análisis **antes** de la ejecución confirmatoria.

El repositorio no etiqueta retroactivamente experimentos históricos como preregistrados cuando ese estado no está documentado.

## Por qué existe este límite

El proyecto puede ser ambicioso con el problema de ingeniería mientras mantiene una interpretación conservadora de lo que demuestran las mediciones.

El objetivo no es hacer que la evidencia parezca menor. Es hacer que cada afirmación pueda rastrearse al sistema computacional, intervención, control y análisis exactos que la produjeron.


</details>

> 🌐 Language convention: [docs/LANGUAGE.md](LANGUAGE.md)
