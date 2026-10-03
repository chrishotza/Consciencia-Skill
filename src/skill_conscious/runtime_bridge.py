from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

from .attractor import ExperienceAttractorMemory
from .experience_field import ExperienceFieldProfile
from .reentry import ExperienceFieldReentry


RUNTIME_OWNED_KEYS = {
    "experience_field_state",
    "experience_field_expected",
    "experience_field_sequence",
    "experience_field_regime_preferences",
    "experience_field_evidence",
    "experience_field_history",
    "experience_attractor_center",
    "experience_attractor_radius",
    "experience_attractor_distance",
    "experience_attractor_recurrence",
    "experience_attractor_stability",
    "experience_attractor_recovery",
    "experience_attractor_strength",
    "experience_attractor_sequence",
    "experience_attractor_history",
}


@dataclass(frozen=True)
class BridgeSelection:
    """Auditable trajectory-selection result from the dynamic-core adapter."""

    selected: dict[str, Any]
    ranked: list[dict[str, Any]]
    observed_field_sequence: int
    attractor_sequence: int


class ExperienceDynamicsBridge:
    """Attach the dynamic core to a Skill-Conscious host/runtime boundary."""

    def __init__(self, state_dir: str | Path, *, enabled: bool = True, return_weight: float = 0.50) -> None:
        self.state_dir = Path(state_dir)
        self.enabled = bool(enabled)
        self.return_weight = float(return_weight)
        self.reentry = ExperienceFieldReentry(self.state_dir / "experience-field.json")
        self.attractor = ExperienceAttractorMemory(self.state_dir / "experience-attractor.json")

    @staticmethod
    def _profile(value: ExperienceFieldProfile | Mapping[str, Any]) -> ExperienceFieldProfile:
        if isinstance(value, ExperienceFieldProfile):
            return value
        if not isinstance(value, Mapping):
            raise TypeError("experience profile must be ExperienceFieldProfile or mapping")
        payload: dict[str, float] = {}
        for key in ExperienceFieldProfile.__dataclass_fields__:
            raw = value.get(key, 0.0)
            if not isinstance(raw, (int, float)) or isinstance(raw, bool):
                raise TypeError(f"experience profile field {key!r} must be numeric")
            payload[key] = float(raw)
        return ExperienceFieldProfile(**payload)

    def observe(self, profile: ExperienceFieldProfile | Mapping[str, Any], *, evidence_id: str, regime: str = "baseline") -> dict[str, Any]:
        observed = self._profile(profile)
        if not self.enabled:
            return {"enabled": False, "reentry": None, "attractor": None}
        return {
            "enabled": True,
            "reentry": self.reentry.observe(observed, evidence_id=evidence_id, regime=regime),
            "attractor": self.attractor.observe(observed, evidence_id=evidence_id, adapt=True),
        }

    def _return_bias(self, predicted: ExperienceFieldProfile, *, current: ExperienceFieldProfile | None) -> dict[str, float]:
        if not self.enabled or not self.attractor.state.center:
            return {"predicted_distance": 0.0, "current_distance": 0.0, "basin_membership": 0.0, "improvement": 0.0, "strength": 0.0, "bias": 0.0}
        predicted_distance = self.attractor._distance_from_center(self.attractor.state.center, predicted)
        current_distance = (
            self.attractor._distance_from_center(self.attractor.state.center, current)
            if current is not None else self.attractor.state.last_distance
        )
        radius = max(self.attractor.min_radius, self.attractor.state.radius)
        improvement = max(0.0, min(1.0, (current_distance - predicted_distance) / radius))
        affinity = self.attractor.basin_membership(predicted_distance)
        strength = self.attractor.attractor_strength()
        bias = self.return_weight * strength * (0.5 * affinity + 0.5 * improvement)
        return {
            "predicted_distance": round(predicted_distance, 6),
            "current_distance": round(current_distance, 6),
            "basin_membership": round(affinity, 6),
            "improvement": round(improvement, 6),
            "strength": round(strength, 6),
            "bias": round(bias, 6),
        }

    def score_candidate(self, base_score: float, predicted_profile: ExperienceFieldProfile | Mapping[str, Any] | None, *, current_profile: ExperienceFieldProfile | Mapping[str, Any] | None = None) -> tuple[float, dict[str, float]]:
        base = float(base_score)
        if not self.enabled or predicted_profile is None:
            return round(base, 6), {"base_score": round(base, 6), "experience_attractor_bias": 0.0}
        predicted = self._profile(predicted_profile)
        current = self._profile(current_profile) if current_profile is not None else None
        bias = self._return_bias(predicted, current=current)
        return round(base + bias["bias"], 6), {"base_score": round(base, 6), "experience_attractor_bias": bias["bias"], **bias}

    def select_trajectory(self, candidates: list[Mapping[str, Any]], *, base_scorer: Callable[[Mapping[str, Any]], float], predicted_profiles: Mapping[str, ExperienceFieldProfile | Mapping[str, Any]] | None = None, current_profile: ExperienceFieldProfile | Mapping[str, Any] | None = None) -> BridgeSelection:
        if not candidates:
            raise ValueError("candidates cannot be empty")
        profile_map = dict(predicted_profiles or {})
        ranked: list[dict[str, Any]] = []
        for raw in candidates:
            item = dict(raw)
            candidate_id = str(item.get("id", "")).strip()
            if not candidate_id:
                raise ValueError("candidate requires a non-empty id")
            base = float(base_scorer(item))
            score, diagnostics = self.score_candidate(base, profile_map.get(candidate_id), current_profile=current_profile)
            item["base_score"] = round(base, 6)
            item["experience_dynamics"] = diagnostics
            item["score"] = score
            ranked.append(item)
        ranked.sort(key=lambda item: (float(item.get("score", 0.0)), str(item.get("id", ""))), reverse=True)
        return BridgeSelection(
            selected=dict(ranked[0]),
            ranked=ranked,
            observed_field_sequence=self.reentry.state.sequence,
            attractor_sequence=self.attractor.state.sequence,
        )

    def record_recovery(self, baseline: ExperienceFieldProfile | Mapping[str, Any], perturbed: ExperienceFieldProfile | Mapping[str, Any], recovered: ExperienceFieldProfile | Mapping[str, Any], *, evidence_id: str) -> dict[str, Any]:
        if not self.enabled:
            return {"enabled": False, "recovery_index": 0.0}
        return self.attractor.record_perturbation_recovery(self._profile(baseline), self._profile(perturbed), self._profile(recovered), evidence_id=evidence_id)

    def record_regime_consequence(self, regime: str, utility: float, *, evidence_id: str) -> dict[str, Any]:
        if not self.enabled:
            return {"enabled": False, "updated": False}
        return self.reentry.record_consequence(regime, float(utility), evidence_id=evidence_id)

    def sanitize_model_frame(self, frame: Mapping[str, Any]) -> dict[str, Any]:
        clean = self.reentry.sanitized_model_frame(frame)
        model = clean.get("self_model")
        if isinstance(model, Mapping):
            clean_model = dict(model)
            for key in RUNTIME_OWNED_KEYS:
                clean_model.pop(key, None)
            clean["self_model"] = clean_model
        return clean

    def prepare_runtime_frame(self, frame: Mapping[str, Any], selection: BridgeSelection) -> dict[str, Any]:
        clean = self.sanitize_model_frame(frame)
        clean["selected_trajectory"] = dict(selection.selected)
        clean["candidate_futures"] = [dict(item) for item in selection.ranked]
        workspace = dict(clean.get("workspace", {}))
        workspace["experience_dynamics"] = self.runtime_state()
        workspace["experience_dynamics"]["selection"] = {
            "selected_id": str(selection.selected.get("id", "")),
            "ranked_ids": [str(item.get("id", "")) for item in selection.ranked],
            "observed_field_sequence": selection.observed_field_sequence,
            "attractor_sequence": selection.attractor_sequence,
        }
        clean["workspace"] = workspace
        return clean

    def runtime_state(self) -> dict[str, Any]:
        if not self.enabled:
            return {"experience_dynamics_enabled": False}
        result: dict[str, Any] = {}
        result.update(self.reentry.runtime_state())
        result.update(self.attractor.runtime_state())
        result["experience_dynamics_enabled"] = True
        return result

    def inject_runtime_observation(self, frame: Mapping[str, Any], *, profile: ExperienceFieldProfile | Mapping[str, Any], evidence_id: str, regime: str = "baseline") -> dict[str, Any]:
        clean = self.sanitize_model_frame(frame)
        observation = self.observe(profile, evidence_id=evidence_id, regime=regime)
        workspace = dict(clean.get("workspace", {}))
        workspace["experience_dynamics"] = {"observation": observation, "runtime_state": self.runtime_state()}
        clean["workspace"] = workspace
        return clean
