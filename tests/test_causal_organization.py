from pathlib import Path

from skill_conscious import ConsciousRuntime


def test_present_generates_endogenous_candidate_futures(tmp_path: Path) -> None:
    runtime = ConsciousRuntime("agent", tmp_path / "state.json")

    frame = runtime.prepare_frame("new input")

    assert len(frame["present"]["candidate_futures"]) == 3
    assert frame["present"]["topology_diagnostics"]["integrity"] == 1.0
    assert 0.0 <= frame["present"]["coherence"] <= 1.0


def test_topology_integrity_enters_trajectory_score(tmp_path: Path) -> None:
    runtime = ConsciousRuntime("agent", tmp_path / "state.json")
    runtime.state.self_model = {
        "trajectory_weights": {
            "topology_integrity": 10.0,
        }
    }

    runtime.state.relation_topology = {
        "self": ["world"],
        "world": [],
    }
    good = runtime.score_trajectory({"signals": {"topology_integrity": 1.0}})

    runtime.state.relation_topology = {
        "self": ["missing"],
        "world": [],
    }
    bad = runtime.score_trajectory({"signals": {"topology_integrity": 0.0}})

    assert good > bad


def test_integrate_persists_salience_layers_coherence_and_attractor(
    tmp_path: Path,
) -> None:
    path = tmp_path / "state.json"
    runtime = ConsciousRuntime("agent", path)

    runtime.integrate(
        {
            "response": "cycle",
            "attention": ["goal"],
            "salience": {"goal": 0.9},
            "layers": {"meta": {"active": True}},
            "intention": "preserve continuity",
            "relation_topology": {
                "self": ["goal"],
                "goal": [],
            },
        }
    )

    reloaded = ConsciousRuntime("agent", path)

    assert reloaded.state.salience == {"goal": 0.9}
    assert reloaded.state.layers == {"meta": {"active": True}}
    assert reloaded.state.attractor is not None
    assert 0.0 <= reloaded.state.coherence <= 1.0


def test_self_model_changes_generated_future_selection(tmp_path: Path) -> None:
    runtime = ConsciousRuntime("agent", tmp_path / "state.json")

    candidates = runtime.generate_candidate_futures()

    runtime.state.self_model = {
        "trajectory_weights": {
            "continuity": 10.0,
            "risk": -10.0,
        }
    }
    continuity_choice = runtime.select_trajectory(candidates)["id"]

    runtime.state.self_model = {
        "trajectory_weights": {
            "learning": 10.0,
            "risk": 2.0,
        }
    }
    exploration_choice = runtime.select_trajectory(candidates)["id"]

    assert continuity_choice != exploration_choice
