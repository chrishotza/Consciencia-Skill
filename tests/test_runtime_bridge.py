from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "experiments"))
from integrated_ablation import profile, run
from skill_conscious.runtime_bridge import ExperienceDynamicsBridge


def test_bridge_selection_is_causal_and_restart_persistent(tmp_path: Path):
    bridge = ExperienceDynamicsBridge(tmp_path / "state", return_weight=0.50)
    baseline = profile()
    bridge.observe(baseline, evidence_id="obs-1")
    bridge.observe(profile(0.01), evidence_id="obs-2")
    bridge.observe(profile(-0.01), evidence_id="obs-3")
    bridge.record_recovery(baseline, profile(0.35), profile(0.01), evidence_id="recovery-1")
    candidates = [{"id": "preserve", "base_score": 0.49}, {"id": "explore", "base_score": 0.52}]
    predicted = {"preserve": profile(0.01), "explore": profile(0.35)}
    result = bridge.select_trajectory(candidates, base_scorer=lambda item: float(item["base_score"]), predicted_profiles=predicted, current_profile=profile(0.35))
    assert result.selected["id"] == "preserve"
    restarted = ExperienceDynamicsBridge(tmp_path / "state", return_weight=0.50)
    result2 = restarted.select_trajectory(candidates, base_scorer=lambda item: float(item["base_score"]), predicted_profiles=predicted, current_profile=profile(0.35))
    assert result2.selected["id"] == "preserve"
    assert restarted.runtime_state()["experience_attractor_sequence"] > 0


def test_model_frame_cannot_overwrite_runtime_owned_dynamic_state(tmp_path: Path):
    bridge = ExperienceDynamicsBridge(tmp_path / "state")
    bridge.observe(profile(), evidence_id="obs-1")
    clean = bridge.sanitize_model_frame({"response": "ok", "self_model": {"experience_attractor_strength": 999, "experience_field_sequence": 999, "ordinary": "accepted"}})
    assert "experience_attractor_strength" not in clean["self_model"]
    assert "experience_field_sequence" not in clean["self_model"]
    assert clean["self_model"]["ordinary"] == "accepted"


def test_integrated_ablation_changes_selection_and_survives_restart():
    result = run()
    assert result["A_runtime_only"]["selected"] == "explore"
    assert result["B_reentry"]["selected"] == "explore"
    assert result["C_attractor"]["selected"] == "preserve"
    assert result["D_restart"]["selected"] == "preserve"
    assert result["C_attractor"]["recovery"]["recovery_index"] > 0.8


def test_prepare_runtime_frame_makes_bridge_selection_explicit(tmp_path: Path):
    bridge = ExperienceDynamicsBridge(tmp_path / "state")
    bridge.observe(profile(), evidence_id="obs-1")
    selection = bridge.select_trajectory(
        [{"id": "preserve", "base_score": 0.49}, {"id": "explore", "base_score": 0.52}],
        base_scorer=lambda item: float(item["base_score"]),
        predicted_profiles={"preserve": profile(0.01), "explore": profile(0.35)},
        current_profile=profile(),
    )
    frame = bridge.prepare_runtime_frame({"response": "selected", "self_model": {"experience_attractor_strength": 999, "ordinary": 1}}, selection)
    assert frame["selected_trajectory"]["id"] == selection.selected["id"]
    assert frame["candidate_futures"][0]["id"] == selection.selected["id"]
    assert "experience_attractor_strength" not in frame["self_model"]
    assert frame["self_model"]["ordinary"] == 1
