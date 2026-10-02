from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .attention_controller import AttentionSchema
from .workspace_query import QUERY_CODES, QUERY_MODULES, StateDependentQuery


@dataclass(frozen=True)
class BottleneckDecision:
    target_module: int
    target_action: float
    query_module: int
    query_accuracy: float
    attention_mass: float
    attended_module: int
    masked_score: float
    predicted_action: float
    bottleneck_enabled: bool
    query_mode: str
    attention_mode: str


class CausalQueryBottleneck:
    """State-dependent query + attention bottleneck with a causal action readout."""

    def __init__(
        self,
        *,
        threshold: float = 0.20,
    ):
        if threshold <= 0:
            raise ValueError("threshold must be positive")
        self.threshold = float(threshold)
        self.query = StateDependentQuery()
        self.attention = AttentionSchema()

    @staticmethod
    def _query_broadcast(
        target_module: int,
        rng: np.random.Generator,
        mode: str,
    ) -> np.ndarray:
        if mode == "full":
            return np.asarray(QUERY_CODES[target_module], dtype=float) + rng.normal(0.0, 0.06, size=2)
        if mode == "shuffled":
            b = np.asarray(QUERY_CODES[target_module], dtype=float) + rng.normal(0.0, 0.06, size=2)
            return b[::-1]
        if mode == "zero":
            return np.zeros(2, dtype=float)
        if mode == "random":
            module = int(rng.choice(QUERY_MODULES))
            return np.asarray(QUERY_CODES[module], dtype=float)
        raise ValueError(f"unknown query mode={mode!r}")

    @staticmethod
    def _target_contents(
        target_module: int,
        target_action: float,
        rng: np.random.Generator,
    ) -> np.ndarray:
        values = np.full((6, 2), 0.0, dtype=float)
        for module in QUERY_MODULES:
            # Distractors carry the opposite action code.
            action = target_action if module == target_module else -target_action
            values[module, 0] = action + float(rng.normal(0.0, 0.04))
            values[module, 1] = float(rng.normal(0.0, 0.04))
        values[0] = np.asarray(QUERY_CODES[target_module], dtype=float)
        values[1] = np.asarray([0.0, 0.0], dtype=float)
        return values

    def decide(
        self,
        *,
        target_module: int,
        target_action: float,
        seed: int,
        query_mode: str = "full",
        attention_mode: str = "full",
        bottleneck_enabled: bool = True,
    ) -> BottleneckDecision:
        if target_module not in QUERY_MODULES:
            raise ValueError("invalid target module")
        if target_action not in (-1.0, 1.0):
            raise ValueError("target_action must be -1 or +1")
        rng = np.random.default_rng(seed)

        vectors = self._target_contents(target_module, target_action, rng)
        broadcast = self._query_broadcast(target_module, rng, query_mode)
        query_result = self.query.query(vectors, broadcast)
        attention = self.attention.allocate(
            broadcast,
            mode=attention_mode,
            rng=rng,
        )

        query_module = int(query_result.module_index)
        query_accuracy = float(query_module == target_module)
        attended_module = int(attention.selected_index) + 1
        query_idx = query_module - 2
        attention_mass = float(
            attention.weights[query_idx]
            if 0 <= query_idx < len(attention.weights)
            else 0.0
        )

        if bottleneck_enabled:
            mask = np.zeros(len(QUERY_MODULES), dtype=float)
            mask[query_idx] = 1.0
        else:
            mask = np.ones(len(QUERY_MODULES), dtype=float)

        content = np.asarray(
            [vectors[module, 0] for module in QUERY_MODULES],
            dtype=float,
        )
        # Attention supplies the resource weights; the query supplies access.
        # With the bottleneck, only the queried module can contribute.
        score = float(np.sum(content * np.asarray(attention.weights) * mask))
        predicted_action = (
            1.0 if score >= self.threshold
            else -1.0 if score <= -self.threshold
            else 0.0
        )

        return BottleneckDecision(
            target_module=target_module,
            target_action=target_action,
            query_module=query_module,
            query_accuracy=query_accuracy,
            attention_mass=attention_mass,
            attended_module=attended_module,
            masked_score=score,
            predicted_action=predicted_action,
            bottleneck_enabled=bottleneck_enabled,
            query_mode=query_mode,
            attention_mode=attention_mode,
        )
