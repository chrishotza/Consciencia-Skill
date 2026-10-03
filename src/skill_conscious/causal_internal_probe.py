from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping

from .core import ConsciousRuntime


_ADAPTATION_EVIDENCE_KEYS = (
    "homeostatic_adaptation_evidence",
    "homeostatic_adaptation_history",
    "trajectory_priority_adaptation_evidence",
    "trajectory_priority_adaptation_history",
    "trajectory_priority_adaptation_sequence",
    "self_model_adaptation_evidence",
    "self_model_adaptation_history",
    "self_model_adaptation_sequence",
)


def _adaptation_evidence_snapshot(runtime: ConsciousRuntime) -> dict[str, Any]:
    return {
        key: deepcopy(runtime.state.self_model.get(key))
        for key in _ADAPTATION_EVIDENCE_KEYS
        if key in runtime.state.self_model
    }


@dataclass(frozen=True)
class ReversibleValuationInterventionResult:
    baseline_selection: str
    intervention_selection: str
    restored_selection: str
    baseline_score: float
    intervention_score: float
    restored_score: float
    downstream_divergence: bool
    reversible: bool
    valuation_restored: bool
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
            "valuation_restored": self.valuation_restored,
            "evidence_unchanged": self.evidence_unchanged,
        }


def run_reversible_valuation_intervention(
    runtime: ConsciousRuntime,
    candidates: list[Mapping[str, Any]],
    *,
    intervention_valuation: Mapping[str, Any],
    intervention_id: str = "causal-valuation-intervention",
) -> ReversibleValuationInterventionResult:
    """Intervene on persistent valuation, measure selection, then restore exactly.

    The intervention changes only runtime valuation used by trajectory scoring.
    It does not create consequence evidence, advance adaptation ledgers, or
    execute an action.
    """
    snapshot = runtime.snapshot_valuation()
    before_valuation = dict(snapshot.get("valuation", {}))
    before_evidence = _adaptation_evidence_snapshot(runtime)

    baseline = runtime.select_trajectory(candidates)
    intervention = runtime.intervene_valuation(
        intervention_valuation,
        persist=False,
        intervention_id=intervention_id,
    )
    if not intervention.get("intervened"):
        raise RuntimeError("valuation intervention did not change valuation")

    intervened = runtime.select_trajectory(candidates)
    runtime.restore_valuation(
        snapshot,
        persist=False,
        intervention_id=intervention_id,
    )
    restored = runtime.select_trajectory(candidates)

    after_valuation = runtime.snapshot_valuation().get("valuation", {})
    after_evidence = _adaptation_evidence_snapshot(runtime)

    baseline_score = float(baseline.get("score", 0.0))
    intervention_score = float(intervened.get("score", 0.0))
    restored_score = float(restored.get("score", 0.0))

    return ReversibleValuationInterventionResult(
        baseline_selection=str(baseline.get("id", "")),
        intervention_selection=str(intervened.get("id", "")),
        restored_selection=str(restored.get("id", "")),
        baseline_score=round(baseline_score, 6),
        intervention_score=round(intervention_score, 6),
        restored_score=round(restored_score, 6),
        downstream_divergence=str(baseline.get("id", "")) != str(intervened.get("id", "")),
        reversible=str(baseline.get("id", "")) == str(restored.get("id", "")),
        valuation_restored=before_valuation == after_valuation,
        evidence_unchanged=before_evidence == after_evidence,
    )
