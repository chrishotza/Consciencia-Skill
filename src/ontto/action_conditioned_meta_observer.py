from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class ActionConditionedMetaPrediction:
    predicted_error: float
    baseline_error: float
    confidence: float
    samples: int


class ActionConditionedMetaObserver:
    """Second-order observer conditioned on the first-order self-model output.

    The target is the absolute prediction error of the first-order
    SelfObserver. Features include the candidate signal and the first-order
    predicted next state, making the meta-model explicitly action-conditioned.
    """

    FEATURE_COUNT = 12

    def __init__(self, ridge: float = 1e-3, max_samples: int = 2048):
        self.ridge = float(ridge)
        self.max_samples = int(max_samples)
        self.features: list[np.ndarray] = []
        self.targets: list[float] = []

    @staticmethod
    def features_for(
        *,
        previous_state: float,
        state: float,
        memory: float,
        pressure: float,
        last_input: float,
        attractor_distance: float,
        steps_delta: int,
        predicted_state: float,
        predicted_displacement: float,
    ) -> np.ndarray:
        signal = float(last_input)
        predicted = float(predicted_state)
        displacement = float(predicted_displacement)
        return np.asarray(
            [
                1.0,
                float(previous_state),
                float(state),
                float(memory),
                float(pressure),
                signal,
                float(attractor_distance),
                float(steps_delta),
                predicted,
                displacement,
                signal * predicted,
                signal * displacement,
            ],
            dtype=float,
        )

    @staticmethod
    def _fit(
        features: list[np.ndarray],
        targets: list[float],
        ridge: float,
    ) -> np.ndarray:
        if not features:
            return np.zeros(
                ActionConditionedMetaObserver.FEATURE_COUNT,
                dtype=float,
            )
        x = np.vstack(features)
        y = np.asarray(targets, dtype=float)
        reg = ridge * np.eye(x.shape[1], dtype=float)
        reg[0, 0] = ridge * 0.1
        try:
            return np.linalg.solve(
                x.T @ x + reg,
                x.T @ y,
            )
        except np.linalg.LinAlgError:
            return np.linalg.pinv(x.T @ x + reg) @ x.T @ y

    def predict_error(
        self,
        *,
        previous_state: float,
        state: float,
        memory: float,
        pressure: float,
        last_input: float,
        attractor_distance: float,
        steps_delta: int,
        predicted_state: float,
        predicted_displacement: float,
    ) -> float:
        x = self.features_for(
            previous_state=previous_state,
            state=state,
            memory=memory,
            pressure=pressure,
            last_input=last_input,
            attractor_distance=attractor_distance,
            steps_delta=steps_delta,
            predicted_state=predicted_state,
            predicted_displacement=predicted_displacement,
        )
        if not self.features:
            return 0.0
        weights = self._fit(self.features, self.targets, self.ridge)
        return float(max(0.0, x @ weights))

    def predict(
        self,
        *,
        previous_state: float,
        state: float,
        memory: float,
        pressure: float,
        last_input: float,
        attractor_distance: float,
        steps_delta: int,
        predicted_state: float,
        predicted_displacement: float,
    ) -> ActionConditionedMetaPrediction:
        predicted = self.predict_error(
            previous_state=previous_state,
            state=state,
            memory=memory,
            pressure=pressure,
            last_input=last_input,
            attractor_distance=attractor_distance,
            steps_delta=steps_delta,
            predicted_state=predicted_state,
            predicted_displacement=predicted_displacement,
        )
        samples = len(self.targets)
        confidence = min(1.0, samples / 32.0)
        baseline = float(np.mean(self.targets)) if self.targets else 0.0
        return ActionConditionedMetaPrediction(
            predicted_error=predicted,
            baseline_error=baseline,
            confidence=confidence,
            samples=samples,
        )

    def observe(
        self,
        *,
        features: np.ndarray,
        prediction_error: float,
    ) -> None:
        self.features.append(np.asarray(features, dtype=float))
        self.targets.append(max(0.0, float(prediction_error)))
        if len(self.features) > self.max_samples:
            self.features.pop(0)
            self.targets.pop(0)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ridge": self.ridge,
            "max_samples": self.max_samples,
            "features": [row.tolist() for row in self.features],
            "targets": list(self.targets),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ActionConditionedMetaObserver":
        observer = cls(
            ridge=float(payload.get("ridge", 1e-3)),
            max_samples=int(payload.get("max_samples", 2048)),
        )
        for row, target in zip(
            payload.get("features", []),
            payload.get("targets", []),
        ):
            observer.observe(
                features=np.asarray(row, dtype=float),
                prediction_error=float(target),
            )
        return observer

    def reset(self) -> None:
        self.features.clear()
        self.targets.clear()
