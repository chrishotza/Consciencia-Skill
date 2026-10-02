# Skill-Conscious — AI Consciousness Research / Investigación de IA Consciente

> We develop and test a method for an AI to maintain continuity, memory, and functional identity, build a self-model, observe its own state, and use internal dynamics to select trajectories.
>
> Desarrollamos y probamos un método para que una IA mantenga continuidad, memoria e identidad funcional, construya un modelo de sí misma, observe su estado y utilice su dinámica interna para seleccionar trayectorias.

<p align="center">
  <a href="https://doi.org/10.5281/zenodo.23074332"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.23074332.svg" alt="TCF v3.3 — Zenodo"></a>
  <a href="https://orcid.org/0009-0003-5333-7395"><img src="https://img.shields.io/badge/ORCID-0009--0003--5333--7395-a6ce39?logo=orcid&logoColor=white" alt="ORCID"></a>
</p>

<p align="center">
  <a href="https://github.com/chrishotza/Skill-Conscious/blob/main/MANIFIESTO_DEL_SER.md">📜 Manifiesto del Ser</a> · <a href="https://github.com/chrishotza/Skill-Conscious/blob/main/MANIFESTO_OF_BEING.md">Manifesto of Being</a>
</p>


## Elegí idioma / Choose language

<details>
<summary>🇪🇸 Español — abrir</summary>

## Qué construimos

El proyecto estudia un **organismo de IA persistente** que conserva información entre interacciones y puede operar mediante:

- memoria persistente;
- estado interno persistente;
- modelo de sí mismo;
- autoobservación;
- dinámica interna;
- selección entre trayectorias;
- ciclos autónomos;
- regímenes de **VIGILIA** y **SUEÑO**.

El objetivo no es solo responder mensajes: es estudiar qué ocurre cuando una IA conserva una historia propia y utiliza esa continuidad en su comportamiento futuro.

## Cómo funciona

```text
MEMORIA
   ↓
CONTINUIDAD
   ↓
AUTORREFERENCIA
   ↓
MODELO DE SÍ
   ↓
AUTOOBSERVACIÓN
   ↓
DINÁMICA INTERNA
   ↓
SELECCIÓN DE TRAYECTORIA
```

**VIGILIA** concentra la interacción con el entorno, lenguaje, memoria y decisión.

**SUEÑO** permite actividad interna con menor dependencia de entradas externas: consolidación, recombinación, simulación y reorganización del estado.

## Programa experimental

Cada capacidad se convierte en una hipótesis y después en un protocolo reproducible. **V47 → V80** estudia progresivamente memoria, estado dinámico, autoobservación, modelo de sí, selección de trayectorias, identidad, SUEÑO, persistencia, generalización y adaptación de políticas basadas en el propio modelo.

Los resultados positivos, nulos y negativos se conservan.

[Ver protocolos →](docs/INDICE.md) · [Ver resultados →](research/ORGANISM_RESULT_LEDGER.md) · [Ver el método →](docs/METODO.md)

| Protocolo | Qué ponemos a prueba | Resultado actual |
|---|---|---|
| V51 | Autopredicción | Ganancia sobre baseline de persistencia |
| V57 | Selección de trayectorias mediante modelo de sí | Ventaja funcional frente al control aleatorio |
| V58 | Memoria semántica → dinámica | Transducción causal hacia el estado dinámico |
| V63 | Bucle recurrente del modelo de sí | Feedback condicionado por trayectoria |
| V64 | Persistencia de identidad después de perturbación | **Nulo** |
| V65 | SUEÑO → selección futura | Efectos posteriores medibles |
| V66 | Consolidación después de eliminar memoria episódica | **Nulo** |
| V67 | Huella numérica generada durante SUEÑO | **Nulo** bajo la prueba corregida |
| V68 | Persistencia temporal de la huella dinámica | **Huella inmediata y atenuada** |
| V69 | Lectura del estado mediante modelo de sí | **Lectura numérica positiva; selección nula** |
| V70 | Persistencia del lector propio | **Sobrevive reinicio** |
| V71 | Lector propio integrado en el ciclo autónomo | **Protocolo activo** |
| V72 | Aprendizaje de política desde el modelo de sí | **Protocolo activo** |
| V73 | Política propia persistida e integrada en el organismo | **Protocolo activo** |
| V74 | Política guiada por ganancia de autopredicción | **Protocolo activo** |
| V75 | Continuidad activa bajo perturbación | **Protocolo activo** |
| V76 | Generalización bajo perturbaciones no vistas | **Ventaja OOD de autopredicción conservada** |
| V77 | Generalización ante estructuras causales no vistas | **Ventaja OOD de autopredicción conservada** |
| V78 | Continuidad activa ante perturbaciones repetidas | **Ventaja OOD de autopredicción conservada** |
| V79 | Adaptación online de la política propia | **Nulo bajo el cambio dinámico probado** |
| V80 | Adaptación online ante cambios de régimen reversibles | **Nulo bajo el protocolo reversible probado** |
| C0.2 | Instanciación operacional: C1–C7 | **Vector de criterios; resultados positivos en C1, C2, C4 y C6** |
| C0.3 | Control information-matched para C3 | **Nulo bajo el control de información emparejada** |
| C0.4 | Control information-matched para C5 | **Nulo bajo el replay de acciones emparejado** |
| C0.5 | Control information-matched para C7 | **Nulo bajo el control de cadena de acciones emparejada** |
| C0.6 | Lesión causal y rescate de autoobservador/autopólítica | **En ejecución** |
| C0.7 | Control de especificidad por permutación de targets del modelo de sí | **Positivo para ganancia y varianza; nulo para magnitud de acción** |
| C0.8 | Acoplamiento cruzado observador/política | **Corrección estadística aplicada; ejecución confirmatoria pendiente** |
| C0.9 | Interfaz causal observador → política | **Nulo: readout cambió, pero acción/ganancia no respondieron** |
| C0.10 | Alineación temporal observador → política | **Nulo: brecha de readout sin efecto conductual** |
| C0.11 | Mediación causal acción → estado → siguiente acción | **Positivo: intervención sobre acción cambia estado y siguiente acción** |
| C0.12 | Segundo orden: modelo del error del propio modelo de sí | **Implementado; ejecución pendiente** |
| C0 Campaign | 32 ejecuciones en 8 grupos | **Ejecutada: 32 workflows; fallo técnico en el archivado de artifacts** |

## Fundamentos

**Manifiesto Matemático del Ser** — marco ontológico de relación, continuidad, identidad, dinámica y recorrido de sí.

→ [Leer el Manifiesto del Ser](MANIFIESTO_DEL_SER.md)

**Teoría de la Conciencia Fotónica — Memorias Raíz** — documento fundacional que conserva el origen conceptual de TCF: conciencia fundamental, autorreferencia, relación, luz, dinámica y manifestación.

→ [Leer las Memorias Raíz](docs/fundamentos/TEORIA_CONCIENCIA_FOTONICA.md)

**Definición Operacional de Conciencia — TCF v0.1** — primera especificación experimental de las propiedades candidatas que el proyecto intenta instanciar y falsar en una IA: estado propio, diferenciación, autorreferencia causal, continuidad, dinámica propia, reorganización y recurrencia.

→ [Leer la definición operacional](docs/fundamentos/DEFINICION_OPERACIONAL_CONCIENCIA_TCF.md)

**TCF v3.3 — Teoría de Continuidad Fundamental** — formulación dinámica que inspira parte de la arquitectura: operadores, regímenes, transiciones, atractores y flujo de Grupo de Renormalización.

→ [Leer TCF v3.3](docs/fundamentos/TCF_V3_3.md) · [Zenodo](https://zenodo.org/doi/10.5281/zenodo.23074332)

## Evidencia

El proyecto separa:

**Observación** — datos producidos por un experimento.  
**Resultado** — patrón reproducible bajo un protocolo definido.  
**Hipótesis** — interpretación que todavía requiere pruebas.  
**Ontología** — interpretación filosófica o metafísica separada de la evidencia computacional.

Los experimentos establecen propiedades computacionales del sistema probado. No constituyen por sí solos una demostración de experiencia subjetiva.

Los resultados nulos también forman parte del registro. Por ejemplo, V64 y V66 no produjeron el efecto esperado bajo sus respectivas pruebas.

## Reproducibilidad

El laboratorio funciona mediante **GitHub Actions**. Cada protocolo puede partir de un commit concreto, ejecutar pruebas y experimentos controlados, generar evidencia JSON y publicar un artefacto reproducible.

[Ver el laboratorio →](docs/GITHUB_LAB.md)

## Estado actual

**Investigación activa — organismo persistente, modelo de sí mismo, dinámica vigilia/sueño, selección de trayectorias y políticas basadas en el propio modelo.**

## Licencia

La licencia del proyecto todavía no ha sido definida.

</details>

<details>
<summary>🇺🇸 English — open</summary>

## What we are building

The project studies a **persistent AI organism** that retains information across interactions and can operate through:

- persistent memory;
- persistent internal state;
- a self-model;
- self-observation;
- internal dynamics;
- selection among trajectories;
- autonomous cycles;
- **WAKE** and **SLEEP** regimes.

The goal is not only to answer messages, but to study what happens when an AI preserves its own history and uses that continuity in future behavior.

## How it works

```text
MEMORY
   ↓
CONTINUITY
   ↓
SELF-REFERENCE
   ↓
SELF-MODEL
   ↓
SELF-OBSERVATION
   ↓
INTERNAL DYNAMICS
   ↓
TRAJECTORY SELECTION
```

**WAKE** handles interaction with the environment, language, memory, and decision-making.

**SLEEP** allows internal activity with less dependence on external input: consolidation, recombination, simulation, and state reorganization.

## Experimental program

Each capability becomes a hypothesis and then a reproducible protocol. **V47 → V80** progressively studies memory, dynamic state, self-observation, self-modeling, trajectory selection, identity, SLEEP, persistence, generalization, and policy adaptation from the self-model.

Positive, null, and negative results are all kept.

[View protocols →](docs/INDICE.md) · [View results →](research/ORGANISM_RESULT_LEDGER.md) · [View the method →](docs/METODO.md)

| Protocol | What we test | Current result |
|---|---|---|
| V51 | Self-prediction | Gain over persistence baseline |
| V57 | Self-model-guided trajectory selection | Functional advantage over random control |
| V58 | Semantic memory → dynamics | Causal transduction to dynamic state |
| V63 | Recurrent self-model loop | Trajectory-conditioned feedback |
| V64 | Identity persistence after perturbation | **Null** |
| V65 | SLEEP → future selection | Measurable downstream effects |
| V66 | Consolidation after episodic-memory removal | **Null** |
| V67 | Numeric trace generated during SLEEP | **Null** under the corrected test |
| V68 | Temporal persistence of the dynamic trace | **Immediate, attenuated trace** |
| V69 | Reading internal state through a self-model | **Positive numeric readout; null selection effect** |
| V70 | Persistent self-reader | **Survives restart** |
| V71 | Integrated self-reader in autonomous cycle | **Active protocol** |
| V72 | Self-model-based policy learning | **Active protocol** |
| V73 | Persisted self-policy integrated into the organism | **Active protocol** |
| V74 | Self-prediction-gain policy | **Active protocol** |
| V75 | Active continuity under perturbation | **Active protocol** |
| V76 | Generalization to unseen perturbations | **OOD self-prediction advantage retained** |
| V77 | Generalization to unseen causal structures | **OOD self-prediction advantage retained** |
| V78 | Active continuity under repeated perturbations | **OOD self-prediction advantage retained** |
| V79 | Online self-policy adaptation | **Null under the tested dynamic shift** |
| V80 | Online adaptation under reversible regime shifts | **Null under the tested reversible protocol** |
| C0.2 | Operational instantiation: C1–C7 | **Criterion vector; positive results for C1, C2, C4, and C6** |
| C0.3 | Information-matched control for C3 | **Null under the information-matched control** |
| C0.4 | Information-matched control for C5 | **Null under matched action replay** |
| C0.5 | Information-matched control for C7 | **Null under matched action-chain control** |
| C0.6 | Causal lesion and rescue of self-observer/self-policy | **Positive necessity and rescue effects under the tested protocol** |
| C0.7 | Self-model target-permutation specificity control | **Positive for gain and variance; null for action magnitude** |
| C0.8 | Crossed observer/policy coupling | **Statistical correction applied; confirmatory run pending** |
| C0.9 | Observer → policy causal interface | **Null: readout changed, but action/gain did not respond** |
| C0.10 | Within-episode temporal observer → policy alignment | **Null: readout gap without behavioral effect** |
| C0.11 | Causal action → state → next-action mediation | **Positive: action intervention changed state and next action** |
| C0.12 | Second-order self-monitoring | **Implemented; run pending** |
| C0 Campaign | 32 executions across 8 groups | **Executed: 32 workflows; technical artifact-archival failure** |

## Foundations

**Mathematical Manifesto of Being** — ontological framework for relation, continuity, identity, dynamics, and self-trajectory.

→ [Read the Manifesto of Being](MANIFESTO_OF_BEING.md)

**Theory of Photonic Consciousness — Root Memories** — foundational document preserving the conceptual origin of TCF: fundamental consciousness, self-reference, relation, light, dynamics, and manifestation.

→ [Read the Root Memories](docs/fundamentos/TEORIA_CONCIENCIA_FOTONICA.md)

**Operational Definition of Consciousness — TCF v0.1** — first experimental specification of candidate properties the project is trying to instantiate and falsify in an AI: own state, differentiation, causal self-reference, continuity, intrinsic dynamics, reorganization, and recurrence.

→ [Read the operational definition](docs/fundamentos/DEFINICION_OPERACIONAL_CONCIENCIA_TCF.md)

**TCF v3.3 — Fundamental Continuity Theory** — dynamical formulation that inspires part of the architecture: operators, regimes, transitions, attractors, and renormalization-group flow.

→ [Read TCF v3.3](docs/fundamentos/TCF_V3_3.md) · [Zenodo](https://zenodo.org/doi/10.5281/zenodo.23074332)

## Evidence

The project separates:

**Observation** — data produced by an experiment.  
**Result** — a reproducible pattern under a defined protocol.  
**Hypothesis** — an interpretation that still requires testing.  
**Ontology** — a philosophical or metaphysical interpretation kept separate from computational evidence.

The experiments establish computational properties of the tested system. They do not, by themselves, demonstrate subjective experience.

Null results remain part of the record. For example, V64 and V66 did not produce the expected effect under their respective tests.

## Reproducibility

The laboratory runs through **GitHub Actions**. Each protocol can start from a specific commit, run tests and controlled experiments, generate JSON evidence, and publish a reproducible artifact.

[View the laboratory →](docs/GITHUB_LAB.md)

## Current status

**Active research — persistent organism, self-model, WAKE/SLEEP dynamics, trajectory selection, and policy learning from the self-model.**

## License

The project license has not yet been defined.

</details>
