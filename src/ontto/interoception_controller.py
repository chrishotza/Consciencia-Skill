from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from .bridge import DynamicStateBridge
from .storage import OntologicalState
from .interoception import InteroceptiveProbe, InteroceptiveSnapshot


@dataclass(frozen=True)
class InteroceptiveActionCandidate:
    signal: float
    predicted_snapshot: InteroceptiveSnapshot
    score: float


class InteroceptiveController:
    """Counterfactual controller driven by an internal-state readout.

    The controller is experimental and default-off at the organism level.
    It scores candidate actions by the predicted post-action operating
    condition. No semantic label is provided to the controller.
    """

    def __init__(self, probe: InteroceptiveProbe | None = None, memory_count: int = 0):
        self.probe = probe or InteroceptiveProbe()
        self.memory_count = max(0, int(memory_count))

    @staticmethod
    def _state_from_snapshot(snapshot) -> OntologicalState:
        return OntologicalState(
            dynamic_state=float(snapshot.state),
            dynamic_prev_state=float(snapshot.previous_state),
            dynamic_memory=float(snapshot.memory),
            dynamic_pressure=float(snapshot.pressure),
            dynamic_attractor_distance=float(snapshot.attractor_distance),
            dynamic_last_input=float(snapshot.last_input),
        )

    def evaluate(
        self,
        bridge: DynamicStateBridge,
        *,
        previous_state: float,
        state: float,
        memory: float,
        pressure: float,
        signals: Iterable[float] = (-1.0, 0.0, 1.0),
        step_index: int = 0,
        mode: str = "full",
        shuffle_seed: int = 0,
    ) -> tuple[InteroceptiveActionCandidate, ...]:
        candidates = []
        baseline_state = OntologicalState(
            dynamic_state=float(state),
            dynamic_prev_state=float(previous_state),
            dynamic_memory=float(memory),
            dynamic_pressure=float(pressure),
            dynamic_attractor_distance=abs(float(state) - bridge.cfg.attractor),
        )
        baseline_snapshot = self.probe.read(
            baseline_state,
            memory_count=self.memory_count,
        )
        baseline_values = baseline_snapshot.to_dict()
        rng = np.random.default_rng(int(shuffle_seed))

        for signal in signals:
            predicted = bridge.advance(
                previous_state=previous_state,
                state=state,
                memory=memory,
                pressure=pressure,
                signal=float(signal),
                steps=1,
                step_index=step_index,
            )
            predicted_state = self._state_from_snapshot(predicted)
            snapshot = self.probe.read(
                predicted_state,
                memory_count=self.memory_count,
            )
            values = snapshot.to_dict()
            if mode == "shuffled":
                keys = list(values)
                permutation = rng.permutation(len(keys))
                values = {key: values[keys[int(permutation[i])]] for i, key in enumerate(keys)}
                operating = 0.5 * values["operating_condition"] + 0.5 * snapshot.prediction_confidence
                score_snapshot = InteroceptiveSnapshot(
                    prediction_error=values["prediction_error"],
                    prediction_confidence=values["prediction_confidence"],
                    dynamic_pressure=values["dynamic_pressure"],
                    attractor_distance=values["attractor_distance"],
                    memory_load=values["memory_load"],
                    dynamic_activity=values["dynamic_activity"],
                    state_change=values["state_change"],
                    operating_condition=operating,
                )
            elif mode == "clamped":
                score_snapshot = baseline_snapshot
            elif mode == "lesion":
                score_snapshot = InteroceptiveSnapshot(
                    **{key: 0.5 for key in baseline_values}
                )
            else:
                score_snapshot = snapshot
            candidates.append(
                InteroceptiveActionCandidate(
                    signal=float(signal),
                    predicted_snapshot=score_snapshot,
                    score=float(score_snapshot.operating_condition),
                )
            )
        return tuple(candidates)

    @staticmethod
    def choose(candidates: tuple[InteroceptiveActionCandidate, ...], *, seed: int = 0) -> InteroceptiveActionCandidate:
        if not candidates:
            raise ValueError("at least one candidate is required")
        return max(candidates, key=lambda candidate: (candidate.score, -abs(candidate.signal), -candidate.signal))
