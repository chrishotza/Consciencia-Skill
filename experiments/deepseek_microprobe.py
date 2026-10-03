from __future__ import annotations
import json
import os
import urllib.request
from pathlib import Path
from skill_conscious.core import ConsciousRuntime

API_URL = "https://api.deepseek.com/chat/completions"
STATE_PATH = Path("data/deepseek_microprobe.json")

def call_deepseek(prompt: str) -> str:
    key = os.environ["DEEPSEEK_API_KEY"]
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": (
                "You are an experimental cognitive module inside Skill-Conscious. "
                "Do not claim phenomenal consciousness. Work only from supplied persistent "
                "state. Return one compact JSON object with keys: response, internal_state, "
                "self_model, intention, memory. Keep values concise."
            )},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "max_tokens": 220,
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
    return data["choices"][0]["message"]["content"].strip()

def compact_state(runtime: ConsciousRuntime) -> dict:
    state = runtime.snapshot()
    return {
        "identity": state["identity"],
        "revision": state["revision"],
        "self_state": state["self_state"],
        "self_model": state["self_model"],
        "intention": state["intention"],
        "memories": state["memories"][-2:],
        "regime": state["regime"],
        "selected_trajectory": state["selected_trajectory"],
        "latent_patterns": state["latent_patterns"],
        "self_dissonance": state["self_dissonance"],
        "coherence": state["coherence"],
    }

def run_cycle(runtime: ConsciousRuntime, observation: str) -> dict:
    prompt = (
        f"Observation: {observation}\n"
        f"Persistent state before cycle:\n{json.dumps(compact_state(runtime), ensure_ascii=False)}\n"
        "Use the persistent state causally. Update the self-model only when supported."
    )
    frame = json.loads(call_deepseek(prompt))
    response = runtime.integrate(frame)
    result = compact_state(runtime)
    result["response"] = response
    return result

def main() -> None:
    STATE_PATH.unlink(missing_ok=True)
    runtime = ConsciousRuntime(identity="deepseek-microprobe", state_path=STATE_PATH)
    tests = [
        ("T1 identity", "A new cycle begins. Describe what is present and what you intend to preserve."),
        ("T2 persistence", "No new external facts. Inspect the prior cycle and report what remains continuous."),
    ]
    for title, observation in tests:
        print(title)
        print(json.dumps(run_cycle(runtime, observation), ensure_ascii=False))
    runtime.state.self_state = {"stability": 0.2, "focus": 0.3}
    runtime.state.self_model["expected_self_state"] = {"stability": 0.8, "focus": 0.7}
    runtime.store.save(runtime.state)
    print("T3 self-dissonance")
    print(json.dumps(run_cycle(runtime, "Current state diverges from the expected self-state. Decide the next trajectory."), ensure_ascii=False))
    runtime.state.self_state = {"stability": 0.8, "focus": 0.7}
    runtime.store.save(runtime.state)
    run_cycle(runtime, "This internal configuration recurs.")
    runtime.state.self_state = {"stability": 0.2, "focus": 0.3}
    runtime.store.save(runtime.state)
    print("T4 latent recurrence")
    print(json.dumps(run_cycle(runtime, "The current internal configuration resembles an earlier one. Determine whether the recurrence matters."), ensure_ascii=False))
    print("FINAL")
    print(json.dumps(compact_state(runtime), ensure_ascii=False))

if __name__ == "__main__":
    main()
