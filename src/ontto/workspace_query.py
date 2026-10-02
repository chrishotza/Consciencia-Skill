from __future__ import annotations

from dataclasses import dataclass
import numpy as np

QUERY_MODULES = (2, 3, 4, 5)
QUERY_CODES = {
    2: np.asarray([1.0, 0.0], dtype=float),
    3: np.asarray([0.0, 1.0], dtype=float),
    4: np.asarray([-1.0, 0.0], dtype=float),
    5: np.asarray([0.0, -1.0], dtype=float),
}

@dataclass(frozen=True)
class QueryResult:
    module_index: int
    distance: float
    broadcast: tuple[float, float]

class StateDependentQuery:
    """Queries a module by matching global workspace state to a fixed codebook."""

    def __init__(self, codes: dict[int, np.ndarray] | None = None):
        self.codes = {k: np.asarray(v, dtype=float) for k, v in (codes or QUERY_CODES).items()}
        if set(self.codes) != set(QUERY_MODULES):
            raise ValueError("codebook must cover the four query modules")

    def query(self, module_vectors: np.ndarray, broadcast: np.ndarray) -> QueryResult:
        x = np.asarray(module_vectors, dtype=float)
        b = np.asarray(broadcast, dtype=float)
        if x.ndim != 2 or x.shape[1] != 2:
            raise ValueError("module_vectors must be [modules, 2]")
        if b.shape != (2,):
            raise ValueError("broadcast must be a 2-vector")
        distances = {i: float(np.linalg.norm(b - code)) for i, code in self.codes.items()}
        chosen = min(distances, key=lambda i: (distances[i], i))
        return QueryResult(
            module_index=int(chosen),
            distance=float(distances[chosen]),
            broadcast=(float(b[0]), float(b[1])),
        )

    def target_value(self, module_vectors: np.ndarray, result: QueryResult) -> float:
        x = np.asarray(module_vectors, dtype=float)
        if result.module_index >= x.shape[0]:
            raise IndexError(result.module_index)
        return float(x[result.module_index, 0])