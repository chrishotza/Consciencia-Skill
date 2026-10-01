from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np

from .dynamics import Config, simulate


@dataclass(frozen=True)
class DynamicSnapshot:
    """Observable state produced by one bridge advancement."""

    previous_state: float
    state: float
    memory: float
    pressure: float
    attractor_distance: float
    last_input: float
    steps: int

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


class DynamicStateBridge:
    """Bridge organism events into the scalar research dynamics.

    The bridge deliberately does not infer semantics, valence, intelligence, or
    consciousness from text. A wake event supplies an explicit bounded scalar
    signal; DREAM and autonomous cycles can use zero input. This keeps the
    integration auditable and makes the signal policy an experimental variable.
    """

    def __init__(self, cfg: Config | None = None, seed: int = 7001):
        self.cfg = cfg or Config()
        self.seed = int(seed)

    def advance(
        self,
        *,
        previous_state: float,
        state: float,
        memory: float,
        pressure: float,
        signal: float,
        steps: int,
        step_index: int = 0,
    ) -> DynamicSnapshot:
        if steps < 1:
            raise ValueError("steps must be >= 1")
        if step_index < 0:
            raise ValueError("step_index must be >= 0")

        bounded_signal = float(np.clip(signal, -1.0, 1.0))
        previous = float(previous_state)
        current = float(state)
        current_memory = float(memory)
        current_pressure = float(pressure)

        for offset in range(steps):
            run = simulate(
                np.asarray([0.0, bounded_signal, bounded_signal]),
                self.cfg,
                seed=self.seed + step_index + offset,
                initial_prev_state=previous,
                initial_state=current,
                initial_memory=current_memory,
                initial_pressure=current_pressure,
            )

            previous = current
            current = float(run["state"][2])
            current_memory = float(run["memory"][2])
            current_pressure = float(run["pressure"][2])

        return DynamicSnapshot(
            previous_state=previous,
            state=current,
            memory=current_memory,
            pressure=current_pressure,
            attractor_distance=abs(current - float(self.cfg.attractor)),
            last_input=bounded_signal,
            steps=int(step_index + steps),
        )
