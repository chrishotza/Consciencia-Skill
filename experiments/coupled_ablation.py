from __future__ import annotations
import json, sys
from pathlib import Path
from typing import Any
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from skill_conscious.experience_field import build_experience_field, sensory_counterfactual_action_delta


def channels(perturbed: bool = False) -> list[list[float]]:
    base = [
        [0.2 * i + 0.03 * ((i % 2) - 0.5) for i in range(64)],
        [0.2 * i + 0.02 * ((i % 3) - 1.0) for i in range(64)],
        [0.2 * i - 0.02 * ((i % 4) - 1.5) for i in range(64)],
    ]
    return [[value * (-1 if i % 2 else 1) for i, value in enumerate(channel)] for channel in base] if perturbed else base


def score_candidate(utility: float, predicted_vision: float, *, affective_weight: float, dynamic_repertoire: float = 0.0, dynamic_weight: float = 0.0) -> float:
    affect_delta = sensory_counterfactual_action_delta(
        utility, {"vision": predicted_vision}, {"vision": 0.0},
        affective_weights={"vision": affective_weight}, affect_weight=1.0,
    )
    return round(utility + affect_delta + dynamic_weight * dynamic_repertoire, 6)


def run_ablation() -> dict[str, dict[str, Any]]:
    candidates = {"preserve": {"utility": 0.55, "predicted_vision": 1.0}, "explore": {"utility": 0.50, "predicted_vision": 0.0}}
    result: dict[str, dict[str, Any]] = {}
    scores_a = {name: data["utility"] for name, data in candidates.items()}
    result["A_baseline"] = {"selected": max(scores_a, key=scores_a.get), "scores": scores_a}

    scores_b = {name: score_candidate(data["utility"], data["predicted_vision"], affective_weight=-1.0) for name, data in candidates.items()}
    result["B_sensory_affect"] = {"selected": max(scores_b, key=scores_b.get), "scores": scores_b, "counterfactual_delta": sensory_counterfactual_action_delta(candidates["preserve"]["utility"], {"vision": 1.0}, {"vision": 0.0}, affective_weights={"vision": -1.0})}

    profile, _, _ = build_experience_field({"vision": 1.0}, {"vision": 0.0}, channels(perturbed=True), affective_weights={"vision": -1.0}, self_relevance_weights={"vision": 1.0})
    scores_c = {name: score_candidate(data["utility"], data["predicted_vision"], affective_weight=-1.0, dynamic_repertoire=profile.dynamic_repertoire, dynamic_weight=0.25) for name, data in candidates.items()}
    result["C_sensory_plus_dynamics"] = {"selected": max(scores_c, key=scores_c.get), "scores": scores_c, "dynamic_repertoire": profile.dynamic_repertoire, "field_coherence": profile.field_coherence}
    return result


if __name__ == "__main__":
    print(json.dumps(run_ablation(), indent=2, ensure_ascii=False, sort_keys=True))
