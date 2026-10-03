from __future__ import annotations

from pathlib import Path

from skill_conscious import ConsciousRuntime, run_metacognitive_causal_probe


def test_metacognitive_trace_tracks_causal_intervention(tmp_path: Path):
    runtime = ConsciousRuntime(
        "meta-causal",
        state_path=tmp_path / "runtime.json",
    )
    runtime.state.valuation = {"goal_fit": 2.0}

    candidates = [
        {"id": "preserve", "signals": {"goal_fit": 0.8}},
        {"id": "explore", "signals": {"goal_fit": 0.4}},
    ]

    result = run_metacognitive_causal_probe(
        runtime,
        candidates,
        intervention_valuation={"goal_fit": -2.0},
    )

    assert result.baseline_selection == "preserve"
    assert result.intervention_selection == "explore"
    assert result.restored_selection == "preserve"
    assert result.selection_diverged is True
    assert result.attribution_diverged is True
    assert result.reversible is True
    assert result.valuation_restored is True

    assert (
        result.baseline_trace["valuation_weights"]["goal_fit"]
        == 2.0
    )
    assert (
        result.intervention_trace["valuation_weights"]["goal_fit"]
        == -2.0
    )
    assert (
        result.restored_trace["valuation_weights"]["goal_fit"]
        == 2.0
    )
