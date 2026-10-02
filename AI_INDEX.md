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
- Verified null/inconclusive primary endpoint: signed state delta at t+1 did not separate significantly; no causal re-entry effect is claimed.

### I5.8 — Action-clamp mediation of recurrent self-access
- `docs/I5_8_ACTION_CLAMP_REENTRY.md`
- `experiments/i5_8_action_clamp_reentry.py`
- `tests/test_i5_8_action_clamp_reentry.py`
- Verified: action-clamp removed the pulse state divergence; pulse vs clamp t+1 and AUC contrasts both p=4.99975e-05.

### I5.9 — Action-replay sufficiency
- `docs/I5_9_ACTION_REPLAY_SUFFICIENCY.md`
- `experiments/i5_9_action_replay_sufficiency.py`
- `tests/test_i5_9_action_replay_sufficiency.py`
- Verified: exact action replay produced zero PULSE-vs-REPLAY state divergence; t+1 and AUC both p=1.0.

### I5.10 — Semantic re-entry under action replay
- `docs/I5_10_SEMANTIC_REENTRY_ACTION_REPLAY.md`
- `experiments/i5_10_semantic_reentry_under_action_replay.py`
- `tests/test_i5_10_semantic_reentry_action_replay.py`
- Verified: 100% action match; 45.83% post-pulse self-model divergence; PULSE-vs-REPLAY t+1 and AUC p=4.99975e-05; bridge ON-vs-OFF AUC p=4.99975e-05.

### I5.11 — Semantic re-entry into future trajectory selection
- `docs/I5_11_SEMANTIC_REENTRY_TRAJECTORY_SELECTION.md`
- `experiments/i5_11_semantic_reentry_trajectory_selection.py`
- `tests/test_i5_11_semantic_reentry_trajectory_selection.py`
- Verified: 100% t0 action match; 55.95% future action-change rate, p=4.99975e-05; state AUC p=4.99975e-05; bridge ON-vs-OFF AUC p=4.99975e-05.

### I5.12 — Information-matched semantic self-model control
- `docs/I5_12_INFORMATION_MATCHED_SELF_MODEL_CONTROL.md`
- `experiments/i5_12_information_matched_self_model_control.py`
- `tests/test_i5_12_information_matched_self_model_control.py`
- Verified: 100% t0 action match and 100% self-model distribution match; future action change 41.07%, p=4.99975e-05; state AUC p=4.99975e-05; bridge ON-vs-OFF AUC p=4.99975e-05.

### I5.13 — Semantic correspondence causal specificity
- `docs/I5_13_SEMANTIC_CORRESPONDENCE_CAUSAL_SPECIFICITY.md`
- `experiments/i5_13_semantic_correspondence_causal_specificity.py`
- `tests/test_i5_13_semantic_correspondence_causal_specificity.py`
- Verified: run 37042091184 / artifact 11242354548; 100% t0 applied-action match and 100% self-model distribution match; future action change 46.43%, p=4.99975e-05; state AUC 2.1867184440, p=4.99975e-05; bridge ON-vs-OFF AUC 2.6656102772, p=4.99975e-05.

### I5.14 — Phase-matched temporal specificity control
- `docs/I5_14_PHASE_MATCHED_TEMPORAL_SPECIFICITY.md`
- `experiments/i5_14_phase_matched_temporal_specificity_control.py`
- `tests/test_i5_14_phase_matched_temporal_specificity.py`
- Verified: run 37042551701 / artifact 11243190387; 100% t0 action match and 100% SELF_MODEL distribution match; SHIFT+1 future action change 11.90%, SHIFT-1 44.64%, both p=4.99975e-05; BASE-vs-SHIFT+1 AUC 0.2414241371, BASE-vs-SHIFT-1 AUC 1.9526574097; SHIFT+1 bridge ON-vs-OFF AUC 2.1221765870, all p=4.99975e-05.

### I5.15 — Bidirectional temporal-lag response map
- `docs/I5_15_BIDIRECTIONAL_TEMPORAL_LAG_RESPONSE_MAP.md`
- `experiments/i5_15_bidirectional_temporal_lag_response_map.py`
- `tests/test_i5_15_bidirectional_temporal_lag_response_map.py`
- Verified: run 37044533566 / artifact 11243557588; 100% t0 action match and 100% SELF_MODEL distribution match across all lags; future-action change ranged from 11.31% (+1) to 58.93% (-2); absolute state AUC ranged from 0.262091 (+1) to 2.363792 (-2); +1 vs -1 absolute AUC symmetry difference -1.978122, p=4.99975e-05. Signed contrasts were significant only for -2 (p=0.04740) and +2 (p=0.04430); signed +k vs -k symmetry remained non-significant. The result motivates a pure-phase, longer-period counterbalanced control before stronger causal-specificity claims.


### I5.17 — Phase-resolved bridge mediation map
### I5.18 — Global phase × bridge interaction and multiplicity control
- `docs/I5_18_GLOBAL_PHASE_BRIDGE_INTERACTION.md`
- `experiments/i5_18_global_phase_bridge_interaction.py`
- `tests/test_i5_18_global_phase_bridge_interaction.py`
- Verified: research-lab **37052907187** / artifact **11246744569**; 24 replicates, 15 cycles, 20,000 permutations; tests/package/research workflows all successful.
- Global bridge effect across six lags: signed AUC **-1.38013**, p **0.00005**; absolute AUC **-0.52589**, p **0.00290**; future-action change **-0.08681**, p **0.00090**.
- Global phase × bridge interaction was non-significant for signed AUC (**p=0.49323**), absolute AUC (**p=0.46618**), and future-action change (**p=0.26739**).
- Boundary: this is a statistical follow-up on frozen I5.17 data; no new trajectories and no consciousness claim.

- `docs/I5_17_PHASE_RESOLVED_BRIDGE_MEDIATION_MAP.md`
- `experiments/i5_17_phase_resolved_bridge_mediation_map.py`
- `tests/test_i5_17_phase_resolved_bridge_mediation_map.py`
- Verified: run **37047719727** / artifact **11244733803** / commit **578802962b4f37066db95d46567245dcbb9ac83b**; **24** replicates, **24** warmup cycles, **15** cycles, **180 tests passed**; 100% t0 action match and 100% SELF_MODEL distribution match.
- Signed bridge ON−OFF AUC was negative at all six lags; absolute-AUC bridge effects were significant at -3 and +1, while +k/-k absolute bridge symmetry was non-significant for k=1,2,3.
- Boundary: per-lag 20,000-permutation sign-flip tests; no global multiplicity-corrected claim or consciousness claim.

### I5.16 — Counterbalanced pure-phase temporal control
- `docs/I5_16_COUNTERBALANCED_PURE_PHASE_TEMPORAL_CONTROL.md`
- `experiments/i5_16_counterbalanced_pure_phase_temporal_control.py`
- `tests/test_i5_16_counterbalanced_pure_phase_temporal_control.py`
- Verified: run 37046361416 / artifact 11245200134; 100% t0 action match and 100% SELF_MODEL distribution match; +1 vs -1 absolute-AUC symmetry difference -1.138780, p=0.000300; +2 vs -2 and +3 vs -3 absolute symmetry were non-significant; all signed BASE-vs-lag contrasts were non-significant. The -1/+1 magnitude asymmetry therefore survives the pure-phase and semantic-counterbalancing control, motivating phase-resolved bridge mapping.
### I5.17 — Phase-resolved bridge mediation map
### I5.18 — Global phase × bridge interaction and multiplicity control
- `docs/I5_18_GLOBAL_PHASE_BRIDGE_INTERACTION.md`
- `experiments/i5_18_global_phase_bridge_interaction.py`
- `tests/test_i5_18_global_phase_bridge_interaction.py`
- Verified: research-lab **37052907187** / artifact **11246744569**; 24 replicates, 15 cycles, 20,000 permutations; tests/package/research workflows all successful.
- Global bridge effect across six lags: signed AUC **-1.38013**, p **0.00005**; absolute AUC **-0.52589**, p **0.00290**; future-action change **-0.08681**, p **0.00090**.
- Global phase × bridge interaction was non-significant for signed AUC (**p=0.49323**), absolute AUC (**p=0.46618**), and future-action change (**p=0.26739**).
- Boundary: this is a statistical follow-up on frozen I5.17 data; no new trajectories and no consciousness claim.

- `docs/I5_17_PHASE_RESOLVED_BRIDGE_MEDIATION_MAP.md`
- `experiments/i5_17_phase_resolved_bridge_mediation_map.py`
- `tests/test_i5_17_phase_resolved_bridge_mediation_map.py`
- Protocol pending verification: same 15-cycle, seven-phase pure-phase construction as I5.16, with bridge ON and OFF for every lag ±1, ±2, ±3; phase-resolved bridge-effect and +k/-k symmetry endpoints.

### I5.19 — Independent bridge replication
- `docs/I5_19_INDEPENDENT_BRIDGE_REPLICATION.md`
- `experiments/i5_19_independent_bridge_replication.py`
- `tests/test_i5_19_independent_bridge_replication.py`
- Verified: research-lab **37056574657** / artifact **11247979913**; 24 replicates, 24 warmup cycles, 15 cycles, 20,000 permutations; tests/package/research workflows all successful.
- Independent seed **20261019** reproduced a non-zero average bridge ON−OFF effect for signed AUC (**-1.39819**, p=0.00030), absolute AUC (**-0.73065**, p=0.00190), and future-action change (**-0.11806**, p=0.00110).
- Global phase × bridge interaction remained non-significant for all three endpoints.
- Boundary: independent computational replication under the frozen protocol; no consciousness claim.

### I5.20 — Semantic permutation specificity control
- `docs/I5_20_SEMANTIC_PERMUTATION_SPECIFICITY.md`
- `experiments/i5_20_semantic_permutation_specificity.py`
- `tests/test_i5_20_semantic_permutation_specificity.py`
- Verified: research-lab **37058932661** / artifact **11249457646**; tests **37058932554** and package check **37058932500** successful.
- 24 replicates; t0 action and post-t0 semantic multiset both preserved at **100%**.
- Semantic specificity gap: signed AUC **-0.10367**, p=0.24169; absolute AUC **+0.71459**, p=0.00005; future-action change **+0.07292**, p=0.00005.
- Global lag×specificity interaction was non-significant for all three endpoints.
- max-T global any-lag p: **0.65022** signed AUC, **0.01060** absolute AUC, **0.01110** future action.
- Boundary: computational semantic-correspondence specificity; no consciousness claim.
- Next: I5.21 phase-local semantic permutation.

### I5.21 — Phase-local semantic permutation
- `docs/I5_21_PHASE_LOCAL_SEMANTIC_PERMUTATION.md`
- `experiments/i5_21_phase_local_semantic_permutation.py`
- `tests/test_i5_21_phase_local_semantic_permutation.py`
- Verified: research-lab **37059465725** / artifact **11249378346**; tests **37059465807** and package check **37059465643** successful.
- 24 replicates; 100% t0 match; 100% global and within-period semantic multiset preservation.
- Signed-AUC specificity gap **+0.02155**, p=0.85726; absolute-AUC gap **+0.44740**, p=0.00010; future-action gap **+0.04663**, p=0.00100.
- Global lag×specificity interaction: signed p=0.29069, absolute p=0.00030, action p<0.00005.
- max-T any-lag p: signed **0.35483**, absolute **0.00065**, action **0.00100**.
- Boundary: computational semantic-correspondence specificity; no consciousness claim.
- Next: I5.22 cyclic semantic phase-shift control.

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
- Resultado nulo/inconcluso verificado en el endpoint primario: el Δ estado firmado en t+1 no se separó significativamente; no se reclama un efecto causal de reentrada.

### I5.8 — Mediación por action-clamp del acceso recurrente
- `docs/I5_8_ACTION_CLAMP_REENTRY.md`
- `experiments/i5_8_action_clamp_reentry.py`
- `tests/test_i5_8_action_clamp_reentry.py`
- Verificado: el action-clamp eliminó la divergencia de estado del pulso; los contrastes pulse vs clamp en t+1 y AUC dieron p=4.99975e-05.

### I5.9 — Suficiencia por action-replay
- `docs/I5_9_ACTION_REPLAY_SUFFICIENCY.md`
- `experiments/i5_9_action_replay_sufficiency.py`
- `tests/test_i5_9_action_replay_sufficiency.py`
- Verificado: el action replay exacto produjo divergencia de estado PULSE-vs-REPLAY igual a cero; t+1 y AUC dieron p=1.0.

### I5.10 — Reentrada semántica bajo action replay
- `docs/I5_10_SEMANTIC_REENTRY_ACTION_REPLAY.md`
- `experiments/i5_10_semantic_reentry_under_action_replay.py`
- `tests/test_i5_10_semantic_reentry_action_replay.py`
- Verificado: 100% de coincidencia de acciones; 45.83% de divergencia post-pulso de modelo de sí; t+1 y AUC PULSE-vs-REPLAY con p=4.99975e-05; AUC bridge ON-vs-OFF con p=4.99975e-05.

### I5.11 — Reentrada semántica en selección de trayectorias futuras
- `docs/I5_11_SEMANTIC_REENTRY_TRAJECTORY_SELECTION.md`
- `experiments/i5_11_semantic_reentry_trajectory_selection.py`
- `tests/test_i5_11_semantic_reentry_trajectory_selection.py`
- Verificado: 100% de coincidencia de acción en t0; 55.95% de cambio de acción futura, p=4.99975e-05; AUC de estado p=4.99975e-05; AUC bridge ON-vs-OFF p=4.99975e-05.

### I5.12 — Control de modelo de sí con información emparejada
- `docs/I5_12_INFORMATION_MATCHED_SELF_MODEL_CONTROL.md`
- `experiments/i5_12_information_matched_self_model_control.py`
- `tests/test_i5_12_information_matched_self_model_control.py`
- Verificado: 100% de coincidencia de acción t0 y 100% de coincidencia de distribución de modelo de sí; cambio de acción futura 41.07%, p=4.99975e-05; AUC de estado p=4.99975e-05; AUC bridge ON-vs-OFF p=4.99975e-05.

### I5.13 — Especificidad causal de la correspondencia semántica
- `docs/I5_13_SEMANTIC_CORRESPONDENCE_CAUSAL_SPECIFICITY.md`
- `experiments/i5_13_semantic_correspondence_causal_specificity.py`
- `tests/test_i5_13_semantic_correspondence_causal_specificity.py`
- Verificado: run 37042091184 / artifact 11242354548; 100% de coincidencia de acción aplicada en t0 y 100% de coincidencia de distribución de SELF_MODEL; cambio de acción futura 46.43%, p=4.99975e-05; AUC de estado 2.1867184440, p=4.99975e-05; AUC bridge ON-vs-OFF 2.6656102772, p=4.99975e-05.

### I5.14 — Control fase-matcheado de especificidad temporal
- `docs/I5_14_PHASE_MATCHED_TEMPORAL_SPECIFICITY.md`
- `experiments/i5_14_phase_matched_temporal_specificity_control.py`
- `tests/test_i5_14_phase_matched_temporal_specificity.py`
- Verificado: run 37042551701 / artifact 11243190387; 100% de coincidencia de acción t0 y 100% de coincidencia de distribución de SELF_MODEL; cambio de acción futura SHIFT+1 11.90% y SHIFT-1 44.64%, ambos p=4.99975e-05; AUC BASE-vs-SHIFT+1 0.2414241371, BASE-vs-SHIFT-1 1.9526574097; AUC SHIFT+1 bridge ON-vs-OFF 2.1221765870, todos p=4.99975e-05.



### I5.16 — Control temporal de fase pura contrabalanceado
- `docs/I5_16_COUNTERBALANCED_PURE_PHASE_TEMPORAL_CONTROL.md`
- `experiments/i5_16_counterbalanced_pure_phase_temporal_control.py`
- `tests/test_i5_16_counterbalanced_pure_phase_temporal_control.py`
- Verificado: run 37046361416 / artifact 11245200134; 100% de coincidencia de acción t0 y 100% de distribución de SELF_MODEL; simetría absoluta +1 vs -1 = -1.138780, p=0.000300; +2 vs -2 y +3 vs -3 no significativos; ningún contraste firmado BASE-vs-lag fue significativo. La asimetría de magnitud -1/+1 sobrevive al control de fase pura y al contrabalanceo semántico, por lo que el siguiente paso es mapear el bridge por fase.
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


### I5.22 — Cyclic semantic phase-shift control
- `docs/I5_22_CYCLIC_SEMANTIC_PHASE_SHIFT.md`
- `experiments/i5_22_cyclic_semantic_phase_shift.py`
- `tests/test_i5_22_cyclic_semantic_phase_shift.py`
- Validated: research-lab **37061263630** / artifact **11251161457**; tests **37061263638** and package check **37061263624** successful.
- 24 replicates; all four invariants preserved at **100%**.
- Specificity gap: signed AUC **+0.02801**, p=0.74476; absolute AUC **+0.02983**, p=0.71256; future-action change **+0.00645**, p=0.52927.
- Global lag×specificity interaction non-significant for all three endpoints.
- max-T any-lag p: **0.22344** signed AUC, **0.76186** absolute AUC, **0.78481** future action.
- Interpretation: strict cyclic phase-shift control was null; I5.21 cannot be attributed solely to phase↔content decoupling.
- Next: I5.23 cyclic shift sweep.


### I5.23 — Cyclic shift sweep
- `docs/I5_23_CYCLIC_SHIFT_SWEEP.md`
- `experiments/i5_23_cyclic_shift_sweep.py`
- `tests/test_i5_23_cyclic_shift_sweep.py`
- Verified: research-lab **37062538761** / artifact **11251207688**; tests **37062538733** and package check **37062538712** successful.
- 24 replicates; six shifts × six lags; 100% preservation across 864 control cells.
- Signed AUC: no shift survives max-T (global any-shift p=0.14534).
- Absolute AUC and future-action change: five of six shifts survive max-T; +1 is null.
- Global max-T over 36 shift×lag cells is significant for absolute AUC and future action.
- Next: I5.24 formal global shift×lag interaction.


### I5.24 — Global shift×lag interaction
- docs/I5_24_GLOBAL_SHIFT_LAG_INTERACTION.md
- experiments/i5_24_global_shift_lag_interaction.py
- tests/test_i5_24_global_shift_lag_interaction.py
- Frozen-data analysis of I5.23; no new trajectories.
- Verified workflow 37063264401 / artifact 11252345042; tests 37063264520 and package 37063264454 successful.
- Signed AUC: p=0.89461; absolute AUC and future-action interaction p=0.00005 each, Bonferroni 0.00015.
- Next: I5.25 shift×lag orientation and symmetry control.


### I5.25 — Shift×lag orientation and symmetry control
- docs/I5_25_SHIFT_LAG_ORIENTATION_SYMMETRY.md
- experiments/i5_25_shift_lag_orientation_symmetry.py
- tests/test_i5_25_shift_lag_orientation_symmetry.py
- Frozen I5.23 analysis; no new trajectories.
- Verified workflow **37065168288** / artifact **11251708654**; package **37065168296**, tests **37065168323** successful.
- Signed AUC: orientation p=0.30128; diagonal p=0.62617.
- Absolute AUC: orientation and diagonal p=0.00005 each; Bonferroni 0.00030.
- Future action: orientation and diagonal p=0.00005 each; Bonferroni 0.00030.
- Next: I5.26 matched-magnitude sign-coupling control.
