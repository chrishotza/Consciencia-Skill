from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from .interoception import InteroceptiveSnapshot


@dataclass(frozen=True)
class InteroceptiveMetaPrediction:
    predicted_error: float
    baseline_error: float
    confidence: float
    samples: int


class InteroceptiveMetaObserver:
    """Second-order model of first-order interoceptive prediction error.

    The target is the absolute discrepancy between the operating condition
    predicted by the interoceptive controller and the operating condition
    observed after the action is actually executed in the world model.

    This is a computational metacognition primitive, not a consciousness score.
    """

    FEATURE_COUNT = 12

    @staticmethod
    def features_for(
        *,
        snapshot: InteroceptiveSnapshot,
        action: float,
        predicted_operating_condition: float,
    ) -> np.ndarray:
        return np.asarray(
            [
                1.0,
                float(snapshot.prediction_error),
                float(snapshot.prediction_confidence),
                float(snapshot.dynamic_pressure),
                float(snapshot.attractor_distance),
                float(snapshot.memory_load),
                float(snapshot.dynamic_activity),
                float(snapshot.state_change),
                float(snapshot.operating_condition),
                float(action),
                float(predicted_operating_condition),
                abs(float(action)),
            ],
            dtype=float,
        )

    def __init__(self, ridge: float = 1e-3, max_samples: int = 2048):
        self.ridge = float(ridge)
        self.max_samples = int(max_samples)
        self.features: list[np.ndarray] = []
        self.targets: list[float] = []

    @staticmethod
    def _fit(
        features: list[np.ndarray],
        targets: list[float],
        ridge: float,
    ) -> np.ndarray:
        if not features:
            return np.zeros(InteroceptiveMetaObserver.FEATURE_COUNT, dtype=float)
        x = np.vstack(features)
        y = np.asarray(targets, dtype=float)
        reg = ridge * np.eye(x.shape[1], dtype=float)
        reg[0, 0] = ridge * 0.1
        try:
            return np.linalg.solve(x.T @ x + reg, x.T @ y)
        except np.linalg.LinAlgError:
            return np.linalg.pinv(x.T @ x + reg) @ x.T @ y

    def predict_error(
        self,
        *,
        snapshot: InteroceptiveSnapshot,
        action: float,
        predicted_operating_condition: float,
    ) -> float:
        x = self.features_for(
            snapshot=snapshot,
            action=action,
            predicted_operating_condition=predicted_operating_condition,
        )
        if not self.features:
            return 0.0
        weights = self._fit(self.features, self.targets, self.ridge)
        return float(np.clip(x @ weights, 0.0, 1.0))

    def predict(
        self,
        *,
        snapshot: InteroceptiveSnapshot,
        action: float,
        predicted_operating_condition: float,
    ) -> InteroceptiveMetaPrediction:
        predicted = self.predict_error(
            snapshot=snapshot,
            action=action,
            predicted_operating_condition=predicted_operating_condition,
        )
        samples = len(self.targets)
        baseline = float(np.mean(self.targets)) if self.targets else 0.0
        return InteroceptiveMetaPrediction(
            predicted_error=predicted,
            baseline_error=baseline,
            confidence=min(1.0, samples / 64.0),
            samples=samples,
        )

    def observe(
        self,
        *,
        snapshot: InteroceptiveSnapshot,
        action: float,
        predicted_operating_condition: float,
        actual_operating_condition: float,
    ) -> float:
        prediction_error = abs(
            float(actual_operating_condition)
            - float(predicted_operating_condition)
        )
        self.features.append(
            self.features_for(
                snapshot=snapshot,
                action=action,
                predicted_operating_condition=predicted_operating_condition,
            )
        )
        self.targets.append(float(np.clip(prediction_error, 0.0, 1.0)))
        if len(self.features) > self.max_samples:
            self.features.pop(0)
            self.targets.pop(0)
        return prediction_error

    def absolute_error(
        self,
        *,
        predicted_error: float,
        actual_error: float,
    ) -> float:
        return abs(float(predicted_error) - float(actual_error))

    def to_dict(self) -> dict[str, Any]:
        return {
            "ridge": self.ridge,
            "max_samples": self.max_samples,
            "features": [row.tolist() for row in self.features],
            "targets": list(self.targets),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "InteroceptiveMetaObserver":
        observer = cls(
            ridge=float(payload.get("ridge", 1e-3)),
            max_samples=int(payload.get("max_samples", 2048)),
        )
        for row, target in zip(
            payload.get("features", []),
            payload.get("targets", []),
        ):
            observer.features.append(np.asarray(row, dtype=float))
            observer.targets.append(float(np.clip(float(target), 0.0, 1.0)))
        return observer

    def permuted(self, seed: int) -> "InteroceptiveMetaObserver":
        rng = np.random.default_rng(int(seed))
        observer = self.from_dict(self.to_dict())
        if len(observer.targets) > 1:
            observer.targets = list(rng.permutation(observer.targets))
        return observer

    def reset(self) -> None:
        self.features.clear()
        self.targets.clear()
