from pathlib import Path

from skill_conscious import ConsciousRuntime


def test_latent_patterns_persist_and_enter_present(tmp_path: Path) -> None:
    path = tmp_path / "state.json"
    runtime = ConsciousRuntime("agent", path)

    runtime.integrate(
        {
            "response": "cycle",
            "latent_patterns": {
                "avoidance": {
                    "activation": 0.8,
                    "evidence": ["repeated hesitation"],
                }
            },
            "self_dissonance": 0.4,
        }
    )

    reloaded = ConsciousRuntime("agent", path)
    frame = reloaded.prepare_frame("next input")

    assert reloaded.state.latent_patterns["avoidance"]["activation"] == 0.8
    assert reloaded.state.self_dissonance == 0.4
    assert frame["present"]["latent_patterns"]["avoidance"]["activation"] == 0.8
    assert "integrate_latent_pattern" in {
        candidate["id"] for candidate in frame["present"]["candidate_futures"]
    }


def test_expected_self_state_can_generate_self_dissonance(tmp_path: Path) -> None:
    runtime = ConsciousRuntime("agent", tmp_path / "state.json")

    runtime.integrate(
        {
            "response": "cycle",
            "internal_state": {"stability": 0.2},
            "self_model": {
                "expected_self_state": {"stability": 0.9},
            },
        }
    )

    assert runtime.state.self_dissonance == 0.7
    assert runtime.state.coherence < 1.0


def test_self_dissonance_penalizes_matching_trajectory_signal(tmp_path: Path) -> None:
    runtime = ConsciousRuntime("agent", tmp_path / "state.json")

    runtime.state.self_model = {
        "trajectory_weights": {"self_dissonance": -10.0}
    }
    runtime.state.self_dissonance = 0.8

    high_dissonance = runtime.score_trajectory(
        {"signals": {"self_dissonance": 0.8}}
    )
    low_dissonance = runtime.score_trajectory(
        {"signals": {"self_dissonance": 0.1}}
    )

    assert low_dissonance > high_dissonance
