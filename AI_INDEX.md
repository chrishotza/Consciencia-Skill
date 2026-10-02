# AI Index — Skill-Conscious

## One-screen route

| Need | Read first | Then |
|---|---|---|
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
- `docs/C0_8_CROSSED_OBSERVER_POLICY.md` — crossed observer/policy coupling test; first execution required a statistical correction and a confirmatory rerun.
- `experiments/tcf_consciousness_instantiation_c0_8.py` — elementwise paired interaction statistics.

### C0.9
- `docs/C0_9_OBSERVER_POLICY_INTERFACE_SHUFFLE.md` — observer → policy interface causal shuffle.
- `experiments/tcf_consciousness_instantiation_c0_9.py` — matched first-step interface test with donor derangement.

### C0.10
- `docs/C0_10_WITHIN_EPISODE_TEMPORAL_ALIGNMENT.md` — within-episode temporal lag control for observer → policy alignment.
- `experiments/tcf_consciousness_instantiation_c0_10.py` — current-state vs. pre-intervention observer-readout comparison.

### C0.11
- `docs/C0_11_CAUSAL_ACTION_MEDIATION.md` — direct action intervention on the middle of the action → internal-state → next-action chain.
- `experiments/tcf_consciousness_instantiation_c0_11.py` — paired factual vs. forced-action causal test.

### V69
- `docs/V69_SELF_STATE_READOUT.md` — numeric readout; discrete action endpoint is null.
- `docs/V69_SELF_READ_STATE.md` — readout participates in trajectory selection; includes blinded control and state-swap intervention.

### V70
- `docs/V70_SELF_MODEL_ACTION.md` — prediction from self-model becomes continuous action.
- `docs/V70_PERSISTENT_SELF_READER.md` — self-reader persistence across restart.

### Evidence
- `research/ORGANISM_RESULT_LEDGER.md` — first stop for consolidated experimental claims.

## Architecture map
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
