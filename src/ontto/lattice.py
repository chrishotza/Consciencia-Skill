from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

import numpy as np


BooleanOp = Literal["xor", "and", "or"]


@dataclass(frozen=True)
class LatticeConfig:
    """Computational lattice substrate inspired by the source material."""
    size: int = 16
    coupling: float = 0.22
    leak: float = 0.08
    input_gain: float = 0.85
    nonlinearity: float = 1.20
    noise_std: float = 0.0

    def validate(self) -> None:
        if self.size < 3:
            raise ValueError("size must be >= 3")
        if self.coupling < 0.0:
            raise ValueError("coupling must be >= 0")
        if not 0.0 <= self.leak < 1.0:
            raise ValueError("leak must be in [0, 1)")
        if self.input_gain < 0.0:
            raise ValueError("input_gain must be >= 0")
        if self.nonlinearity <= 0.0:
            raise ValueError("nonlinearity must be > 0")
        if self.noise_std < 0.0:
            raise ValueError("noise_std must be >= 0")


class LatticeComputer:
    """Distributed storage plus local recurrent computation."""

    def __init__(self, config: LatticeConfig | None = None, *, seed: int = 0):
        self.config = config or LatticeConfig()
        self.config.validate()
        self.rng = np.random.default_rng(seed)
        self.state = np.zeros((self.config.size, self.config.size), dtype=float)
        self.step_count = 0

    @property
    def size(self) -> int:
        return self.config.size

    def reset(self) -> None:
        self.state.fill(0.0)
        self.step_count = 0

    def copy(self) -> "LatticeComputer":
        other = LatticeComputer(self.config, seed=0)
        other.state = self.state.copy()
        other.step_count = self.step_count
        return other

    def _neighbor_mean(self) -> np.ndarray:
        s = self.state
        return (
            np.roll(s, 1, axis=0)
            + np.roll(s, -1, axis=0)
            + np.roll(s, 1, axis=1)
            + np.roll(s, -1, axis=1)
        ) / 4.0

    def step(self, external: np.ndarray | None = None) -> np.ndarray:
        if external is None:
            external_field = np.zeros_like(self.state)
        else:
            external_field = np.asarray(external, dtype=float)
            if external_field.shape != self.state.shape:
                raise ValueError("external field must match lattice shape")

        neighbor = self._neighbor_mean()
        drive = (
            (1.0 - self.config.leak) * self.state
            + self.config.coupling * (neighbor - self.state)
            + self.config.input_gain * external_field
        )
        if self.config.noise_std:
            drive += self.rng.normal(
                0.0, self.config.noise_std, size=self.state.shape
            )

        self.state = np.tanh(self.config.nonlinearity * drive)
        self.step_count += 1
        return self.state.copy()

    def run(self, external_sequence: np.ndarray | None = None, *, steps: int = 1) -> np.ndarray:
        if external_sequence is None:
            sequence = np.zeros((steps, self.size, self.size), dtype=float)
        else:
            sequence = np.asarray(external_sequence, dtype=float)
            if sequence.ndim != 3 or sequence.shape[1:] != self.state.shape:
                raise ValueError("external_sequence must have shape (steps, size, size)")
            steps = sequence.shape[0]

        trajectory = np.zeros((steps, self.size, self.size), dtype=float)
        for i in range(steps):
            trajectory[i] = self.step(sequence[i])
        return trajectory

    def write(self, field: np.ndarray, *, gain: float = 1.0) -> None:
        field = np.asarray(field, dtype=float)
        if field.shape != self.state.shape:
            raise ValueError("field must match lattice shape")
        self.state = np.tanh(self.state + float(gain) * field)

    def encode_bits(self, bits: np.ndarray, *, row: int) -> None:
        bits = np.asarray(bits, dtype=int).ravel()
        if bits.size > self.size:
            raise ValueError("bit sequence exceeds lattice width")
        if not 0 <= row < self.size:
            raise ValueError("row out of range")
        if not np.all(np.isin(bits, [0, 1])):
            raise ValueError("bits must be binary")

        self.state[row, :] = 0.0
        self.state[row, : bits.size] = np.where(bits > 0, 1.0, -1.0)

    def decode_bits(self, *, row: int, width: int) -> np.ndarray:
        if not 0 <= row < self.size:
            raise ValueError("row out of range")
        if not 0 < width <= self.size:
            raise ValueError("width must be in [1, size]")
        return (self.state[row, :width] >= 0.0).astype(int)

    def local_boolean_gate(
        self,
        *,
        left_row: int,
        right_row: int,
        output_row: int,
        width: int,
        op: BooleanOp,
    ) -> None:
        a = self.decode_bits(row=left_row, width=width)
        b = self.decode_bits(row=right_row, width=width)
        if op == "xor":
            result = np.logical_xor(a, b).astype(int)
        elif op == "and":
            result = np.logical_and(a, b).astype(int)
        elif op == "or":
            result = np.logical_or(a, b).astype(int)
        else:
            raise ValueError(f"unsupported Boolean op: {op}")
        self.encode_bits(result, row=output_row)

    def coherence(self) -> float:
        neighbor = self._neighbor_mean()
        disagreement = float(np.mean(np.abs(self.state - neighbor)))
        return float(np.clip(1.0 - disagreement, -1.0, 1.0))

    def redundancy(self) -> float:
        s = self.state
        centered = s - float(np.mean(s))
        neighbor = self._neighbor_mean()
        neighbor_centered = neighbor - float(np.mean(neighbor))
        denom = float(np.linalg.norm(centered) * np.linalg.norm(neighbor_centered))
        if denom < 1e-12:
            return 1.0
        return float(
            np.clip(
                np.dot(centered.ravel(), neighbor_centered.ravel()) / denom,
                -1.0,
                1.0,
            )
        )

    def perturbation_spread(
        self,
        *,
        row: int,
        col: int,
        amplitude: float = 1.0,
        steps: int = 6,
        threshold: float = 1e-3,
    ) -> dict[str, float]:
        baseline = self.state.copy()
        perturbed = self.copy()
        perturbed.state[row, col] += float(amplitude)
        for _ in range(steps):
            perturbed.step()

        delta = np.abs(perturbed.state - baseline)
        self.state = perturbed.state
        self.step_count = perturbed.step_count
        affected = int(np.count_nonzero(delta > threshold))
        return {
            "affected_cells": float(affected),
            "affected_fraction": float(affected / self.state.size),
            "mean_change": float(np.mean(delta)),
            "max_change": float(np.max(delta)),
        }

    def lesion(self, mask: np.ndarray) -> None:
        mask = np.asarray(mask, dtype=bool)
        if mask.shape != self.state.shape:
            raise ValueError("lesion mask must match lattice shape")
        self.state[mask] = 0.0

    def summary(self) -> dict[str, Any]:
        return {
            "config": asdict(self.config),
            "step_count": int(self.step_count),
            "coherence": self.coherence(),
            "redundancy": self.redundancy(),
            "mean_abs_state": float(np.mean(np.abs(self.state))),
            "state_variance": float(np.var(self.state)),
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "config": asdict(self.config),
            "step_count": int(self.step_count),
            "state": self.state.tolist(),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "LatticeComputer":
        obj = cls(LatticeConfig(**payload["config"]), seed=0)
        state = np.asarray(payload["state"], dtype=float)
        if state.shape != obj.state.shape:
            raise ValueError("serialized state shape does not match config")
        obj.state = state.copy()
        obj.step_count = int(payload["step_count"])
        return obj
