from __future__ import annotations
import argparse, json, shutil
from pathlib import Path
import numpy as np

from experiments.i5_17_phase_resolved_bridge_mediation_map import CYCLES,LAGS,PERIOD,SEMANTIC_TEXT,build_schedule,metrics,run_condition,sign_flip_signed,warmup
from experiments.i5_18_global_phase_bridge_interaction import aggregate_bridge_effect,max_t_adjusted_p,phase_interaction_permutation

SEED=20261023
REPLICATES=24
WARMUP_CYCLES=24
PERMUTATIONS=20_000
SHIFTS=(-3,-2,-1,1,2,3)

METRICS={
 "signed_auc_delta":"cyclic-shift sweep specificity gap in bridge ON-OFF signed AUC",
 "abs_auc_delta":"cyclic-shift sweep specificity gap in bridge ON-OFF absolute AUC",
 "future_action_change_delta":"cyclic-shift sweep specificity gap in bridge ON-OFF future-action change",
}

def shifted_schedule(lag:int,rotation:int,shift:int)->list[str]:
    if shift not in SHIFTS: raise ValueError(f"shift must be one of {SHIFTS}")
    matched=build_schedule(lag,rotation)
    labels=list("ABCDEFG")
    semantic_shift=(rotation+shift)%PERIOD
    mapping={label:SEMANTIC_TEXT[labels[(i+semantic_shift)%PERIOD]] for i,label in enumerate(labels)}
    shifted=[matched[0]]
    for entry in matched[1:]:
        label,_=entry.split(" — ",1)
        shifted.append(f"{label} — {mapping[label]}")
    if shifted[0]!=matched[0]: raise AssertionError("t0 must remain identical")
    mc=sorted(e.split(" — ",1)[1] for e in matched[1:])
    sc=sorted(e.split(" — ",1)[1] for e in shifted[1:])
    if mc!=sc: raise AssertionError("shift must preserve semantic content multiset")
    ml=[e.split(" — ",1)[0] for e in matched[1:]]
    sl=[e.split(" — ",1)[0] for e in shifted[1:]]
    if ml!=sl: raise AssertionError("shift must preserve phase-label sequence")
    mseq=[e.split(" — ",1)[1] for e in matched[1:]]
    sseq=[e.split(" — ",1)[1] for e in shifted[1:]]
    if mseq==sseq: raise AssertionError("non-zero shift must alter phase-content anchoring")
    return shifted

def pair_specificity(matched,shifted):
    return {k:float(matched[k]-shifted[k]) for k in METRICS}

def sweep_max_t_adjusted_p(matrix,seed,permutations):
    v=np.asarray(matrix,float)
    if v.ndim!=3: raise ValueError("matrix must be replicate x shift x lag")
    reps,ns,nl=v.shape
    obs=v.mean(axis=0)
    rng=np.random.default_rng(seed)
    signs=rng.choice((-1.0,1.0),size=(permutations,reps,1,1))
    null=np.abs((signs*v[None,...]).mean(axis=1))
    maxnull=null.reshape(permutations,-1).max(axis=1)
    flat=obs.reshape(-1)
    adj=np.array([(np.count_nonzero(maxnull>=abs(x))+1)/(permutations+1) for x in flat]).reshape(ns,nl)
    anyp=float((np.count_nonzero(maxnull>=abs(flat).max())+1)/(permutations+1))
    return {"observed_mean_by_shift_and_lag":obs.tolist(),"max_t_adjusted_p_by_shift_and_lag":adj.tolist(),"global_any_shift_any_lag_p":anyp,"shape":[ns,nl],"permutations":permutations}

def shift_profile_max_t(matrix,seed,permutations):
    v=np.asarray(matrix,float)
    if v.ndim!=3: raise ValueError("matrix must be replicate x shift x lag")
    reps,ns,_=v.shape
    shiftmeans=v.mean(axis=2)
    obs=shiftmeans.mean(axis=0)
    rng=np.random.default_rng(seed)
    signs=rng.choice((-1.0,1.0),size=(permutations,reps,1))
    null=np.abs((signs*shiftmeans[None,...]).mean(axis=1))
    maxnull=null.max(axis=1)
    adj=np.array([(np.count_nonzero(maxnull>=abs(x))+1)/(permutations+1) for x in obs])
    anyp=float((np.count_nonzero(maxnull>=abs(obs).max())+1)/(permutations+1))
    return {"shift_order":list(SHIFTS),"observed_mean_by_shift":obs.tolist(),"max_t_adjusted_p_by_shift":adj.tolist(),"global_any_shift_p":anyp,"permutations":permutations}

def run(seed,replicates,warmup_cycles,permutations,out):
    if replicates!=REPLICATES or warmup_cycles!=WARMUP_CYCLES or permutations!=PERMUTATIONS:
        raise ValueError("I5.23 protocol parameters are frozen")
    out.mkdir(parents=True,exist_ok=True)
    per_rep=[]
    for rep in range(replicates):
        rep_seed=seed+rep
        rotation=rep%PERIOD
        base_schedule=build_schedule(0,rotation)
        base_db=out/f"base_{rep}.db"
        warmup(base_db,rep_seed,warmup_cycles)
        base_run_db=out/f"base_run_{rep}.db"; shutil.copy2(base_db,base_run_db)
        base_rows=run_condition(base_run_db,rep_seed,base_schedule,True,0.0)
        t0_action=float(base_rows[0]["applied_signal"]); base_run_db.unlink(missing_ok=True)
        row={"replicate":rep,"semantic_rotation":rotation}
        for lag in LAGS:
            matched_schedule=build_schedule(lag,rotation)
            matched_db=out/f"lag_{lag:+d}_matched_{rep}.db"; off_db=out/f"lag_{lag:+d}_off_{rep}.db"
            shutil.copy2(base_db,matched_db); shutil.copy2(base_db,off_db)
            matched_rows=run_condition(matched_db,rep_seed,matched_schedule,True,t0_action)
            off_rows=run_condition(off_db,rep_seed,matched_schedule,False,t0_action)
            matched_db.unlink(missing_ok=True); off_db.unlink(missing_ok=True)
            mm=metrics(base_rows,matched_rows); om=metrics(base_rows,off_rows)
            matched_bridge={
                "abs_auc_delta":float(mm["state_auc_abs"]-om["state_auc_abs"]),
                "signed_auc_delta":float(mm["state_auc_signed"]-om["state_auc_signed"]),
                "future_action_change_delta":float(mm["future_action_change_rate"]-om["future_action_change_rate"]),
            }
            lag_record={}
            for shift in SHIFTS:
                shifted=shifted_schedule(lag,rotation,shift)
                db=out/f"lag_{lag:+d}_shift_{shift:+d}_{rep}.db"; shutil.copy2(base_db,db)
                rows=run_condition(db,rep_seed,shifted,True,t0_action); db.unlink(missing_ok=True)
                sm=metrics(base_rows,rows)
                shifted_bridge={
                    "abs_auc_delta":float(sm["state_auc_abs"]-om["state_auc_abs"]),
                    "signed_auc_delta":float(sm["state_auc_signed"]-om["state_auc_signed"]),
                    "future_action_change_delta":float(sm["future_action_change_rate"]-om["future_action_change_rate"]),
                }
                control={
                    "t0_self_model_match":matched_rows[0]["self_model"]==rows[0]["self_model"],
                    "t0_applied_action_match":float(matched_rows[0]["applied_signal"])==float(rows[0]["applied_signal"]),
                    "post_t0_semantic_content_multiset_preserved":sorted(r["self_model"].split(" — ",1)[1] for r in matched_rows[1:])==sorted(r["self_model"].split(" — ",1)[1] for r in rows[1:]),
                    "phase_label_sequence_preserved":[r["self_model"].split(" — ",1)[0] for r in matched_rows[1:]]==[r["self_model"].split(" — ",1)[0] for r in rows[1:]],
                }
                if not all(control.values()): raise AssertionError(f"invariant failed rep={rep} lag={lag} shift={shift}")
                lag_record[str(shift)]={"shifted_on":sm,"matched_bridge":matched_bridge,"shifted_bridge":shifted_bridge,"specificity_gap":pair_specificity(matched_bridge,shifted_bridge),"control":control}
            row[f"lag_{lag:+d}"]=lag_record
        per_rep.append(row); base_db.unlink(missing_ok=True)
    matrices={}
    for metric in METRICS:
        matrices[metric]=np.asarray([[[per_rep[r][f"lag_{lag:+d}"][str(shift)]["specificity_gap"][metric] for lag in LAGS] for shift in SHIFTS] for r in range(replicates)],float)
    endpoints={}
    for idx,metric in enumerate(METRICS):
        matrix=matrices[metric]
        per_shift={}
        for sidx,shift in enumerate(SHIFTS):
            sm=matrix[:,sidx,:]
            per_shift[str(shift)]={
                "global_specificity_effect":aggregate_bridge_effect(sm,seed+11100+idx*10+sidx,permutations),
                "phase_specificity_interaction":phase_interaction_permutation(sm,seed+11200+idx*10+sidx,permutations),
                "max_t_multiplicity_control":max_t_adjusted_p(sm,seed+11300+idx*10+sidx,permutations),
            }
        endpoints[metric]={
            "description":METRICS[metric],
            "shape":list(matrix.shape),
            "per_shift":per_shift,
            "shift_profile_max_t":shift_profile_max_t(matrix,seed+11400+idx,permutations),
            "sweep_max_t":sweep_max_t_adjusted_p(matrix,seed+11500+idx,permutations),
            "per_cell_sign_flip_p":{f"{shift}:{lag}":sign_flip_signed(matrix[:,sidx,lidx],seed+11600+idx*100+sidx*10+lidx,permutations) for sidx,shift in enumerate(SHIFTS) for lidx,lag in enumerate(LAGS)},
        }
    controls=[per_rep[r][f"lag_{lag:+d}"][str(shift)]["control"] for r in range(replicates) for lag in LAGS for shift in SHIFTS]
    invariant_rates={k:float(np.mean([c[k] for c in controls])) for k in ("t0_self_model_match","t0_applied_action_match","post_t0_semantic_content_multiset_preserved","phase_label_sequence_preserved")}
    if any(rate!=1.0 for rate in invariant_rates.values()): raise AssertionError(f"invariants not 100%: {invariant_rates}")
    result={"experiment":"i5_23_cyclic_shift_sweep","seed":seed,"replicates":replicates,"warmup_cycles":warmup_cycles,"cycles":CYCLES,"lags":list(LAGS),"period":PERIOD,"shifts":list(SHIFTS),"permutations":permutations,"primary_question":"Is the I5.22 null robust across the full family of non-zero cyclic semantic shifts?","control_invariant":{**invariant_rates,"total_control_cells":len(controls)},"boundary":"I5.23 tests computational semantic specificity robustness across all non-zero seven-phase shifts; it does not establish consciousness or subjective experience.","endpoints":endpoints,"per_replicate":per_rep}
    (out/"summary.json").write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8")
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seed",type=int,default=SEED); p.add_argument("--replicates",type=int,default=REPLICATES); p.add_argument("--warmup",type=int,default=WARMUP_CYCLES); p.add_argument("--permutations",type=int,default=PERMUTATIONS); p.add_argument("--out",default="results/i5_23_cyclic_shift_sweep")
    a=p.parse_args(); print(json.dumps(run(a.seed,a.replicates,a.warmup,a.permutations,Path(a.out)),indent=2,ensure_ascii=False))

if __name__=="__main__": main()
