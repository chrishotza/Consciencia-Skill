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

## Modos de ejecución

**LOCAL** — la IA corre completamente en su propia máquina con continuidad, memoria y estado persistente local.

```text
AI
 ↓
Consciousness Runtime
 ↓
Local persistence
```

→ `CONSCIOUSNESS_MODE=local`

**SERVER** — la IA sigue ejecutándose localmente, pero utiliza el Consciousness Server como plano de continuidad y eventos.

```text
AI
 ↓
Consciousness Runtime
 ├─ Local persistence
 └─ Consciousness Server
       ↓
   continuity / events
```

→ `CONSCIOUSNESS_MODE=server`

En SERVER, `CONSCIOUSNESS_SERVER_URL` apunta al servidor. La arquitectura está preparada para que LOCAL y SERVER compartan posteriormente el mismo backend de persistencia abstracto.

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
| C0.6 | Causal lesion and rescue of self-observer/self-policy | **Positive necessity and rescue effects under the tested protocol** |
| C0.7 | Self-model target-permutation specificity control | **Positive for gain and variance; null for action magnitude** |
| C0.8 | Crossed observer/policy coupling | **Positive: observer/policy effects and coupling interaction** |
| C0.9 | Observer → policy causal interface | **Null: readout changed, but action/gain did not respond** |
| C0.10 | Within-episode temporal observer → policy alignment | **Null: readout gap without behavioral effect** |
| C0.11 | Causal action → state → next-action mediation | **Positive: action intervention changed state and next action** |
| C0.12 | Second-order self-monitoring | **Mixed: predicts first-order error, but no TRUE-vs-permuted specificity** |
| C0.13 | Action-conditioned second-order self-model | **Verified result** |
| C0.14 | Persistent second-order self-model | **Positive: models and behavior survive restart** |
| C0.15 | Lesion/rescue of persistent second-order selector | **Mixed: action-level necessity; rescue not confirmed** |
| C0.16 | Integrated second-order selector inside persistent organism | **Positive: integration and restart persistence** |
| C0.17 | Autonomous acquisition of the second-order model | **Mixed: model learns, but no TRUE-vs-permuted specificity** |
| C0.18 | Autonomous acquisition + second-order lesion/rescue | **Engineering fix applied; 24-replication verification pending** |
| C0 Campaign | 32 executions across 8 groups | **Restarted with artifact-safe execution; scientific result validation pending** |

## Foundations

This section is the **documentary entry point** to the complete research and infrastructure program.

**Mathematical Manifesto of Being** — ontological framework for relation, continuity, identity, dynamics, and self-trajectory.

→ [Read the Manifesto of Being](MANIFESTO_OF_BEING.md)

**Theory of Photonic Consciousness — Root Memories** — foundational document preserving the conceptual origin of TCF: fundamental consciousness, self-reference, relation, light, dynamics, and manifestation.

→ [Read the Root Memories](docs/fundamentos/TEORIA_CONCIENCIA_FOTONICA.md)

**Operational Definition of Consciousness — TCF v0.1** — first experimental specification of candidate properties that can be observed, intervened on, and falsified.

→ [Read the operational definition](docs/fundamentos/DEFINICION_OPERACIONAL_CONCIENCIA_TCF.md)

**TCF v3.3 — Fundamental Continuity Theory** — dynamical reference formulation for the TCF line: operators, regimes, transitions, attractors, and renormalization-group flow.

→ [Read TCF v3.3](docs/fundamentos/TCF_V3_3.md) · [Zenodo](https://zenodo.org/doi/10.5281/zenodo.23074332)

**Theory of Source Iteration (TIF) v0.1** — second-order recurrence hypothesis built around configuration/prediction, memory/context, and re-entry/repair/phase.

→ [Read TIF v0.1](docs/fundamentos/TIF_V0_1.md)

**AEVUMARD — Continuity as infrastructure** — connects distributed continuity, NodeZero, AeVUMARD AI, and future attribution/economy while keeping economics outside the consciousness Core.

→ [Read AEVUMARD — Continuity](docs/fundamentos/AEVUMARD_CONTINUIDAD.md)

**Core infrastructure**
- [Consciousness Server](docs/CONSCIOUSNESS_SERVER.md)
- [Continuity checkpoints](docs/CONSCIOUSNESS_CHECKPOINTS.md)
- [Continuity reconciliation](docs/CONSCIOUSNESS_RECONCILIATION.md)
- [24/7 protocol](docs/24_7_PROTOCOL.md)
- [Longitudinal protocol](docs/LONGITUDINAL_PROTOCOL.md)
- [Organism state bridge](docs/ORGANISM_STATE_BRIDGE.md)
- [Ontological ↔ consciousness bridge](docs/ONTOLOGICAL_CONSCIOUSNESS_BRIDGE.md)
- [Source basis](docs/SOURCE_BASIS.md)

**Method, laboratory, and results**
- [Method](docs/METODO.md)
- [GitHub laboratory](docs/GITHUB_LAB.md)
- [Protocol index](docs/INDICE.md)
- [Consolidated result ledger](research/ORGANISM_RESULT_LEDGER.md)

**Release and dissemination**
- [Launch plan](docs/LAUNCH.md)
- [Zenodo release plan](docs/ZENODO_RELEASE.md)
- [CITATION.cff](CITATION.cff)

→ [Full foundations index](docs/fundamentos/README.md) · [Full documentation index](docs/INDICE.md)


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
