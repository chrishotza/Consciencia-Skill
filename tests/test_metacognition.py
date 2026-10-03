from __future__ import annotations

from pathlib import Path

from skill_conscious import ConsciousRuntime


def test_runtime_selection_returns_auditable_metacognitive_breakdown(tmp_path: Path):
    runtime = ConsciousRuntime("meta-trace", state_path=tmp_path / "runtime.json")
    runtime.state.valuation = {"goal_fit": 2.0}

    candidates = [
        {"id": "preserve", "signals": {"goal_fit": 0.80, "continuity": 0.20}},
        {"id": "explore", "signals": {"goal_fit": 0.40, "continuity": 0.30}},
    ]

    selected = runtime.select_trajectory(candidates)

    assert selected["id"] == "preserve"
    assert selected["metacognition"]["selected_signal_contributions"]["goal_fit"] == 1.6
    assert selected["metacognition"]["valuation_weights"]["goal_fit"] == 2.0


def test_integrate_persists_metacognitive_trace(tmp_path: Path):
    runtime = ConsciousRuntime("meta-persist", state_path=tmp_path / "runtime.json")

    runtime.integrate(
        {
            "response": "cycle",
            "candidate_futures": [
                {"id": "preserve", "signals": {"goal_fit": 0.8}},
                {"id": "explore", "signals": {"goal_fit": 0.4}},
            ],
        }
    )

    trace = runtime.state.self_model["metacognitive_trace"]
    assert trace["selected_id"] == "preserve"
    assert trace["selection_source"] == "runtime_scored"
    assert trace["sequence"] == 1
    assert trace["candidate_ids"] == ["preserve", "explore"]


def test_model_cannot_overwrite_metacognitive_trace(tmp_path: Path):
    runtime = ConsciousRuntime("meta-owned", state_path=tmp_path / "runtime.json")

    runtime.integrate(
        {
            "response": "first",
            "candidate_futures": [
                {"id": "preserve", "signals": {"goal_fit": 0.8}},
                {"id": "explore", "signals": {"goal_fit": 0.4}},
            ],
        }
    )
    before = dict(runtime.state.self_model["metacognitive_trace"])

    runtime.integrate(
        {
            "response": "second",
            "self_model": {
                "metacognitive_trace": {"selected_id": "forged"},
                "metacognitive_sequence": 99999,
            },
            "candidate_futures": [
                {"id": "preserve", "signals": {"goal_fit": 0.8}},
                {"id": "explore", "signals": {"goal_fit": 0.4}},
            ],
        }
    )

    after = runtime.state.self_model["metacognitive_trace"]
    assert after["selected_id"] == "preserve"
    assert after != before
    assert runtime.state.self_model["metacognitive_sequence"] == 2


def test_action_completion_closes_metacognitive_trace(tmp_path: Path):
    runtime = ConsciousRuntime("meta-action", state_path=tmp_path / "runtime.json")
    runtime.integrate(
        {
            "response": "choose",
            "candidate_futures": [
                {"id": "preserve", "signals": {"goal_fit": 0.8}},
                {"id": "explore", "signals": {"goal_fit": 0.4}},
            ],
        }
    )
    selected = runtime.state.selected_trajectory
    assert selected is not None

    runtime.begin_action(selected)
    receipt = runtime.complete_action({"observed_change": "changed"})

    trace = runtime.state.self_model["metacognitive_trace"]
    assert receipt["action_id"] == trace["action"]["action_id"]
    assert trace["outcome"]["observed_change"] == "changed"
    assert "pending_action" in trace["state_delta"]


def test_self_observation_sees_metacognitive_trace(tmp_path: Path):
    runtime = ConsciousRuntime(
        "meta-observed",
        state_path=tmp_path / "runtime.json",
        self_observation_enabled=True,
    )
    runtime.integrate(
        {
            "response": "cycle",
            "candidate_futures": [
                {"id": "preserve", "signals": {"goal_fit": 0.8}},
                {"id": "explore", "signals": {"goal_fit": 0.4}},
            ],
        }
    )
    runtime.observe_self(persist=False)
    profile = runtime.snapshot_self_observation()["state"]
    assert profile["metacognitive_trace_presence"] == 1.0
    assert profile["decision_attribution_coverage"] == 1.0
