from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from .core import ConsciousRuntime


ModelFn = Callable[[str], Mapping[str, Any]]
ActionExecutor = Callable[
    [Mapping[str, Any], Mapping[str, Any]],
    Mapping[str, Any],
]


class ConsciousHostLoop:
    """Connect a host model and real action executor to the Skill-Conscious runtime."""

    def __init__(
        self,
        runtime: ConsciousRuntime,
        *,
        model: ModelFn,
        execute_action: ActionExecutor,
    ) -> None:
        self.runtime = runtime
        self.model = model
        self.execute_action = execute_action

    @staticmethod
    def _frame(value: Mapping[str, Any], stage: str) -> dict[str, Any]:
        frame = dict(value)
        if not str(frame.get("response", "")).strip():
            raise ValueError(f"{stage} model frame requires a non-empty response")
        return frame

    def step(self, external_input: str) -> dict[str, Any]:
        """Run one complete host cycle, including real action execution and consequence re-entry."""
        initial_prompt = self.runtime.prepare(external_input)
        initial_frame = self._frame(self.model(initial_prompt), "initial")

        self.runtime.integrate(initial_frame)
        selected = self.runtime.state.selected_trajectory

        result: dict[str, Any] = {
            "response": initial_frame["response"],
            "selected_trajectory": selected,
            "action_executed": False,
            "consequence": None,
            "next_trajectory": selected,
        }

        if not isinstance(selected, Mapping):
            return result

        outcome = self.execute_action(
            dict(selected),
            self.runtime.snapshot(),
        )
        if not isinstance(outcome, Mapping):
            raise ValueError("execute_action must return a mapping")

        trajectory_id = str(selected.get("id", "")).strip()
        if not trajectory_id:
            raise ValueError("selected trajectory requires a non-empty id")

        consequence_prompt = self.runtime.prepare_consequence(
            trajectory_id,
            outcome,
        )
        evaluation_frame = self._frame(
            self.model(consequence_prompt),
            "consequence",
        )
        evaluation_frame["consequence_trajectory"] = trajectory_id
        evaluation_frame["consequence"] = dict(outcome)

        # The actual host-observed outcome is authoritative. The model may
        # evaluate it, but it must not manufacture or replace the observation.
        self.runtime.integrate(evaluation_frame)

        result.update(
            {
                "action_executed": True,
                "consequence": dict(outcome),
                "next_trajectory": self.runtime.state.selected_trajectory,
                "consequence_evaluation": evaluation_frame.get(
                    "self_evaluation",
                    {},
                ),
            }
        )
        return result
