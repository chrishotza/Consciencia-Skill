from __future__ import annotations

from pathlib import Path

from skill_conscious import ConsciousRuntime, run_reversible_valuation_intervention


def test_reversible_valuation_intervention_changes_and_restores_selection(tmp_path: Path):
    runtime = ConsciousRuntime("valuation-probe", state_path=tmp_path / "runtime.json")
    runtime.state.valuation = {"goal_fit": 1.0}
    runtime.store.save(runtime.state)

    candidates = [
        {"id": "preserve", "signals": {"goal_fit": 0.80}},
        {"id": "explore", "signals": {"goal_fit": 0.70}},
    ]

    result = run_reversible_valuation_intervention(
        runtime,
        candidates,
        intervention_valuation={"goal_fit": -1.0},
    )

    assert result.baseline_selection == "preserve"
    assert result.intervention_selection == "explore"
    assert result.restored_selection == "preserve"
    assert result.downstream_divergence is True
    assert result.reversible is True
    assert result.valuation_restored is True
    assert result.evidence_unchanged is True


def test_valuation_intervention_does_not_create_learning_evidence(tmp_path: Path):
    runtime = ConsciousRuntime("valuation-evidence", state_path=tmp_path / "runtime.json")
    runtime.state.valuation = {"goal_fit": 1.0}
    runtime.store.save(runtime.state)

    before = runtime.adaptation_evidence_snapshot()
    runtime.intervene_valuation(
        {"goal_fit": -1.0},
        persist=False,
        intervention_id="unit-test",
    )
    runtime.restore_valuation(
        {"valuation": {"goal_fit": 1.0}},
        persist=False,
        intervention_id="unit-test",
    )

    assert runtime.adaptation_evidence_snapshot() == before


def test_restored_valuation_persists_across_restart(tmp_path: Path):
    state_path = tmp_path / "runtime.json"
    runtime = ConsciousRuntime("valuation-restart", state_path=state_path)
    runtime.state.valuation = {"goal_fit": 1.0}
    runtime.store.save(runtime.state)

    snapshot = runtime.snapshot_valuation()
    runtime.intervene_valuation({"goal_fit": -1.0}, persist=True)
    runtime.restore_valuation(snapshot, persist=True)

    restarted = ConsciousRuntime("valuation-restart", state_path=state_path)
    assert restarted.state.valuation == {"goal_fit": 1.0}
