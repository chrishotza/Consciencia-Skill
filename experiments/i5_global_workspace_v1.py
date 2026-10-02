from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
from src.ontto.global_workspace import GlobalWorkspace, WorkspaceConfig

def sign_flip(values, seed, permutations=20000):
    values=np.asarray(values,dtype=float); observed=abs(float(values.mean()))
    rng=np.random.default_rng(seed); signs=rng.choice((-1.0,1.0),size=(permutations,values.size))
    null=np.abs((signs*values[None,:]).mean(axis=1))
    return float((np.count_nonzero(null>=observed)+1)/(permutations+1))

def episode(rng, module_count=6):
    target=int(rng.choice((-1,1))); relevant=int(rng.integers(0,module_count))
    x=rng.normal(0.0,0.55,size=(module_count,2)); x[relevant]+=np.asarray([target,target],dtype=float)
    reliability=np.full(module_count,0.35); reliability[relevant]=1.0
    return x,reliability,target

def score(ws,x,reliability,target,*,broadcast_enabled=True,lesion=None):
    updated,sel=ws.step(x,reliability,broadcast_enabled=broadcast_enabled,selected_lesion=lesion)
    decoded=1 if float(np.mean(updated[:,0]+updated[:,1]))>=0 else -1
    return float(decoded==target),sel

def run(seed,episodes):
    rng=np.random.default_rng(seed)
    bounded=GlobalWorkspace(6,2,WorkspaceConfig(capacity=2,broadcast_gain=0.65,local_gain=0.35))
    unbounded=GlobalWorkspace(6,2,WorkspaceConfig(capacity=6,broadcast_gain=0.65,local_gain=0.35))
    broadcast=[]; capacity=[]; lesion=[]
    for _ in range(episodes):
        x,rel,target=episode(rng)
        full,sel=score(bounded,x,rel,target,broadcast_enabled=True)
        local,_=score(bounded,x,rel,target,broadcast_enabled=False)
        all_access,_=score(unbounded,x,rel,target,broadcast_enabled=True)
        broadcast.append(full-local); capacity.append(full-all_access)
        selected_source=sel.indices[0]
        selected_out,_=score(bounded,x,rel,target,broadcast_enabled=True,lesion=selected_source)
        unselected_source=next(i for i in range(6) if i not in sel.indices)
        unselected_out,_=score(bounded,x,rel,target,broadcast_enabled=True,lesion=unselected_source)
        lesion.append(selected_out-unselected_out)
    b=np.asarray(broadcast); c=np.asarray(capacity); l=np.asarray(lesion)
    return {"experiment":"i5_global_workspace_v1","seed":seed,"episodes":episodes,"config":{"modules":6,"vector_dim":2,"capacity":2,"unbounded_capacity":6,"broadcast_gain":0.65,"local_gain":0.35},"endpoints":{"broadcast_accuracy_advantage_mean":float(b.mean()),"broadcast_accuracy_advantage_p":sign_flip(b,seed+1),"bounded_minus_unbounded_accuracy_mean":float(c.mean()),"bounded_minus_unbounded_p":sign_flip(c,seed+2),"selected_minus_unselected_lesion_effect_mean":float(l.mean()),"selected_minus_unselected_lesion_effect_p":sign_flip(l,seed+3)},"boundary":"Synthetic bounded-workspace feasibility experiment; computational architecture only."}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--seed',type=int,default=20261002); ap.add_argument('--episodes',type=int,default=512); ap.add_argument('--out',default='results/i5_global_workspace_v1')
    args=ap.parse_args(); out=Path(args.out); out.mkdir(parents=True,exist_ok=True); s=run(args.seed,args.episodes)
    (out/'summary.json').write_text(json.dumps(s,indent=2),encoding='utf-8'); print(json.dumps(s,indent=2))

if __name__=='__main__': main()