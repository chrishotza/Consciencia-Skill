from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Mapping


METACOGNITIVE_PREDICTION_RUNTIME_KEYS = {
    "metacognitive_prediction_error",
    "metacognitive_prediction_accuracy",
    "metacognitive_prediction_expected_accuracy",
    "metacognitive_prediction_sequence",
    "metacognitive_prediction_evidence",
    "metacognitive_prediction_history",
}


_MISSING = object()


def _leaf_values(value: Any, prefix: str = "") -> dict[str, Any]:
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, child in value.items():
            child_key = f"{prefix}.{key}" if prefix else str(key)
            result.update(_leaf_values(child, child_key))
        return result
    return {prefix: value}


def _leaf_error(predicted: Any, actual: Any) -> float:
    if actual is _MISSING:
        return 1.0

    if (
        isinstance(predicted, (int, float))
        and not isinstance(predicted, bool)
        and isinstance(actual, (int, float))
        and not isinstance(actual, bool)
    ):
        left = float(predicted)
        right = float(actual)
        return max(0.0, min(1.0, abs(left - right) / (1.0 + abs(left) + abs(right))))

    return 0.0 if predicted == actual else 1.0


def compare_prediction_mapping(
    predicted: Mapping[str, Any] | None,
    actual: Mapping[str, Any] | None,
) -> dict[str, Any]:
    if not isinstance(predicted, Mapping):
        return {
            "available": False,
            "error": None,
            "accuracy": None,
            "compared_fields": 0,
            "missing_fields": [],
        }

    predicted_leaves = _leaf_values(predicted)
    actual_leaves = _leaf_values(actual) if isinstance(actual, Mapping) else {}

    if not predicted_leaves:
        return {
            "available": False,
            "error": None,
            "accuracy": None,
            "compared_fields": 0,
            "missing_fields": [],
        }

    errors: list[float] = []
    missing_fields: list[str] = []
    for key, predicted_value in predicted_leaves.items():
        actual_value = actual_leaves.get(key, _MISSING)
        if actual_value is _MISSING:
            missing_fields.append(key)
        errors.append(_leaf_error(predicted_value, actual_value))

    error = round(sum(errors) / len(errors), 6)
    return {
        "available": True,
        "error": error,
        "accuracy": round(1.0 - error, 6),
        "compared_fields": len(errors),
        "missing_fields": missing_fields,
    }


@dataclass(frozen=True)
class MetacognitivePredictionResult:
    available: bool
    error: float | None
    accuracy: float | None
    outcome: dict[str, Any]
    state_delta: dict[str, Any]
    fields_compared: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def compare_metacognitive_prediction(
    *,
    predicted_outcome: Mapping[str, Any] | None,
    predicted_state_delta: Mapping[str, Any] | None,
    actual_outcome: Mapping[str, Any],
    actual_state_delta: Mapping[str, Any],
) -> MetacognitivePredictionResult:
    outcome = compare_prediction_mapping(predicted_outcome, actual_outcome)
    transition = compare_prediction_mapping(
        predicted_state_delta,
        actual_state_delta,
    )

    components = [
        item
        for item in (outcome, transition)
        if item["available"]
    ]

    if not components:
        return MetacognitivePredictionResult(
            available=False,
            error=None,
            accuracy=None,
            outcome=outcome,
            state_delta=transition,
            fields_compared=0,
        )

    error = round(
        sum(float(item["error"]) for item in components) / len(components),
        6,
    )
    return MetacognitivePredictionResult(
        available=True,
        error=error,
        accuracy=round(1.0 - error, 6),
        outcome=outcome,
        state_delta=transition,
        fields_compared=sum(
            int(item["compared_fields"])
            for item in components
        ),
    )
