from __future__ import annotations
import json
import os
import tempfile
import urllib.request
from pathlib import Path
from skill_conscious.core import ConsciousRuntime

API_URL = "https://api.deepseek.com/chat/completions"

def ask_model(snapshot):
    key = os.environ["DEEPSEEK_API_KEY"]
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Return compact JSON only. Do not claim subjective experience."},
            {"role": "user", "content": (
                "Inspect this persistent runtime state and propose one minimal self-model update. "
                "Keys: response, internal_state, self_model, intention.\n"
                + json.dumps(snapshot, ensure_ascii=False)
            )},
        ],
        "temperature": 0,
        "max_tokens": 120,
        "response_format": {"type": "json_object"},
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))
    return json.loads(data["choices"][0]["message"]["content"])

def select_with(runtime, continuity, learning):
    runtime.state.self_model = dict(runtime.state.self_model)
    weights = dict(runtime.state.self_model.get("trajectory_weights", {}))
    weights["continuity"] = continuity
    weights["learning"] = learning
    runtime.state.self_model["trajectory_weights"] = weights
    runtime.store.save(runtime.state)
    selected = runtime.select_trajectory(runtime.generate_candidate_futures())
    runtime.state.selected_trajectory = dict(selected)
    runtime.store.save(runtime.state)
    return selected

def main():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        seed = root / "seed.json"
        runtime = ConsciousRuntime(identity="deepseek-causal-ab", state_path=seed)
        runtime.state.self_state = {"stability": 0.5, "focus": 0.5}
        runtime.state.self_model = {
            "identity": "deepseek-causal-ab",
            "trajectory_weights": {"continuity": 1.0, "learning": 0.5},
        }
        runtime.state.intention = "Maintain continuity while learning from new evidence."
        runtime.store.save(runtime.state)

        frame = ask_model({
            "self_state": runtime.state.self_state,
            "self_model": runtime.state.self_model,
            "intention": runtime.state.intention,
            "revision": runtime.state.revision,
        })
        frame.setdefault("response", "causal seed")
        frame.setdefault("internal_state", runtime.state.self_state)
        frame.setdefault("self_model", runtime.state.self_model)
        frame.setdefault("intention", runtime.state.intention)
        runtime.integrate(frame)

        base = runtime.state.to_dict()
        a_path, b_path = root / "a.json", root / "b.json"
        text = json.dumps(base, ensure_ascii=False)
        a_path.write_text(text, encoding="utf-8")
        b_path.write_text(text, encoding="utf-8")

        a = ConsciousRuntime(identity="deepseek-causal-ab", state_path=a_path)
        b = ConsciousRuntime(identity="deepseek-causal-ab", state_path=b_path)
        selected_a = select_with(a, 3.0, 0.0)
        selected_b = select_with(b, 0.0, 3.0)

        restart_a = ConsciousRuntime(identity="deepseek-causal-ab", state_path=a_path)
        restart_b = ConsciousRuntime(identity="deepseek-causal-ab", state_path=b_path)

        print("MODEL_SEED")
        print(json.dumps(frame, ensure_ascii=False))
        print("A_CONTINUITY")
        print(json.dumps(selected_a, ensure_ascii=False))
        print("B_LEARNING")
        print(json.dumps(selected_b, ensure_ascii=False))
        print("RESTART_CHECK")
        print(json.dumps({
            "A_selected": restart_a.state.selected_trajectory,
            "A_weights": restart_a.state.self_model.get("trajectory_weights"),
            "B_selected": restart_b.state.selected_trajectory,
            "B_weights": restart_b.state.self_model.get("trajectory_weights"),
        }, ensure_ascii=False))

        assert selected_a["id"] != selected_b["id"]
        assert restart_a.state.selected_trajectory["id"] == selected_a["id"]
        assert restart_b.state.selected_trajectory["id"] == selected_b["id"]
        print("CAUSAL_AB_PASS")

if __name__ == "__main__":
    main()
