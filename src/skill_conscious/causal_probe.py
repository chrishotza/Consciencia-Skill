from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .core import ConsciousRuntime
from .experience_field import ExperienceFieldProfile


@dataclass(frozen=True)
class ReversibleInterventionResult:
    baseline_selection: str
    intervention_selection: str
    restored_selection: str
    baseline_score: float
    intervention_score: float
    restored_score: float
    downstream_divergence: bool
    reversible: bool
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
            "evidence_unchanged": self.evidence_unchanged,
        }


def run_reversible_intervention(
    runtime: ConsciousRuntime,
    candidates: list[Mapping[str, Any]],
    *,
    intervention_center: Mapping[str, Any],
    intervention_id: str = "causal-intervention",
) -> ReversibleInterventionResult:
    """Intervene, measure downstream divergence, then reverse the exact intervention.

    The intervention changes only the attractor center. It does not add evidence,
    increment learning sequences, or commit a normal adaptation event.
    """
    if not runtime.dynamic_core_enabled:
        raise RuntimeError("dynamic_core_enabled must be true")
    snapshot = runtime.snapshot_experience_dynamics()
    before_evidence = snapshot["attractor"].get("evidence", {})
    before_sequence = snapshot["attractor"].get("sequence", 0)

    baseline = runtime.select_trajectory(candidates)
    intervention = runtime.intervene_experience_attractor(
        intervention_center,
        persist=False,
        intervention_id=intervention_id,
    )
    if not intervention.get("intervened"):
        raise RuntimeError("intervention did not change attractor center")

    # The trajectory scorer already consumes predicted_experience_field. This
    # call is made after the explicit intervention and uses the same candidates.
    intervened = runtime.select_trajectory(candidates)
    runtime.restore_experience_dynamics(
        snapshot,
        persist=False,
        intervention_id=intervention_id,
    )
    restored = runtime.select_trajectory(candidates)

    after_state = runtime.snapshot_experience_dynamics()
    after_evidence = after_state["attractor"].get("evidence", {})
    after_sequence = after_state["attractor"].get("sequence", 0)

    baseline_score = float(baseline.get("score", 0.0))
    intervention_score = float(intervened.get("score", 0.0))
    restored_score = float(restored.get("score", 0.0))

    return ReversibleInterventionResult(
        baseline_selection=str(baseline.get("id", "")),
        intervention_selection=str(intervened.get("id", "")),
        restored_selection=str(restored.get("id", "")),
        baseline_score=round(baseline_score, 6),
        intervention_score=round(intervention_score, 6),
        restored_score=round(restored_score, 6),
        downstream_divergence=str(baseline.get("id", "")) != str(intervened.get("id", "")),
        reversible=str(baseline.get("id", "")) == str(restored.get("id", "")),
        evidence_unchanged=before_evidence == after_evidence and before_sequence == after_sequence,
    )
