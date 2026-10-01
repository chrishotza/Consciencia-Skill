from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ontto.bridge import DynamicStateBridge
from src.ontto.dynamics import Config as DynamicsConfig
from src.ontto.self_policy import SelfPolicy

from experiments.tcf_consciousness_instantiation_c0 import (
    AUTONOMOUS_STEPS,
    choose_action,
    sign_p,
    train_policy,
    train_self_observer,
    warmup_context,
)
from experiments.organism_repeated_active_continuity_v78 import (
    DynamicContext,
    self_prediction_gain,
)


PROTOCOL_VERSION="C0.4"
EPISODES=64
REPLAYS=8


def derangement(rng: np.random.Generator, size: int) -> np.ndarray:
    reference=np.arange(size)
    while True:
        p=rng.permutation(size)
        if not np.any(p==reference):
            return p


def full_trajectory(observer, policy, *, episode: int):
    seed=90010+episode
    bridge=DynamicStateBridge(DynamicsConfig(), seed=seed)
    context=warmup_context(bridge, seed=seed+1000)
    initial=context
    states=[float(context.state)]
    signals=[]
    for _ in range(AUTONOMOUS_STEPS):
        signal=choose_action(
            policy,
            observer,
            context=context,
            state_blind=False,
            open_loop=False,
        )
        _,_,context=self_prediction_gain(
            observer,
            bridge,
            context=context,
            signal=signal,
        )
        signals.append(float(signal))
        states.append(float(context.state))
    return initial, np.asarray(signals,dtype=float), np.asarray(states,dtype=float)


def replay_variance(observer, *, initial: DynamicContext, actions: np.ndarray, seed: int) -> float:
    bridge=DynamicStateBridge(DynamicsConfig(), seed=seed)
    context=initial
    states=[float(context.state)]
    for signal in actions:
        _,_,context=self_prediction_gain(
            observer,
            bridge,
            context=context,
            signal=float(signal),
        )
        states.append(float(context.state))
    return float(np.var(np.asarray(states,dtype=float)))


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--episodes",type=int,default=EPISODES)
    ap.add_argument("--train-episodes",type=int,default=64)
    ap.add_argument("--observer-samples",type=int,default=512)
    ap.add_argument("--out",default="results/tcf_consciousness_instantiation_c0_4")
    args=ap.parse_args()

    out=Path(args.out)
    shutil.rmtree(out,ignore_errors=True)
    out.mkdir(parents=True)

    observer=train_self_observer(seed=90001,samples=args.observer_samples)
    policy=train_policy(
        observer,
        seed=90002,
        episodes=args.train_episodes,
        recovery_steps=12,
    )
    snapshot=json.loads(json.dumps(policy.to_dict()))
    probe=SelfPolicy.from_dict(json.loads(json.dumps(snapshot)))

    initials=[]
    full_actions=[]
    full_vars=[]
    for episode in range(args.episodes):
        initial,actions,states=full_trajectory(observer,probe,episode=episode)
        initials.append(initial)
        full_actions.append(actions)
        full_vars.append(float(np.var(states)))

    rng=np.random.default_rng(90504)
    replay_rows=[]
    for episode in range(args.episodes):
        replay_vars=[]
        for _ in range(REPLAYS):
            p=derangement(rng,args.episodes)
            donor=int(p[episode])
            replay_vars.append(
                replay_variance(
                    observer,
                    initial=initials[episode],
                    actions=full_actions[donor],
                    seed=90010+episode,
                )
            )
        replay_rows.append(float(np.mean(replay_vars)))

    full=np.asarray(full_vars,dtype=float)
    replay=np.asarray(replay_rows,dtype=float)
    contrast=full-replay

    summary={
        "experiment":"tcf_consciousness_instantiation_c0_4",
        "protocol_version":PROTOCOL_VERSION,
        "episodes":args.episodes,
        "train_episodes":args.train_episodes,
        "observer_samples":args.observer_samples,
        "replays_per_episode":REPLAYS,
        "control":"information_matched_action_replay",
        "primary_output":"full_autonomous_variance_minus_replayed_action_variance",
        "semantic_input_during_probe":False,
        "external_retraining_during_probe":False,
        "policy_snapshot_shared_across_control":True,
        "phenomenal_consciousness_claimed":False,
        "full_autonomous_variance_mean":float(np.mean(full)),
        "matched_replay_variance_mean":float(np.mean(replay)),
        "contrast_mean":float(np.mean(contrast)),
        "contrast_p":float(sign_p(contrast,90604)),
        "interpretation_rule":(
            "C0.4 asks whether state-coupled action selection contributes autonomous "
            "state variance beyond replaying action sequences drawn from the same empirical "
            "action distribution; this is a computational feedback test, not a demonstration "
            "of phenomenal consciousness."
        ),
    }

    (out/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    (out/"policy_snapshot.json").write_text(json.dumps(snapshot,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps(summary,indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
