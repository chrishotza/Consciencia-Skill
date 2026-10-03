from __future__ import annotations

import json
import math
import os
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from statistics import pstdev
from typing import Any, Mapping

from .experience_field import ExperienceFieldProfile, profile_distance


@dataclass
class AttractorState:
    center: dict[str, float] = field(default_factory=dict)
    radius: float = 0.25
    sample_count: int = 0
    sequence: int = 0
    last_distance: float = 0.0
    recurrence: float = 0.0
    stability: float = 0.0
    recovery_index: float = 0.0
    evidence: dict[str, dict[str, Any]] = field(default_factory=dict)
    distances: list[float] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ExperienceAttractorMemory:
    """Persistent attractor model for the integrated experience field."""

    def __init__(
        self,
        state_path: str | os.PathLike[str],
        *,
        history_limit: int = 32,
        learning_rate: float = 0.15,
        max_center_step: float = 0.05,
        initial_radius: float = 0.25,
        min_radius: float = 0.05,
        max_radius: float = 0.75,
        radius_learning_rate: float = 0.10,
    ) -> None:
        self.path = Path(state_path)
        self.history_limit = max(1, int(history_limit))
        self.learning_rate = max(0.0, min(1.0, float(learning_rate)))
        self.max_center_step = max(0.0, float(max_center_step))
        self.initial_radius = max(1e-6, float(initial_radius))
        self.min_radius = max(1e-6, float(min_radius))
        self.max_radius = max(self.min_radius, float(max_radius))
        self.radius_learning_rate = max(0.0, min(1.0, float(radius_learning_rate)))
        self.state = self._load()

    def _load(self) -> AttractorState:
        if not self.path.exists():
            return AttractorState(radius=self.initial_radius)
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return AttractorState(
            center={str(k): float(v) for k, v in dict(payload.get("center", {})).items() if isinstance(v, (int, float)) and not isinstance(v, bool)},
            radius=max(self.min_radius, min(self.max_radius, float(payload.get("radius", self.initial_radius)))),
            sample_count=int(payload.get("sample_count", 0)),
            sequence=int(payload.get("sequence", 0)),
            last_distance=float(payload.get("last_distance", 0.0)),
            recurrence=max(0.0, min(1.0, float(payload.get("recurrence", 0.0)))),
            stability=max(0.0, min(1.0, float(payload.get("stability", 0.0)))),
            recovery_index=max(0.0, min(1.0, float(payload.get("recovery_index", 0.0)))),
            evidence={str(k): dict(v) for k, v in dict(payload.get("evidence", {})).items() if isinstance(v, Mapping)},
            distances=[float(v) for v in payload.get("distances", []) if isinstance(v, (int, float)) and not isinstance(v, bool)][-self.history_limit:],
            history=[dict(v) for v in payload.get("history", []) if isinstance(v, Mapping)][-self.history_limit:],
        )

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix=".experience-attractor-", suffix=".json", dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(self.state.to_dict(), handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, self.path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    @staticmethod
    def _profile_dict(profile: ExperienceFieldProfile) -> dict[str, float]:
        return {str(key): float(value) for key, value in profile.to_dict().items() if isinstance(value, (int, float)) and not isinstance(value, bool)}

    @staticmethod
    def _distance_from_center(center: Mapping[str, float], profile: ExperienceFieldProfile) -> float:
        if not center:
            return 0.0
        current = ExperienceAttractorMemory._profile_dict(profile)
        shared = sorted(set(center).intersection(current))
        if not shared:
            return 1.0
        values = [current[key] - float(center[key]) for key in shared]
        return round(min(1.0, math.sqrt(sum(value * value for value in values) / len(values))), 6)

    def _adapt_center(self, profile: ExperienceFieldProfile) -> dict[str, float]:
        current = self._profile_dict(profile)
        if not self.state.center:
            self.state.center = dict(current)
            return {key: 0.0 for key in current}
        updated = dict(self.state.center)
        changed: dict[str, float] = {}
        for key, observed in current.items():
            expected = float(updated.get(key, observed))
            raw_delta = self.learning_rate * (observed - expected)
            delta = max(-self.max_center_step, min(self.max_center_step, raw_delta))
            updated[key] = round(expected + delta, 6)
            if abs(delta) > 1e-12:
                changed[key] = round(delta, 6)
        self.state.center = updated
        return changed

    def _update_stability(self, distance: float) -> None:
        distances = (self.state.distances + [float(distance)])[-self.history_limit:]
        self.state.distances = distances
        self.state.sample_count = len(distances)
        if not distances:
            self.state.stability = self.state.recurrence = 0.0
            return
        radius = max(self.min_radius, self.state.radius)
        self.state.recurrence = round(sum(1 for value in distances if value <= radius) / len(distances), 6)
        variability = pstdev(distances) if len(distances) > 1 else 0.0
        self.state.stability = round(max(0.0, min(1.0, 1.0 - variability / max(radius, 1e-6))), 6)

    def observe(self, profile: ExperienceFieldProfile, *, evidence_id: str | None = None, adapt: bool = True) -> dict[str, Any]:
        token = str(evidence_id).strip() if evidence_id else None
        if token and token in self.state.evidence:
            return {"accepted": False, "updated": False, "reason": "duplicate_evidence_id", "evidence_id": token}

        self.state.sequence += 1
        if not self.state.center:
            distance = 0.0
            center_delta = self._adapt_center(profile)
        else:
            distance = self._distance_from_center(self.state.center, profile)
            center_delta = self._adapt_center(profile) if adapt and distance <= max(self.min_radius, self.state.radius) else {}
        self.state.last_distance = distance
        self._update_stability(distance)
        event = {
            "type": "attractor_observation",
            "sequence": self.state.sequence,
            "evidence_id": token,
            "distance": round(distance, 6),
            "basin_membership": round(self.basin_membership(distance), 6),
            "radius": round(self.state.radius, 6),
            "recurrence": self.state.recurrence,
            "stability": self.state.stability,
            "center_delta": center_delta,
            "adapted": bool(center_delta),
        }
        if token:
            self.state.evidence[token] = dict(event)
        self.state.history.append(dict(event))
        self.state.history = self.state.history[-self.history_limit:]
        self.save()
        return {"accepted": True, "updated": bool(center_delta), "distance": round(distance, 6), "basin_membership": round(self.basin_membership(distance), 6), "stability": self.state.stability, "recurrence": self.state.recurrence}

    def basin_membership(self, distance: float) -> float:
        radius = max(self.min_radius, self.state.radius)
        return round(math.exp(-max(0.0, float(distance)) / radius), 6)

    def return_pressure(self, distance: float | None = None) -> float:
        observed = self.state.last_distance if distance is None else float(distance)
        return round(max(0.0, min(1.0, observed / max(self.state.radius, self.min_radius))), 6)

    def attractor_strength(self) -> float:
        return round(max(0.0, min(1.0, 0.4 * self.state.recurrence + 0.35 * self.state.stability + 0.25 * self.state.recovery_index)), 6)

    def score_return(self, base_score: float, profile: ExperienceFieldProfile, *, weight: float = 0.25) -> float:
        if not self.state.center:
            return round(float(base_score), 6)
        distance = self._distance_from_center(self.state.center, profile)
        return round(float(base_score) + float(weight) * self.basin_membership(distance), 6)

    def record_perturbation_recovery(self, baseline: ExperienceFieldProfile, perturbed: ExperienceFieldProfile, recovered: ExperienceFieldProfile, *, evidence_id: str | None = None) -> dict[str, Any]:
        token = str(evidence_id).strip() if evidence_id else None
        if token and token in self.state.evidence:
            return {"accepted": False, "updated": False, "reason": "duplicate_evidence_id", "evidence_id": token}
        perturbation_distance = profile_distance(baseline, perturbed)
        recovery_distance = profile_distance(baseline, recovered)
        if perturbation_distance <= 1e-12:
            recovery_index = 1.0 if recovery_distance <= 1e-12 else 0.0
        else:
            recovery_index = max(0.0, min(1.0, 1.0 - recovery_distance / perturbation_distance))
        self.state.sequence += 1
        self.state.recovery_index = round(recovery_index, 6)
        event = {
            "type": "attractor_recovery",
            "sequence": self.state.sequence,
            "evidence_id": token,
            "perturbation_distance": perturbation_distance,
            "recovery_distance": recovery_distance,
            "recovery_index": round(recovery_index, 6),
            "running_recovery_index": self.state.recovery_index,
        }
        if token:
            self.state.evidence[token] = dict(event)
        self.state.history.append(dict(event))
        self.state.history = self.state.history[-self.history_limit:]
        self.save()
        return {"accepted": True, "updated": True, "recovery_index": round(recovery_index, 6), "running_recovery_index": self.state.recovery_index}

    def runtime_state(self) -> dict[str, Any]:
        return {
            "experience_attractor_center": dict(self.state.center),
            "experience_attractor_radius": round(self.state.radius, 6),
            "experience_attractor_distance": round(self.state.last_distance, 6),
            "experience_attractor_recurrence": self.state.recurrence,
            "experience_attractor_stability": self.state.stability,
            "experience_attractor_recovery": self.state.recovery_index,
            "experience_attractor_strength": self.attractor_strength(),
            "experience_attractor_sequence": self.state.sequence,
            "experience_attractor_history": list(self.state.history[-self.history_limit:]),
        }
