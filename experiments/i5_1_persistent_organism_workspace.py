from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import numpy as np

from src.ontto.bridge import DynamicStateBridge
from src.ontto.dynamics import Config as DynamicsConfig
from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.provider import LLMResponse
from src.ontto.storage import MemoryStore
from src.ontto.workspace_controller import WorkspaceRuntimeConfig, WorkspaceTrajectoryController

CANDIDATE_SIGNALS = (-1.0, 1.0)

class FakeProvider:
    def chat(self, messages, temperature=0.7):
        return LLMResponse(text='Calibration response.\nMEMORY: retain dynamic continuity.\nSELF_MODEL: internal state follows trajectory.', raw={'fake': True})

def sign_flip(values: np.ndarray, seed: int, permutations: int = 20000) -> float:
    values=np.asarray(values,dtype=float)
    if values.size == 0: return 1.0
    observed=abs(float(values.mean()))
    rng=np.random.default_rng(seed)
    signs=rng.choice(np.array([-1.0,1.0]), size=(permutations, values.size))
    null=np.abs((signs*values[None,:]).mean(axis=1))
    return float((np.count_nonzero(null>=observed)+1)/(permutations+1))

def warmup(db_path: Path, seed: int, cycles: int) -> None:
    store=MemoryStore(db_path)
    cfg=OrganismConfig(agent_id='receiver', dynamic_seed=seed, dream_every_cycles=10000, event_limit=0, self_observer_enabled=True, self_selection_enabled=False, workspace_enabled=False)
    organism=PersistentOrganism(cfg, store, FakeProvider(), lambda _: None)
    for i in range(cycles):
        organism.wake_cycle(f'calibration {i}')
        organism.autonomous_wake_cycle()
    store.conn.close()

def oracle_for_state(state, seed: int, step_index: int) -> dict[str, object]:
    bridge=DynamicStateBridge(DynamicsConfig(), seed=seed)
    outcomes={}
    for signal in CANDIDATE_SIGNALS:
        snap=bridge.advance(previous_state=state.dynamic_prev_state,state=state.dynamic_state,memory=state.dynamic_memory,pressure=state.dynamic_pressure,signal=signal,steps=1,step_index=step_index)
        outcomes[signal]={'state':float(snap.state),'distance':float(abs(snap.state-snap.attractor_distance*0.0))}
    oracle_signal=min(CANDIDATE_SIGNALS,key=lambda s:(abs(outcomes[s]['state']-0.0),abs(s)))
    return {'oracle_signal':oracle_signal,'oracle_distance':abs(outcomes[oracle_signal]['state']-0.0),'outcomes':outcomes}

def baseline_workspace_source(state, capacity=2) -> int:
    ctl=WorkspaceTrajectoryController(WorkspaceRuntimeConfig(capacity=capacity))
    selection=ctl.select(state)
    return int(selection.indices[0])

def run_arm(db_path: Path, *, seed: int, workspace: bool, broadcast: bool, lesion_index: int | None, influence: float) -> dict[str, object]:
    store=MemoryStore(db_path)
    cfg=OrganismConfig(agent_id='receiver',dynamic_seed=seed,dream_every_cycles=10000,event_limit=0,self_observer_enabled=True,self_selection_enabled=True,self_selection_policy='self_model',self_selection_signals=CANDIDATE_SIGNALS,workspace_enabled=workspace,workspace_broadcast_enabled=broadcast,workspace_capacity=2,workspace_influence_weight=influence,workspace_lesion_index=lesion_index)
    organism=PersistentOrganism(cfg,store,FakeProvider(),lambda _: None)
    before=store.load_state('receiver')
    oracle=oracle_for_state(before,seed,before.dynamic_steps)
    organism.autonomous_wake_cycle()
    after=store.load_state('receiver')
    event=store.recent_events('receiver',1)[0]
    chosen=float(event['payload']['self_selection']['chosen_signal'])
    actual=float(abs(after.dynamic_state-after.dynamic_attractor_distance*0.0))
    regret=actual-float(oracle['oracle_distance'])
    control=event['payload']['self_selection'].get('workspace_control')
    persisted_before={k:v for k,v in store.persistence_observables('receiver').items() if k.startswith('workspace_')}
    store.conn.close()
    restored=MemoryStore(db_path)
    persisted_after={k:v for k,v in restored.persistence_observables('receiver').items() if k.startswith('workspace_')}
    restored.conn.close()
    return {'workspace_enabled':workspace,'broadcast_enabled':broadcast,'lesion_index':lesion_index,'chosen_signal':chosen,'oracle_signal':oracle['oracle_signal'],'regret':regret,'workspace_control':control,'workspace_persistence_equal':persisted_before==persisted_after}

def run(seed: int, replicates: int, warmup_cycles: int, influence: float, out: Path) -> dict[str, object]:
    out.mkdir(parents=True,exist_ok=True)
    rows=[]
    for rep in range(replicates):
        rep_seed=seed+rep
        base=out/f'base_{rep}.db'; full_db=out/f'full_{rep}.db'; nobroadcast_db=out/f'nobroadcast_{rep}.db'; lesion_db=out/f'lesion_{rep}.db'; baseline_db=out/f'baseline_{rep}.db'
        warmup(base,rep_seed,warmup_cycles)
        state=MemoryStore(base).load_state('receiver')
        source=baseline_workspace_source(state)
        shutil.copy2(base,full_db); shutil.copy2(base,nobroadcast_db); shutil.copy2(base,lesion_db); shutil.copy2(base,baseline_db)
        full=run_arm(full_db,seed=rep_seed,workspace=True,broadcast=True,lesion_index=None,influence=influence)
        nobroadcast=run_arm(nobroadcast_db,seed=rep_seed,workspace=True,broadcast=False,lesion_index=None,influence=influence)
        lesion=run_arm(lesion_db,seed=rep_seed,workspace=True,broadcast=True,lesion_index=source,influence=influence)
        baseline=run_arm(baseline_db,seed=rep_seed,workspace=False,broadcast=False,lesion_index=None,influence=influence)
        rows.append({'replicate':rep,'seed':rep_seed,'selected_source':source,'full':full,'no_broadcast':nobroadcast,'lesion':lesion,'no_workspace':baseline,'broadcast_regret_advantage':nobroadcast['regret']-full['regret'],'workspace_regret_advantage':baseline['regret']-full['regret'],'lesion_regret_cost':lesion['regret']-full['regret'],'broadcast_action_change':int(full['chosen_signal']!=nobroadcast['chosen_signal']),'lesion_action_change':int(full['chosen_signal']!=lesion['chosen_signal'])})
    b=np.asarray([r['broadcast_regret_advantage'] for r in rows]); w=np.asarray([r['workspace_regret_advantage'] for r in rows]); l=np.asarray([r['lesion_regret_cost'] for r in rows])
    summary={'experiment':'i5_1_persistent_organism_workspace','seed':seed,'replicates':replicates,'warmup_cycles':warmup_cycles,'candidate_signals':list(CANDIDATE_SIGNALS),'influence_weight':influence,'endpoints':{'broadcast_regret_advantage_mean':float(b.mean()),'broadcast_regret_advantage_p':sign_flip(b,seed+1),'workspace_regret_advantage_mean':float(w.mean()),'workspace_regret_advantage_p':sign_flip(w,seed+2),'lesion_regret_cost_mean':float(l.mean()),'lesion_regret_cost_p':sign_flip(l,seed+3),'broadcast_action_change_rate':float(np.mean([r['broadcast_action_change'] for r in rows])),'lesion_action_change_rate':float(np.mean([r['lesion_action_change'] for r in rows])),'workspace_persistence_rate':float(np.mean([r['full']['workspace_persistence_equal'] for r in rows]))},'boundary':'I5.1 tests opt-in bounded workspace integration into PersistentOrganism. It evaluates computational broadcast/lesion effects inside the persistent runtime and does not establish consciousness.'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),'utf-8')
    (out/'runs.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),'utf-8')
    return summary

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--seed',type=int,default=20261002); ap.add_argument('--replicates',type=int,default=24); ap.add_argument('--warmup',type=int,default=24); ap.add_argument('--influence',type=float,default=0.35); ap.add_argument('--out',default='results/i5_1_persistent_organism_workspace')
    args=ap.parse_args(); summary=run(args.seed,args.replicates,args.warmup,args.influence,Path(args.out)); print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=='__main__': main()