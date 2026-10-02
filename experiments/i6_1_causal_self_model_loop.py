from __future__ import annotations

import argparse
import copy
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from src.ontto.bridge import DynamicStateBridge
from src.ontto.dynamics import Config
from src.ontto.self_observer import SelfObserver
from src.ontto.trajectory_selector import TrajectorySelector

SEED = 20261027
REPLICATES = 24
WARMUP_CYCLES = 24
EVALUATION_CYCLES = 48
PERMUTATIONS = 20_000
SIGNALS = (-1.0, 0.0, 1.0)

@dataclass
class LoopState:
    previous_state: float = 0.0
    state: float = 0.0
    memory: float = 0.0
    pressure: float = 0.0
    attractor_distance: float = 0.0
    last_input: float = 0.0
    steps: int = 0

def advance(state, bridge, signal, steps=1):
    snapshot = bridge.advance(
        previous_state=state.previous_state,
        state=state.state,
        memory=state.memory,
        pressure=state.pressure,
        signal=signal,
        steps=steps,
        step_index=state.steps,
    )
    next_state = LoopState(
        previous_state=snapshot.previous_state,
        state=snapshot.state,
        memory=snapshot.memory,
        pressure=snapshot.pressure,
        attractor_distance=snapshot.attractor_distance,
        last_input=snapshot.last_input,
        steps=snapshot.steps,
    )
    return next_state, snapshot.to_dict()

def simulate_candidate(state, bridge, signal, steps):
    candidate_bridge = DynamicStateBridge(Config(**bridge.cfg.__dict__), seed=bridge.seed)
    next_state, _ = advance(state, candidate_bridge, signal, steps=steps)
    return float(next_state.attractor_distance)

def train_shared_self_observer(*, bridge, state, observer, warmup_cycles):
    warmup_signals = [SIGNALS[i % len(SIGNALS)] for i in range(warmup_cycles)]
    for signal in warmup_signals:
        features = SelfObserver.features_for(
            previous_state=state.previous_state,
            state=state.state,
            memory=state.memory,
            pressure=state.pressure,
            last_input=signal,
            attractor_distance=state.attractor_distance,
            steps_delta=1,
        )
        state, snapshot = advance(state, bridge, signal, steps=1)
        observer.observe(features=features, actual_state=float(snapshot['state']))
    return state

def choose_intact(observer, state, selector):
    candidates = selector.evaluate(
        observer,
        current_state=state.state,
        current_memory=state.memory,
        current_pressure=state.pressure,
        current_input=state.last_input,
        current_attractor=0.0,
        steps_delta=1,
        signals=SIGNALS,
    )
    chosen = selector.choose(candidates)
    return float(chosen.signal), float(chosen.prediction.predicted_state)

def choose_prediction_lesion(state, selector):
    class BaselineObserver:
        def predict(self, **kwargs):
            from src.ontto.self_observer import SelfPrediction
            current_state = float(kwargs['state'])
            return SelfPrediction(
                predicted_state=current_state,
                baseline_state=current_state,
                confidence=1.0,
                samples=0,
            )

    candidates = selector.evaluate(
        BaselineObserver(),
        current_state=state.state,
        current_memory=state.memory,
        current_pressure=state.pressure,
        current_input=state.last_input,
        current_attractor=0.0,
        steps_delta=1,
        signals=SIGNALS,
    )
    chosen = selector.choose(candidates)
    return float(chosen.signal), float(chosen.prediction.predicted_state)

def sign_flip_test(values, seed, permutations):
    values = np.asarray(values, dtype=float)
    observed = float(values.mean())
    rng = np.random.default_rng(seed)
    signs = rng.choice((-1.0, 1.0), size=(permutations, values.size))
    null = (signs * values[None, :]).mean(axis=1)
    p_value = float((np.count_nonzero(np.abs(null) >= abs(observed)) + 1) / (permutations + 1))
    return {'observed_mean': observed, 'permutation_p': p_value, 'permutations': permutations}

def run_replicate(*, seed, warmup_cycles, evaluation_cycles):
    cfg = Config()
    warmup_bridge = DynamicStateBridge(cfg, seed=seed)
    warmup_state = LoopState(attractor_distance=abs(cfg.attractor))
    observer = SelfObserver(ridge=1e-3, max_samples=2048)
    warmup_state = train_shared_self_observer(
        bridge=warmup_bridge, state=warmup_state, observer=observer, warmup_cycles=warmup_cycles
    )

    intact_state = copy.deepcopy(warmup_state)
    prediction_lesion_state = copy.deepcopy(warmup_state)
    frozen_update_state = copy.deepcopy(warmup_state)
    intact_observer = SelfObserver.from_dict(observer.to_dict())
    frozen_observer = SelfObserver.from_dict(observer.to_dict())

    intact_bridge = DynamicStateBridge(cfg, seed=seed)
    prediction_lesion_bridge = DynamicStateBridge(cfg, seed=seed)
    frozen_update_bridge = DynamicStateBridge(cfg, seed=seed)
    selector = TrajectorySelector(attractor_weight=0.70, coherence_weight=0.30, meta_error_weight=0.0)

    regret = {'intact': [], 'prediction_lesion': [], 'frozen_update': []}
    matched_choice_diff = {'prediction_lesion': [], 'frozen_update': []}
    choices = {'intact': [], 'prediction_lesion': [], 'frozen_update': []}

    for _ in range(evaluation_cycles):
        intact_choice, _ = choose_intact(intact_observer, intact_state, selector)
        frozen_choice, _ = choose_intact(frozen_observer, intact_state, selector)
        lesion_choice, _ = choose_prediction_lesion(intact_state, selector)

        matched_choice_diff['prediction_lesion'].append(float(intact_choice != lesion_choice))
        matched_choice_diff['frozen_update'].append(float(intact_choice != frozen_choice))

        condition_inputs = [
            ('intact', intact_state, intact_bridge, intact_observer, intact_choice, True),
            ('prediction_lesion', prediction_lesion_state, prediction_lesion_bridge, intact_observer, lesion_choice, True),
            ('frozen_update', frozen_update_state, frozen_update_bridge, frozen_observer, frozen_choice, False),
        ]
        next_states = {}

        for name, state, bridge, observer_for_prediction, chosen_signal, update in condition_inputs:
            candidates = {float(signal): simulate_candidate(state, bridge, float(signal), steps=1) for signal in SIGNALS}
            regret[name].append(float(candidates[float(chosen_signal)] - min(candidates.values())))

            features = SelfObserver.features_for(
                previous_state=state.previous_state,
                state=state.state,
                memory=state.memory,
                pressure=state.pressure,
                last_input=float(chosen_signal),
                attractor_distance=state.attractor_distance,
                steps_delta=1,
            )
            prediction = observer_for_prediction.predict(
                previous_state=state.previous_state,
                state=state.state,
                memory=state.memory,
                pressure=state.pressure,
                last_input=float(chosen_signal),
                attractor_distance=state.attractor_distance,
                steps_delta=1,
            )
            next_state, snapshot = advance(state, bridge, float(chosen_signal), steps=1)
            actual = float(snapshot['state'])
            if update and name == 'intact':
                intact_observer.observe(features=features, actual_state=actual)
            next_states[name] = next_state
            choices[name].append(float(chosen_signal))

        intact_state = next_states['intact']
        prediction_lesion_state = next_states['prediction_lesion']
        frozen_update_state = next_states['frozen_update']

    intact_regret = np.asarray(regret['intact'], dtype=float)
    prediction_lesion_regret = np.asarray(regret['prediction_lesion'], dtype=float)
    frozen_update_regret = np.asarray(regret['frozen_update'], dtype=float)

    return {
        'intact_regret_mean': float(intact_regret.mean()),
        'prediction_lesion_regret_mean': float(prediction_lesion_regret.mean()),
        'frozen_update_regret_mean': float(frozen_update_regret.mean()),
        'intact_minus_prediction_lesion_regret': float(intact_regret.mean() - prediction_lesion_regret.mean()),
        'intact_minus_frozen_update_regret': float(intact_regret.mean() - frozen_update_regret.mean()),
        'prediction_lesion_choice_dependence_rate': float(np.mean(matched_choice_diff['prediction_lesion'])),
        'frozen_update_choice_dependence_rate': float(np.mean(matched_choice_diff['frozen_update'])),
        'intact_nonzero_action_rate': float(np.mean(np.abs(np.asarray(choices['intact'])) > 0)),
        'prediction_lesion_nonzero_action_rate': float(np.mean(np.abs(np.asarray(choices['prediction_lesion'])) > 0)),
        'frozen_update_nonzero_action_rate': float(np.mean(np.abs(np.asarray(choices['frozen_update'])) > 0)),
        'final_intact_attractor_distance': float(intact_state.attractor_distance),
        'final_prediction_lesion_attractor_distance': float(prediction_lesion_state.attractor_distance),
        'final_frozen_update_attractor_distance': float(frozen_update_state.attractor_distance),
    }

def run(*, seed, replicates, warmup_cycles, evaluation_cycles, permutations, out):
    if replicates != REPLICATES: raise ValueError(f'I6.1 replicates are frozen at {REPLICATES}')
    if warmup_cycles != WARMUP_CYCLES: raise ValueError(f'I6.1 warmup is frozen at {WARMUP_CYCLES}')
    if evaluation_cycles != EVALUATION_CYCLES: raise ValueError(f'I6.1 evaluation is frozen at {EVALUATION_CYCLES}')
    if permutations != PERMUTATIONS: raise ValueError(f'I6.1 uses {PERMUTATIONS} permutations')

    per_rep = [run_replicate(seed=seed + rep, warmup_cycles=warmup_cycles, evaluation_cycles=evaluation_cycles) for rep in range(replicates)]
    primary = np.asarray([row['intact_minus_prediction_lesion_regret'] for row in per_rep], dtype=float)
    frozen = np.asarray([row['intact_minus_frozen_update_regret'] for row in per_rep], dtype=float)

    result = {
        'experiment': 'i6_1_causal_self_model_loop',
        'seed': seed, 'replicates': replicates, 'warmup_cycles': warmup_cycles,
        'evaluation_cycles': evaluation_cycles, 'signals': list(SIGNALS), 'permutations': permutations,
        'conditions': {
            'intact': 'self-model predicts and trajectory selection uses those predictions; self-model updates after each actual transition',
            'prediction_lesion': 'same inputs and information, but selection uses a baseline current-state prediction while the self-model continues learning',
            'frozen_update': 'selection uses the learned self-model, but the model is frozen during evaluation',
        },
        'primary_endpoint': 'counterfactual regret difference: intact regret minus prediction-lesion regret',
        'primary': sign_flip_test(primary, seed + 1000, permutations),
        'secondary_frozen_update': sign_flip_test(frozen, seed + 2000, permutations),
        'aggregate': {
            'choice_dependence_prediction_lesion_rate': float(np.mean([row['prediction_lesion_choice_dependence_rate'] for row in per_rep])),
            'choice_dependence_frozen_update_rate': float(np.mean([row['frozen_update_choice_dependence_rate'] for row in per_rep])),
            'intact_regret_mean': float(np.mean([row['intact_regret_mean'] for row in per_rep])),
            'prediction_lesion_regret_mean': float(np.mean([row['prediction_lesion_regret_mean'] for row in per_rep])),
            'frozen_update_regret_mean': float(np.mean([row['frozen_update_regret_mean'] for row in per_rep])),
        },
        'boundary': 'I6.1 tests causal necessity of self-model use in trajectory selection within a deterministic computational organism. It does not establish consciousness or subjective experience.',
        'per_replicate': per_rep,
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / 'summary.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--seed',type=int,default=SEED)
    parser.add_argument('--replicates',type=int,default=REPLICATES)
    parser.add_argument('--warmup',type=int,default=WARMUP_CYCLES)
    parser.add_argument('--evaluation-cycles',type=int,default=EVALUATION_CYCLES)
    parser.add_argument('--permutations',type=int,default=PERMUTATIONS)
    parser.add_argument('--out',default='results/i6_1_causal_self_model_loop')
    args=parser.parse_args()
    print(json.dumps(run(seed=args.seed,replicates=args.replicates,warmup_cycles=args.warmup,evaluation_cycles=args.evaluation_cycles,permutations=args.permutations,out=Path(args.out)),indent=2,ensure_ascii=False))

if __name__=='__main__': main()