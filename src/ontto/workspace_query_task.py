from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .attention_controller import AttentionSchema
from .storage import OntologicalState
from .trajectory_selector import TrajectoryCandidate
from .workspace_query import QUERY_CODES, QUERY_MODULES, StateDependentQuery


@dataclass(frozen=True)
class PersistentQueryTaskResult:
    target_module: int
    target_action: float
    query_module: int
    query_accuracy: float
    attention_module: int
    attention_mass: float
    predicted_action: float
    action_accuracy: float
    access_strength: float
    bottleneck_enabled: bool
    query_mode: str
    attention_mode: str


class PersistentQueryTaskController:
    """Internal task-level integration of query, attention, and trajectory selection."""

    def __init__(
        self,
        *,
        threshold: float = 0.20,
        task_weight: float = 0.35,
        seed_offset: int = 0,
    ):
        if threshold <= 0:
            raise ValueError("threshold must be positive")
        if task_weight < 0:
            raise ValueError("task_weight must be non-negative")
        self.threshold = float(threshold)
        self.task_weight = float(task_weight)
        self.seed_offset = int(seed_offset)
        self.query = StateDependentQuery()
        self.attention = AttentionSchema()

    def _episode(
        self,
        state: OntologicalState,
        *,
        step_index: int,
        seed: int,
    ) -> tuple[int, float, np.ndarray, np.ndarray]:
        idx = (
            abs(int(step_index))
            + abs(int(self.seed_offset))
            + abs(int(round(state.dynamic_memory * 7.0)))
        ) % len(QUERY_MODULES)
        target_module = int(QUERY_MODULES[idx])

        parity = (
            abs(int(step_index))
            + abs(int(round(state.dynamic_pressure * 11.0)))
            + abs(int(round(state.dynamic_state * 13.0)))
            + abs(int(self.seed_offset))
        )
        target_action = 1.0 if parity % 2 == 0 else -1.0

        rng = np.random.default_rng(seed)
        route_noise = 0.03 * np.asarray(
            [np.tanh(state.dynamic_last_input), np.tanh(state.dynamic_prev_state)],
            dtype=float,
        )
        route = np.asarray(QUERY_CODES[target_module], dtype=float) + route_noise

        vectors = np.zeros((6, 2), dtype=float)
        vectors[0] = route
        for module in QUERY_MODULES:
            action = target_action if module == target_module else -target_action
            vectors[module, 0] = action + float(rng.normal(0.0, 0.03))
            vectors[module, 1] = float(rng.normal(0.0, 0.03))
        return target_module, target_action, vectors, route

    def choose(
        self,
        state: OntologicalState,
        candidates: tuple[TrajectoryCandidate, ...],
        *,
        seed: int,
        query_mode: str = "full",
        attention_mode: str = "full",
        bottleneck_enabled: bool = True,
        lesion_target: bool = False,
    ) -> tuple[TrajectoryCandidate, PersistentQueryTaskResult]:
        if not candidates:
            raise ValueError("at least one candidate is required")
        if query_mode not in {"full", "shuffled", "zero", "random"}:
            raise ValueError(f"unknown query_mode={query_mode!r}")
        if attention_mode not in {"full", "shuffled", "uniform", "random"}:
            raise ValueError(f"unknown attention_mode={attention_mode!r}")

        target_module, target_action, vectors, route = self._episode(
            state,
            step_index=state.dynamic_steps,
            seed=seed,
        )

        if query_mode == "shuffled":
            broadcast = route[::-1]
        elif query_mode == "zero":
            broadcast = np.zeros(2, dtype=float)
        elif query_mode == "random":
            rng = np.random.default_rng(seed + 17)
            module = int(rng.choice(QUERY_MODULES))
            broadcast = np.asarray(QUERY_CODES[module], dtype=float)
        else:
            broadcast = route

        query_result = self.query.query(vectors, broadcast)
        attention = self.attention.allocate(
            broadcast,
            mode=attention_mode,
            rng=np.random.default_rng(seed + 29),
        )

        query_module = int(query_result.module_index)
        attention_module = int(attention.selected_index) + 1
        query_idx = query_module - 2
        attention_mass = float(
            attention.weights[query_idx]
            if 0 <= query_idx < len(attention.weights)
            else 0.0
        )

        content = np.asarray(
            [vectors[module, 0] for module in QUERY_MODULES],
            dtype=float,
        )
        if bottleneck_enabled and 0 <= query_idx < len(QUERY_MODULES):
            mask = np.eye(len(QUERY_MODULES))[query_idx]
        else:
            mask = np.ones(len(QUERY_MODULES), dtype=float)
        if lesion_target and 0 <= (target_module - 2) < len(QUERY_MODULES):
            mask = mask.copy()
            mask[target_module - 2] = 0.0
        score = float(np.sum(content * np.asarray(attention.weights) * mask))

        predicted_action = (
            1.0 if score >= self.threshold
            else -1.0 if score <= -self.threshold
            else 0.0
        )
        action_accuracy = float(predicted_action == target_action)
        query_accuracy = float(query_module == target_module)
        access_strength = (
            float(attention_mass * abs(content[query_idx]))
            if 0 <= query_idx < len(content)
            else 0.0
        )

        scored = []
        for candidate in candidates:
            local = float(candidate.score)
            support = (
                self.task_weight * access_strength
                if predicted_action == float(candidate.signal)
                else -self.task_weight * access_strength
            )
            scored.append((local + support, local, candidate, support))
        _, _, chosen, _ = max(
            scored,
            key=lambda row: (row[0], -abs(row[2].signal)),
        )

        return chosen, PersistentQueryTaskResult(
            target_module=target_module,
            target_action=target_action,
            query_module=query_module,
            query_accuracy=query_accuracy,
            attention_module=attention_module,
            attention_mass=attention_mass,
            predicted_action=predicted_action,
            action_accuracy=action_accuracy,
            access_strength=access_strength,
            bottleneck_enabled=bottleneck_enabled,
            query_mode=query_mode,
            attention_mode=attention_mode,
        )
