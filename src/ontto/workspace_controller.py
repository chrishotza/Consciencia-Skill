from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .global_workspace import GlobalWorkspace, WorkspaceConfig, WorkspaceSelection
from .storage import OntologicalState
from .trajectory_selector import TrajectoryCandidate

@dataclass(frozen=True)
class WorkspaceRuntimeConfig:
    capacity: int = 2
    broadcast_gain: float = 0.65
    local_gain: float = 0.35
    influence_weight: float = 0.35
    broadcast_enabled: bool = True
    lesion_index: int | None = None

class WorkspaceTrajectoryController:
    """Maps organism internal signals into a bounded workspace that biases trajectory selection."""

    def __init__(self, cfg: WorkspaceRuntimeConfig):
        self.cfg = cfg
        self.workspace = GlobalWorkspace(
            module_count=6,
            vector_dim=2,
            config=WorkspaceConfig(
                capacity=cfg.capacity,
                broadcast_gain=cfg.broadcast_gain,
                local_gain=cfg.local_gain,
            ),
        )

    @staticmethod
    def _clip(x: float) -> float:
        return float(np.tanh(float(x)))

    def module_vectors(self, state: OntologicalState) -> tuple[np.ndarray, np.ndarray]:
        vectors = np.asarray([
            [self._clip(state.dynamic_state), self._clip(state.dynamic_prev_state)],
            [self._clip(state.self_prediction), self._clip(state.self_prediction_gain)],
            [self._clip(state.dynamic_memory), self._clip(state.memory_strength)],
            [self._clip(state.dynamic_pressure), self._clip(state.dynamic_attractor_distance)],
            [self._clip(state.self_prediction_confidence), self._clip(state.self_prediction_error)],
            [self._clip(state.dynamic_last_input), self._clip(state.dynamic_state - state.dynamic_prev_state)],
        ], dtype=float)
        reliability = np.asarray([
            1.0,
            max(0.05, min(1.0, state.self_prediction_confidence)),
            max(0.05, min(1.0, state.memory_strength)),
            1.0 / (1.0 + abs(float(state.dynamic_pressure))),
            max(0.05, min(1.0, state.self_prediction_confidence)),
            1.0,
        ], dtype=float)
        return vectors, reliability

    def select(self, state: OntologicalState) -> WorkspaceSelection:
        vectors, reliability = self.module_vectors(state)
        return self.workspace.select(vectors, reliability)

    def candidate_vector(self, candidate: TrajectoryCandidate) -> np.ndarray:
        return np.asarray([
            self._clip(candidate.prediction.predicted_state),
            self._clip(candidate.displacement),
        ], dtype=float)

    def choose(self, state: OntologicalState, candidates: tuple[TrajectoryCandidate, ...]) -> tuple[TrajectoryCandidate, dict[str, object]]:
        if not candidates:
            raise ValueError('at least one candidate is required')
        selection = self.select(state)
        vectors, _ = self.module_vectors(state)
        if self.cfg.broadcast_enabled:
            if self.cfg.lesion_index is None:
                broadcast = selection.broadcast
            else:
                selected = [i for i in selection.indices if i != self.cfg.lesion_index]
                if selected:
                    weights = selection.salience[selected] + 1e-12
                    broadcast = np.average(vectors[selected], axis=0, weights=weights)
                else:
                    broadcast = np.zeros(2, dtype=float)
        else:
            broadcast = np.zeros(2, dtype=float)

        scored = []
        influence = float(max(0.0, min(1.0, self.cfg.influence_weight)))
        for candidate in candidates:
            local = float(candidate.score)
            vec = self.candidate_vector(candidate)
            broadcast_alignment = float(1.0 / (1.0 + np.linalg.norm(vec - broadcast)))
            combined = (1.0 - influence) * local + influence * broadcast_alignment
            scored.append((combined, local, candidate, broadcast_alignment))
        _, _, chosen, chosen_alignment = max(
            scored, key=lambda row: (row[0], -abs(row[2].signal))
        )
        return chosen, {
            'enabled': True,
            'capacity': self.cfg.capacity,
            'broadcast_enabled': self.cfg.broadcast_enabled,
            'influence_weight': influence,
            'selected_modules': list(selection.indices),
            'selected_source_lesion': self.cfg.lesion_index,
            'module_salience': selection.salience.tolist(),
            'broadcast': [float(x) for x in broadcast],
            'candidate_scores': [
                {'signal': float(s[2].signal), 'base_score': float(s[1]), 'broadcast_alignment': float(s[3]), 'combined_score': float(s[0])}
                for s in scored
            ],
            'chosen_signal': float(chosen.signal),
            'chosen_broadcast_alignment': float(chosen_alignment),
        }