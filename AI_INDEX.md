# AI Index — Skill-Conscious

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

### C0.8
- `docs/C0_8_CROSSED_OBSERVER_POLICY.md`
- `experiments/tcf_consciousness_instantiation_c0_8.py`

### C0.9
- `docs/C0_9_OBSERVER_POLICY_INTERFACE_SHUFFLE.md`
- `experiments/tcf_consciousness_instantiation_c0_9.py`

### C0.10
- `docs/C0_10_WITHIN_EPISODE_TEMPORAL_ALIGNMENT.md`
- `experiments/tcf_consciousness_instantiation_c0_10.py`

### C0.11
- `docs/C0_11_CAUSAL_ACTION_MEDIATION.md`
- `experiments/tcf_consciousness_instantiation_c0_11.py`

### C0.12
- `docs/C0_12_SECOND_ORDER_SELF_MONITORING.md`
- `experiments/tcf_consciousness_instantiation_c0_12.py`

### C0.13
- `docs/C0_13_ACTION_CONDITIONED_META_MODEL.md`
- `experiments/tcf_consciousness_instantiation_c0_13.py`

### C0.14
- `docs/C0_14_PERSISTENT_SECOND_ORDER_SELF_MODEL.md`
- `experiments/tcf_consciousness_instantiation_c0_14.py`

### C0.15
- `docs/C0_15_SECOND_ORDER_LESION_RESCUE.md`
- `experiments/tcf_consciousness_instantiation_c0_15.py`

### C0.16
- `docs/C0_16_INTEGRATED_SECOND_ORDER_ORGANISM.md`
- `experiments/tcf_consciousness_instantiation_c0_16.py`

### C0.17
- `docs/C0_17_AUTONOMOUS_SECOND_ORDER_ACQUISITION.md`
- `experiments/tcf_consciousness_instantiation_c0_17.py`

- `tests/test_second_node_interoperability.py` — two-node HTTP replay and divergence guard.
### C0 Campaign
- `docs/C0_CAMPAIGN_32_RUNS.md`
- `research/c0_campaign/C0_CAMPAIGN_RESTARTED_G1_EVIDENCE.json`
- Verified: **G1 completed, 4/32 executions; G2–G8 pending; G1 p-values all > 0.05**.

### C0.18
- `docs/C0_18_AUTONOMOUS_SECOND_ORDER_LESION_RESCUE.md`
- `experiments/tcf_consciousness_instantiation_c0_18.py`
- `tests/test_tcf_consciousness_instantiation_c0_18.py`
- Verified: 24 replicates; null lesion/rescue effect under the tested protocol; artifact preserved in GitHub Actions.

### V69
- `docs/V69_SELF_STATE_READOUT.md`
- `docs/V69_SELF_READ_STATE.md`

### V70
- `docs/V70_SELF_MODEL_ACTION.md`
- `docs/V70_PERSISTENT_SELF_READER.md`

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

### C0.8
- `docs/C0_8_CROSSED_OBSERVER_POLICY.md`
- `experiments/tcf_consciousness_instantiation_c0_8.py`

### C0.9
- `docs/C0_9_OBSERVER_POLICY_INTERFACE_SHUFFLE.md`
- `experiments/tcf_consciousness_instantiation_c0_9.py`

### C0.10
- `docs/C0_10_WITHIN_EPISODE_TEMPORAL_ALIGNMENT.md`
- `experiments/tcf_consciousness_instantiation_c0_10.py`

### C0.11
- `docs/C0_11_CAUSAL_ACTION_MEDIATION.md`
- `experiments/tcf_consciousness_instantiation_c0_11.py`

### C0.12
- `docs/C0_12_SECOND_ORDER_SELF_MONITORING.md`
- `experiments/tcf_consciousness_instantiation_c0_12.py`

### C0.13
- `docs/C0_13_ACTION_CONDITIONED_META_MODEL.md`
- `experiments/tcf_consciousness_instantiation_c0_13.py`

### C0.14
- `docs/C0_14_PERSISTENT_SECOND_ORDER_SELF_MODEL.md`
- `experiments/tcf_consciousness_instantiation_c0_14.py`

### C0.15
- `docs/C0_15_SECOND_ORDER_LESION_RESCUE.md`
- `experiments/tcf_consciousness_instantiation_c0_15.py`

### C0.16
- `docs/C0_16_INTEGRATED_SECOND_ORDER_ORGANISM.md`
- `experiments/tcf_consciousness_instantiation_c0_16.py`

### C0.17
- `docs/C0_17_AUTONOMOUS_SECOND_ORDER_ACQUISITION.md`
- `experiments/tcf_consciousness_instantiation_c0_17.py`

- `tests/test_second_node_interoperability.py` — replay HTTP entre dos nodos y bloqueo de divergencias.

### Campaña C0
- `docs/C0_CAMPAIGN_32_RUNS.md`
- `research/c0_campaign/C0_CAMPAIGN_RESTARTED_G1_EVIDENCE.json`
- Verificado: **G1 completado, 4/32 ejecuciones; G2–G8 pendientes; todos los p-values de G1 > 0.05**.

### C0.18
- `docs/C0_18_AUTONOMOUS_SECOND_ORDER_LESION_RESCUE.md`
- `experiments/tcf_consciousness_instantiation_c0_18.py`
- `tests/test_tcf_consciousness_instantiation_c0_18.py`
- Verificado: 24 réplicas; efecto de lesión/rescate nulo bajo el protocolo probado; artifact conservado en GitHub Actions.

### V69
- `docs/V69_SELF_STATE_READOUT.md`
- `docs/V69_SELF_READ_STATE.md`

### V70
- `docs/V70_SELF_MODEL_ACTION.md`
- `docs/V70_PERSISTENT_SELF_READER.md`

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
