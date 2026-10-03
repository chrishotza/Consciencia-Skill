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

def ask_outcome(snapshot, outcome):
    key = os.environ['DEEPSEEK_API_KEY']
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Return compact JSON only. Do not claim subjective experience. Keys: response, internal_state, self_model, intention."},
            {"role": "user", "content": "A prior trajectory was selected. Observe its consequence and revise the self-model only when supported.\nOUTCOME=" + json.dumps(outcome, ensure_ascii=False) + "\nSTATE=" + json.dumps(snapshot, ensure_ascii=False)},
        ],
        "temperature": 0,
        "max_tokens": 100,
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
                return {'stability': 0.2, 'focus': 0.0, 'source': 'selected_trajectory'}
            if trajectory_id == 'learn':
                return {'stability': 0.0, 'focus': 0.2, 'source': 'selected_trajectory'}
            return {'stability': -0.1, 'focus': 0.1, 'source': 'selected_trajectory'}

        actual_path = root / 'actual.json'
        counter_path = root / 'counter.json'
        actual = ConsciousRuntime(identity='deepseek-causal-loop', state_path=actual_path)
        counter = ConsciousRuntime(identity='deepseek-causal-loop', state_path=counter_path)
        actual.state = ConsciousRuntime.from_dict(base) if hasattr(ConsciousRuntime, 'from_dict') else actual.state
        counter.state = ConsciousRuntime.from_dict(base) if hasattr(ConsciousRuntime, 'from_dict') else counter.state
        actual.store.save(actual.state)
        counter.store.save(counter.state)
        selected_id = runtime.state.selected_trajectory['id']
        candidates = [c for c in runtime.generate_candidate_futures() if c['id'] != selected_id]
        alternative_id = candidates[0]['id'] if candidates else 'learn'
        actual_outcome = consequence_for(selected_id)
        counter_outcome = consequence_for(alternative_id)
        for branch, outcome in ((actual, actual_outcome), (counter, counter_outcome)):
            branch.state.self_state = {'stability': max(0.0, min(1.0, 0.5 + outcome['stability'])), 'focus': max(0.0, min(1.0, 0.5 + outcome['focus']))}
            branch.state.workspace = {'last_action': branch.state.selected_trajectory['id'], 'last_outcome': outcome}
            branch.store.save(branch.state)
        actual_frame = ask_outcome({'self_state': actual.state.self_state, 'self_model': actual.state.self_model, 'selected_trajectory': actual.state.selected_trajectory, 'revision': actual.state.revision}, actual_outcome)
        counter_frame = ask_outcome({'self_state': counter.state.self_state, 'self_model': counter.state.self_model, 'selected_trajectory': counter.state.selected_trajectory, 'revision': counter.state.revision}, counter_outcome)
        for branch, frame2 in ((actual, actual_frame), (counter, counter_frame)):
            frame2.setdefault('response', 'outcome observed')
            frame2.setdefault('internal_state', branch.state.self_state)
            frame2.setdefault('self_model', branch.state.self_model)
            frame2.setdefault('intention', branch.state.intention)
            branch.integrate(frame2)
        print('CONSEQUENCE_LOOP')
        print(json.dumps({'selected': selected_id, 'counterfactual': alternative_id, 'actual_outcome': actual_outcome, 'counterfactual_outcome': counter_outcome, 'actual_model': actual.state.self_model, 'counter_model': counter.state.self_model, 'model_diverged': actual.state.self_model != counter.state.self_model}, ensure_ascii=False))
        print('CONSEQUENCE_MODEL_DIVERGENCE', actual.state.self_model != counter.state.self_model)

if __name__ == '__main__':
    main()