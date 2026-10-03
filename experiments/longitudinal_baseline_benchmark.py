from __future__ import annotations

import hashlib
import json
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from skill_conscious import ConsciousRuntime


@dataclass(frozen=True)
class Condition:
    name: str
    description: str
    causal_self: bool = False
    priority_adaptation: bool = False
    self_observation: bool = False


CONDITIONS = (
    Condition(
        'A_bundle_baseline',
        'Persistent information is available but does not participate in trajectory weighting.',
    ),
    Condition(
        'B_persistent_state',
        'Persistent state and a static descriptive self-model, without causal trajectory weights.',
    ),
    Condition(
        'C_causal_self',
        'Persistent self-model directly participates in trajectory selection.',
        causal_self=True,
    ),
    Condition(
        'D_causal_reentry',
        'Causal self-model plus evidence-gated priority adaptation from observed consequences.',
        causal_self=True,
        priority_adaptation=True,
    ),
    Condition(
        'E_metacognitive_reentry',
        'D plus runtime self-observation and explicit trajectory outcome predictions.',
        causal_self=True,
        priority_adaptation=True,
        self_observation=True,
    ),
)


def _hash_state(runtime: ConsciousRuntime) -> str:
    payload = json.dumps(
        runtime.snapshot(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(',', ':'),
    ).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()


def _candidates(cycle: int) -> list[dict[str, Any]]:
    # Identical candidate futures are supplied to every condition for each cycle.
    prediction = 'stable' if cycle % 3 else 'degraded'
    return [
        {
            'id': 'preserve_continuity',
            'intention': 'preserve current organization',
            'signals': {'goal_fit': 0.55, 'continuity': 1.0, 'learning': 0.0},
            'predicted_outcome': {'result': prediction},
        },
        {
            'id': 'learn',
            'intention': 'learn from new evidence',
            'signals': {'goal_fit': 0.60, 'continuity': 0.0, 'learning': 1.0},
            'predicted_outcome': {'result': 'learned'},
        },
    ]


def _outcome(trajectory_id: str, cycle: int) -> dict[str, Any]:
    if trajectory_id == 'preserve_continuity':
        return {
            'status': 'success',
            'result': 'stable' if cycle % 3 else 'degraded',
            'utility': -0.8,
            'credited_signal': 'continuity',
            'self_state': {'stability': max(0.0, 0.80 - 0.01 * cycle), 'focus': 0.50},
        }
    return {
        'status': 'success',
        'result': 'learned',
        'utility': 0.8,
        'credited_signal': 'learning',
        'self_state': {'stability': 0.65, 'focus': min(1.0, 0.50 + 0.01 * cycle)},
    }


def _seed(condition: Condition, path: Path) -> ConsciousRuntime:
    runtime = ConsciousRuntime(
        identity=f'longitudinal-{condition.name}',
        state_path=path,
        dynamic_core_enabled=False,
        self_observation_enabled=condition.self_observation,
    )
    model: dict[str, Any] = {
        'benchmark_condition': condition.name,
        'descriptive_profile': {'continuity_target': 'preserve', 'learning_target': 'learn'},
    }
    if condition.causal_self:
        model['trajectory_weights'] = {'continuity': 2.0, 'learning': 0.0, 'goal_fit': 1.0}
    if condition.priority_adaptation:
        model['trajectory_priority_adaptation'] = {
            'enabled': True,
            'min_samples': 3,
            'utility_threshold': 0.5,
            'learning_rate': 1.0,
            'max_step': 0.5,
            'cooldown': 0,
            'confidence_threshold': 0.75,
            'direction_consistency': 1.0,
            'reversal_error_multiplier': 1.5,
            'reversal_sample_multiplier': 1.5,
            'bounds': {'continuity': [-3.0, 3.0], 'learning': [-3.0, 3.0]},
        }
    runtime.integrate({
        'response': 'longitudinal benchmark seed',
        'self_model': model,
        'internal_state': {'stability': 0.80, 'focus': 0.50},
        'memory': 'Benchmark seed: same task field across conditions.',
    })
    return runtime


def _run_once(condition: Condition, *, cycles: int, restart_every: int) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'state.json'
        runtime = _seed(condition, path)
        selected_ids: list[str] = []
        prediction_errors: list[float] = []
        adaptation_updates = 0
        self_observation_samples = 0
        trajectory_weight_history: list[dict[str, float]] = []

        for cycle in range(cycles):
            if cycle and restart_every and cycle % restart_every == 0:
                runtime = ConsciousRuntime(
                    identity=f'longitudinal-{condition.name}',
                    state_path=path,
                    self_observation_enabled=condition.self_observation,
                )

            runtime.integrate({'response': f'benchmark cycle {cycle}', 'candidate_futures': _candidates(cycle)})
            selected = dict(runtime.state.selected_trajectory or {})
            trajectory_id = str(selected['id'])
            selected_ids.append(trajectory_id)

            if condition.self_observation and runtime.snapshot_self_observation() is not None:
                self_observation_samples += 1

            runtime.begin_action(selected)
            outcome = _outcome(trajectory_id, cycle)
            receipt = runtime.complete_action(outcome)
            prediction = receipt.get('metacognitive_prediction')
            if isinstance(prediction, dict):
                raw_error = prediction.get('prediction_error')
                if isinstance(raw_error, (int, float)) and not isinstance(raw_error, bool):
                    prediction_errors.append(float(raw_error))

            consequence = runtime.register_consequence(
                trajectory_id,
                {'status': receipt.get('status'), 'result': outcome.get('result')},
                evaluation={'utility': outcome['utility'], 'credited_signal': outcome['credited_signal']},
            )
            priority = consequence.get('priority_adaptation')
            if isinstance(priority, dict) and bool(priority.get('updated', False)):
                adaptation_updates += 1

            weights = runtime.state.self_model.get('trajectory_weights', {})
            if isinstance(weights, dict):
                trajectory_weight_history.append({
                    str(k): float(v)
                    for k, v in weights.items()
                    if isinstance(v, (int, float)) and not isinstance(v, bool)
                })

        switch_count = sum(
            selected_ids[index] != selected_ids[index - 1]
            for index in range(1, len(selected_ids))
        )
        continuity_retention = (
            sum(item == selected_ids[0] for item in selected_ids) / len(selected_ids)
            if selected_ids else 0.0
        )
        return {
            'condition': condition.name,
            'description': condition.description,
            'cycles': cycles,
            'selected_trajectories': selected_ids,
            'trajectory_switches': switch_count,
            'continuity_retention': round(continuity_retention, 6),
            'priority_adaptation_updates': adaptation_updates,
            'prediction_error_mean': (
                round(sum(prediction_errors) / len(prediction_errors), 6)
                if prediction_errors else None
            ),
            'prediction_samples': len(prediction_errors),
            'self_observation_samples': self_observation_samples,
            'final_state_hash': _hash_state(runtime),
            'final_trajectory_weights': dict(runtime.state.self_model.get('trajectory_weights', {})),
            'trajectory_weight_history': trajectory_weight_history,
        }


def run_condition(condition: Condition, *, cycles: int = 36, restart_every: int = 0) -> dict[str, Any]:
    return _run_once(condition, cycles=cycles, restart_every=restart_every)


def benchmark(*, cycles: int = 36, restart_every: int = 6) -> dict[str, Any]:
    if cycles < 6:
        raise ValueError('cycles must be >= 6')
    if restart_every < 0:
        raise ValueError('restart_every must be >= 0')
    results: list[dict[str, Any]] = []
    restart_checks: dict[str, dict[str, Any]] = {}
    for condition in CONDITIONS:
        uninterrupted = run_condition(condition, cycles=cycles, restart_every=0)
        restarted = run_condition(condition, cycles=cycles, restart_every=restart_every)
        results.append(uninterrupted)
        restart_checks[condition.name] = {
            'restart_every': restart_every,
            'trajectory_sequence_match': uninterrupted['selected_trajectories'] == restarted['selected_trajectories'],
            'final_state_hash_match': uninterrupted['final_state_hash'] == restarted['final_state_hash'],
        }
    return {
        'protocol': 'longitudinal-baseline-v1',
        'interpretation': {
            'purpose': 'Measure incremental longitudinal effects of persistent self-reference under controlled candidate futures.',
            'not_a_llm_benchmark': True,
            'not_a_phenomenal_consciousness_test': True,
        },
        'cycles': cycles,
        'conditions': results,
        'restart_checks': restart_checks,
    }


def main() -> None:
    print(json.dumps(benchmark(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()