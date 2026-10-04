from __future__ import annotations

import json
from collections.abc import Callable, Mapping, Sequence
from typing import Any, Protocol

LLMOutput = str | Mapping[str, Any]
CompletionFn = Callable[[str], LLMOutput]

RUNTIME_OWNED_FRAME_KEYS = frozenset(
    {
        "selected_trajectory",
        "pending_action",
        "action_history",
        "revision",
        "metacognition",
        "metacognitive_trace",
        "metacognitive_prediction_error",
        "metacognitive_prediction_accuracy",
        "metacognitive_prediction_expected_accuracy",
        "metacognitive_prediction_sequence",
        "metacognitive_prediction_evidence",
        "metacognitive_prediction_history",
        "consequence",
        "consequence_trajectory",
        "action_receipt",
        "interoceptive_state",
        "affective_state",
        "temporal_state",
    }
)


class LLMCompletion(Protocol):
    def __call__(self, prompt: str) -> LLMOutput:
        ...


class LLMProtocolError(ValueError):
    """Raised when an external model violates the host/runtime frame contract."""


class ProviderNeutralLLMAdapter:
    """Normalize an external LLM into the runtime model-frame contract."""

    def __init__(
        self,
        complete: CompletionFn,
        *,
        fixed_candidate_futures: Sequence[Mapping[str, Any]] | None = None,
    ) -> None:
        self.complete = complete
        self._fixed_candidates = (
            [dict(item) for item in fixed_candidate_futures]
            if fixed_candidate_futures is not None
            else None
        )

    @property
    def fixed_candidate_futures(self) -> list[dict[str, Any]] | None:
        if self._fixed_candidates is None:
            return None
        return [dict(item) for item in self._fixed_candidates]

    def __call__(self, prompt: str) -> dict[str, Any]:
        raw = self.complete(prompt)
        frame = self._normalize_output(raw)
        self._validate_runtime_boundary(frame)
        self._apply_candidate_boundary(frame)
        return frame

    @staticmethod
    def _normalize_output(raw: LLMOutput) -> dict[str, Any]:
        if isinstance(raw, Mapping):
            return dict(raw)

        if not isinstance(raw, str):
            raise LLMProtocolError(
                "LLM completion must return a mapping or a JSON string"
            )

        text = raw.strip()
        if not text:
            raise LLMProtocolError(
                "LLM completion returned an empty response"
            )

        try:
            decoded = json.loads(text)
        except json.JSONDecodeError as exc:
            raise LLMProtocolError(
                "LLM completion must be valid JSON when returned as text"
            ) from exc

        if not isinstance(decoded, Mapping):
            raise LLMProtocolError(
                "LLM JSON completion must decode to an object"
            )
        return dict(decoded)

    @staticmethod
    def _validate_runtime_boundary(frame: Mapping[str, Any]) -> None:
        forbidden = sorted(RUNTIME_OWNED_FRAME_KEYS.intersection(frame))
        if forbidden:
            joined = ", ".join(forbidden)
            raise LLMProtocolError(
                f"LLM cannot directly write runtime-owned keys: {joined}"
            )

        self_model = frame.get("self_model")
        if isinstance(self_model, Mapping):
            forbidden_self_model = sorted(
                key
                for key in self_model
                if str(key) in {
                    "metacognitive_prediction_error",
                    "metacognitive_prediction_accuracy",
                    "metacognitive_prediction_expected_accuracy",
                    "metacognitive_prediction_sequence",
                    "metacognitive_prediction_evidence",
                    "metacognitive_prediction_history",
                    "trajectory_priority_adaptation_evidence",
                    "trajectory_priority_adaptation_history",
                    "trajectory_priority_adaptation_sequence",
                }
            )
            if forbidden_self_model:
                joined = ", ".join(forbidden_self_model)
                raise LLMProtocolError(
                    "LLM cannot directly write runtime-owned self_model keys: "
                    + joined
                )

        response = frame.get("response")
        if not isinstance(response, str) or not response.strip():
            raise LLMProtocolError(
                "LLM frame requires a non-empty string 'response'"
            )

    def _apply_candidate_boundary(self, frame: dict[str, Any]) -> None:
        if self._fixed_candidates is None:
            return

        supplied = frame.get("candidate_futures")
        expected = self._fixed_candidates
        if supplied is not None:
            if not isinstance(supplied, Sequence) or isinstance(
                supplied, (str, bytes, bytearray)
            ):
                raise LLMProtocolError(
                    "'candidate_futures' must be a sequence when supplied"
                )
            supplied_normalized = [
                dict(item) for item in supplied if isinstance(item, Mapping)
            ]
            if len(supplied_normalized) != len(supplied):
                raise LLMProtocolError(
                    "'candidate_futures' entries must all be mappings"
                )
            if supplied_normalized != expected:
                raise LLMProtocolError(
                    "LLM attempted to replace the controlled candidate field"
                )

        frame["candidate_futures"] = [dict(item) for item in expected]
