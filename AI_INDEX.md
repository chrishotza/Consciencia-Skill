# AI Index — Skill-Conscious

## One-screen route

| Need | Read first | Then |
|---|---|---|
| Consciousness Server | `docs/CONSCIOUSNESS_SERVER.md` | `src/consciousness_server/` |
| Local seed | `src/consciousness_server/core.py` | `src/consciousness_server/server.py` |
| Overview | `README.md` | `docs/METODO.md` |
| Current state | `research/ORGANISM_RESULT_LEDGER.md` | V69/V70 docs |
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

### V69
- `docs/V69_SELF_STATE_READOUT.md`
- `docs/V69_SELF_READ_STATE.md`

### V70
- `docs/V70_SELF_MODEL_ACTION.md`
- `docs/V70_PERSISTENT_SELF_READER.md`

### Evidence
- `research/ORGANISM_RESULT_LEDGER.md` — first stop for consolidated experimental claims.

## Architecture map

### Existing organism
- `src/ontto/organism.py` — organism lifecycle/orchestration.
- `src/ontto/dynamics.py` — internal dynamics.
- `src/ontto/self_observer.py` — self-model/self-observation.
- `src/ontto/meta_observer.py` — higher-order observation.
- `src/ontto/trajectory_selector.py` — trajectory/action selection.
- `src/ontto/memory_policy.py` — memory handling.
- `src/ontto/storage.py` — persistence/restart state.
- `src/ontto/continuity.py` — continuity primitives.
- `src/ontto/bridge.py` — semantic ↔ internal-state bridge.
- `src/ontto/provider.py` — model-provider contract.

### Consciousness infrastructure
- `src/consciousness_server/core.py` — durable identity, continuity state, events and node registry.
- `src/consciousness_server/server.py` — local HTTP control plane.
- `src/consciousness_server/cli.py` — local server launcher.
- `src/consciousness_server/client.py` — optional fail-open bridge for the organism runtime.
- `docs/CONSCIOUSNESS_SERVER.md` — architecture and roadmap.
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
