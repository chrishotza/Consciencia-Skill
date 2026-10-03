from __future__ import annotations
import json, sys, tempfile
from dataclasses import replace
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from skill_conscious.attractor import ExperienceAttractorMemory
from skill_conscious.experience_field import ExperienceFieldProfile


def profile(offset: float = 0.0) -> ExperienceFieldProfile:
    base = ExperienceFieldProfile(0.1, 0.9, 0.2, 0.5, 0.7, 0.8, 0.1, 0.4, 0.2, 0.85, 0.25)
    return replace(
        base,
        prediction_error=max(0.0, min(1.0, base.prediction_error + offset)),
        sensory_coherence=max(0.0, min(1.0, base.sensory_coherence - offset)),
        valence=max(-1.0, min(1.0, base.valence + offset)),
        self_relevance=max(0.0, min(1.0, base.self_relevance + offset)),
        dynamic_persistence=max(0.0, min(1.0, base.dynamic_persistence - offset)),
        dynamic_synchrony=max(0.0, min(1.0, base.dynamic_synchrony - offset)),
        dynamic_metastability=max(0.0, min(1.0, base.dynamic_metastability + abs(offset))),
        dynamic_complexity=max(0.0, min(1.0, base.dynamic_complexity + offset)),
        avalanche_activity=max(0.0, min(1.0, base.avalanche_activity + abs(offset))),
        field_coherence=max(0.0, min(1.0, base.field_coherence - abs(offset))),
        dynamic_repertoire=max(0.0, min(1.0, base.dynamic_repertoire + abs(offset))),
    )


def run_ablation(path: str | None = None) -> dict[str, dict[str, object]]:
    baseline, perturbation, recovery = profile(), profile(0.35), profile(0.01)
    static_scores = {"preserve": 0.49, "explore": 0.52}
    result = {"A_no_attractor": {"selected": max(static_scores, key=static_scores.get), "scores": static_scores}}
    temporary_directory = tempfile.TemporaryDirectory() if path is None else None
    state_path = path or str(Path(temporary_directory.name) / "attractor.json")
    memory = ExperienceAttractorMemory(state_path)
    memory.observe(baseline, evidence_id="baseline")
    memory.record_perturbation_recovery(baseline, perturbation, recovery, evidence_id="recovery")
    scores = {"preserve": memory.score_return(0.49, recovery, weight=0.5), "explore": memory.score_return(0.52, perturbation, weight=0.5)}
    result["B_attractor_return"] = {"selected": max(scores, key=scores.get), "scores": scores, "strength": memory.attractor_strength(), "recovery_index": memory.state.recovery_index, "stability": memory.state.stability}
    restarted = ExperienceAttractorMemory(state_path)
    restart_scores = {"preserve": restarted.score_return(0.49, recovery, weight=0.5), "explore": restarted.score_return(0.52, perturbation, weight=0.5)}
    result["C_restart"] = {"selected": max(restart_scores, key=restart_scores.get), "scores": restart_scores, "strength": restarted.attractor_strength()}
    if temporary_directory is not None:
        temporary_directory.cleanup()
    return result


if __name__ == "__main__":
    print(json.dumps(run_ablation(), indent=2, ensure_ascii=False, sort_keys=True))
