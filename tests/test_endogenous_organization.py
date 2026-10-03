from pathlib import Path

from skill_conscious import ConsciousRuntime


def test_endogenous_latent_pattern_forms_after_recurrence(tmp_path: Path) -> None:
    runtime = ConsciousRuntime("agent", tmp_path / "state.json")

    for index, stability in enumerate((0.2, 0.8, 0.2)):
        runtime.integrate(
            {
                "response": f"cycle-{index}",
                "internal_state": {"stability": stability},
            }
        )

    assert len(runtime.state.latent_patterns) == 1
    pattern = next(iter(runtime.state.latent_patterns.values()))
    assert pattern["source"] == "endogenous"
    assert pattern["evidence_count"] == 1
    assert pattern["last_matched_revision"] == 3
    assert pattern["activation"] >= 0.6


def test_latent_pattern_learning_can_be_disabled_for_ablation(
    tmp_path: Path,
) -> None:
    runtime = ConsciousRuntime(
        "agent",
        tmp_path / "state.json",
        learn_latent_patterns=False,
    )

    for index, stability in enumerate((0.2, 0.8, 0.2)):
        runtime.integrate(
            {
                "response": f"cycle-{index}",
                "internal_state": {"stability": stability},
            }
        )

    assert runtime.state.latent_patterns == {}


def test_high_self_dissonance_drives_endogenous_integration_regime(
    tmp_path: Path,
) -> None:
    runtime = ConsciousRuntime("agent", tmp_path / "state.json")

    runtime.integrate(
        {
            "response": "cycle",
            "internal_state": {"stability": 0.1},
            "self_model": {
                "expected_self_state": {"stability": 1.0},
            },
        }
    )

    assert runtime.state.self_dissonance == 0.9
    assert runtime.state.regime == "integration"


def test_explicit_regime_override_remains_authoritative(tmp_path: Path) -> None:
    runtime = ConsciousRuntime("agent", tmp_path / "state.json")

    runtime.integrate(
        {
            "response": "cycle",
            "internal_state": {"stability": 0.1},
            "self_model": {
                "expected_self_state": {"stability": 1.0},
            },
            "regime": "custom",
        }
    )

    assert runtime.state.regime == "custom"


def test_recurrent_latent_pattern_revises_self_model(tmp_path: Path) -> None:
    runtime = ConsciousRuntime(
        "agent",
        tmp_path / "state.json",
        learn_self_model_from_latent_patterns=True,
    )
    runtime.state.self_model = {
        "latent_self_model_learning_rate": 0.2,
        "learned_self_state": {"stability": 0.8},
    }

    for index, stability in enumerate((0.2, 0.8, 0.2)):
        runtime.integrate(
            {
                "response": f"cycle-{index}",
                "internal_state": {"stability": stability},
            }
        )

    learned = runtime.state.self_model["learned_self_state"]
    tendencies = runtime.state.self_model["latent_tendencies"]

    assert "stability" in learned
    assert learned["stability"] > 0.2
    assert len(tendencies) == 1
    assert runtime.state.transformation_log[-1]["type"] in {
        "latent_self_model_revision",
        "regime_transition",
        "changes",
    }


def test_latent_self_model_revision_is_ablated_independently(
    tmp_path: Path,
) -> None:
    runtime = ConsciousRuntime(
        "agent",
        tmp_path / "state.json",
        learn_self_model_from_latent_patterns=False,
    )

    for index, stability in enumerate((0.2, 0.8, 0.2)):
        runtime.integrate(
            {
                "response": f"cycle-{index}",
                "internal_state": {"stability": stability},
            }
        )

    assert runtime.state.latent_patterns
    assert "learned_self_state" not in runtime.state.self_model
    assert "latent_tendencies" not in runtime.state.self_model


def test_learned_self_model_changes_generated_self_alignment(
    tmp_path: Path,
) -> None:
    runtime = ConsciousRuntime("agent", tmp_path / "state.json")
    runtime.state.self_state = {"stability": 0.9}
    runtime.state.self_model = {
        "learned_self_state": {"stability": 0.9},
    }

    before = runtime.generate_candidate_futures()
    preserve = next(
        candidate
        for candidate in before
        if candidate["id"] == "preserve_continuity"
    )

    runtime.state.self_model["learned_self_state"]["stability"] = 0.1
    after = runtime.generate_candidate_futures()
    shifted = next(
        candidate
        for candidate in after
        if candidate["id"] == "preserve_continuity"
    )

    assert shifted["signals"]["self_alignment"] < preserve["signals"]["self_alignment"]
