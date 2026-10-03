from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from skill_conscious.experience_field import build_experience_field
from skill_conscious.reentry import ExperienceFieldReentry


def _channels(flip: bool = False) -> list[list[float]]:
    base = [
        [0.2 * i + 0.03 * ((i % 2) - 0.5) for i in range(64)],
        [0.2 * i + 0.02 * ((i % 3) - 1.0) for i in range(64)],
        [0.2 * i - 0.02 * ((i % 4) - 1.5) for i in range(64)],
    ]
    return [[v * (-1 if i % 2 else 1) for i, v in enumerate(ch)] for ch in base] if flip else base


def run_ablation(path: str = "/tmp/skill-conscious-reentry.json") -> dict[str, dict[str, object]]:
    field = build_experience_field({"vision": 1.0}, {"vision": 0.0}, _channels(True), affective_weights={"vision": -1.0}, self_relevance_weights={"vision": 1.0})[0]
    base = {"baseline": 0.50, "exploration": 0.49}
    result: dict[str, dict[str, object]] = {"A_static": {"selected": max(base, key=base.get), "scores": dict(base)}}
    reentry = ExperienceFieldReentry(path)
    for index in range(3):
        reentry.record_consequence("exploration", 1.0, evidence_id=f"utility-{index}")
    scores = {regime: reentry.score_regime(score, regime, field=field) for regime, score in base.items()}
    result["B_persistent_reentry"] = {"selected": max(scores, key=scores.get), "scores": scores, "preferences": dict(reentry.state.regime_preferences), "sequence": reentry.state.sequence}
    restarted = ExperienceFieldReentry(path)
    restarted_scores = {regime: restarted.score_regime(score, regime, field=field) for regime, score in base.items()}
    result["C_after_restart"] = {"selected": max(restarted_scores, key=restarted_scores.get), "scores": restarted_scores, "preferences": dict(restarted.state.regime_preferences), "sequence": restarted.state.sequence}
    return result


if __name__ == "__main__":
    print(json.dumps(run_ablation(), indent=2, ensure_ascii=False, sort_keys=True))
