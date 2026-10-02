from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from .attention_controller import AttentionSchema
from .workspace_controller import WorkspaceTrajectoryController, WorkspaceRuntimeConfig
from .workspace_query import StateDependentQuery, QUERY_CODES, QUERY_MODULES
from .storage import OntologicalState
from .trajectory_selector import TrajectoryCandidate


@dataclass(frozen=True)
class SelectiveAccessResult:
    chosen_signal: float
    query_module: int
    query_distance: float
    query_value: float
    attention_module: int
    attention_mass: float
    attention_weights: tuple[float, ...]
    access_strength: float
    workspace_control: dict[str, object]
    query_mode: str
    attention_mode: str


class WorkspaceSelectiveAccessController:
    """Combines I5.2 state-dependent querying with I5.3 attention allocation."""

    def __init__(
        self,
        workspace_cfg: WorkspaceRuntimeConfig,
        *,
        query_mode: str = "full",
        attention_mode: str = "full",
        access_weight: float = 0.35,
    ):
        if query_mode not in {"full", "shuffled", "zero", "random", "lesion"}:
            raise ValueError(f"unknown query_mode={query_mode!r}")
        if attention_mode not in {"full", "shuffled", "uniform", "random", "lesion"}:
            raise ValueError(f"unknown attention_mode={attention_mode!r}")
        if access_weight < 0:
            raise ValueError("access_weight must be non-negative")
        self.workspace_controller = WorkspaceTrajectoryController(workspace_cfg)
        self.query = StateDependentQuery()
        self.attention = AttentionSchema()
        self.query_mode = query_mode
        self.attention_mode = attention_mode
        self.access_weight = float(access_weight)

    def _broadcast(
        self,
        state: OntologicalState,
        *,
        selection,
        vectors: np.ndarray,
        rng: np.random.Generator,
    ) -> np.ndarray:
        if self.query_mode == "full":
            return np.asarray(selection.broadcast, dtype=float)
        if self.query_mode == "shuffled":
            return np.asarray(selection.broadcast, dtype=float)[::-1]
        if self.query_mode == "zero":
            return np.zeros(2, dtype=float)
        if self.query_mode == "random":
            module = int(rng.choice(QUERY_MODULES))
            return np.asarray(QUERY_CODES[module], dtype=float)
        selected = list(selection.indices)
        if self.workspace_controller.cfg.lesion_index is not None:
            selected = [i for i in selected if i != self.workspace_controller.cfg.lesion_index]
        if not selected:
            return np.zeros(2, dtype=float)
        weights = selection.salience[selected] + 1e-12
        return np.average(vectors[selected], axis=0, weights=weights)

    def choose(
        self,
        state: OntologicalState,
        candidates: tuple[TrajectoryCandidate, ...],
        *,
        seed: int,
    ) -> tuple[TrajectoryCandidate, SelectiveAccessResult]:
        if not candidates:
            raise ValueError("at least one candidate is required")

        vectors, reliability = self.workspace_controller.module_vectors(state)
        selection = self.workspace_controller.workspace.select(vectors, reliability)
        rng = np.random.default_rng(seed)
        broadcast = self._broadcast(
            state,
            selection=selection,
            vectors=vectors,
            rng=rng,
        )
        query_result = self.query.query(vectors, broadcast)
        attention_alloc = self.attention.allocate(
            broadcast,
            mode=self.attention_mode,
            rng=rng,
        )
        attention_module = int(attention_alloc.selected_index) + 1
        attention_index = query_result.module_index - 2
        attention_mass = float(
            attention_alloc.weights[attention_index]
            if 0 <= attention_index < len(attention_alloc.weights)
            else 0.0
        )
        query_value = float(np.clip(vectors[query_result.module_index, 0], -1.0, 1.0))
        access_strength = float(attention_mass * abs(query_value))

        scored = []
        for candidate in candidates:
            local = float(candidate.score)
            access_bonus = (
                self.access_weight
                * attention_mass
                * query_value
                * float(candidate.signal)
            )
            combined = local + access_bonus
            scored.append((combined, local, candidate, access_bonus))

        _, _, chosen, _ = max(
            scored,
            key=lambda row: (row[0], -abs(row[2].signal)),
        )

        workspace_control = {
            "enabled": True,
            "capacity": self.workspace_controller.cfg.capacity,
            "selected_modules": list(selection.indices),
            "module_salience": selection.salience.tolist(),
            "broadcast": [float(x) for x in broadcast],
            "query_mode": self.query_mode,
            "attention_mode": self.attention_mode,
        }
        result = SelectiveAccessResult(
            chosen_signal=float(chosen.signal),
            query_module=int(query_result.module_index),
            query_distance=float(query_result.distance),
            query_value=query_value,
            attention_module=attention_module,
            attention_mass=attention_mass,
            attention_weights=tuple(float(x) for x in attention_alloc.weights),
            access_strength=access_strength,
            workspace_control=workspace_control,
            query_mode=self.query_mode,
            attention_mode=self.attention_mode,
        )
        return chosen, result
