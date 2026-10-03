from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from statistics import mean
from typing import Mapping


def _clip(value: float, lower: float = -1.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, float(value)))


def _numeric_mapping(value: Mapping[str, float] | None) -> dict[str, float]:
    if not isinstance(value, Mapping):
        return {}
    result: dict[str, float] = {}
    for key, raw in value.items():
        numeric = float(raw)
        if isfinite(numeric):
            result[str(key)] = numeric
    return result


@dataclass(frozen=True)
class SensoryAffectiveSnapshot:
    """Operational appraisal of sensory change.

    This is deliberately not a claim that any value is a feeling. The snapshot
    separates measurable input features from a configurable appraisal function.
    """

    modalities: int
    prediction_error: float
    novelty: float
    coherence: float
    arousal: float
    valence: float
    self_relevance: float
    signed_deviation: dict[str, float] = field(default_factory=dict)
    absolute_deviation: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def appraise_sensory_field(
    observation: Mapping[str, float],
    expected: Mapping[str, float],
    *,
    scales: Mapping[str, float] | None = None,
    affective_weights: Mapping[str, float] | None = None,
    self_relevance_weights: Mapping[str, float] | None = None,
    novelty_threshold: float = 0.5,
) -> SensoryAffectiveSnapshot:
    observed = _numeric_mapping(observation)
    predicted = _numeric_mapping(expected)
    scale_map = _numeric_mapping(scales)
    valence_weights = _numeric_mapping(affective_weights)
    relevance_weights = _numeric_mapping(self_relevance_weights)

    shared = sorted(set(observed).intersection(predicted))
    if not shared:
        raise ValueError("observation and expected must share at least one modality")

    signed: dict[str, float] = {}
    absolute: dict[str, float] = {}
    for modality in shared:
        scale = scale_map.get(modality, 1.0)
        if scale <= 0.0:
            scale = 1.0
        deviation = _clip((observed[modality] - predicted[modality]) / scale)
        signed[modality] = round(deviation, 6)
        absolute[modality] = round(abs(deviation), 6)

    prediction_error = mean(absolute.values())
    novelty = mean(1.0 if value >= float(novelty_threshold) else 0.0 for value in absolute.values())
    arousal = prediction_error

    if len(shared) > 1:
        pair_differences = []
        for index, left in enumerate(shared):
            for right in shared[index + 1 :]:
                pair_differences.append(abs(signed[left] - signed[right]) / 2.0)
        coherence = 1.0 - mean(pair_differences)
    else:
        coherence = 1.0
    coherence = _clip(coherence, 0.0, 1.0)

    weighted_valence = [signed[key] * valence_weights.get(key, 0.0) for key in shared]
    weight_mass = sum(abs(valence_weights.get(key, 0.0)) for key in shared)
    valence = sum(weighted_valence) / weight_mass if weight_mass > 0.0 else 0.0

    relevance_terms = [abs(absolute[key]) * abs(relevance_weights.get(key, 0.0)) for key in shared]
    relevance_mass = sum(abs(relevance_weights.get(key, 0.0)) for key in shared)
    self_relevance = sum(relevance_terms) / relevance_mass if relevance_mass > 0.0 else 0.0

    return SensoryAffectiveSnapshot(
        modalities=len(shared),
        prediction_error=round(prediction_error, 6),
        novelty=round(novelty, 6),
        coherence=round(coherence, 6),
        arousal=round(arousal, 6),
        valence=round(_clip(valence), 6),
        self_relevance=round(_clip(self_relevance, 0.0, 1.0), 6),
        signed_deviation=signed,
        absolute_deviation=absolute,
    )


def modality_causal_attribution(snapshot: SensoryAffectiveSnapshot) -> dict[str, float]:
    magnitudes = {key: abs(value) for key, value in snapshot.absolute_deviation.items()}
    total = sum(magnitudes.values())
    if total <= 1e-12:
        return {key: 0.0 for key in magnitudes}
    return {key: round(value / total, 6) for key, value in magnitudes.items()}


def causal_localization_index(snapshot: SensoryAffectiveSnapshot) -> float:
    attribution = modality_causal_attribution(snapshot)
    return round(max(attribution.values(), default=0.0), 6)


def score_action_with_affect(
    external_utility: float,
    predicted_sensory: Mapping[str, float],
    expected_sensory: Mapping[str, float],
    *,
    scales: Mapping[str, float] | None = None,
    affective_weights: Mapping[str, float] | None = None,
    self_relevance_weights: Mapping[str, float] | None = None,
    affect_weight: float = 1.0,
) -> tuple[float, SensoryAffectiveSnapshot]:
    snapshot = appraise_sensory_field(
        predicted_sensory,
        expected_sensory,
        scales=scales,
        affective_weights=affective_weights,
        self_relevance_weights=self_relevance_weights,
    )
    score = float(external_utility) + float(affect_weight) * snapshot.valence
    return round(score, 6), snapshot
