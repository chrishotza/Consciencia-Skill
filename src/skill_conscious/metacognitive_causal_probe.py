from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping

from .core import ConsciousRuntime


@dataclass(frozen=True)
class MetacognitiveCausalProbeResult:
    baseline_selection: str
    intervention_selection: str
    restored_selection: str
    baseline_trace: dict[str, Any]
    intervention_trace: dict[str, Any]
    restored_trace: dict[str, Any]
    selection_diverged: bool
    attribution_diverged: bool
    reversible: bool
    valuation_restored: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "baseline_selection": self.baseline_selection,
            "intervention_selection": self.intervention_selection,
            "restored_selection": self.restored_selection,
            "baseline_trace": self.baseline_trace,
            "intervention_trace": self.intervention_trace,
            "restored_trace": self.restored_trace,
            "selection_diverged": self.selection_diverged,
            "attribution_diverged": self.attribution_diverged,
            "reversible": self.reversible,
            "valuation_restored": self.valuation_restored,
        }


def run_metacognitive_causal_probe(
    runtime: ConsciousRuntime,
    candidates: list[Mapping[str, Any]],
    *,
    intervention_valuation: Mapping[str, Any],
) -> MetacognitiveCausalProbeResult:
    """Test whether internal intervention changes both action and its attribution trace."""
    snapshot = runtime.snapshot_valuation()
    before = deepcopy(snapshot.get("valuation", {}))

    baseline = runtime.select_trajectory(candidates)
    runtime.intervene_valuation(intervention_valuation, persist=False, intervention_id="metacognitive-causal")
    intervention = runtime.select_trajectory(candidates)
    runtime.restore_valuation(snapshot, persist=False, intervention_id="metacognitive-causal")
    restored = runtime.select_trajectory(candidates)

    baseline_trace = dict(baseline.get("metacognition", {}))
    intervention_trace = dict(intervention.get("metacognition", {}))
    restored_trace = dict(restored.get("metacognition", {}))

    baseline_contrib = dict(baseline_trace.get("selected_signal_contributions", {}))
    intervention_contrib = dict(intervention_trace.get("selected_signal_contributions", {}))
    restored_contrib = dict(restored_trace.get("selected_signal_contributions", {}))

    return MetacognitiveCausalProbeResult(
        baseline_selection=str(baseline.get("id", "")),
        intervention_selection=str(intervention.get("id", "")),
        restored_selection=str(restored.get("id", "")),
        baseline_trace=baseline_trace,
        intervention_trace=intervention_trace,
        restored_trace=restored_trace,
        selection_diverged=str(baseline.get("id", "")) != str(intervention.get("id", "")),
        attribution_diverged=baseline_contrib != intervention_contrib,
        reversible=(
            str(baseline.get("id", "")) == str(restored.get("id", ""))
            and baseline_contrib == restored_contrib
        ),
        valuation_restored=before == runtime.snapshot_valuation().get("valuation", {}),
    )
