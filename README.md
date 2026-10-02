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

→ [Research scope / Alcance científico](docs/RESEARCH_SCOPE.md#espanol)

## Elegí idioma / Choose language

> 🌐 La documentación pública sigue el mismo selector bilingüe del README. Ver [docs/LANGUAGE.md](docs/LANGUAGE.md#espanol) para la convención.

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

## Estado actual / Current frontier

- **I4.3** está verificado sobre tres estructuras de perturbación no vistas; la generalización del error predictivo es positiva, mientras que el endpoint agregado de recuperación es nulo.
- **I5.0** está verificado sobre 512 episodios emparejados y el prototipo de workspace acotado ya está en `main`.
- **I5.1** ya está integrado en `PersistentOrganism` y produjo un resultado nulo para los endpoints conductuales del mapeo broadcast→trayectoria probado; la persistencia del estado del workspace sí fue verificada.
- **I5.2** está verificado como mecanismo independiente GWT-4: FULL−SHUFFLED **+1.0**, p **4.99975×10⁻⁵**, con FULL−LESION **+0.76367**, p **4.99975×10⁻⁵**.
- **I5.3** está verificado como mecanismo independiente de asignación causal de atención: FULL−SHUFFLED target-mass **+0.97682**, p **4.99975×10⁻⁵**.
- **I5.4** integró I5.2 + I5.3 en `PersistentOrganism`: controles de consulta nulos; atención barajada cambió la acción en **20.83%** pero el costo de regret fue no significativo (p **0.5022**); persistencia exacta **100%**.
- **I5.5** verificó el mecanismo combinado de consulta + atención: FULL−SHUFFLED_QUERY **+1.0**, p **4.99975×10⁻⁵**; FULL−SHUFFLED_ATTENTION **+1.0**, p **4.99975×10⁻⁵**; NO_BOTTLENECK fue nulo.
- **Lattice v0/v1** son protocolos verificados del sustrato computacional; las afirmaciones físicas siguen explícitamente separadas de la implementación.
- **Siguiente integración:** llevar I5.2 a `PersistentOrganism` y después probar asignación causal de atención.
## Resultados más sólidos hasta ahora

| Protocolo | Qué se probó | Resultado observado |
|---|---|---|
| **V51** | Autopredicción del estado interno | MAE **0.0424** frente a **0.2211** del baseline de persistencia; ganancia media **0.1787**; p **0.00005**. |
| **V57** | Selección de trayectorias guiada por modelo de sí | Regret **0.0231** frente a **0.1369** aleatorio; p **0.00435** bajo el protocolo emparejado. |
| **V70** | Persistencia y uso del lector propio | El lector numérico sobrevivió al reinicio y volvió a utilizarse después de la ablación semántica; la cadena modelo de sí → acción → nuevo estado permaneció operacional bajo el arnés probado. |
| **V76–V78** | Generalización OOD de la política de autopredicción | La ventaja se conservó ante magnitudes, estructuras y secuencias no vistas; los endpoints secundarios de continuidad **no** se separaron de la selección aleatoria. |
| **I4.2** | Interocepción metacognitiva persistente | FULL superó a LESION en error y recuperación y a PERMUTED en ambos endpoints bajo la perturbación declarada; serialización/restauración exacta. |
| **I4.3** | Generalización estructural OOD del modelo de segundo orden | META−LESION error medio **−0.001549**, p **4.27×10⁻⁶**; META−PERMUTED **−0.001567**, p **9.38×10⁻⁶**; recuperación agregada META−LESION nula (p **0.1505**). |
| **C0.6** | Lesión y rescate causal de autoobservador/autopolítica | Las lesiones cambiaron la organización medida y la restauración produjo efectos de rescate significativos bajo el protocolo probado. |
| **Lattice v0** | Computación local, propagación y organización distribuida | XOR **1.0**; coupling cambió coherencia, redundancia y spread de perturbación; el control desacoplado retuvo más del patrón bruto. |
| **Lattice v1** | Retención temporal de huella después de retirar input | 128 réplicas; retención media a delay 8 **0.74870**; AUC **0.75976**; pérdida media por perturbación **0.00172** a delay 8. |
| **I5.0** | Workspace global acotado | 512 episodios; broadcast vs no-broadcast **+0.12695** de accuracy, p **5×10⁻⁵**; K=2 vs K=6 **+0.01758**, p **0.02225**; lesión del origen seleccionado diferencial **−0.49023**, p **5×10⁻⁵**. |
| **I5.1** | Integración del workspace en PersistentOrganism | Resultado nulo para los endpoints conductuales probados: NO_BROADCAST−FULL regret **+0.02124**, p **0.4928**; LESION−FULL **0.0**, p **1.0**; persistencia del estado **100%**. |
| **I5.2** | Consulta dependiente del estado / GWT-4 | 512 episodios; FULL−SHUFFLED **+1.0**, p **5×10⁻⁵**; FULL−ZERO **+0.77148**, p **5×10⁻⁵**; FULL−RANDOM **+0.74219**, p **5×10⁻⁵**; FULL−LESION **+0.76367**, p **5×10⁻⁵**. |
| **I5.3** | Asignación causal de atención | 512 episodios; target attention mass FULL **0.98456**; FULL−SHUFFLED **+0.97682**, p **5×10⁻⁵**; FULL−LESION **+0.73456**, p **5×10⁻⁵**. |
| **I5.4** | Integración persistente de consulta + atención | 24 réplicas; controles de consulta nulos; SHUFFLED_ATTENTION action-change **20.83%**, regret cost **+0.02804**, p **0.5022**; persistencia **100%**. |
| **I5.5** | Cuello de botella causal de consulta + atención | 512 episodios; FULL−SHUFFLED_QUERY **+1.0**, p **5×10⁻⁵**; FULL−SHUFFLED_ATTENTION **+1.0**, p **5×10⁻⁵**; NO_BOTTLENECK nulo. |

Estos resultados describen propiedades computacionales de protocolos concretos. **No constituyen por sí solos una demostración de experiencia subjetiva.**

→ [Registro consolidado de resultados](research/ORGANISM_RESULT_LEDGER.md#espanol) · [I5.0 Workspace](docs/I5_GLOBAL_WORKSPACE.md#espanol) · [I5.1 PersistentOrganism](docs/I5_1_PERSISTENT_ORGANISM_WORKSPACE.md#espanol) · [I5.2 State-Dependent Query](docs/I5_2_STATE_DEPENDENT_QUERY.md#espanol) · [Lattice v1](docs/LATTICE_COMPUTER_V1.md#espanol)
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

→ [Consciousness Server](docs/CONSCIOUSNESS_SERVER.md#espanol) · [Replay determinista](docs/DETERMINISTIC_EVENT_REPLAY.md#espanol) · [Sincronización entre pares](src/consciousness_server/synchronization.py)

## Estructura y consistencia

- Reglas para agentes: [AGENTS.md](AGENTS.md#espanol)
- Convenciones del repositorio: [docs/REPO_CONVENTIONS.md](docs/REPO_CONVENTIONS.md#espanol)
- Material histórico de CI retirado: [docs/ARCHIVED_CI.md](docs/ARCHIVED_CI.md#espanol)

## Empezar

- Instalación: [INSTALL.md](INSTALL.md#espanol)
- Método: [docs/METODO.md](docs/METODO.md#espanol)
- Laboratorio: [docs/GITHUB_LAB.md](docs/GITHUB_LAB.md#espanol)
- Protocolos: [docs/INDICE.md](docs/INDICE.md#espanol)
- Resultados: [research/ORGANISM_RESULT_LEDGER.md](research/ORGANISM_RESULT_LEDGER.md#espanol)
- Infraestructura: [docs/CONSCIOUSNESS_SERVER.md](docs/CONSCIOUSNESS_SERVER.md#espanol)
- Programa de indicadores: [docs/CONSCIOUSNESS_INDICATOR_PROGRAM.md](docs/CONSCIOUSNESS_INDICATOR_PROGRAM.md#espanol)
- Interocepción I0/I1/I2/I3/I4/I4.1/I4.2/I4.3: [docs/I0_INTEROCEPTIVE_INSTRUMENTATION.md](docs/I0_INTEROCEPTIVE_INSTRUMENTATION.md#espanol) · [docs/I1_INTEROCEPTIVE_SELF_ASSESSMENT.md](docs/I1_INTEROCEPTIVE_SELF_ASSESSMENT.md#espanol) · [docs/I2_INTEROCEPTIVE_REGULATION.md](docs/I2_INTEROCEPTIVE_REGULATION.md#espanol) · [docs/I3_REPEATED_INTEROCEPTIVE_RECOVERY.md](docs/I3_REPEATED_INTEROCEPTIVE_RECOVERY.md#espanol) · [docs/I4_METACOGNITIVE_INTEROCEPTION.md](docs/I4_METACOGNITIVE_INTEROCEPTION.md#espanol) · [docs/I4_1_METACOGNITIVE_RELIABILITY.md](docs/I4_1_METACOGNITIVE_RELIABILITY.md#espanol) · [docs/I4_2_PERSISTENT_METACOGNITIVE_LESION_RESCUE.md](docs/I4_2_PERSISTENT_METACOGNITIVE_LESION_RESCUE.md#espanol) · [docs/I4_3_STRUCTURAL_OOD_METACOGNITIVE_GENERALIZATION.md](docs/I4_3_STRUCTURAL_OOD_METACOGNITIVE_GENERALIZATION.md#espanol)
 - Lattice Computer: [v0](docs/LATTICE_COMPUTER_V0.md#espanol) · [v1](docs/LATTICE_COMPUTER_V1.md#espanol)
 - Workspace global I5.0: [docs/I5_GLOBAL_WORKSPACE.md](docs/I5_GLOBAL_WORKSPACE.md#espanol)
## Limitaciones conocidas

- No existe todavía una política global única de preregistro para toda la familia histórica de protocolos.
- No existe todavía una corrección global predefinida por comparaciones múltiples para convertir la colección completa de protocolos en una única inferencia confirmatoria.
- Varios mecanismos de segundo orden produjeron resultados nulos o mixtos; C0.18 no mostró necesidad causal ni rescate funcional significativos bajo el protocolo probado.
- Algunos protocolos históricos fueron corregidos antes de considerar sus resultados; esas correcciones y sus límites están documentados en el ledger.
- La licencia del repositorio todavía no está definida.

## Marco teórico — separado de la evidencia

El repositorio conserva una capa teórica que incluye **TCF v3.3, TIF, el Manifiesto del Ser y AEVUMARD**.

Estos documentos pueden motivar hipótesis de ingeniería, pero están separados de los resultados computacionales. Una prueba funcional del runtime no valida automáticamente la ontología.

→ [Índice de fundamentos](docs/fundamentos/README.md#espanol) · [TCF v3.3](docs/fundamentos/TCF_V3_3.md#espanol) · [TIF v0.1](docs/fundamentos/TIF_V0_1.md#espanol) · [Manifiesto del Ser](MANIFIESTO_DEL_SER.md#espanol)

## Reproducibilidad

El laboratorio usa **GitHub Actions**. El CI activo se limita a workflows que verifican código o ejecutan protocolos reproducibles; los workflows one-shot de materialización fueron retirados y documentados en `docs/ARCHIVED_CI.md`. Los workflows conservan commits, manifiestos y artifacts para que los resultados puedan rastrearse hasta el código que los produjo.

La evidencia se interpreta como:

**Observación → Resultado → Hipótesis/modelo → Ontología**

y no se permite convertir automáticamente una propiedad computacional en una afirmación de experiencia subjetiva.

→ [Laboratorio GitHub](docs/GITHUB_LAB.md#espanol)

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

## Current frontier

- **I4.3** is verified across three unseen disturbance structures; prediction-error generalization is positive while the aggregate recovery endpoint is null.
- **I5.0** is verified on 512 paired episodes and the bounded-workspace prototype is now on `main`.
- **I5.1** is integrated into `PersistentOrganism` and produced a null result for the tested broadcast→trajectory behavioral endpoints; workspace-state persistence was verified.
- **I5.2** is verified as a standalone GWT-4 mechanism: FULL−SHUFFLED **+1.0**, p **4.99975×10⁻⁵**, with FULL−LESION **+0.76367**, p **4.99975×10⁻⁵**.
- **I5.3** is verified as a standalone causal attention-allocation mechanism: FULL−SHUFFLED target mass **+0.97682**, p **4.99975×10⁻⁵**.
- **I5.4** integrated I5.2 + I5.3 into `PersistentOrganism`: query controls were null; shuffled attention changed action in **20.83%** but regret cost was non-significant (p **0.5022**); exact persistence **100%**.
- **I5.5** verified the combined query + attention mechanism: FULL−SHUFFLED_QUERY **+1.0**, p **4.99975×10⁻⁵**; FULL−SHUFFLED_ATTENTION **+1.0**, p **4.99975×10⁻⁵**; NO_BOTTLENECK was null.
- **Lattice v0/v1** are verified computational-substrate protocols; physical claims remain explicitly separated from the implementation.
- **Next integration:** bring I5.2 into `PersistentOrganism`, then test causal attention allocation.
## Strongest results so far

| Protocol | What was tested | Observed result |
|---|---|---|
| **V51** | Internal-state self-prediction | MAE **0.0424** vs **0.2211** persistence baseline; mean gain **0.1787**; p **0.00005**. |
| **V57** | Self-model-guided trajectory selection | Regret **0.0231** vs **0.1369** random control; p **0.00435** under the paired protocol. |
| **V70** | Persistence and use of the self-reader | The numerical reader survived restart and was reused after semantic ablation; self-model → action → new-state remained operational under the tested harness. |
| **V76–V78** | OOD generalization of the self-prediction policy | The advantage persisted across unseen magnitudes, structures, and sequences; secondary continuity endpoints **did not** separate from random selection. |
| **I4.2** | Persistent metacognitive interoception | FULL separated from LESION on error and recovery and from PERMUTED on both endpoints under the declared disturbance; serialization/restore was exact. |
| **I4.3** | Structural OOD generalization of the second-order model | META−LESION mean error **−0.001549**, p **4.27×10⁻⁶**; META−PERMUTED **−0.001567**, p **9.38×10⁻⁶**; aggregate META−LESION recovery was null (p **0.1505**). |
| **C0.6** | Causal lesion/rescue of self-observer/self-policy | Lesions changed measured organization and restoration produced significant rescue effects under the tested protocol. |
| **Lattice v0** | Local computation, propagation, and distributed organization | XOR **1.0**; coupling changed coherence, redundancy, and perturbation spread; the decoupled control retained more raw pattern. |
| **Lattice v1** | Temporal trace retention after input removal | 128 replicates; mean retention at delay 8 **0.74870**; AUC **0.75976**; mean perturbation loss **0.00172** at delay 8. |
| **I5.0** | Bounded global workspace | 512 episodes; broadcast vs no-broadcast accuracy **+0.12695**, p **5×10⁻⁵**; K=2 vs K=6 **+0.01758**, p **0.02225**; selected-source lesion differential **−0.49023**, p **5×10⁻⁵**. |
| **I5.1** | PersistentOrganism workspace integration | Null behavioral result under the tested mapping: NO_BROADCAST−FULL regret **+0.02124**, p **0.4928**; LESION−FULL **0.0**, p **1.0**; workspace-state persistence **100%**. |
| **I5.2** | State-dependent query / GWT-4 | 512 episodes; FULL−SHUFFLED **+1.0**, p **5×10⁻⁵**; FULL−ZERO **+0.77148**, p **5×10⁻⁵**; FULL−RANDOM **+0.74219**, p **5×10⁻⁵**; FULL−LESION **+0.76367**, p **5×10⁻⁵**. |
| **I5.3** | Causal attention allocation | 512 episodes; FULL target attention mass **0.98456**; FULL−SHUFFLED **+0.97682**, p **5×10⁻⁵**; FULL−LESION **+0.73456**, p **5×10⁻⁵**. |
| **I5.4** | Persistent query + attention integration | 24 replicates; query controls null; SHUFFLED_ATTENTION action-change **20.83%**, regret cost **+0.02804**, p **0.5022**; persistence **100%**. |
| **I5.5** | Causal query + attention bottleneck | 512 episodes; FULL−SHUFFLED_QUERY **+1.0**, p **5×10⁻⁵**; FULL−SHUFFLED_ATTENTION **+1.0**, p **5×10⁻⁵**; NO_BOTTLENECK null. |

These results describe computational properties under concrete protocols. **They do not by themselves demonstrate subjective experience.**

→ [Consolidated results ledger](research/ORGANISM_RESULT_LEDGER.md#english) · [I5.0 Workspace](docs/I5_GLOBAL_WORKSPACE.md#english) · [I5.1 PersistentOrganism](docs/I5_1_PERSISTENT_ORGANISM_WORKSPACE.md#english) · [I5.2 State-Dependent Query](docs/I5_2_STATE_DEPENDENT_QUERY.md#english) · [Lattice v1](docs/LATTICE_COMPUTER_V1.md#english)
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

→ [Consciousness Server](docs/CONSCIOUSNESS_SERVER.md#english) · [Deterministic replay](docs/DETERMINISTIC_EVENT_REPLAY.md#english) · [Peer synchronization](src/consciousness_server/synchronization.py)

## Getting started

- Installation: [INSTALL.md](INSTALL.md#english)
- Method: [docs/METODO.md](docs/METODO.md#english)
- Laboratory: [docs/GITHUB_LAB.md](docs/GITHUB_LAB.md#english)
- Protocols: [docs/INDICE.md](docs/INDICE.md#english)
- Results: [research/ORGANISM_RESULT_LEDGER.md](research/ORGANISM_RESULT_LEDGER.md#english)
- Infrastructure: [docs/CONSCIOUSNESS_SERVER.md](docs/CONSCIOUSNESS_SERVER.md#english)
- Indicator program: [docs/CONSCIOUSNESS_INDICATOR_PROGRAM.md](docs/CONSCIOUSNESS_INDICATOR_PROGRAM.md#english)
- Interoception I0/I1/I2/I3/I4/I4.1/I4.2/I4.3: [docs/I0_INTEROCEPTIVE_INSTRUMENTATION.md](docs/I0_INTEROCEPTIVE_INSTRUMENTATION.md#english) · [docs/I1_INTEROCEPTIVE_SELF_ASSESSMENT.md](docs/I1_INTEROCEPTIVE_SELF_ASSESSMENT.md#english) · [docs/I2_INTEROCEPTIVE_REGULATION.md](docs/I2_INTEROCEPTIVE_REGULATION.md#english) · [docs/I3_REPEATED_INTEROCEPTIVE_RECOVERY.md](docs/I3_REPEATED_INTEROCEPTIVE_RECOVERY.md#english) · [docs/I4_METACOGNITIVE_INTEROCEPTION.md](docs/I4_METACOGNITIVE_INTEROCEPTION.md#english) · [docs/I4_1_METACOGNITIVE_RELIABILITY.md](docs/I4_1_METACOGNITIVE_RELIABILITY.md#english) · [docs/I4_2_PERSISTENT_METACOGNITIVE_LESION_RESCUE.md](docs/I4_2_PERSISTENT_METACOGNITIVE_LESION_RESCUE.md#english) · [docs/I4_3_STRUCTURAL_OOD_METACOGNITIVE_GENERALIZATION.md](docs/I4_3_STRUCTURAL_OOD_METACOGNITIVE_GENERALIZATION.md#english)
 - Lattice Computer: [v0](docs/LATTICE_COMPUTER_V0.md#english) · [v1](docs/LATTICE_COMPUTER_V1.md#english)
 - I5.0 bounded global workspace: [docs/I5_GLOBAL_WORKSPACE.md](docs/I5_GLOBAL_WORKSPACE.md#english)
## Known limitations

- There is not yet one global preregistration policy for the full historical protocol family.
- There is not yet a single prespecified repository-wide multiple-comparisons correction that turns the full protocol collection into one confirmatory inference.
- Several second-order mechanisms produced null or mixed results; C0.18 did not show significant causal necessity or functional rescue under its tested protocol.
- Some historical protocols were corrected before their results were considered; those corrections and limitations are documented in the ledger.
- The repository license is not yet defined.

## Theoretical framework — separate from evidence

The repository preserves a theoretical layer including **TCF v3.3, TIF, the Manifesto of Being, and AEVUMARD**.

These documents can motivate engineering hypotheses, but they are kept separate from computational results. A functional test of the runtime does not automatically validate the ontology.

→ [Foundations index](docs/fundamentos/README.md#english) · [TCF v3.3](docs/fundamentos/TCF_V3_3.md#english) · [TIF v0.1](docs/fundamentos/TIF_V0_1.md#english) · [Manifesto of Being](MANIFESTO_OF_BEING.md#english)

## Reproducibility

The laboratory uses **GitHub Actions**. Active CI is limited to workflows that verify code or run reproducible protocols; one-shot materialization workflows were retired and documented in `docs/ARCHIVED_CI.md`. Workflows preserve commits, manifests, and artifacts so results can be traced to the code that produced them.

Evidence is interpreted as:

**Observation → Result → Hypothesis/model → Ontology**

and computational properties are not automatically converted into claims of subjective experience.

→ [GitHub Laboratory](docs/GITHUB_LAB.md#english)

## Citation

See [CITATION.cff](CITATION.cff)

</details>
