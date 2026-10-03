from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping

from .core import ConsciousRuntime
from .self_observation import SelfObservationProfile


@dataclass(frozen=True)
class ReversibleSelfObservationInterventionResult:
    baseline_selection: str
    intervention_selection: str
    restored_selection: str
    baseline_score: float
    intervention_score: float
    restored_score: float
    downstream_divergence: bool
    reversible: bool
    expected_observation_restored: bool
    evidence_unchanged: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "baseline_selection": self.baseline_selection,
            "intervention_selection": self.intervention_selection,
            "restored_selection": self.restored_selection,
            "baseline_score": self.baseline_score,
            "intervention_score": self.intervention_score,
            "restored_score": self.restored_score,
            "downstream_divergence": self.downstream_divergence,
            "reversible": self.reversible,
            "expected_observation_restored": self.expected_observation_restored,
            "evidence_unchanged": self.evidence_unchanged,
        }


def _evidence_snapshot(runtime: ConsciousRuntime) -> dict[str, Any]:
    keys = (
        "homeostatic_adaptation_evidence",
        "homeostatic_adaptation_history",
        "trajectory_priority_adaptation_evidence",
        "trajectory_priority_adaptation_history",
        "trajectory_priority_adaptation_sequence",
        "self_model_adaptation_evidence",
        "self_model_adaptation_history",
        "self_model_adaptation_sequence",
    )
    return {
        key: deepcopy(runtime.state.self_model.get(key))
        for key in keys
        if key in runtime.state.self_model
    }


def run_reversible_self_observation_intervention(
    runtime: ConsciousRuntime,
    candidates: list[Mapping[str, Any]],
    *,
    intervention_expected: Mapping[str, Any],
    intervention_id: str = "causal-self-observation-intervention",
) -> ReversibleSelfObservationInterventionResult:
    """Intervene on the runtime's self-observation expectation and reverse it."""
    if not runtime.self_observation_enabled:
        raise RuntimeError("self_observation_enabled must be true")

    snapshot = runtime.snapshot_self_observation()
    expected_before = deepcopy(snapshot.get("expected", {}))
    evidence_before = _evidence_snapshot(runtime)

    baseline = runtime.select_trajectory(candidates)
    runtime.intervene_self_observation_expected(
        intervention_expected,
        persist=False,
        intervention_id=intervention_id,
    )
    intervened = runtime.select_trajectory(candidates)
    runtime.restore_self_observation(
        snapshot,
        persist=False,
        intervention_id=intervention_id,
    )
    restored = runtime.select_trajectory(candidates)

    after = runtime.snapshot_self_observation()
    expected_after = after.get("expected", {})
    evidence_after = _evidence_snapshot(runtime)

    return ReversibleSelfObservationInterventionResult(
        baseline_selection=str(baseline.get("id", "")),
        intervention_selection=str(intervened.get("id", "")),
        restored_selection=str(restored.get("id", "")),
        baseline_score=round(float(baseline.get("score", 0.0)), 6),
        intervention_score=round(float(intervened.get("score", 0.0)), 6),
        restored_score=round(float(restored.get("score", 0.0)), 6),
        downstream_divergence=str(baseline.get("id", "")) != str(intervened.get("id", "")),
        reversible=str(baseline.get("id", "")) == str(restored.get("id", "")),
        expected_observation_restored=expected_before == expected_after,
        evidence_unchanged=evidence_before == evidence_after,
    )
