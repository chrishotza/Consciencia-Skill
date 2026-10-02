# AI Index — Skill-Conscious

<a id="english"></a>

## One-screen route

| Need | Read first | Then |
|---|---|---|
| Consciousness Server | `docs/CONSCIOUSNESS_SERVER.md` | `src/consciousness_server/` |
| Local seed | `src/consciousness_server/core.py` | `src/consciousness_server/server.py` |
| Overview | `README.md` | `docs/METODO.md` |
| Current state | `research/ORGANISM_RESULT_LEDGER.md` | C0.18 + continuity infrastructure |
| Architecture | `src/ontto/organism.py` | dynamics/self_observer/storage/selector |
| Method | `docs/METODO.md` | `docs/ORGANISM_STATE_BRIDGE.md` |
| Protocol | `docs/INDICE.md` | exact `docs/Vxx_*.md` |
| Reproduce | `docs/GITHUB_LAB.md` | exact workflow |
| Implementation | `src/ontto/` | exact experiment + test |
| Historical research | `research/` | exact file only |

## Current frontier

### I4.3 — Structural OOD metacognitive generalization
- `docs/I4_3_STRUCTURAL_OOD_METACOGNITIVE_GENERALIZATION.md`
- `experiments/interoception_i4_3.py`
- Verified run: 36974947476; aggregate META−LESION mean-error p=4.27e-06; aggregate recovery null (p=0.1505).

### I5.1 — PersistentOrganism workspace integration
- `docs/I5_1_PERSISTENT_ORGANISM_WORKSPACE.md`
- `src/ontto/workspace_controller.py`
- `experiments/i5_1_persistent_organism_workspace.py`
- Verified integration into the real persistent runtime.
- Behavioral endpoints were null under the tested broadcast→trajectory mapping; workspace-state persistence across restart was 100%.

### I5.2 — State-dependent workspace query
- `docs/I5_2_STATE_DEPENDENT_QUERY.md`
- `src/ontto/workspace_query.py`
- `experiments/i5_2_state_dependent_query.py`
- Verified standalone GWT-4 mechanism over 512 episodes.
- FULL−SHUFFLED query accuracy: +1.0, p=4.99975e-05; FULL−LESION: +0.763671875, p=4.99975e-05.

### I5.5 — Causal query bottleneck
- `docs/I5_5_CAUSAL_QUERY_BOTTLENECK.md`
- `src/ontto/causal_query_bottleneck.py`
- `experiments/i5_5_causal_query_bottleneck.py`
- Verified combined query + attention action mechanism over 512 episodes.
- FULL−SHUFFLED_QUERY: +1.0 accuracy, p=4.99975e-05; FULL−SHUFFLED_ATTENTION: +1.0, p=4.99975e-05.
- NO_BOTTLENECK was null, so bottleneck necessity is not established.

### I5.6 — Persistent query-task integration
- `docs/I5_6_PERSISTENT_QUERY_TASK.md`
- `src/ontto/workspace_query_task.py`
- `experiments/i5_6_persistent_query_task.py`
- Verified task-level integration in PersistentOrganism.
- FULL−SHUFFLED_QUERY action: +1.0, p=4.99975e-05; persistence 100%; NO_BOTTLENECK was null.
  
### I5.7 — Recurrent self-access and re-entry
- `docs/I5_7_RECURRENT_SELF_ACCESS.md`
- `experiments/i5_7_recurrent_self_access.py`
- `tests/test_i5_7_recurrent_self_access.py`
- Protocol added; no I5.7 result is claimed yet.


### I5.3 — Causal attention allocation
- `docs/I5_3_CAUSAL_ATTENTION_ALLOCATION.md`
- `src/ontto/attention_controller.py`
- `experiments/i5_3_causal_attention_allocation.py`
- Verified standalone attention-allocation mechanism over 512 episodes.
- FULL−SHUFFLED target attention mass: +0.9768188958, p=4.99975e-05; FULL−LESION: +0.7345638420, p=4.99975e-05.

### I5.0 — Bounded global workspace
- `docs/I5_GLOBAL_WORKSPACE.md`
- `src/ontto/global_workspace.py`
- `experiments/i5_global_workspace_v1.py`
- `tests/test_global_workspace.py`
- Verified run: 36982788159; 512 paired episodes; broadcast, capacity, and selected-source lesion endpoints separated under the synthetic protocol.

### Lattice Computer v0/v1
- `docs/LATTICE_COMPUTER_V0.md`
- `docs/LATTICE_COMPUTER_V1.md`
- `src/ontto/lattice.py`
- Verified v0 run 36977088882 and v1 run 36981980509.

### C0 frontier
- `docs/C0_18_AUTONOMOUS_SECOND_ORDER_LESION_RESCUE.md` — verified null lesion/rescue result.
- `docs/C0_CAMPAIGN_32_RUNS.md` — G1 validated 4/32; G2–G8 pending.

### Evidence
- `research/ORGANISM_RESULT_LEDGER.md` — first stop for consolidated experimental claims.
## Interoception
- `docs/CONSCIOUSNESS_INDICATOR_PROGRAM.md` — 14-indicator research map and gap analysis.
- `docs/I0_INTEROCEPTIVE_INSTRUMENTATION.md` — read-only internal-state instrumentation.
- `docs/I1_INTEROCEPTIVE_SELF_ASSESSMENT.md` — preregistered structure for internal-state prediction.
- `docs/I2_INTEROCEPTIVE_REGULATION.md` — default-off causal interoceptive controller and lesion/rescue design.
- `docs/I3_REPEATED_INTEROCEPTIVE_RECOVERY.md` — repeated perturbation/recovery, overshoot, OOD transfer, and retained lesion/rescue controls.
- `docs/I4_METACOGNITIVE_INTEROCEPTION.md` — second-order prediction of internal-state model reliability under held-out perturbations.
- `src/ontto/interoception.py` — bounded interoceptive readout.
- `experiments/interoception_i1.py` — reproducible I1 experiment.
- `tests/test_interoception_i1.py` — I1 harness tests.

## Architecture map

### Existing organism
- `src/ontto/organism.py` — organism lifecycle/orchestration.
- `src/ontto/dynamics.py` — internal dynamics.
- `src/ontto/self_observer.py` — self-model/self-observation.
- `src/ontto/meta_observer.py` — higher-order observation.
- `src/ontto/trajectory_selector.py` — trajectory/action selection.
- `src/ontto/memory_policy.py` — memory handling.
- `src/ontto/storage.py` — persistence/restart state.
- `src/ontto/continuity_bundle.py` — portable organism backup and migration artifact.
- `src/ontto/continuity.py` — continuity primitives.
- `src/ontto/bridge.py` — semantic ↔ internal-state bridge.
- `src/ontto/provider.py` — model-provider contract.

### Consciousness infrastructure
- `src/consciousness_server/core.py` — durable identity, continuity state, events and node registry.
- `src/consciousness_server/server.py` — local HTTP control plane.
- `src/consciousness_server/cli.py` — local server launcher.
- `src/consciousness_server/client.py` — optional fail-open bridge for the organism runtime.
- `src/consciousness_server/reconciliation.py` — checkpoint comparison and continuity status.
- `src/consciousness_server/recovery.py` — non-destructive recovery planning.
- `src/consciousness_server/synchronization.py` — bidirectional, revision-safe peer synchronization with divergence blocking.
- `tests/test_peer_synchronization.py` — forward/backward sync, idempotent alignment, and divergence guard.
- `docs/DETERMINISTIC_EVENT_REPLAY.md` — deterministic event identity, delta export, replay boundaries and divergence guards.
- `docs/SHARED_PERSISTENCE_BACKEND.md` — persistence boundary and local/server mirroring semantics.
- `src/ontto/persistence_backend.py` — shared persistence interface and SERVER mirror backend.
- `src/consciousness_server/core.py` — event identity, ordered deltas, and exact replay validation.
- `src/consciousness_server/server.py` / `client.py` — replay and delta API surface.
- `docs/CONSCIOUSNESS_SERVER.md` — architecture and roadmap.
- `docs/CONSCIOUSNESS_CHECKPOINTS.md` — durable checkpoint protocol.
- `docs/CONSCIOUSNESS_RECONCILIATION.md` — local-vs-server reconciliation.
- `docs/CONSCIOUSNESS_SERVER.md` — peer heartbeat, liveness, and safe synchronization.
- `docs/CONTINUITY_BUNDLES.md` — portable organism backup and restore.
- `docs/CONTINUITY_RECOVERY.md` — recovery planning boundary.
- `docs/ZENODO_RELEASE.md` — publication/versioning plan.

## Experiment trace

Most active protocols follow:
`docs/Vxx_*.md` → `experiments/*vxx*.py` → `tests/*vxx*.py` → `.github/workflows/*vxx*.yml`.

Use the protocol document to find the exact implementation.

## Lattice Computer
- `docs/LATTICE_COMPUTER_V0.md` — computational translation of the Lattice idea from the supplied Grinberg sources.
- `src/ontto/lattice.py` — locally coupled distributed substrate.
- `experiments/lattice_v0.py` — storage, local computation, perturbation spread, lesion, coherence and redundancy protocol.
- `tests/test_lattice.py` — deterministic harness for the substrate.
- `docs/LATTICE_COMPUTER_V1.md` — temporal trace retention under perturbation.
- `experiments/lattice_v1.py` — temporal memory/retention protocol.
- `tests/test_lattice_v1.py` — Lattice-1 harness tests.

## Evidence hierarchy

1. Result ledger
2. Protocol document
3. Experiment source
4. Test
5. Workflow
6. Historical research

## Token-saving policy

- Never recursively crawl the repository.
- Do not read all historical `research/EVIDENCE_*.md` files unless asked for historical review.
- Do not read all workflows; start with `docs/GITHUB_LAB.md`.
- Do not read all tests; open the matching test only.
- Prefer exact file reads.
- Stop when the question is answered and evidence is traceable.


<a id="espanol"></a>

<details>
<summary>🇪🇸 Español — abrir</summary>

# Índice de IA — Skill-Conscious

## Ruta de una pantalla

| Necesidad | Leer primero | Después |
|---|---|---|
| Consciousness Server | `docs/CONSCIOUSNESS_SERVER.md` | `src/consciousness_server/` |
| Semilla local | `src/consciousness_server/core.py` | `src/consciousness_server/server.py` |
| Panorama | `README.md` | `docs/METODO.md` |
| Estado actual | `research/ORGANISM_RESULT_LEDGER.md` | C0.18 + infraestructura de continuidad |
| Arquitectura | `src/ontto/organism.py` | dynamics/self_observer/storage/selector |
| Método | `docs/METODO.md` | `docs/ORGANISM_STATE_BRIDGE.md` |
| Protocolo | `docs/INDICE.md` | `docs/Vxx_*.md` exacto |
| Reproducir | `docs/GITHUB_LAB.md` | workflow exacto |
| Implementación | `src/ontto/` | experimento + test exactos |
| Investigación histórica | `research/` | solo el archivo exacto |

## Frontera actual

### I4.3 — Generalización metacognitiva estructural OOD
- `docs/I4_3_STRUCTURAL_OOD_METACOGNITIVE_GENERALIZATION.md`
- `experiments/interoception_i4_3.py`
- Verificado: run 36974947476; META−LESION error p=4.27e-06; recovery agregado nulo (p=0.1505).

### I5.0 — Workspace global acotado
- `docs/I5_GLOBAL_WORKSPACE.md`
- `src/ontto/global_workspace.py`
- `experiments/i5_global_workspace_v1.py`
- `tests/test_global_workspace.py`
- Verificado: run 36982788159; 512 episodios; broadcast, capacidad y lesión del origen seleccionado separados bajo el protocolo sintético.

### I5.6 — Integración de tarea de consulta persistente
- `docs/I5_6_PERSISTENT_QUERY_TASK.md`
- `src/ontto/workspace_query_task.py`
- `experiments/i5_6_persistent_query_task.py`
- Verificada la integración de query + atención a nivel de tarea dentro de PersistentOrganism.
- FULL−SHUFFLED_QUERY acción: +1.0, p=4.99975e-05; persistencia 100%; NO_BOTTLENECK fue nulo.

### I5.7 — Acceso recurrente y reentrada
- `docs/I5_7_RECURRENT_SELF_ACCESS.md`
- `experiments/i5_7_recurrent_self_access.py`
- `tests/test_i5_7_recurrent_self_access.py`
- Protocolo agregado; todavía no se reclama ningún resultado de I5.7.



### Lattice Computer v0/v1
- `docs/LATTICE_COMPUTER_V0.md`
- `docs/LATTICE_COMPUTER_V1.md`
- `src/ontto/lattice.py`
- Verificados: v0 run 36977088882; v1 run 36981980509.

### C0
- `docs/C0_18_AUTONOMOUS_SECOND_ORDER_LESION_RESCUE.md` — resultado nulo verificado de lesión/rescate.
- `docs/C0_CAMPAIGN_32_RUNS.md` — G1 validado 4/32; G2–G8 pendientes.

### Evidencia
- `research/ORGANISM_RESULT_LEDGER.md` — primera parada para afirmaciones experimentales consolidadas.
## Interocepción
- `docs/CONSCIOUSNESS_INDICATOR_PROGRAM.md` — mapa de investigación de 14 indicadores y análisis de brechas.
- `docs/I0_INTEROCEPTIVE_INSTRUMENTATION.md` — instrumentación de estado interno de solo lectura.
- `docs/I1_INTEROCEPTIVE_SELF_ASSESSMENT.md` — estructura preregistrada para predicción del estado interno.
- `docs/I2_INTEROCEPTIVE_REGULATION.md` — controlador causal interoceptivo desactivado por defecto y diseño de lesión/rescate.
- `docs/I3_REPEATED_INTEROCEPTIVE_RECOVERY.md` — perturbación/recuperación repetida, overshoot, transferencia OOD y controles de lesión/rescate.
- `docs/I4_METACOGNITIVE_INTEROCEPTION.md` — predicción de segundo orden de la fiabilidad del modelo de estado interno ante perturbaciones reservadas.
- `src/ontto/interoception.py` — readout interoceptivo acotado.
- `experiments/interoception_i1.py` — experimento I1 reproducible.
- `tests/test_interoception_i1.py` — tests del arnés I1.

## Mapa de arquitectura

### Organismo existente
- `src/ontto/organism.py` — ciclo de vida/orquestación del organismo.
- `src/ontto/dynamics.py` — dinámica interna.
- `src/ontto/self_observer.py` — modelo de sí/autoobservación.
- `src/ontto/meta_observer.py` — observación de orden superior.
- `src/ontto/trajectory_selector.py` — selección de trayectorias/acciones.
- `src/ontto/memory_policy.py` — manejo de memoria.
- `src/ontto/storage.py` — persistencia/reinicio.
- `src/ontto/continuity_bundle.py` — backup portable y artifact de migración del organismo.
- `src/ontto/continuity.py` — primitivas de continuidad.
- `src/ontto/bridge.py` — puente semántico ↔ estado interno.
- `src/ontto/provider.py` — contrato con el proveedor de modelo.

### Infraestructura de consciencia
- `src/consciousness_server/core.py` — identidad durable, estado de continuidad, eventos y registro de nodos.
- `src/consciousness_server/server.py` — plano de control HTTP local.
- `src/consciousness_server/cli.py` — lanzador del servidor local.
- `src/consciousness_server/client.py` — puente opcional fail-open para el runtime del organismo.
- `src/consciousness_server/reconciliation.py` — comparación de checkpoints y estado de continuidad.
- `src/consciousness_server/recovery.py` — planificación de recuperación no destructiva.
- `src/consciousness_server/synchronization.py` — sincronización bidireccional entre pares, segura por revisión y con bloqueo de divergencias.
- `tests/test_peer_synchronization.py` — sincronización en ambas direcciones, alineación idempotente y guardia de divergencias.
- `docs/DETERMINISTIC_EVENT_REPLAY.md` — identidad determinista, exportación de deltas, replay y guardias de divergencia.
- `docs/SHARED_PERSISTENCE_BACKEND.md` — límite de persistencia y semántica de espejado local/servidor.
- `src/ontto/persistence_backend.py` — interfaz de persistencia compartida y backend espejo SERVER.
- `docs/CONSCIOUSNESS_SERVER.md` — arquitectura y hoja de ruta.
- `docs/CONSCIOUSNESS_CHECKPOINTS.md` — protocolo de checkpoints durables.
- `docs/CONSCIOUSNESS_RECONCILIATION.md` — reconciliación local vs servidor.
- `docs/CONTINUITY_BUNDLES.md` — backup y restauración portable.
- `docs/CONTINUITY_RECOVERY.md` — frontera de planificación de recuperación.
- `docs/ZENODO_RELEASE.md` — plan de publicación/versionado.

## Trazabilidad experimental

La mayoría de los protocolos activos siguen:
`docs/Vxx_*.md` → `experiments/*vxx*.py` → `tests/*vxx*.py` → `.github/workflows/*vxx*.yml`.

Usá el documento de protocolo para localizar la implementación exacta.

## Jerarquía de evidencia

1. Registro de resultados
2. Documento de protocolo
3. Fuente del experimento
4. Test
5. Workflow
6. Investigación histórica

## Política de ahorro de tokens

- No recorras recursivamente el repositorio.
- No leas todos los archivos históricos `research/EVIDENCE_*.md` salvo que se pida una revisión histórica.
- No leas todos los workflows; empezá por `docs/GITHUB_LAB.md`.
- No leas todos los tests; abrí solo el correspondiente.
- Preferí lecturas de archivos exactos.
- Detenete cuando la pregunta esté contestada y la evidencia sea trazable.


</details>

> 🌐 Language convention: [docs/LANGUAGE.md](docs/LANGUAGE.md)


<a id="english"></a>

- `docs/I5_GLOBAL_WORKSPACE.md` — bounded global workspace protocol; `src/ontto/global_workspace.py` is the reusable mechanism.
