from __future__ import annotations
import json, tempfile
from dataclasses import replace
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from skill_conscious import ExperienceDynamicsBridge
from skill_conscious.experience_field import ExperienceFieldProfile


def profile(offset: float = 0.0) -> ExperienceFieldProfile:
    base = ExperienceFieldProfile(0.10, 0.90, 0.20, 0.50, 0.70, 0.80, 0.10, 0.40, 0.20, 0.85, 0.25)
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


def run(base_dir: str | None = None) -> dict[str, object]:
    root = Path(base_dir) if base_dir else Path(tempfile.mkdtemp(prefix="skill-conscious-integrated-"))
    root.mkdir(parents=True, exist_ok=True)
    candidates = [{"id": "preserve", "base_score": 0.49}, {"id": "explore", "base_score": 0.52}]
    predicted = {"preserve": profile(0.01), "explore": profile(0.35)}
    baseline, perturbed, recovered = profile(), profile(0.35), profile(0.01)
    base_scorer = lambda item: float(item["base_score"])
    output: dict[str, object] = {}

    scores_a = {item["id"]: item["base_score"] for item in candidates}
    output["A_runtime_only"] = {"selected": max(scores_a, key=scores_a.get), "scores": scores_a}

    bridge_b = ExperienceDynamicsBridge(root / "B", return_weight=0.0)
    bridge_b.observe(baseline, evidence_id="obs-1")
    selection_b = bridge_b.select_trajectory(candidates, base_scorer=base_scorer, predicted_profiles={"preserve": predicted["preserve"]}, current_profile=baseline)
    output["B_reentry"] = {"selected": selection_b.selected["id"], "ranked": selection_b.ranked, "runtime_state": bridge_b.runtime_state()}

    bridge_c = ExperienceDynamicsBridge(root / "C", return_weight=0.50)
    for token, observed in (("obs-1", baseline), ("obs-2", profile(0.01)), ("obs-3", profile(-0.01))):
        bridge_c.observe(observed, evidence_id=token)
    recovery = bridge_c.record_recovery(baseline, perturbed, recovered, evidence_id="recovery-1")
    selection_c = bridge_c.select_trajectory(candidates, base_scorer=base_scorer, predicted_profiles=predicted, current_profile=perturbed)
    output["C_attractor"] = {"selected": selection_c.selected["id"], "ranked": selection_c.ranked, "recovery": recovery, "runtime_state": bridge_c.runtime_state()}

    bridge_d = ExperienceDynamicsBridge(root / "C", return_weight=0.50)
    selection_d = bridge_d.select_trajectory(candidates, base_scorer=base_scorer, predicted_profiles=predicted, current_profile=perturbed)
    output["D_restart"] = {"selected": selection_d.selected["id"], "ranked": selection_d.ranked, "runtime_state": bridge_d.runtime_state()}
    output["invariants"] = {
        "baseline_selects_explore": output["A_runtime_only"]["selected"] == "explore",
        "reentry_without_attractor_selects_explore": output["B_reentry"]["selected"] == "explore",
        "attractor_selects_preserve": output["C_attractor"]["selected"] == "preserve",
        "restart_preserves_selection": output["D_restart"]["selected"] == "preserve",
        "recovery_index_gt_0_8": output["C_attractor"]["recovery"]["recovery_index"] > 0.8,
    }
    return output


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False, sort_keys=True))
