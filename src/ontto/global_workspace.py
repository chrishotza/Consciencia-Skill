from __future__ import annotations

from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class WorkspaceConfig:
    capacity: int = 2
    broadcast_gain: float = 0.65
    local_gain: float = 0.35

@dataclass(frozen=True)
class WorkspaceSelection:
    indices: tuple[int, ...]
    salience: np.ndarray
    broadcast: np.ndarray

class GlobalWorkspace:
    """Deterministic bounded workspace for causal broadcast experiments."""
    def __init__(self, module_count: int, vector_dim: int, config: WorkspaceConfig):
        if module_count < 2: raise ValueError("module_count must be >= 2")
        if vector_dim < 1: raise ValueError("vector_dim must be >= 1")
        if not 1 <= config.capacity <= module_count: raise ValueError("invalid capacity")
        self.module_count = int(module_count)
        self.vector_dim = int(vector_dim)
        self.config = config

    @staticmethod
    def salience(module_vectors: np.ndarray, reliability: np.ndarray) -> np.ndarray:
        x = np.asarray(module_vectors, dtype=float)
        r = np.asarray(reliability, dtype=float)
        if x.ndim != 2: raise ValueError("module_vectors must be [modules, dimensions]")
        if r.shape != (x.shape[0],): raise ValueError("reliability shape mismatch")
        return np.linalg.norm(x, axis=1) * np.clip(r, 0.0, None)

    def select(self, module_vectors: np.ndarray, reliability: np.ndarray, *, forced_indices: tuple[int, ...] | None = None) -> WorkspaceSelection:
        x = np.asarray(module_vectors, dtype=float)
        if x.shape != (self.module_count, self.vector_dim): raise ValueError("unexpected module_vectors shape")
        sal = self.salience(x, reliability)
        if forced_indices is None:
            order = np.argsort(-sal, kind="mergesort")
            indices = tuple(int(i) for i in order[: self.config.capacity])
        else:
            indices = tuple(int(i) for i in forced_indices)
            if len(indices) != self.config.capacity or len(set(indices)) != len(indices): raise ValueError("forced_indices mismatch")
        weights = sal[list(indices)] + 1e-12
        broadcast = np.average(x[list(indices)], axis=0, weights=weights)
        return WorkspaceSelection(indices=indices, salience=sal, broadcast=broadcast)

    def integrate(self, module_vectors: np.ndarray, selection: WorkspaceSelection, *, broadcast_enabled: bool = True, selected_lesion: int | None = None) -> np.ndarray:
        x = np.asarray(module_vectors, dtype=float).copy()
        if selected_lesion is not None:
            x[int(selected_lesion)] = 0.0
            selected = [i for i in selection.indices if i != int(selected_lesion)]
            if selected:
                weights = selection.salience[selected] + 1e-12
                b = np.average(x[selected], axis=0, weights=weights)
            else: b = np.zeros(self.vector_dim, dtype=float)
        else: b = selection.broadcast
        if not broadcast_enabled: return x
        return self.config.local_gain * x + self.config.broadcast_gain * b[None, :]

    def step(self, module_vectors: np.ndarray, reliability: np.ndarray, *, broadcast_enabled: bool = True, forced_indices: tuple[int, ...] | None = None, selected_lesion: int | None = None) -> tuple[np.ndarray, WorkspaceSelection]:
        selection = self.select(module_vectors, reliability, forced_indices=forced_indices)
        return self.integrate(module_vectors, selection, broadcast_enabled=broadcast_enabled, selected_lesion=selected_lesion), selection