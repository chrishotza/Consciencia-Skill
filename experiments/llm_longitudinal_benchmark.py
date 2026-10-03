from __future__ import annotations

import argparse
import json
import os
import tempfile
import urllib.request
from pathlib import Path
from typing import Any

from skill_conscious import ConsciousRuntime
from skill_conscious.llm_adapter import ProviderNeutralLLMAdapter
from experiments.longitudinal_baseline_benchmark import CONDITIONS, _candidates, _outcome, _seed


class DeterministicProvider:
    """Stable provider used by CI to verify the external-model boundary."""

    def __call__(self, prompt: str) -> dict[str, Any]:
        return {
            "response": "deterministic external model frame",
            "workspace": {"prompt_length": len(prompt)},
        }


class OpenAICompatibleProvider:
    """Minimal stdlib-only adapter for OpenAI-compatible JSON chat endpoints."""

    def __init__(self, *, url: str, api_key: str, model: str) -> None:
        self.url = url
        self.api_key = api_key
        self.model = model

    def __call__(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Return a JSON object with a concise string field "
                        "'response'. Do not write runtime-owned fields."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        }
        request = urllib.request.Request(
            self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
        try:
            return str(data["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError("OpenAI-compatible endpoint returned an invalid response") from exc




class SelfModelPolicyProvider:
    """Deterministic providers that differ only in their self-model policy."""

    def __init__(self, *, continuity: float, learning: float) -> None:
        self.continuity = float(continuity)
        self.learning = float(learning)

    def __call__(self, _prompt: str) -> dict[str, Any]:
        return {
            "response": "causal policy frame",
            "self_model": {
                "trajectory_weights": {
                    "goal_fit": 1.0,
                    "continuity": self.continuity,
                    "learning": self.learning,
                }
            },
        }


def run_causal_provider_ab(*, cycles: int = 8) -> dict[str, Any]:
    condition = CONDITIONS[2]
    policies = {
        "continuity_policy": SelfModelPolicyProvider(continuity=3.0, learning=0.0),
        "learning_policy": SelfModelPolicyProvider(continuity=0.0, learning=3.0),
    }

    branches: dict[str, dict[str, Any]] = {}
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name, provider in policies.items():
            path = root / f"{name}.json"
            runtime = _seed(condition, path)
            selected_ids: list[str] = []

            for cycle in range(cycles):
                candidates = _candidates(cycle)
                adapter = ProviderNeutralLLMAdapter(
                    provider,
                    fixed_candidate_futures=candidates,
                )
                frame = adapter(
                    runtime.prepare(
                        f"causal A/B cycle {cycle}",
                        candidate_futures=candidates,
                    )
                )
                runtime.integrate(frame)
                selected = dict(runtime.state.selected_trajectory or {})
                selected_ids.append(str(selected["id"]))

                runtime.begin_action(selected, persist=False)
                outcome = _outcome(str(selected["id"]), cycle)
                runtime.complete_action(outcome, persist=False)

                evaluation = adapter(
                    runtime.prepare_consequence(
                        str(selected["id"]),
                        outcome,
                        candidate_futures=candidates,
                    )
                )
                evaluation["consequence_trajectory"] = str(selected["id"])
                evaluation["consequence"] = dict(outcome)
                runtime.integrate(evaluation)
                runtime.store.save(runtime.state)

            branches[name] = {
                "selected_trajectories": selected_ids,
                "trajectory_switches": sum(
                    selected_ids[i] != selected_ids[i - 1]
                    for i in range(1, len(selected_ids))
                ),
                "final_state_hash": __import__("hashlib").sha256(
                    json.dumps(
                        runtime.snapshot(),
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    ).encode("utf-8")
                ).hexdigest(),
                "final_trajectory_weights": dict(
                    runtime.state.self_model.get("trajectory_weights", {})
                ),
            }

    a = branches["continuity_policy"]["selected_trajectories"]
    b = branches["learning_policy"]["selected_trajectories"]
    divergence_cycles = [
        index
        for index, (left, right) in enumerate(zip(a, b))
        if left != right
    ]

    return {
        "protocol": "llm-causal-ab-v1",
        "same_initial_runtime": True,
        "same_candidate_field": True,
        "same_outcome_rule": True,
        "causal_variable": "provider-authored self_model.trajectory_weights",
        "branches": branches,
        "selection_diverged": bool(divergence_cycles),
        "divergence_cycles": divergence_cycles,
        "not_a_phenomenal_consciousness_test": True,
    }

def completion_from_environment() -> Any:
    provider = os.getenv("SKILL_CONSCIOUS_LLM_PROVIDER", "deterministic").strip().lower()
    if provider == "deterministic":
        return DeterministicProvider()
    if provider != "openai_compatible":
        raise ValueError("SKILL_CONSCIOUS_LLM_PROVIDER must be deterministic or openai_compatible")

    url = os.getenv("SKILL_CONSCIOUS_LLM_URL", "").strip()
    api_key = os.getenv("SKILL_CONSCIOUS_LLM_API_KEY", "").strip()
    model = os.getenv("SKILL_CONSCIOUS_LLM_MODEL", "").strip()
    if not url or not api_key or not model:
        raise ValueError(
            "openai_compatible requires SKILL_CONSCIOUS_LLM_URL, "
            "SKILL_CONSCIOUS_LLM_API_KEY, and SKILL_CONSCIOUS_LLM_MODEL"
        )
    return OpenAICompatibleProvider(url=url, api_key=api_key, model=model)


def run_condition_with_llm(
    condition,
    completion,
    *,
    cycles: int = 8,
    restart_every: int = 4,
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "state.json"
        runtime = _seed(condition, path)
        selected_ids: list[str] = []
        prediction_errors: list[float] = []
        self_observation_samples = 0
        adaptation_updates = 0

        for cycle in range(cycles):
            if cycle and restart_every and cycle % restart_every == 0:
                runtime = ConsciousRuntime(
                    identity=f"longitudinal-{condition.name}",
                    state_path=path,
                    self_observation_enabled=condition.self_observation,
                )

            # Candidate futures are controlled by the harness, not by the model.
            candidates = _candidates(cycle)
            adapter = ProviderNeutralLLMAdapter(
                completion,
                fixed_candidate_futures=candidates,
            )
            frame = adapter(
                runtime.prepare(
                    f"LLM longitudinal cycle {cycle}",
                    candidate_futures=candidates,
                )
            )
            runtime.integrate(frame)
            selected = dict(runtime.state.selected_trajectory or {})
            trajectory_id = str(selected["id"])
            selected_ids.append(trajectory_id)

            runtime.begin_action(selected, persist=False)
            outcome = _outcome(trajectory_id, cycle)
            receipt = runtime.complete_action(outcome, persist=False)

            if condition.self_observation and isinstance(
                receipt.get("self_observation"), dict
            ):
                self_observation_samples += 1

            prediction = receipt.get("metacognitive_prediction")
            if isinstance(prediction, dict):
                error = prediction.get("prediction_error")
                if isinstance(error, (int, float)) and not isinstance(error, bool):
                    prediction_errors.append(float(error))

            # Real host consequence re-entry through the same provider boundary.
            consequence_prompt = runtime.prepare_consequence(
                trajectory_id,
                outcome,
                candidate_futures=candidates,
            )
            evaluation = adapter(consequence_prompt)
            evaluation["consequence_trajectory"] = trajectory_id
            evaluation["consequence"] = dict(outcome)
            evaluation["workspace"] = {
                **dict(evaluation.get("workspace", {})),
                "action_receipt": receipt,
            }
            runtime.integrate(evaluation)

            consequence = runtime.register_consequence(
                trajectory_id,
                {
                    "status": receipt.get("status"),
                    "result": outcome.get("result"),
                },
                evaluation={
                    "utility": outcome["utility"],
                    "credited_signal": outcome["credited_signal"],
                },
                persist=False,
            )
            runtime.store.save(runtime.state)

            priority = consequence.get("priority_adaptation")
            if isinstance(priority, dict) and priority.get("updated", False):
                adaptation_updates += 1

        return {
            "condition": condition.name,
            "cycles": cycles,
            "selected_trajectories": selected_ids,
            "trajectory_switches": sum(
                selected_ids[i] != selected_ids[i - 1]
                for i in range(1, len(selected_ids))
            ),
            "priority_adaptation_updates": adaptation_updates,
            "prediction_samples": len(prediction_errors),
            "prediction_error_mean": (
                round(sum(prediction_errors) / len(prediction_errors), 6)
                if prediction_errors
                else None
            ),
            "self_observation_samples": self_observation_samples,
            "final_state_hash": __import__("hashlib").sha256(
                json.dumps(
                    runtime.snapshot(),
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest(),
        }


def benchmark_with_llm(
    completion,
    *,
    cycles: int = 8,
    restart_every: int = 4,
) -> dict[str, Any]:
    results = [
        run_condition_with_llm(
            condition,
            completion,
            cycles=cycles,
            restart_every=restart_every,
        )
        for condition in CONDITIONS
    ]
    return {
        "protocol": "llm-longitudinal-v1",
        "provider_boundary": "provider-neutral",
        "cycles": cycles,
        "restart_every": restart_every,
        "conditions": results,
        "not_a_phenomenal_consciousness_test": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cycles", type=int, default=8)
    parser.add_argument("--restart-every", type=int, default=4)
    args = parser.parse_args()
    report = benchmark_with_llm(
        completion_from_environment(),
        cycles=args.cycles,
        restart_every=args.restart_every,
    )
    report["causal_provider_ab"] = run_causal_provider_ab(cycles=args.cycles)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
