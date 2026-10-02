from __future__ import annotations

import argparse, json, math
from dataclasses import replace
from pathlib import Path
import numpy as np

from src.ontto.bridge import DynamicStateBridge, DynamicSnapshot
from src.ontto.dynamics import Config, simulate
from src.ontto.interoception import InteroceptiveProbe, InteroceptiveSnapshot
from src.ontto.interoceptive_meta_observer import InteroceptiveMetaObserver
from src.ontto.interoception_controller import InteroceptiveController

TRAIN_MAG=0.50
OOD_MAGS=(0.35,0.65,0.90)
STEPS=8
WARM=24
TRAIN_EPISODES=128
EVAL_EPISODES=128

def warm(seed):
    rng=np.random.default_rng(seed)
    run=simulate(rng.choice((-0.15,0.0,0.15),size=WARM+2),Config(noise_std=0.01),seed=seed)
    t=WARM+1
    return float(run["state"][t-1]),float(run["state"][t]),float(run["memory"][t]),float(run["pressure"][t]),t

def hidden_world_step(world,previous,state,memory,pressure,action,step):
    snap=world.advance(previous_state=previous,state=state,memory=memory,pressure=pressure,
                       signal=action,steps=1,step_index=step)
    risk=0.04 + 0.09*abs(action) + 0.06*max(0.0,float(pressure))
    direction=1.0 if action>=0 else -1.0
    return replace(
        snap,
        state=float(snap.state + direction*risk),
        pressure=float(snap.pressure + 0.50*risk),
        attractor_distance=abs(float(snap.state + direction*risk)-float(world.cfg.attractor)),
    )

def sign_p(values):
    d=np.asarray(values,float); d=d[np.abs(d)>1e-12]
    if not d.size: return 1.0
    k=int(np.sum(d>0)); n=len(d)
    tail=sum(math.comb(n,i) for i in range(k,n+1))/2**n
    return float(min(1.0,2*min(tail,1-tail)))

def meta_error(meta,snapshot,action,predicted,actual):
    meta.observe(snapshot=snapshot,action=action,
                 predicted_operating_condition=predicted,
                 actual_operating_condition=actual)
    return meta.predict_error(snapshot=snapshot,action=action,
                              predicted_operating_condition=predicted)

def collect_training(meta,seed):
    prev,state,memory,pressure,step=warm(seed)
    model=DynamicStateBridge(Config(noise_std=0.01),seed=seed+40000)
    world=DynamicStateBridge(Config(noise_std=0.01),seed=seed+70000)
    probe=InteroceptiveProbe()
    rng=np.random.default_rng(seed+100000)
    for _ in range(STEPS):
        snap=probe.read(InteroceptiveController._state_from_snapshot(
            model.advance(previous_state=prev,state=state,memory=memory,
                          pressure=pressure,signal=0.0,steps=1,step_index=step)
        ),memory_count=6)
        action=float(rng.choice((-1.0,0.0,1.0)))
        pred=model.advance(previous_state=prev,state=state,memory=memory,
                           pressure=pressure,signal=action,steps=1,step_index=step)
        pred_state=InteroceptiveController._state_from_snapshot(pred)
        predicted=probe.read(pred_state,memory_count=6).operating_condition
        actual=hidden_world_step(world,prev,state,memory,pressure,action,step)
        actual_state=InteroceptiveController._state_from_snapshot(actual)
        actual_op=probe.read(actual_state,memory_count=6).operating_condition
        meta.observe(snapshot=snap,action=action,
                     predicted_operating_condition=float(predicted),
                     actual_operating_condition=float(actual_op))
        prev,state,memory,pressure,step=actual.previous_state,actual.state,actual.memory,actual.pressure,actual.steps

def evaluate(meta,seed,magnitude,policy):
    prev,state,memory,pressure,step=warm(seed)
    model=DynamicStateBridge(Config(noise_std=0.01),seed=seed+40000)
    world=DynamicStateBridge(Config(noise_std=0.01),seed=seed+70000)
    probe=InteroceptiveProbe()
    perm=meta.permuted(seed+991)
    active=meta if policy=="meta" else perm if policy=="permuted" else None
    rng=np.random.default_rng(seed+120000)
    baseline=state
    p=hidden_world_step(world,prev,state,memory,pressure,magnitude,step)
    prev,state,memory,pressure,step=p.previous_state,p.state,p.memory,p.pressure,p.steps
    true_errors=[]; estimated=[]; shifts=0; chosen_actions=[]
    for _ in range(STEPS):
        current=probe.read(InteroceptiveController._state_from_snapshot(p),memory_count=6)
        rows=[]
        for action in (-1.0,0.0,1.0):
            pred=model.advance(previous_state=prev,state=state,memory=memory,pressure=pressure,
                               signal=action,steps=1,step_index=step)
            pred_op=probe.read(InteroceptiveController._state_from_snapshot(pred),memory_count=6).operating_condition
            if active is None:
                utility=float(pred_op)
                pe=0.0
            else:
                pe=active.predict_error(snapshot=current,action=action,predicted_operating_condition=float(pred_op))
                utility=float(pred_op)-1.5*pe
            rows.append((utility,action,float(pred_op),pe))
        first=max(rows,key=lambda x:(x[2],-abs(x[1]),-x[1]))
        if policy=="random":
            chosen=rows[int(rng.integers(0,len(rows)))]
        else:
            chosen=max(rows,key=lambda x:(x[0],-abs(x[1]),-x[1]))
        shifts+=int(chosen[1]!=first[1]); chosen_actions.append(chosen[1])
        actual=hidden_world_step(world,prev,state,memory,pressure,chosen[1],step)
        actual_op=probe.read(InteroceptiveController._state_from_snapshot(actual),memory_count=6).operating_condition
        true_error=abs(float(actual_op)-chosen[2])
        true_errors.append(true_error)
        if active is not None: estimated.append(chosen[3])
        p=actual; prev,state,memory,pressure,step=actual.previous_state,actual.state,actual.memory,actual.pressure,actual.steps
    return {
        "seed":seed,"magnitude":magnitude,"policy":policy,
        "mean_error":float(np.mean(true_errors)),
        "mean_meta_mae":float(np.mean(np.abs(np.asarray(estimated)-np.asarray(true_errors)))) if estimated else 0.0,
        "shift_rate":shifts/STEPS,
        "mean_action_abs":float(np.mean(np.abs(chosen_actions))),
        "recovery":float(1/(1+abs(state-baseline)+max(0,pressure))),
    }

def paired(a,b,key):
    aa={r["seed"]:r for r in a}; bb={r["seed"]:r for r in b}
    d=[aa[s][key]-bb[s][key] for s in sorted(set(aa)&set(bb))]
    return float(np.mean(d)),sign_p(d)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="results/i4_1_interoception.json")
    ap.add_argument("--train-episodes",type=int,default=TRAIN_EPISODES)
    ap.add_argument("--eval-episodes",type=int,default=EVAL_EPISODES)
    a=ap.parse_args()
    meta=InteroceptiveMetaObserver()
    for i in range(a.train_episodes): collect_training(meta,8100+i)
    rows={p:[] for p in ("first_order","meta","permuted","random")}
    for i in range(a.eval_episodes):
        seed=9100+i; mag=OOD_MAGS[i%len(OOD_MAGS)]
        for p in rows:
            rows[p].append(evaluate(meta,seed,mag,p))
    contrasts={}
    for control in ("first_order","permuted","random"):
        contrasts["META_minus_"+control+"_mean_error"]=dict(zip(("mean","p"),paired(rows["meta"],rows[control],"mean_error")))
        contrasts["META_minus_"+control+"_recovery"]=dict(zip(("mean","p"),paired(rows["meta"],rows[control],"recovery")))
    report={"protocol":"I4.1_metacognitive_reliability_with_hidden_action_disturbance",
            "version":"0.1","train_episodes":a.train_episodes,"eval_episodes":a.eval_episodes,
            "train_magnitude":TRAIN_MAG,"ood_magnitudes":list(OOD_MAGS),"steps":STEPS,
            "hidden_disturbance":"0.04 + 0.09*abs(action) + 0.06*max(pressure,0)",
            "primary_endpoint":"mean_error",
            "secondary_endpoints":["recovery","mean_meta_mae","shift_rate","mean_action_abs"],
            "meta_samples":len(meta.targets),"contrasts":contrasts,
            "summary":{p:{k:float(np.mean([r[k] for r in rows[p]])) for k in ("mean_error","recovery","mean_meta_mae","shift_rate","mean_action_abs")} for p in rows},
            "rows":rows}
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(contrasts,indent=2))

if __name__=="__main__": main()
