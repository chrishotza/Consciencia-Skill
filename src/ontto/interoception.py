from __future__ import annotations

from dataclasses import asdict, dataclass
from math import exp, isfinite
from typing import Any

from .storage import OntologicalState


def _bounded(value: float, scale: float = 1.0) -> float:
    value = float(value)
    if not isfinite(value):
        return 0.0
    scale = max(float(scale), 1e-12)
    x = value / scale
    return 1.0 / (1.0 + exp(-2.0 * x))


@dataclass(frozen=True)
class InteroceptiveSnapshot:
    prediction_error: float
    prediction_confidence: float
    dynamic_pressure: float
    attractor_distance: float
    memory_load: float
    dynamic_activity: float
    state_change: float
    operating_condition: float

    def to_dict(self) -> dict[str, float]:
        return {k: float(v) for k, v in asdict(self).items()}


class InteroceptiveProbe:
    """Read-only instrumentation of internal runtime variables.

    The probe does not change organism state and does not define a
    consciousness score. It provides bounded internal-state signals that can
    later be used by preregistered regulation/interoception protocols.
    """

    def __init__(self, memory_limit: int = 12):
        if int(memory_limit) <= 0:
            raise ValueError("memory_limit must be > 0")
        self.memory_limit = int(memory_limit)

    def read(
        self,
        state: OntologicalState,
        *,
        memory_count: int = 0,
    ) -> InteroceptiveSnapshot:
        prediction_error = max(0.0, min(1.0, float(state.self_prediction_error)))
        confidence = max(0.0, min(1.0, float(state.self_prediction_confidence)))
        pressure = _bounded(state.dynamic_pressure)
        attractor = _bounded(abs(state.dynamic_attractor_distance))
        memory_load = max(0.0, min(1.0, float(memory_count) / self.memory_limit))
        dynamic_activity = _bounded(abs(state.dynamic_state) + abs(state.dynamic_memory))
        state_change = _bounded(
            abs(float(state.dynamic_state) - float(state.dynamic_prev_state))
        )
        operating_condition = (
            0.25 * (1.0 - prediction_error)
            + 0.20 * confidence
            + 0.20 * (1.0 - pressure)
            + 0.15 * (1.0 - attractor)
            + 0.10 * (1.0 - memory_load)
            + 0.10 * (1.0 - state_change)
        )
        operating_condition = max(0.0, min(1.0, operating_condition))
        return InteroceptiveSnapshot(
            prediction_error=prediction_error,
            prediction_confidence=confidence,
            dynamic_pressure=pressure,
            attractor_distance=attractor,
            memory_load=memory_load,
            dynamic_activity=dynamic_activity,
            state_change=state_change,
            operating_condition=operating_condition,
        )

    def describe(self, state: OntologicalState, *, memory_count: int = 0) -> dict[str, Any]:
        return self.read(state, memory_count=memory_count).to_dict()
