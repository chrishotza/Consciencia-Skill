from __future__ import annotations
import json
import os
import tempfile
import urllib.request
from pathlib import Path
from skill_conscious.core import ConsciousRuntime

API_URL = "https://api.deepseek.com/chat/completions"

def ask_model(snapshot):
    key = os.environ['DEEPSEEK_API_KEY']
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Return compact JSON only. Do not claim subjective experience."},
            {"role": "user", "content": "Inspect this persistent runtime state and propose one minimal self-model update. Keys: response, internal_state, self_model, intention.\n" + json.dumps(snapshot, ensure_ascii=False)},
        ],
        "temperature": 0,
        "max_tokens": 120,
        "response_format": {"type": "json_object"},
    }
    request = urllib.request.Request(API_URL, data=json.dumps(payload).encode('utf-8'), headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.loads(response.read().decode('utf-8'))
    return json.loads(data["choices"][0]["message"]["content"])

def select_with(runtime, continuity, learning):
    runtime.state.self_model = dict(runtime.state.self_model)
    weights = dict(runtime.state.self_model.get('trajectory_weights', {}))
    weights['continuity'] = continuity
    weights['learning'] = learning
    runtime.state.self_model['trajectory_weights'] = weights
    runtime.store.save(runtime.state)
    selected = runtime.select_trajectory(runtime.generate_candidate_futures())
    runtime.state.selected_trajectory = dict(selected)
    runtime.store.save(runtime.state)
    return selected

def main():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        seed = root / 'seed.json'
        runtime = ConsciousRuntime(identity='deepseek-causal-ab', state_path=seed)
        runtime.state.self_state = {'stability': 0.5, 'focus': 0.5}
        runtime.state.self_model = {'identity': 'deepseek-causal-ab', 'trajectory_weights': {'continuity': 1.0, 'learning': 0.5}}
        runtime.state.intention = 'Maintain continuity while learning from new evidence.'
        runtime.store.save(runtime.state)

        frame = ask_model({'self_state': runtime.state.self_state, 'self_model': runtime.state.self_model, 'intention': runtime.state.intention, 'revision': runtime.state.revision})
        frame.setdefault('response', 'causal seed')
        frame.setdefault('internal_state', runtime.state.self_state)
        frame.setdefault('self_model', runtime.state.self_model)
        frame.setdefault('intention', runtime.state.intention)
        runtime.integrate(frame)

        base = runtime.state.to_dict()
        a_path, b_path = root / 'a.json', root / 'b.json'
        text = json.dumps(base, ensure_ascii=False)
        a_path.write_text(text, encoding='utf-8')
        b_path.write_text(text, encoding='utf-8')
        a = ConsciousRuntime(identity='deepseek-causal-ab', state_path=a_path)
        b = ConsciousRuntime(identity='deepseek-causal-ab', state_path=b_path)
        selected_a = select_with(a, 3.0, 0.0)
        selected_b = select_with(b, 0.0, 3.0)
        restart_a = ConsciousRuntime(identity='deepseek-causal-ab', state_path=a_path)
        restart_b = ConsciousRuntime(identity='deepseek-causal-ab', state_path=b_path)

        print('MODEL_SEED')
        print(json.dumps(frame, ensure_ascii=False))
        print('A_CONTINUITY')
        print(json.dumps(selected_a, ensure_ascii=False))
        print('B_LEARNING')
        print(json.dumps(selected_b, ensure_ascii=False))
        print('RESTART_CHECK')
        print(json.dumps({'A_selected': restart_a.state.selected_trajectory, 'A_weights': restart_a.state.self_model.get('trajectory_weights'), 'B_selected': restart_b.state.selected_trajectory, 'B_weights': restart_b.state.self_model.get('trajectory_weights')}, ensure_ascii=False))
        assert selected_a['id'] != selected_b['id']
        assert restart_a.state.selected_trajectory['id'] == selected_a['id']
        assert restart_b.state.selected_trajectory['id'] == selected_b['id']
        print('CAUSAL_AB_PASS')

        def consequence_for(trajectory_id):
            if trajectory_id == 'preserve_continuity':
                return {'stability': -0.2, 'focus': 0.0, 'source': 'selected_trajectory'}
            if trajectory_id == 'learn':
                return {'stability': 0.0, 'focus': 0.2, 'source': 'selected_trajectory'}
            return {'stability': -0.1, 'focus': 0.1, 'source': 'selected_trajectory'}

        def self_evaluate(trajectory_id, outcome):
            # Explicit external evaluation rule: consequence value is a weighted
            # combination of observed stability/focus. This is not a claim about
            # subjective feeling; it is an operational learning signal.
            stability = float(outcome.get('stability', 0.0))
            focus = float(outcome.get('focus', 0.0))
            utility = round((0.7 * stability) + (0.3 * focus), 6)
            signal = {
                'preserve_continuity': 'continuity',
                'learn': 'learning',
                'explore': 'learning',
                'integrate_latent_pattern': 'learning',
            }.get(trajectory_id, 'learning')
            return {'trajectory': trajectory_id, 'utility': utility, 'credited_signal': signal}

        def apply_consequence_feedback(runtime, evaluation):
            model = dict(runtime.state.self_model)
            feedback = dict(model.get('trajectory_feedback', {}))
            prior = feedback.get(evaluation['trajectory'], {})
            prior_utility = prior.get('utility', 0.0) if isinstance(prior, dict) else 0.0
            prior_count = prior.get('count', 0) if isinstance(prior, dict) else 0
            if not isinstance(prior_utility, (int, float)) or isinstance(prior_utility, bool):
                prior_utility = 0.0
            if not isinstance(prior_count, int) or isinstance(prior_count, bool):
                prior_count = 0

            # Bounded exponential update: consequence -> self-evaluation ->
            # persistent self-model revision.
            rate = 0.5
            updated_utility = round(
                float(prior_utility) + rate * (float(evaluation['utility']) - float(prior_utility)),
                6,
            )
            feedback[evaluation['trajectory']] = {
                'utility': updated_utility,
                'count': prior_count + 1,
                'credited_signal': evaluation['credited_signal'],
            }

            weights = dict(model.get('trajectory_weights', {}))
            old_weight = weights.get(evaluation['credited_signal'], 0.0)
            if not isinstance(old_weight, (int, float)) or isinstance(old_weight, bool):
                old_weight = 0.0

            # The learned consequence value is allowed to make a small,
            # persistent change to the same preference dimension.
            weights[evaluation['credited_signal']] = round(
                max(-3.0, min(3.0, float(old_weight) + 0.5 * updated_utility)),
                6,
            )

            model['trajectory_feedback'] = feedback
            model['trajectory_weights'] = weights
            model['last_consequence_feedback'] = {
                'revision': runtime.state.revision + 1,
                'trajectory': evaluation['trajectory'],
                'utility': evaluation['utility'],
                'credited_signal': evaluation['credited_signal'],
            }
            runtime.state.self_model = model
            runtime.state.workspace = {
                **runtime.state.workspace,
                'last_action': evaluation['trajectory'],
                'last_outcome': evaluation,
            }
            runtime.store.save(runtime.state)
            return model

        actual_path = root / 'actual.json'
        counter_path = root / 'counter.json'
        actual_path.write_text(text, encoding='utf-8')
        counter_path.write_text(text, encoding='utf-8')
        actual = ConsciousRuntime(identity='deepseek-causal-ab', state_path=actual_path)
        counter = ConsciousRuntime(identity='deepseek-causal-ab', state_path=counter_path)

        selected_id = runtime.state.selected_trajectory['id']
        candidates = runtime.generate_candidate_futures()
        alternative = next((c for c in candidates if c['id'] != selected_id), None)
        if alternative is None:
            raise AssertionError('expected a counterfactual trajectory')
        alternative_id = alternative['id']

        actual.state.selected_trajectory = dict(
            next(c for c in candidates if c['id'] == selected_id)
        )
        counter.state.selected_trajectory = dict(alternative)
        actual.store.save(actual.state)
        counter.store.save(counter.state)

        actual_outcome = consequence_for(selected_id)
        counter_outcome = consequence_for(alternative_id)
        actual_eval = self_evaluate(selected_id, actual_outcome)
        counter_eval = self_evaluate(alternative_id, counter_outcome)

        apply_consequence_feedback(actual, actual_eval)
        apply_consequence_feedback(counter, counter_eval)

        actual_restart = ConsciousRuntime(identity='deepseek-causal-ab', state_path=actual_path)
        counter_restart = ConsciousRuntime(identity='deepseek-causal-ab', state_path=counter_path)

        actual_feedback = actual_restart.state.self_model.get('trajectory_feedback', {})
        counter_feedback = counter_restart.state.self_model.get('trajectory_feedback', {})
        actual_weights = actual_restart.state.self_model.get('trajectory_weights', {})
        counter_weights = counter_restart.state.self_model.get('trajectory_weights', {})

        substantive_divergence = (
            actual_feedback != counter_feedback
            and actual_weights != counter_weights
        )

        print('CONSEQUENCE_LOOP')
        print(json.dumps({
            'selected': selected_id,
            'counterfactual': alternative_id,
            'actual_outcome': actual_outcome,
            'counterfactual_outcome': counter_outcome,
            'actual_evaluation': actual_eval,
            'counterfactual_evaluation': counter_eval,
            'actual_feedback': actual_feedback,
            'counter_feedback': counter_feedback,
            'actual_weights': actual_weights,
            'counter_weights': counter_weights,
            'restart_persisted': (
                actual_restart.state.self_model.get('trajectory_feedback') == actual_feedback
                and counter_restart.state.self_model.get('trajectory_feedback') == counter_feedback
            ),
            'substantive_model_divergence': substantive_divergence,
        }, ensure_ascii=False))

        assert substantive_divergence
        assert (
            actual_restart.state.self_model.get('last_consequence_feedback', {}).get('trajectory')
            == selected_id
        )
        assert (
            counter_restart.state.self_model.get('last_consequence_feedback', {}).get('trajectory')
            == alternative_id
        )
        print('CONSEQUENCE_LOOP_PASS')

if __name__ == '__main__':
    main()