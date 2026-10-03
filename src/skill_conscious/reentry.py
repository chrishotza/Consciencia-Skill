from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping

from .experience_field import ExperienceFieldProfile


RUNTIME_OWNED_KEYS = {
    "experience_field_state",
    "experience_field_history",
    "experience_field_sequence",
    "experience_field_evidence",
    "experience_field_regime_preferences",
}


@dataclass
class ExperienceFieldMemory:
    sample_count: int = 0
    sequence: int = 0
    expected_profile: dict[str, float] = field(default_factory=dict)
    previous_profile: dict[str, float] = field(default_factory=dict)
    regime_preferences: dict[str, float] = field(default_factory=dict)
    evidence: dict[str, dict[str, Any]] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ExperienceFieldReentry:
    """Persistent re-entry layer for the integrated experience field."""

    def __init__(
        self,
        state_path: str | os.PathLike[str],
        *,
        history_limit: int = 32,
        learning_rate: float = 0.25,
        max_step: float = 0.25,
        min_samples: int = 3,
        error_threshold: float = 0.25,
        cooldown: int = 2,
        direction_consistency: float = 1.0,
        reversal_error_multiplier: float = 1.5,
        reversal_sample_multiplier: float = 1.5,
    ) -> None:
        self.path = Path(state_path)
        self.history_limit = max(1, int(history_limit))
        self.learning_rate = max(0.0, min(1.0, float(learning_rate)))
        self.max_step = max(0.0, float(max_step))
        self.min_samples = max(1, int(min_samples))
        self.error_threshold = max(0.0, float(error_threshold))
        self.cooldown = max(0, int(cooldown))
        self.direction_consistency = max(0.0, min(1.0, float(direction_consistency)))
        self.reversal_error_multiplier = max(1.0, float(reversal_error_multiplier))
        self.reversal_sample_multiplier = max(1.0, float(reversal_sample_multiplier))
        self.state = self._load()

    def _load(self) -> ExperienceFieldMemory:
        if not self.path.exists():
            return ExperienceFieldMemory()
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return ExperienceFieldMemory(
            sample_count=int(payload.get("sample_count", 0)),
            sequence=int(payload.get("sequence", 0)),
            expected_profile={str(k): float(v) for k, v in dict(payload.get("expected_profile", {})).items() if isinstance(v, (int, float)) and not isinstance(v, bool)},
            previous_profile={str(k): float(v) for k, v in dict(payload.get("previous_profile", {})).items() if isinstance(v, (int, float)) and not isinstance(v, bool)},
            regime_preferences={str(k): float(v) for k, v in dict(payload.get("regime_preferences", {})).items() if isinstance(v, (int, float)) and not isinstance(v, bool)},
            evidence={str(k): dict(v) for k, v in dict(payload.get("evidence", {})).items() if isinstance(v, Mapping)},
            history=[dict(v) for v in payload.get("history", []) if isinstance(v, Mapping)][-self.history_limit:],
        )

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=".experience-field-", suffix=".json", dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(self.state.to_dict(), handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp, self.path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)

    @staticmethod
    def _profile_dict(profile: ExperienceFieldProfile) -> dict[str, float]:
        return {str(key): float(value) for key, value in profile.to_dict().items() if isinstance(value, (int, float)) and not isinstance(value, bool)}

    @staticmethod
    def _direction(value: float) -> int:
        if value > 1e-12:
            return 1
        if value < -1e-12:
            return -1
        return 0

    def _dedupe_evidence(self, evidence_id: str | None) -> bool:
        if not evidence_id:
            return False
        token = str(evidence_id).strip()
        return bool(token and token in self.state.evidence)

    def observe(self, profile: ExperienceFieldProfile, *, evidence_id: str | None = None, regime: str = "baseline") -> dict[str, Any]:
        token = str(evidence_id).strip() if evidence_id else None
        if self._dedupe_evidence(token):
            return {"accepted": False, "updated": False, "reason": "duplicate_evidence_id", "evidence_id": token}

        self.state.sequence += 1
        self.state.sample_count += 1
        current = self._profile_dict(profile)

        if not self.state.expected_profile:
            self.state.expected_profile = dict(current)
            prediction_error = 0.0
            adaptation = {"updated": False, "reason": "initialized_expectation"}
        else:
            keys = sorted(set(current).intersection(self.state.expected_profile))
            errors = [min(1.0, abs(current[key] - self.state.expected_profile[key])) for key in keys]
            prediction_error = sum(errors) / len(errors) if errors else 0.0
            adaptation = self._adapt_expected(current, prediction_error)

        self.state.previous_profile = dict(current)
        event = {
            "sequence": self.state.sequence,
            "evidence_id": token,
            "regime": str(regime).strip() or "baseline",
            "sample_count": self.state.sample_count,
            "prediction_error": round(prediction_error, 6),
            "expected_profile": dict(self.state.expected_profile),
            "profile": current,
            "expected_adaptation": adaptation,
        }
        if token:
            self.state.evidence[token] = dict(event)
        self.state.history.append(dict(event))
        self.state.history = self.state.history[-self.history_limit:]
        self.save()
        return {
            "accepted": True,
            "updated": bool(adaptation.get("updated", False)),
            "prediction_error": round(prediction_error, 6),
            "expected_adaptation": adaptation,
            "sequence": self.state.sequence,
        }

    def _adapt_expected(self, current: Mapping[str, float], prediction_error: float) -> dict[str, Any]:
        if prediction_error < self.error_threshold:
            return {"updated": False, "reason": "below_error_threshold"}
        if self.state.sample_count < self.min_samples:
            return {"updated": False, "reason": "insufficient_samples"}

        changed: dict[str, float] = {}
        proposed: dict[str, float] = {}
        for key, observed in current.items():
            expected = self.state.expected_profile.get(key, observed)
            delta = max(-self.max_step, min(self.max_step, self.learning_rate * (observed - expected)))
            proposed[key] = expected + delta
            if abs(delta) > 1e-12:
                changed[key] = round(delta, 6)

        if not changed:
            return {"updated": False, "reason": "zero_bounded_delta"}
        self.state.expected_profile = proposed
        return {"updated": True, "delta": changed, "cause": "accumulated_field_observation"}

    def record_consequence(self, regime: str, utility: float, *, evidence_id: str | None = None) -> dict[str, Any]:
        regime = str(regime).strip() or "baseline"
        token = str(evidence_id).strip() if evidence_id else None
        if token and self._dedupe_evidence(token):
            return {"accepted": False, "updated": False, "reason": "duplicate_evidence_id", "evidence_id": token}

        self.state.sequence += 1
        entry = dict(self.state.evidence.get(f"regime:{regime}", {}))
        count = int(entry.get("sample_count", 0)) + 1
        utility_sum = float(entry.get("utility_sum", 0.0)) + float(utility)
        positive_count = int(entry.get("positive_count", 0))
        negative_count = int(entry.get("negative_count", 0))
        direction = self._direction(float(utility))
        if direction > 0:
            positive_count += 1
        elif direction < 0:
            negative_count += 1

        mean_utility = utility_sum / count
        dominant = 1 if positive_count >= negative_count else -1
        consistency = max(positive_count, negative_count) / max(1, count)
        previous_direction = int(entry.get("last_update_direction", 0))
        reversal = previous_direction != 0 and dominant != previous_direction
        threshold = self.error_threshold * (self.reversal_error_multiplier if reversal else 1.0)
        min_samples = int(round(self.min_samples * (self.reversal_sample_multiplier if reversal else 1.0)))
        in_cooldown = int(entry.get("last_update_sequence", 0)) > 0 and self.state.sequence - int(entry.get("last_update_sequence", 0)) <= self.cooldown
        ready = count >= max(1, min_samples) and abs(mean_utility) >= threshold and consistency >= self.direction_consistency and not in_cooldown

        current = float(self.state.regime_preferences.get(regime, 0.0))
        updated = current
        actual_delta = 0.0
        if ready:
            delta = max(-self.max_step, min(self.max_step, self.learning_rate * mean_utility))
            updated = max(-3.0, min(3.0, current + delta))
            actual_delta = updated - current
            if abs(actual_delta) > 1e-12:
                self.state.regime_preferences[regime] = round(updated, 6)
                entry["last_update_direction"] = self._direction(actual_delta)
                entry["last_update_sequence"] = self.state.sequence

        entry.update({"sample_count": count, "utility_sum": round(utility_sum, 6), "mean_utility": round(mean_utility, 6), "positive_count": positive_count, "negative_count": negative_count})
        if abs(actual_delta) > 1e-12:
            entry = {
                "sample_count": 0,
                "utility_sum": 0.0,
                "mean_utility": 0.0,
                "positive_count": 0,
                "negative_count": 0,
                "last_update_direction": self._direction(actual_delta),
                "last_update_sequence": self.state.sequence,
            }
        self.state.evidence[f"regime:{regime}"] = entry
        if token:
            self.state.evidence[token] = {"sequence": self.state.sequence, "regime": regime, "utility": float(utility)}

        update = {
            "sequence": self.state.sequence,
            "regime": regime,
            "utility": float(utility),
            "mean_utility": round(mean_utility, 6),
            "consistency": round(consistency, 6),
            "reversal": reversal,
            "effective_min_samples": max(1, min_samples),
            "effective_threshold": round(threshold, 6),
            "updated": abs(actual_delta) > 1e-12,
            "before": round(current, 6),
            "after": round(updated, 6),
            "delta": round(actual_delta, 6),
        }
        self.state.history.append({"type": "regime_consequence", **update})
        self.state.history = self.state.history[-self.history_limit:]
        self.save()
        return update

    def score_regime(self, base_score: float, regime: str, *, field: ExperienceFieldProfile | None = None, dynamic_weight: float = 0.25, self_relevance_weight: float = 0.25) -> float:
        regime = str(regime).strip() or "baseline"
        score = float(base_score) + float(self.state.regime_preferences.get(regime, 0.0))
        if field is not None:
            score += float(dynamic_weight) * field.dynamic_repertoire
            score += float(self_relevance_weight) * field.self_relevance
        return round(score, 6)

    def sanitized_model_frame(self, frame: Mapping[str, Any]) -> dict[str, Any]:
        result = dict(frame)
        model = result.get("self_model")
        if isinstance(model, Mapping):
            cleaned = dict(model)
            for key in RUNTIME_OWNED_KEYS:
                cleaned.pop(key, None)
            result["self_model"] = cleaned
        return result

    def runtime_state(self) -> dict[str, Any]:
        return {
            "experience_field_state": dict(self.state.previous_profile),
            "experience_field_expected": dict(self.state.expected_profile),
            "experience_field_sequence": self.state.sequence,
            "experience_field_regime_preferences": dict(self.state.regime_preferences),
            "experience_field_evidence": {key: value for key, value in self.state.evidence.items() if not str(key).startswith("regime:")},
            "experience_field_history": list(self.state.history[-self.history_limit:]),
        }
