from __future__ import annotations

from dataclasses import dataclass
import numpy as np

ATTENTION_MODULES = (1, 2, 3, 4)
ATTENTION_CODES = {
    1: np.asarray([1.0, 0.0], dtype=float),
    2: np.asarray([0.0, 1.0], dtype=float),
    3: np.asarray([-1.0, 0.0], dtype=float),
    4: np.asarray([0.0, -1.0], dtype=float),
}


@dataclass(frozen=True)
class AttentionAllocation:
    weights: tuple[float, ...]
    predicted: tuple[float, ...]
    selected_index: int


class AttentionSchema:
    """Minimal state-to-attention model with an explicit causal allocation step."""

    def __init__(self, codes: dict[int, np.ndarray] | None = None, temperature: float = 0.20):
        self.codes = {k: np.asarray(v, dtype=float) for k, v in (codes or ATTENTION_CODES).items()}
        if set(self.codes) != set(ATTENTION_MODULES):
            raise ValueError("codebook must cover the attention modules")
        if temperature <= 0:
            raise ValueError("temperature must be positive")
        self.temperature = float(temperature)

    def predict(self, global_state: np.ndarray) -> np.ndarray:
        state = np.asarray(global_state, dtype=float)
        if state.shape != (2,):
            raise ValueError("global_state must be a 2-vector")
        scores = np.asarray([float(np.dot(state, self.codes[i])) for i in ATTENTION_MODULES], dtype=float)
        scores -= np.max(scores)
        exp_scores = np.exp(scores / self.temperature)
        return exp_scores / exp_scores.sum()

    def allocate(
        self,
        global_state: np.ndarray,
        *,
        mode: str = "full",
        rng: np.random.Generator | None = None,
    ) -> AttentionAllocation:
        predicted = self.predict(global_state)
        if mode == "full":
            weights = predicted.copy()
        elif mode == "shuffled":
            weights = predicted[::-1].copy()
        elif mode == "uniform":
            weights = np.full(len(ATTENTION_MODULES), 1.0 / len(ATTENTION_MODULES))
        elif mode == "random":
            if rng is None:
                rng = np.random.default_rng(0)
            weights = rng.dirichlet(np.ones(len(ATTENTION_MODULES)))
        elif mode == "lesion":
            weights = np.full(len(ATTENTION_MODULES), 1.0 / len(ATTENTION_MODULES))
        else:
            raise ValueError(f"unknown attention mode: {mode}")

        selected = int(ATTENTION_MODULES[int(np.argmax(weights))])
        return AttentionAllocation(
            weights=tuple(float(x) for x in weights),
            predicted=tuple(float(x) for x in predicted),
            selected_index=selected,
        )

    @staticmethod
    def target_attention(allocation: AttentionAllocation, target_module: int) -> float:
        try:
            idx = ATTENTION_MODULES.index(int(target_module))
        except ValueError as exc:
            raise ValueError("invalid target module") from exc
        return float(allocation.weights[idx])
