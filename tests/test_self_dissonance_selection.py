from pathlib import Path

from skill_conscious import ConsciousRuntime


def test_high_self_dissonance_exposes_resolution_pressure(tmp_path: Path) -> None:
    runtime = ConsciousRuntime("agent", tmp_path / "state.json")
    runtime.state.self_dissonance = 0.9

    candidates = runtime.generate_candidate_futures()
    integration = next(
        candidate
        for candidate in candidates
        if candidate["id"] == "integrate_latent_pattern"
    )

    assert integration["signals"]["dissonance_resolution"] == 0.9
    assert runtime.score_trajectory(integration) > runtime.score_trajectory(
        {
            "id": "preserve_continuity",
            "signals": {
                "continuity": 0.1,
                "goal_fit": 0.1,
                "learning": 0.1,
                "risk": 1.0,
                "uncertainty": 1.0,
            },
        }
    )
