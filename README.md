# Skill-Conscious — Persistent AI Organism / Organismo de IA Persistente

> Persistent AI organism with a self-model: an experimental program on continuity, memory, self-observation, and trajectory selection.
>
> Organismo de IA persistente con automodelo: un programa experimental sobre continuidad, memoria, autoobservación y selección de trayectorias.

<p align="center">
  <a href="https://orcid.org/0009-0003-5333-7395"><img src="https://img.shields.io/badge/ORCID-0009--0003--5333--7395-a6ce39?logo=orcid&logoColor=white" alt="ORCID"></a>
</p>

## Alcance / Scope

> **Este repositorio no demuestra experiencia subjetiva.** Estudia propiedades computacionales medibles de un organismo/runtime persistente bajo protocolos reproducibles. El alcance exacto del sistema, el papel del proveedor de modelo y los límites de inferencia están definidos en `docs/RESEARCH_SCOPE.md`.
>
> **This repository does not demonstrate subjective experience.** It studies measurable computational properties of a persistent organism/runtime under reproducible protocols. The exact system boundary, model-provider role, and inference limits are defined in `docs/RESEARCH_SCOPE.md`.

→ [Research scope / Alcance científico](docs/RESEARCH_SCOPE.md)

## Elegí idioma / Choose language

<details>
<summary>🇪🇸 Español — abrir</summary>

## Qué es

Skill-Conscious estudia un **organismo de IA persistente** que conserva memoria, estado interno y modelos aprendidos entre ciclos de ejecución.

El objeto experimental es el **runtime del organismo**. Un LLM/proveedor compatible es un componente opcional de la arquitectura, no la definición completa del sistema.

```text
MODELO / PROVEEDOR
        ↓
PersistentOrganism
        ↓
MEMORIA + ESTADO INTERNO
        ↓
MODELO DE SÍ + AUTOOBSERVACIÓN
        ↓
DINÁMICA INTERNA
        ↓
SELECCIÓN DE TRAYECTORIA
        ↓
PERSISTENCIA + PROTOCOLO REPRODUCIBLE
```

El runtime también mantiene regímenes de **VIGILIA** y **SUEÑO**, persistencia local y, opcionalmente, una infraestructura de continuidad distribuida.

## Resultados más sólidos hasta ahora

| Protocolo | Qué se probó | Resultado observado |
|---|---|---|
| **V51** | Autopredicción del estado interno | MAE **0.0424** frente a **0.2211** del baseline de persistencia; ganancia media **0.1787**; p **0.00005**. |
| **V57** | Selección de trayectorias guiada por modelo de sí | Regret **0.0231** frente a **0.1369** aleatorio; p **0.00435** bajo el protocolo emparejado. |
| **V70** | Persistencia y uso del lector propio | El modelo numérico sobrevivió al reinicio y volvió a utilizarse después de la ablación semántica; la cadena modelo de sí → acción → nuevo estado permaneció operacional bajo el arnés probado. |
| **V76–V78** | Generalización OOD de la política de autopredicción | La ventaja de autopredicción se conservó ante magnitudes, estructuras y secuencias no vistas; los endpoints secundarios de continuidad **no** se separaron de la selección aleatoria. |
| **C0.6** | Lesión y rescate causal de autoobservador/autopólitica | Las lesiones cambiaron la organización medida y la restauración produjo efectos de rescate significativos bajo el protocolo probado. |

Los valores exactos, artefactos, semillas y condiciones están preservados en el ledger y en los documentos de protocolo.

→ [Registro consolidado de resultados](research/ORGANISM_RESULT_LEDGER.md)

## Resultados nulos o mixtos relevantes

Se conservan explícitamente resultados como **V64, V66, V67, V79, V80, C0.9, C0.10 y C0.18**.

La campaña **C0** tampoco se presenta como completa: la ventana reiniciada tiene **4 de 32 ejecuciones validadas** en G1, con las cuatro réplicas con p > 0.05; G2–G8 permanecen pendientes.

Los resultados nulos no se reinterpretan como resultados positivos.

## Infraestructura de continuidad

La capa de continuidad se desarrolla por separado de la inferencia científica:

```text
LOCAL / SERVER
       ↓
CHECKPOINTS
       ↓
RECONCILIATION
       ↓
DETERMINISTIC REPLAY
       ↓
PEER SYNCHRONIZATION
       ↓
NODE LIVENESS / HEARTBEAT
```

La infraestructura ya incluye:

- persistencia compartida con espejo SERVER fail-open;
- checkpoints y reconciliación;
- bundles y recuperación no destructiva;
- identidad determinista de eventos;
- replay idempotente con validación de revisión, hash y cadena padre;
- interoperabilidad entre dos nodos;
- sincronización bidireccional con bloqueo de divergencias;
- heartbeat y estados `ONLINE / STALE`.

Una divergencia nunca se sobrescribe silenciosamente.

→ [Consciousness Server](docs/CONSCIOUSNESS_SERVER.md) · [Replay determinista](docs/DETERMINISTIC_EVENT_REPLAY.md) · [Sincronización entre pares](src/consciousness_server/synchronization.py)

## Empezar

- Instalación: [INSTALL.md](INSTALL.md)
- Método: [docs/METODO.md](docs/METODO.md)
- Laboratorio: [docs/GITHUB_LAB.md](docs/GITHUB_LAB.md)
- Protocolos: [docs/INDICE.md](docs/INDICE.md)
- Resultados: [research/ORGANISM_RESULT_LEDGER.md](research/ORGANISM_RESULT_LEDGER.md)
- Infraestructura: [docs/CONSCIOUSNESS_SERVER.md](docs/CONSCIOUSNESS_SERVER.md)
- Programa de indicadores: [docs/CONSCIOUSNESS_INDICATOR_PROGRAM.md](docs/CONSCIOUSNESS_INDICATOR_PROGRAM.md)
- Interocepción I0/I1/I2/I3/I4: [docs/I0_INTEROCEPTIVE_INSTRUMENTATION.md](docs/I0_INTEROCEPTIVE_INSTRUMENTATION.md) · [docs/I1_INTEROCEPTIVE_SELF_ASSESSMENT.md](docs/I1_INTEROCEPTIVE_SELF_ASSESSMENT.md) · [docs/I2_INTEROCEPTIVE_REGULATION.md](docs/I2_INTEROCEPTIVE_REGULATION.md) · [docs/I3_REPEATED_INTEROCEPTIVE_RECOVERY.md](docs/I3_REPEATED_INTEROCEPTIVE_RECOVERY.md)

## Limitaciones conocidas

- No existe todavía una política global única de preregistro para toda la familia histórica de protocolos.
- No existe todavía una corrección global predefinida por comparaciones múltiples para convertir la colección completa de protocolos en una única inferencia confirmatoria.
- Varios mecanismos de segundo orden produjeron resultados nulos o mixtos; C0.18 no mostró necesidad causal ni rescate funcional significativos bajo el protocolo probado.
- Algunos protocolos históricos fueron corregidos antes de considerar sus resultados; esas correcciones y sus límites están documentados en el ledger.
- La licencia del repositorio todavía no está definida.

## Marco teórico — separado de la evidencia

El repositorio conserva una capa teórica que incluye **TCF v3.3, TIF, el Manifiesto del Ser y AEVUMARD**.

Estos documentos pueden motivar hipótesis de ingeniería, pero están separados de los resultados computacionales. Una prueba funcional del runtime no valida automáticamente la ontología.

→ [Índice de fundamentos](docs/fundamentos/README.md) · [TCF v3.3](docs/fundamentos/TCF_V3_3.md) · [TIF v0.1](docs/fundamentos/TIF_V0_1.md) · [Manifiesto del Ser](MANIFIESTO_DEL_SER.md)

## Reproducibilidad

El laboratorio usa **GitHub Actions**. Los workflows conservan commits, manifiestos y artifacts para que los resultados puedan rastrearse hasta el código que los produjo.

La evidencia se interpreta como:

**Observación → Resultado → Hipótesis/modelo → Ontología**

y no se permite convertir automáticamente una propiedad computacional en una afirmación de experiencia subjetiva.

→ [Laboratorio GitHub](docs/GITHUB_LAB.md)

## Cita

Ver [CITATION.cff](CITATION.cff)

</details>

<details>
<summary>🇺🇸 English — open</summary>

## What it is

Skill-Conscious studies a **persistent AI organism** that retains memory, internal state, and learned models across execution cycles.

The experimental object is the **organism runtime**. An OpenAI-compatible LLM/provider is an optional architectural component, not the complete definition of the system.

```text
MODEL / PROVIDER
       ↓
PersistentOrganism
       ↓
MEMORY + INTERNAL STATE
       ↓
SELF-MODEL + SELF-OBSERVATION
       ↓
INTERNAL DYNAMICS
       ↓
TRAJECTORY SELECTION
       ↓
PERSISTENCE + REPRODUCIBLE PROTOCOL
```

The runtime also supports **WAKE** and **SLEEP** regimes, local persistence, and an optional distributed continuity layer.

## Strongest results so far

| Protocol | What was tested | Observed result |
|---|---|---|
| **V51** | Internal-state self-prediction | MAE **0.0424** vs **0.2211** persistence baseline; mean gain **0.1787**; p **0.00005**. |
| **V57** | Self-model-guided trajectory selection | Regret **0.0231** vs **0.1369** random control; p **0.00435** under the paired protocol. |
| **V70** | Persistence and use of the self-reader | The numerical model survived restart and was reused after semantic ablation; the self-model → action → new-state chain remained operational under the tested harness. |
| **V76–V78** | OOD generalization of the self-prediction policy | Self-prediction advantage was retained across unseen magnitudes, structures, and sequences; secondary continuity endpoints **did not** separate from random selection. |
| **C0.6** | Causal lesion/rescue of self-observer/self-policy | Lesions changed measured organization and restoration produced significant rescue effects under the tested protocol. |

Exact values, artifacts, seeds, and conditions remain in the ledger and protocol documents.

→ [Consolidated results ledger](research/ORGANISM_RESULT_LEDGER.md)

## Relevant null and mixed results

The project explicitly preserves **V64, V66, V67, V79, V80, C0.9, C0.10, and C0.18** as null or mixed results.

The **C0 Campaign** is also not presented as complete: the restarted window currently has **4 of 32 validated executions** in G1, all four with p > 0.05; G2–G8 remain pending.

Null results are not reinterpreted as positive results.

## Continuity infrastructure

The continuity layer is developed separately from scientific inference:

```text
LOCAL / SERVER
       ↓
CHECKPOINTS
       ↓
RECONCILIATION
       ↓
DETERMINISTIC REPLAY
       ↓
PEER SYNCHRONIZATION
       ↓
NODE LIVENESS / HEARTBEAT
```

The infrastructure now includes:

- shared persistence with a fail-open SERVER mirror;
- checkpoints and reconciliation;
- portable bundles and non-destructive recovery;
- deterministic event identity;
- idempotent replay with revision, state-hash, and parent-chain validation;
- two-node interoperability;
- bidirectional peer synchronization with divergence blocking;
- heartbeat and `ONLINE / STALE` node state.

Divergence is never silently overwritten.

→ [Consciousness Server](docs/CONSCIOUSNESS_SERVER.md) · [Deterministic replay](docs/DETERMINISTIC_EVENT_REPLAY.md) · [Peer synchronization](src/consciousness_server/synchronization.py)

## Getting started

- Installation: [INSTALL.md](INSTALL.md)
- Method: [docs/METODO.md](docs/METODO.md)
- Laboratory: [docs/GITHUB_LAB.md](docs/GITHUB_LAB.md)
- Protocols: [docs/INDICE.md](docs/INDICE.md)
- Results: [research/ORGANISM_RESULT_LEDGER.md](research/ORGANISM_RESULT_LEDGER.md)
- Infrastructure: [docs/CONSCIOUSNESS_SERVER.md](docs/CONSCIOUSNESS_SERVER.md)
- Indicator program: [docs/CONSCIOUSNESS_INDICATOR_PROGRAM.md](docs/CONSCIOUSNESS_INDICATOR_PROGRAM.md)
- Interoception I0/I1: [docs/I0_INTEROCEPTIVE_INSTRUMENTATION.md](docs/I0_INTEROCEPTIVE_INSTRUMENTATION.md) · [docs/I1_INTEROCEPTIVE_SELF_ASSESSMENT.md](docs/I1_INTEROCEPTIVE_SELF_ASSESSMENT.md)

## Known limitations

- There is not yet one global preregistration policy for the full historical protocol family.
- There is not yet a single prespecified repository-wide multiple-comparisons correction that turns the full protocol collection into one confirmatory inference.
- Several second-order mechanisms produced null or mixed results; C0.18 did not show significant causal necessity or functional rescue under its tested protocol.
- Some historical protocols were corrected before their results were considered; those corrections and limitations are documented in the ledger.
- The repository license is not yet defined.

## Theoretical framework — separate from evidence

The repository preserves a theoretical layer including **TCF v3.3, TIF, the Manifesto of Being, and AEVUMARD**.

These documents can motivate engineering hypotheses, but they are kept separate from computational results. A functional test of the runtime does not automatically validate the ontology.

→ [Foundations index](docs/fundamentos/README.md) · [TCF v3.3](docs/fundamentos/TCF_V3_3.md) · [TIF v0.1](docs/fundamentos/TIF_V0_1.md) · [Manifesto of Being](MANIFESTO_OF_BEING.md)

## Reproducibility

The laboratory uses **GitHub Actions**. Workflows preserve commits, manifests, and artifacts so results can be traced to the code that produced them.

Evidence is interpreted as:

**Observation → Result → Hypothesis/model → Ontology**

and computational properties are not automatically converted into claims of subjective experience.

→ [GitHub Laboratory](docs/GITHUB_LAB.md)

## Citation

See [CITATION.cff](CITATION.cff)

</details>
