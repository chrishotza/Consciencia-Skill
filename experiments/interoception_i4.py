from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np
from src.ontto.bridge import DynamicStateBridge
from src.ontto.dynamics import Config, simulate
from src.ontto.interoception import InteroceptiveProbe, InteroceptiveSnapshot
from src.ontto.interoceptive_meta_observer import InteroceptiveMetaObserver
from src.ontto.interoception_controller import InteroceptiveController

TRAIN_MAGNITUDE=0.50
OOD_MAGNITUDES=(0.35,0.65,0.90)
RECOVERY_STEPS=8
WARMUP_STEPS=24
META_LAMBDA=0.75
DEFAULT_TRAIN_EPISODES=96
DEFAULT_EVAL_EPISODES=96

def sign_p(values):
    d=np.asarray(values,float); d=d[np.abs(d)>1e-12]
    if not d.size: return 1.0
    k=int(np.sum(d>0)); n=int(d.size)
    tail=sum(math.comb(n,i) for i in range(k,n+1))/2**n
    return float(min(1.0,2.0*min(tail,1.0-tail)))

def warm(seed):
    rng=np.random.default_rng(seed)
    run=simulate(rng.choice((-0.15,0.0,0.15),size=WARMUP_STEPS+2),Config(noise_std=0.01),seed=seed)
    t=WARMUP_STEPS+1
    return float(run["state"][t-1]),float(run["state"][t]),float(run["memory"][t]),float(run["pressure"][t]),t

def recovery(state,pressure,baseline):
    return 1/(1+abs(float(state)-float(baseline))+max(0.0,float(pressure)))

def choose(controller,candidates,policy,meta,snapshot,rng):
    first=controller.choose(candidates).signal
    if policy=="first_order":
        c=controller.choose(candidates); return float(c.signal),False
    if policy=="random":
        s=float(rng.choice([c.signal for c in candidates])); return s,False
    if meta is None: raise ValueError("meta observer required")
    scored=[]
    for c in candidates:
        pe=meta.predict_error(snapshot=snapshot,action=float(c.signal),
                              predicted_operating_condition=float(c.predicted_snapshot.operating_condition))
        scored.append((float(c.score)-META_LAMBDA*pe,c))
    c=max(scored,key=lambda x:(x[0],-abs(x[1].signal),-x[1].signal))[1]
    return float(c.signal),abs(float(c.signal)-float(first))>1e-12

def train_episode(seed,meta):
    prev,state,memory,pressure,step=warm(seed)
    model=DynamicStateBridge(Config(noise_std=0.01),seed=seed+60000)
    world=DynamicStateBridge(Config(noise_std=0.01),seed=seed+90000)
    ctl=InteroceptiveController(InteroceptiveProbe(),memory_count=6)
    baseline=state
    p=world.advance(previous_state=prev,state=state,memory=memory,pressure=pressure,
                    signal=TRAIN_MAGNITUDE,steps=1,step_index=step)
    prev,state,memory,pressure,step=p.previous_state,p.state,p.memory,p.pressure,p.steps
    for _ in range(RECOVERY_STEPS):
        snap=ctl.probe.read(ctl._state_from_snapshot(p),memory_count=6)
        cs=ctl.evaluate(model,previous_state=prev,state=state,memory=memory,pressure=pressure,
                        signals=(-1.0,0.0,1.0),step_index=step,mode="full")
        chosen=ctl.choose(cs)
        pred=next(c for c in cs if c.signal==chosen.signal)
        nxt=world.advance(previous_state=prev,state=state,memory=memory,pressure=pressure,
                          signal=float(chosen.signal),steps=1,step_index=step)
        actual=ctl.probe.read(ctl._state_from_snapshot(nxt),memory_count=6)
        meta.observe(snapshot=snap,action=float(chosen.signal),
                     predicted_operating_condition=float(pred.predicted_snapshot.operating_condition),
                     actual_operating_condition=float(actual.operating_condition))
        p=nxt; prev,state,memory,pressure,step=nxt.previous_state,nxt.state,nxt.memory,nxt.pressure,nxt.steps
    return recovery(state,pressure,baseline)

def eval_episode(seed,magnitude,policy,meta):
    prev,state,memory,pressure,step=warm(seed)
    model=DynamicStateBridge(Config(noise_std=0.01),seed=seed+60000)
    world=DynamicStateBridge(Config(noise_std=0.01),seed=seed+90000)
    ctl=InteroceptiveController(InteroceptiveProbe(),memory_count=6)
    rng=np.random.default_rng(seed+120000)
    baseline=state
    p=world.advance(previous_state=prev,state=state,memory=memory,pressure=pressure,
                    signal=magnitude,steps=1,step_index=step)
    prev,state,memory,pressure,step=p.previous_state,p.state,p.memory,p.pressure,p.steps
    rec=[]; actual_err=[]; predicted_err=[]; shifts=0
    for _ in range(RECOVERY_STEPS):
        snap=ctl.probe.read(ctl._state_from_snapshot(p),memory_count=6)
        cs=ctl.evaluate(model,previous_state=prev,state=state,memory=memory,pressure=pressure,
                        signals=(-1.0,0.0,1.0),step_index=step,mode="full")
        chosen_signal,shift=choose(ctl,cs,policy,meta,snap,rng)
        shifts+=int(shift)
        chosen=next(c for c in cs if c.signal==chosen_signal)
        pe=0.0 if meta is None else meta.predict_error(
            snapshot=snap,action=chosen_signal,
            predicted_operating_condition=float(chosen.predicted_snapshot.operating_condition))
        nxt=world.advance(previous_state=prev,state=state,memory=memory,pressure=pressure,
                          signal=chosen_signal,steps=1,step_index=step)
        actual=ctl.probe.read(ctl._state_from_snapshot(nxt),memory_count=6)
        ae=abs(float(actual.operating_condition)-float(chosen.predicted_snapshot.operating_condition))
        actual_err.append(ae); predicted_err.append(pe)
        p=nxt; prev,state,memory,pressure,step=nxt.previous_state,nxt.state,nxt.memory,nxt.pressure,nxt.steps
        rec.append(recovery(state,pressure,baseline))
    return {"seed":seed,"magnitude":magnitude,"mean_recovery":float(np.mean(rec)),
            "final_recovery":float(rec[-1]),"mean_prediction_error":float(np.mean(actual_err)),
            "meta_mae":0.0 if meta is None else float(np.mean(np.abs(np.asarray(predicted_err)-np.asarray(actual_err)))),
            "policy_shift_rate":shifts/RECOVERY_STEPS}

def paired(a,b,key):
    aa={int(r["seed"]):r for r in a}; bb={int(r["seed"]):r for r in b}
    s=sorted(set(aa)&set(bb)); d=[aa[x][key]-bb[x][key] for x in s]
    return float(np.mean(d)),sign_p(d)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="results/i4_interoception.json")
    ap.add_argument("--train-episodes",type=int,default=DEFAULT_TRAIN_EPISODES)
    ap.add_argument("--eval-episodes",type=int,default=DEFAULT_EVAL_EPISODES)
    a=ap.parse_args()
    meta=InteroceptiveMetaObserver()
    train=[train_episode(6200+i,meta) for i in range(a.train_episodes)]
    permuted=meta.permuted(620099)
    policies=("first_order","meta_aware","meta_permuted","random")
    rows={p:[] for p in policies}
    for i in range(a.eval_episodes):
        seed=7200+i; mag=OOD_MAGNITUDES[i%len(OOD_MAGNITUDES)]
        for p in policies:
            rows[p].append(eval_episode(seed,mag,p,meta if p=="meta_aware" else permuted if p=="meta_permuted" else None))
    contrasts={}
    for control in ("first_order","meta_permuted","random"):
        m,p=paired(rows["meta_aware"],rows[control],"mean_recovery")
        contrasts[f"META_AWARE_minus_{control}_mean_recovery"]={"mean":m,"p":p}
    summary={p:{
        "mean_recovery":float(np.mean([r["mean_recovery"] for r in rows[p]])),
        "final_recovery":float(np.mean([r["final_recovery"] for r in rows[p]])),
        "mean_prediction_error":float(np.mean([r["mean_prediction_error"] for r in rows[p]])),
        "meta_mae":float(np.mean([r["meta_mae"] for r in rows[p]])),
        "policy_shift_rate":float(np.mean([r["policy_shift_rate"] for r in rows[p]])),
    } for p in policies}
    report={"protocol":"I4_metacognitive_interoception","version":"0.1",
            "train_episodes":a.train_episodes,"eval_episodes":a.eval_episodes,
            "train_magnitude":TRAIN_MAGNITUDE,"ood_magnitudes":list(OOD_MAGNITUDES),
            "recovery_steps":RECOVERY_STEPS,"meta_lambda":META_LAMBDA,
            "primary_endpoint":"mean_recovery",
            "training":{"meta_samples":len(meta.targets),"mean_training_recovery":float(np.mean(train))},
            "contrasts":contrasts,"summary":summary,"rows":rows,
            "scientific_gate":{"interpretation":"computational metacognitive regulation only; not a consciousness claim",
                               "requires":["held-out OOD","permuted-target control","paired seeds",
                                           "independent recovery endpoint","no semantic labels",
                                           "no meta updates during evaluation"]}}
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(contrasts,indent=2))

if __name__=="__main__":
    main()
