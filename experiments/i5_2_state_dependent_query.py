from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from src.ontto.global_workspace import GlobalWorkspace, WorkspaceConfig
from src.ontto.workspace_query import QUERY_CODES, QUERY_MODULES, StateDependentQuery

def sign_flip(values: np.ndarray, seed: int, permutations: int = 20000) -> float:
    values = np.asarray(values, dtype=float)
    observed = abs(float(values.mean()))
    rng = np.random.default_rng(seed)
    signs = rng.choice((-1.0, 1.0), size=(permutations, values.size))
    null = np.abs((signs * values[None, :]).mean(axis=1))
    return float((np.count_nonzero(null >= observed) + 1) / (permutations + 1))

def make_episode(rng: np.random.Generator):
    target = int(rng.choice(QUERY_MODULES))
    code = QUERY_CODES[target]
    cue = code + rng.normal(0.0, 0.08, size=2)
    modules = rng.normal(0.0, 0.06, size=(6, 2))
    modules[0] = cue
    values = rng.choice((-1.0, 1.0), size=4)
    for module, value in zip(QUERY_MODULES, values):
        modules[module, 0] = value
        modules[module, 1] += rng.normal(0.0, 0.03)
    reliability = np.full(6, 0.25, dtype=float)
    reliability[0] = 1.0
    reliability[list(QUERY_MODULES)] = 0.12
    return modules, reliability, target, values

def workspace_broadcast(modules, reliability):
    ws = GlobalWorkspace(6, 2, WorkspaceConfig(capacity=1, broadcast_gain=1.0, local_gain=0.0))
    selection = ws.select(modules, reliability)
    return selection.broadcast, selection

def decode_target(query, modules, target):
    queried = int(query.module_index)
    value = float(modules[queried, 0])
    correct = queried == target
    signal_correct = correct and abs(value) > 0.0
    return queried, signal_correct

def run(seed: int, episodes: int):
    rng = np.random.default_rng(seed)
    q = StateDependentQuery()
    target_hits = []
    target_hits_shuffled = []
    target_hits_zero = []
    target_hits_random = []
    lesion_hits = []
    query_change = []
    for _ in range(episodes):
        modules, reliability, target, _ = make_episode(rng)
        broadcast, selection = workspace_broadcast(modules, reliability)
        full = q.query(modules, broadcast)
        shuffled = q.query(modules, broadcast[::-1])
        zero = q.query(modules, np.zeros(2))
        random_target = int(rng.choice(QUERY_MODULES))
        full_hit = int(full.module_index == target)
        shuffled_hit = int(shuffled.module_index == target)
        zero_hit = int(zero.module_index == target)
        random_hit = int(random_target == target)
        selected_source = int(selection.indices[0])
        lesioned = modules.copy()
        lesioned[selected_source] = 0.0
        lesion_broadcast, _ = workspace_broadcast(lesioned, reliability)
        lesion_query = q.query(lesioned, lesion_broadcast)
        lesion_hits.append(int(lesion_query.module_index == target))
        target_hits.append(full_hit)
        target_hits_shuffled.append(shuffled_hit)
        target_hits_zero.append(zero_hit)
        target_hits_random.append(random_hit)
        query_change.append(int(full.module_index != shuffled.module_index))
    a=np.asarray(target_hits,dtype=float)
    s=np.asarray(target_hits_shuffled,dtype=float)
    z=np.asarray(target_hits_zero,dtype=float)
    r=np.asarray(target_hits_random,dtype=float)
    l=np.asarray(lesion_hits,dtype=float)
    qc=np.asarray(query_change,dtype=float)
    return {
        'experiment':'i5_2_state_dependent_query',
        'seed':seed,
        'episodes':episodes,
        'query_modules':list(QUERY_MODULES),
        'endpoints':{
            'full_query_accuracy':float(a.mean()),
            'full_minus_shuffled_accuracy':float((a-s).mean()),
            'full_minus_shuffled_p':sign_flip(a-s,seed+1),
            'full_minus_zero_accuracy':float((a-z).mean()),
            'full_minus_zero_p':sign_flip(a-z,seed+2),
            'full_minus_random_accuracy':float((a-r).mean()),
            'full_minus_random_p':sign_flip(a-r,seed+3),
            'lesion_query_accuracy':float(l.mean()),
            'full_minus_lesion_accuracy':float((a-l).mean()),
            'full_minus_lesion_p':sign_flip(a-l,seed+4),
            'state_dependent_query_change_rate':float(qc.mean()),
        },
        'boundary':'Standalone GWT-4 mechanism test. It tests whether global state selects a subsequent module query. It does not establish consciousness.',
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--seed',type=int,default=20261002)
    ap.add_argument('--episodes',type=int,default=512)
    ap.add_argument('--out',default='results/i5_2_state_dependent_query')
    args=ap.parse_args()
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    summary=run(args.seed,args.episodes)
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()