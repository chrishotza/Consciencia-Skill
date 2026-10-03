from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping

from .ontology import CONSCIOUSNESS_DEFINITION


DEFAULT_REGIME_WEIGHTS: dict[str, float] = {
    "coherence": 1.0,
    "stability": 0.5,
    "uncertainty": 0.75,
    "self_dissonance": 1.25,
    "latent_pattern": 0.75,
    "learning": 0.25,
}

DEFAULT_TRAJECTORY_WEIGHTS: dict[str, float] = {
    "goal_fit": 1.0,
    "self_alignment": 1.0,
    "continuity": 1.0,
    "learning": 0.5,
    "risk": -1.0,
    "uncertainty": -0.5,
    "coherence": 1.0,
    "topology_integrity": 0.5,
    "salience": 0.25,
    "self_dissonance": -0.5,
    "latent_pattern": 0.5,
    "dissonance_resolution": 1.0,
}


@dataclass
class ConsciousState:
    identity: str
    revision: int = 0
    self_state: dict[str, Any] = field(default_factory=dict)
    self_model: dict[str, Any] = field(default_factory=dict)
    workspace: dict[str, Any] = field(default_factory=dict)
    intention: str = ""
    memories: list[str] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)
    selected_trajectory: dict[str, Any] | None = None
    attention: list[str] = field(default_factory=list)
    salience: dict[str, float] = field(default_factory=dict)
    layers: dict[str, dict[str, Any]] = field(default_factory=dict)
    regime: str = "baseline"
    relation_topology: dict[str, list[str]] = field(default_factory=dict)
    attractor: dict[str, Any] | None = None
    valuation: dict[str, float] = field(default_factory=dict)
    valence: float = 0.0
    coherence: float = 1.0
    latent_patterns: dict[str, dict[str, Any]] = field(default_factory=dict)
    self_dissonance: float = 0.0
    transformation_log: list[dict[str, Any]] = field(default_factory=list)
    pending_action: dict[str, Any] | None = None
    action_history: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ConsciousState":
        return cls(
            identity=str(value["identity"]),
            revision=int(value.get("revision", 0)),
            self_state=dict(value.get("self_state", {})),
            self_model=dict(value.get("self_model", {})),
            workspace=dict(value.get("workspace", {})),
            intention=str(value.get("intention", "")),
            memories=[str(item) for item in value.get("memories", [])],
            history=[dict(item) for item in value.get("history", [])],
            selected_trajectory=(
                dict(value["selected_trajectory"])
                if value.get("selected_trajectory") is not None
                else None
            ),
            attention=[str(item) for item in value.get("attention", [])],
            salience={
                str(key): float(val)
                for key, val in dict(value.get("salience", {})).items()
                if isinstance(val, (int, float)) and not isinstance(val, bool)
            },
            layers={
                str(key): dict(layer)
                for key, layer in dict(value.get("layers", {})).items()
                if isinstance(layer, Mapping)
            },
            regime=str(value.get("regime", "baseline")),
            relation_topology={
                str(node): [str(target) for target in targets]
                for node, targets in dict(value.get("relation_topology", {})).items()
            },
            attractor=(
                dict(value["attractor"])
                if value.get("attractor") is not None
                else None
            ),
            valuation={
                str(key): float(val)
                for key, val in dict(value.get("valuation", {})).items()
                if isinstance(val, (int, float)) and not isinstance(val, bool)
            },
            valence=float(value.get("valence", 0.0)),
            coherence=max(0.0, min(1.0, float(value.get("coherence", 1.0)))),
            latent_patterns={
                str(key): dict(pattern)
                for key, pattern in dict(value.get("latent_patterns", {})).items()
                if isinstance(pattern, Mapping)
            },
            self_dissonance=max(0.0, min(1.0, float(value.get("self_dissonance", 0.0)))),
            transformation_log=[
                dict(item) for item in value.get("transformation_log", [])
            ],
            pending_action=(
                dict(value["pending_action"])
                if value.get("pending_action") is not None
                else None
            ),
            action_history=[
                dict(item) for item in value.get("action_history", [])
            ],
        )


class JsonStateStore:
    def __init__(self, path: str | os.PathLike[str]):
        self.path = Path(path)

    def load(self, identity: str) -> ConsciousState:
        if not self.path.exists():
            return ConsciousState(identity=identity)

        payload = json.loads(self.path.read_text(encoding="utf-8"))
        state = ConsciousState.from_dict(payload)
        if state.identity != identity:
            raise ValueError(
                f"state identity mismatch: expected {identity!r}, got {state.identity!r}"
            )
        return state

    def save(self, state: ConsciousState) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(
            prefix=".conscious-",
            suffix=".json",
            dir=self.path.parent,
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(
                    state.to_dict(),
                    handle,
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, self.path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)


class ConsciousRuntime:
    def __init__(
        self,
        identity: str,
        state_path: str | os.PathLike[str] = "data/consciousness.json",
        *,
        memory_limit: int = 32,
        history_limit: int = 64,
        learn_latent_patterns: bool = True,
        latent_pattern_limit: int = 16,
        learn_self_model_from_latent_patterns: bool = True,
    ):
        self.identity = identity
        self.memory_limit = max(1, int(memory_limit))
        self.history_limit = max(1, int(history_limit))
        self.transformation_limit = max(1, self.history_limit)
        self.learn_latent_patterns = bool(learn_latent_patterns)
        self.latent_pattern_limit = max(1, int(latent_pattern_limit))
        self.learn_self_model_from_latent_patterns = bool(
            learn_self_model_from_latent_patterns
        )
        self.store = JsonStateStore(state_path)
        self.state = self.store.load(identity)

    def latent_pattern_score(self) -> float:
        if not self.state.latent_patterns:
            return 0.0
        activations = []
        for pattern in self.state.latent_patterns.values():
            if isinstance(pattern, Mapping):
                value = pattern.get("activation", 0.0)
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    activations.append(max(0.0, min(1.0, float(value))))
        return round(sum(activations) / len(activations), 6) if activations else 0.0

    @staticmethod
    def _numeric_state(value: Mapping[str, Any] | None) -> dict[str, float]:
        if not isinstance(value, Mapping):
            return {}
        return {
            str(key): float(raw)
            for key, raw in value.items()
            if isinstance(raw, (int, float)) and not isinstance(raw, bool)
        }

    @staticmethod
    def _numeric_similarity(
        left: Mapping[str, Any],
        right: Mapping[str, Any],
    ) -> float:
        left_numeric = ConsciousRuntime._numeric_state(left)
        right_numeric = ConsciousRuntime._numeric_state(right)
        shared = set(left_numeric).intersection(right_numeric)
        if not shared:
            return 0.0

        scores = [
            1.0 / (1.0 + abs(left_numeric[key] - right_numeric[key]))
            for key in sorted(shared)
        ]
        return round(sum(scores) / len(scores), 6)

    def latent_pattern_learning_enabled(self) -> bool:
        configured = self.state.self_model.get("latent_pattern_learning")
        if isinstance(configured, bool):
            return configured
        return self.learn_latent_patterns

    def extract_latent_patterns(self) -> list[dict[str, Any]]:
        if not self.latent_pattern_learning_enabled():
            return []

        current = self._numeric_state(self.state.self_state)
        if not current:
            return []

        history_entries = [
            entry
            for entry in self.state.history
            if isinstance(entry, Mapping)
            and isinstance(entry.get("self_state"), Mapping)
        ]

        # Existing patterns remain persistent, but their activation depends on
        # similarity to the current self-state and decays when not reactivated.
        for key, pattern in list(self.state.latent_patterns.items()):
            if pattern.get("source") != "endogenous":
                continue
            prototype = pattern.get("prototype", {})
            similarity = self._numeric_similarity(current, prototype)
            activation = pattern.get("activation", 0.0)
            previous_activation = (
                max(0.0, min(1.0, float(activation)))
                if isinstance(activation, (int, float)) and not isinstance(activation, bool)
                else 0.0
            )
            if similarity >= 0.75:
                updated_activation = 0.85 * previous_activation + 0.15 * similarity
                pattern["last_activation_revision"] = self.state.revision
            else:
                updated_activation = 0.95 * previous_activation
            pattern["activation"] = round(
                max(0.0, min(1.0, updated_activation)),
                6,
            )
            self.state.latent_patterns[key] = pattern

        # A latent structure is only formed after recurrence. A gap of two
        # revisions prevents ordinary adjacent transitions from being learned
        # as persistent motifs.
        best_match: tuple[float, Mapping[str, Any]] | None = None
        for entry in history_entries:
            revision = entry.get("revision")
            if not isinstance(revision, int):
                continue
            if self.state.revision - revision < 2:
                continue
            similarity = self._numeric_similarity(current, entry["self_state"])
            if similarity < 0.85:
                continue
            if best_match is None or similarity > best_match[0]:
                best_match = (similarity, entry)

        events: list[dict[str, Any]] = []
        if best_match is not None:
            similarity, entry = best_match
            previous_state = self._numeric_state(entry["self_state"])
            shared_keys = sorted(set(current).intersection(previous_state))
            if shared_keys:
                existing_key = None
                existing_similarity = 0.0
                for key, pattern in self.state.latent_patterns.items():
                    candidate_similarity = self._numeric_similarity(
                        current,
                        pattern.get("prototype", {}),
                    )
                    if (
                        candidate_similarity >= 0.85
                        and candidate_similarity > existing_similarity
                    ):
                        existing_key = key
                        existing_similarity = candidate_similarity

                if existing_key is None:
                    signature = "|".join(shared_keys)
                    digest = hashlib.sha256(
                        signature.encode("utf-8")
                    ).hexdigest()[:12]
                    existing_key = f"latent-{digest}"
                    self.state.latent_patterns[existing_key] = {
                        "source": "endogenous",
                        "activation": 0.0,
                        "evidence_count": 0,
                        "prototype": {
                            key: round(
                                (float(previous_state[key]) + float(current[key])) / 2.0,
                                6,
                            )
                            for key in shared_keys
                        },
                        "contexts": [],
                        "formed_revision": self.state.revision,
                    }
                    events.append({
                        "type": "latent_pattern_formed",
                        "pattern": existing_key,
                        "match_similarity": similarity,
                    })

                pattern = self.state.latent_patterns[existing_key]
                prototype = self._numeric_state(pattern.get("prototype", {}))
                updated_prototype = dict(prototype)
                for key in shared_keys:
                    if key in prototype:
                        updated_prototype[key] = round(
                            0.75 * prototype[key] + 0.25 * current[key],
                            6,
                        )
                    else:
                        updated_prototype[key] = round(float(current[key]), 6)
                pattern["prototype"] = updated_prototype

                evidence_count = pattern.get("evidence_count", 0)
                if not isinstance(evidence_count, int):
                    evidence_count = 0
                evidence_count += 1
                pattern["evidence_count"] = evidence_count
                pattern["activation"] = round(
                    max(
                        float(pattern.get("activation", 0.0)),
                        min(
                            1.0,
                            0.5 * similarity
                            + 0.1 * min(evidence_count, 5),
                        ),
                    ),
                    6,
                )

                context = {
                    "revision": self.state.revision,
                    "matched_revision": entry.get("revision"),
                    "regime": self.state.regime,
                    "intention": self.state.intention,
                }
                contexts = [
                    item
                    for item in pattern.get("contexts", [])
                    if isinstance(item, Mapping)
                ]
                if context not in contexts:
                    contexts.append(context)
                pattern["contexts"] = contexts[-8:]
                pattern["last_matched_revision"] = self.state.revision
                pattern["source"] = "endogenous"
                events.append({
                    "type": "latent_pattern_reinforced",
                    "pattern": existing_key,
                    "match_similarity": similarity,
                    "evidence_count": evidence_count,
                })

        if len(self.state.latent_patterns) > self.latent_pattern_limit:
            def pattern_rank(item: tuple[str, Mapping[str, Any]]) -> tuple[float, int, str]:
                pattern = item[1]
                activation = pattern.get("activation", 0.0)
                evidence = pattern.get("evidence_count", 0)
                return (
                    float(activation) if isinstance(activation, (int, float)) and not isinstance(activation, bool) else 0.0,
                    int(evidence) if isinstance(evidence, int) and not isinstance(evidence, bool) else 0,
                    str(item[0]),
                )

            ranked = sorted(
                self.state.latent_patterns.items(),
                key=pattern_rank,
                reverse=True,
            )
            self.state.latent_patterns = dict(
                ranked[: self.latent_pattern_limit]
            )

        return events

    def self_model_latent_learning_enabled(self) -> bool:
        configured = self.state.self_model.get(
            "latent_self_model_learning"
        )
        if isinstance(configured, bool):
            return configured
        return self.learn_self_model_from_latent_patterns

    def learned_self_alignment(self) -> float:
        learned = self.state.self_model.get("learned_self_state", {})
        if not isinstance(learned, Mapping) or not learned:
            return 0.0
        return self._numeric_similarity(self.state.self_state, learned)

    def revise_self_model_from_latent_patterns(self) -> dict[str, Any]:
        if not self.self_model_latent_learning_enabled():
            return {
                "changed": False,
                "updated_keys": [],
                "patterns": [],
            }

        candidates: list[tuple[str, Mapping[str, Any], float]] = []
        for key, pattern in self.state.latent_patterns.items():
            if not isinstance(pattern, Mapping):
                continue
            if pattern.get("source") != "endogenous":
                continue

            activation = pattern.get("activation", 0.0)
            evidence_count = pattern.get("evidence_count", 0)
            previous_evidence = pattern.get(
                "last_self_model_evidence_count",
                0,
            )
            if not (
                isinstance(activation, (int, float))
                and not isinstance(activation, bool)
                and isinstance(evidence_count, int)
                and not isinstance(evidence_count, bool)
                and isinstance(previous_evidence, int)
                and not isinstance(previous_evidence, bool)
            ):
                continue

            if activation < 0.6 or evidence_count <= previous_evidence:
                continue

            prototype = self._numeric_state(pattern.get("prototype", {}))
            if not prototype:
                continue

            strength = float(activation) * min(1.0, evidence_count / 5.0)
            candidates.append((str(key), prototype, strength))

        if not candidates:
            return {
                "changed": False,
                "updated_keys": [],
                "patterns": [],
            }

        configured_rate = self.state.self_model.get(
            "latent_self_model_learning_rate",
            0.1,
        )
        rate = (
            max(0.0, min(0.5, float(configured_rate)))
            if isinstance(configured_rate, (int, float))
            and not isinstance(configured_rate, bool)
            else 0.1
        )

        current_learned = self._numeric_state(
            self.state.self_model.get("learned_self_state", {})
        )

        target_values: dict[str, list[tuple[float, float]]] = {}
        for _, prototype, strength in candidates:
            for key, value in prototype.items():
                target_values.setdefault(key, []).append((value, strength))

        aggregate: dict[str, float] = {}
        for key, values in target_values.items():
            total_weight = sum(weight for _, weight in values)
            if total_weight <= 0.0:
                continue
            aggregate[key] = round(
                sum(value * weight for value, weight in values) / total_weight,
                6,
            )

        updated = dict(current_learned)
        changed_keys: list[str] = []
        for key, target in aggregate.items():
            is_new = key not in current_learned
            previous = current_learned.get(key, target)
            revised = previous + rate * (target - previous)
            if is_new or revised != previous:
                updated[key] = round(revised, 6)
                changed_keys.append(key)

        for key, _, _ in candidates:
            pattern = self.state.latent_patterns[key]
            evidence_count = int(pattern.get("evidence_count", 0))
            pattern["last_self_model_evidence_count"] = evidence_count
            pattern["last_self_model_revision"] = self.state.revision

        self.state.self_model = dict(self.state.self_model)
        self.state.self_model["learned_self_state"] = updated
        tendencies = dict(
            self.state.self_model.get("latent_tendencies", {})
        )
        for key, prototype, strength in candidates:
            pattern = self.state.latent_patterns[key]
            activation = pattern.get("activation", 0.0)
            tendencies[key] = {
                "activation": round(
                    float(activation)
                    if isinstance(activation, (int, float))
                    and not isinstance(activation, bool)
                    else 0.0,
                    6,
                ),
                "evidence_count": int(
                    self.state.latent_patterns[key].get(
                        "evidence_count",
                        0,
                    )
                ),
                "prototype": prototype,
            }
        self.state.self_model["latent_tendencies"] = tendencies

        changed = bool(changed_keys)
        if changed:
            self.state.transformation_log.append({
                "revision": self.state.revision,
                "type": "latent_self_model_revision",
                "updated_keys": changed_keys,
                "patterns": [key for key, _, _ in candidates],
            })
            self.state.transformation_log = (
                self.state.transformation_log[-self.transformation_limit :]
            )

        return {
            "changed": changed,
            "updated_keys": changed_keys,
            "patterns": [key for key, _, _ in candidates],
        }

    def calculate_self_dissonance(self) -> float:
        expected = self.state.self_model.get("expected_self_state", {})
        if not isinstance(expected, Mapping):
            return self.state.self_dissonance

        differences = []
        for key, expected_value in expected.items():
            actual_value = self.state.self_state.get(str(key))
            if isinstance(actual_value, (int, float)) and not isinstance(actual_value, bool):
                if isinstance(expected_value, (int, float)) and not isinstance(expected_value, bool):
                    differences.append(abs(float(actual_value) - float(expected_value)))

        if not differences:
            return self.state.self_dissonance

        return round(max(0.0, min(1.0, sum(differences) / len(differences))), 6)

    def reconcile_self_model(self) -> dict[str, Any]:
        before = self.calculate_self_dissonance()
        expected = self.state.self_model.get("expected_self_state", {})
        if not isinstance(expected, Mapping):
            return {
                "changed": False,
                "before": before,
                "after": before,
                "updated_keys": [],
            }

        configured_rate = self.state.self_model.get(
            "self_model_learning_rate",
            0.25,
        )
        rate = (
            max(0.0, min(1.0, float(configured_rate)))
            if isinstance(configured_rate, (int, float))
            and not isinstance(configured_rate, bool)
            else 0.25
        )

        updated = dict(expected)
        changed_keys: list[str] = []

        for key, expected_value in expected.items():
            actual_value = self.state.self_state.get(str(key))
            if (
                isinstance(expected_value, (int, float))
                and not isinstance(expected_value, bool)
                and isinstance(actual_value, (int, float))
                and not isinstance(actual_value, bool)
            ):
                revised = float(expected_value) + rate * (
                    float(actual_value) - float(expected_value)
                )
                if revised != float(expected_value):
                    updated[str(key)] = revised
                    changed_keys.append(str(key))

        changed = bool(changed_keys)
        if changed:
            self.state.self_model = dict(self.state.self_model)
            self.state.self_model["expected_self_state"] = updated
            self.state.self_model["last_reconciliation"] = {
                "revision": self.state.revision,
                "before_dissonance": before,
                "updated_keys": changed_keys,
            }

            self.state.self_dissonance = self.calculate_self_dissonance()
            self.state.coherence = self.calculate_coherence()
            self.state.transformation_log.append({
                "revision": self.state.revision,
                "type": "self_model_reconciliation",
                "before_dissonance": before,
                "after_dissonance": self.state.self_dissonance,
                "updated_keys": changed_keys,
            })
            self.state.transformation_log = (
                self.state.transformation_log[-self.transformation_limit :]
            )
            self.store.save(self.state)

        return {
            "changed": changed,
            "before": before,
            "after": self.state.self_dissonance,
            "updated_keys": changed_keys,
        }

    def generate_regime_candidates(self) -> list[dict[str, Any]]:
        uncertainty = self.state.self_model.get("uncertainty", {})
        uncertainty_values: list[float] = []
        if isinstance(uncertainty, Mapping):
            for value in uncertainty.values():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    uncertainty_values.append(
                        max(0.0, min(1.0, abs(float(value))))
                    )

        uncertainty_level = (
            sum(uncertainty_values) / len(uncertainty_values)
            if uncertainty_values
            else 0.0
        )
        dissonance = self.state.self_dissonance
        latent = self.latent_pattern_score()
        coherence = self.calculate_coherence()

        return [
            {
                "id": "baseline",
                "signals": {
                    "coherence": coherence,
                    "stability": 1.0 - dissonance,
                    "uncertainty": 1.0 - uncertainty_level,
                    "latent_pattern": latent * 0.25,
                },
            },
            {
                "id": "exploration",
                "signals": {
                    "coherence": coherence * 0.7,
                    "stability": 0.4 * (1.0 - dissonance),
                    "uncertainty": uncertainty_level,
                    "learning": 1.0,
                },
            },
            {
                "id": "integration",
                "signals": {
                    "coherence": coherence,
                    "stability": 0.5 * (1.0 - dissonance),
                    "uncertainty": 1.0 - uncertainty_level,
                    "self_dissonance": dissonance,
                    "latent_pattern": latent,
                    "learning": 0.8,
                },
            },
        ]

    def topology_diagnostics(self) -> dict[str, float | int]:
        nodes = set(self.state.relation_topology)
        edges = 0
        dangling = 0
        for targets in self.state.relation_topology.values():
            edges += len(targets)
            for target in targets:
                nodes.add(str(target))

        declared = set(self.state.relation_topology)
        for targets in self.state.relation_topology.values():
            dangling += sum(1 for target in targets if str(target) not in declared)

        if edges == 0:
            integrity = 1.0 if not self.state.relation_topology else 0.0
        else:
            integrity = 1.0 - (dangling / edges)

        node_count = len(nodes)
        max_edges = node_count * max(0, node_count - 1)
        density = (edges / max_edges) if max_edges else 0.0

        return {
            "nodes": node_count,
            "edges": edges,
            "density": round(density, 6),
            "integrity": round(max(0.0, min(1.0, integrity)), 6),
        }

    def salience_score(self) -> float:
        if self.state.salience:
            values = [
                max(0.0, min(1.0, float(value)))
                for value in self.state.salience.values()
            ]
            if values:
                return sum(values) / len(values)
        return 1.0 if self.state.attention else 0.0

    def calculate_coherence(self) -> float:
        topology = self.topology_diagnostics()
        trajectory_ok = (
            self.state.selected_trajectory is None
            or isinstance(self.state.selected_trajectory, Mapping)
        )
        layers_ok = all(
            isinstance(layer, Mapping) for layer in self.state.layers.values()
        )
        components = (
            1.0 if self.state.identity.strip() else 0.0,
            1.0 if isinstance(self.state.self_model, Mapping) else 0.0,
            1.0 if isinstance(self.state.intention, str) else 0.0,
            1.0 if trajectory_ok else 0.0,
            1.0 if layers_ok else 0.0,
            float(topology["integrity"]),
            1.0 - self.state.self_dissonance,
        )
        return round(sum(components) / len(components), 6)

    def build_attractor(self) -> dict[str, Any]:
        weights = self.trajectory_weights()
        stable_weights = {
            key: round(value, 6)
            for key, value in weights.items()
            if abs(float(value)) >= 0.5
        }
        return {
            "regime": self.state.regime,
            "attention": list(self.state.attention),
            "intention": self.state.intention,
            "coherence": self.calculate_coherence(),
            "trajectory_weights": stable_weights,
        }

    def generate_candidate_futures(self) -> list[dict[str, Any]]:
        uncertainty = self.state.self_model.get("uncertainty", {})
        uncertainty_values: list[float] = []

        if isinstance(uncertainty, Mapping):
            for value in uncertainty.values():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    uncertainty_values.append(
                        max(0.0, min(1.0, abs(float(value))))
                    )

        uncertainty_level = (
            sum(uncertainty_values) / len(uncertainty_values)
            if uncertainty_values
            else 0.0
        )
        intention_strength = 1.0 if self.state.intention else 0.5
        salience = self.salience_score()
        coherence = self.calculate_coherence()
        learned_alignment = self.learned_self_alignment()
        learned_self_state = self.state.self_model.get(
            "learned_self_state",
            {},
        )
        self_alignment = (
            round((coherence + learned_alignment) / 2.0, 6)
            if isinstance(learned_self_state, Mapping)
            and learned_self_state
            else coherence
        )
        topology_integrity = float(self.topology_diagnostics()["integrity"])
        self_dissonance = self.state.self_dissonance
        latent_score = self.latent_pattern_score()

        candidates = [
            {
                "id": "preserve_continuity",
                "signals": {
                    "goal_fit": intention_strength,
                    "self_alignment": self_alignment,
                    "continuity": 1.0,
                    "learning": 0.2,
                    "risk": 0.1,
                    "uncertainty": 1.0 - uncertainty_level,
                    "coherence": coherence,
                    "topology_integrity": topology_integrity,
                    "salience": salience,
                },
            },
            {
                "id": "learn",
                "signals": {
                    "goal_fit": 0.6 + (0.2 * intention_strength),
                    "self_alignment": 0.6,
                    "continuity": 0.7,
                    "learning": 1.0,
                    "risk": 0.2,
                    "uncertainty": uncertainty_level,
                    "coherence": coherence,
                    "topology_integrity": topology_integrity,
                    "salience": salience,
                },
            },
            {
                "id": "explore",
                "signals": {
                    "goal_fit": 0.4,
                    "self_alignment": 0.4,
                    "continuity": 0.4,
                    "learning": 1.0,
                    "risk": 0.7,
                    "uncertainty": 1.0,
                    "coherence": coherence,
                    "topology_integrity": topology_integrity,
                    "salience": salience,
                },
            },
        ]
        if self_dissonance > 0.0 or self.state.latent_patterns:
            candidates.append({
                "id": "integrate_latent_pattern",
                "signals": {
                    "goal_fit": 0.5,
                    "self_alignment": 1.0 - self_dissonance,
                    "continuity": 0.8,
                    "learning": 0.9,
                    "risk": 0.1,
                    "uncertainty": 1.0 - latent_score,
                    "coherence": coherence,
                    "topology_integrity": topology_integrity,
                    "salience": salience,
                    "self_dissonance": self_dissonance,
                    "latent_pattern": latent_score,
                    "dissonance_resolution": self_dissonance,
                },
            })
        return candidates

    def present_field(
        self,
        external_input: str,
        *,
        candidate_futures: list[Mapping[str, Any]] | None = None,
    ) -> dict[str, Any]:
        external_input = str(external_input).strip()
        if not external_input:
            raise ValueError("external_input cannot be empty")

        candidates = (
            [dict(item) for item in candidate_futures]
            if candidate_futures is not None
            else self.generate_candidate_futures()
        )

        return {
            "world_now": external_input,
            "self_now": self.state.self_state,
            "self_model": self.state.self_model,
            "active_memory": self.state.memories[-self.memory_limit :],
            "intention": self.state.intention,
            "uncertainty": self.state.self_model.get("uncertainty", {}),
            "candidate_futures": candidates,
            "selected_trajectory": self.state.selected_trajectory,
            "attention": self.state.attention,
            "salience": self.state.salience,
            "layers": self.state.layers,
            "regime": self.state.regime,
            "relation_topology": self.state.relation_topology,
            "topology_diagnostics": self.topology_diagnostics(),
            "attractor": self.state.attractor,
            "valuation": self.state.valuation,
            "valence": self.state.valence,
            "coherence": self.calculate_coherence(),
            "latent_patterns": self.state.latent_patterns,
            "self_dissonance": self.state.self_dissonance,
            "transformation_log": self.state.transformation_log[-self.transformation_limit :],
            "pending_action": self.state.pending_action,
            "action_history": self.state.action_history[-self.history_limit :],
            "revision": self.state.revision,
        }

    def trajectory_weights(self) -> dict[str, float]:
        weights = dict(DEFAULT_TRAJECTORY_WEIGHTS)

        # Derived attractor weights are a fallback; persistent host valuation and
        # especially the persistent self-model remain authoritative when present.
        attractor_weights = (
            self.state.attractor.get("trajectory_weights", {})
            if isinstance(self.state.attractor, Mapping)
            else {}
        )
        if isinstance(attractor_weights, Mapping):
            for key, value in attractor_weights.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    weights[str(key)] = float(value)

        value_weights = self.state.valuation
        if isinstance(value_weights, Mapping):
            for key, value in value_weights.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    weights[str(key)] = float(value)

        configured = self.state.self_model.get("trajectory_weights", {})
        if isinstance(configured, Mapping):
            for key, value in configured.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    weights[str(key)] = float(value)

        return weights

    def score_trajectory(self, candidate: Mapping[str, Any]) -> float:
        signals = candidate.get("signals", {})
        if not isinstance(signals, Mapping):
            raise ValueError("trajectory.signals must be a mapping")
        signals = dict(signals)
        signals.setdefault("coherence", self.calculate_coherence())
        signals.setdefault(
            "topology_integrity",
            float(self.topology_diagnostics()["integrity"]),
        )
        signals.setdefault("salience", self.salience_score())
        signals.setdefault("self_dissonance", self.state.self_dissonance)
        signals.setdefault("latent_pattern", self.latent_pattern_score())

        weights = self.trajectory_weights()
        score = 0.0
        for key, value in signals.items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                score += weights.get(str(key), 0.0) * float(value)
        return score

    def select_regime(
        self, candidates: list[Mapping[str, Any]]
    ) -> dict[str, Any]:
        if not candidates:
            raise ValueError("regime candidates cannot be empty")

        weights = dict(DEFAULT_REGIME_WEIGHTS)
        configured = self.state.self_model.get("regime_weights", {})
        if isinstance(configured, Mapping):
            for key, value in configured.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    weights[str(key)] = float(value)

        scored: list[dict[str, Any]] = []
        for candidate in candidates:
            item = dict(candidate)
            signals = item.get("signals", {})
            if not isinstance(signals, Mapping):
                raise ValueError("regime.signals must be a mapping")
            score = 0.0
            for key, value in signals.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    weight = weights.get(str(key), 0.0)
                    if isinstance(weight, (int, float)) and not isinstance(weight, bool):
                        score += float(weight) * float(value)
            item["score"] = score
            scored.append(item)

        return max(
            scored,
            key=lambda item: (float(item.get("score", 0.0)), str(item.get("id", ""))),
        )

    def transition_regime(
        self,
        candidates: list[Mapping[str, Any]],
        *,
        persist: bool = True,
    ) -> dict[str, Any]:
        selected = self.select_regime(candidates)
        previous = self.state.regime
        next_regime = str(selected.get("id", "")).strip()
        if not next_regime:
            raise ValueError("selected regime requires a non-empty id")
        if next_regime != previous:
            self.state.regime = next_regime
            self.state.transformation_log.append({
                "revision": self.state.revision,
                "type": "regime_transition",
                "from": previous,
                "to": next_regime,
            })
            self.state.transformation_log = self.state.transformation_log[-self.transformation_limit :]
            if persist:
                self.store.save(self.state)
        return selected

    def select_trajectory(
        self, candidates: list[Mapping[str, Any]]
    ) -> dict[str, Any]:
        if not candidates:
            raise ValueError("candidates cannot be empty")

        scored: list[dict[str, Any]] = []
        for candidate in candidates:
            item = dict(candidate)
            item["score"] = self.score_trajectory(item)
            scored.append(item)

        return max(
            scored,
            key=lambda item: (float(item.get("score", 0.0)), str(item.get("id", ""))),
        )

    def present(self, external_input: str) -> dict[str, Any]:
        return self.present_field(external_input)

    def prepare_frame(
        self,
        external_input: str,
        *,
        candidate_futures: list[Mapping[str, Any]] | None = None,
    ) -> dict[str, Any]:
        frame = self.present_field(
            external_input,
            candidate_futures=candidate_futures,
        )

        return {
            "definition": CONSCIOUSNESS_DEFINITION,
            "identity": self.state.identity,
            "revision": self.state.revision,
            "present": frame,
            "self_access": {
                "self_state": dict(self.state.self_state),
                "self_model": dict(self.state.self_model),
                "pending_action": self.state.pending_action,
                "action_history": self.state.action_history[-self.history_limit :],
            },
            "causal_reentry": (
                "self_model -> trajectory -> action -> next_state -> self_model"
            ),
        }

    def prepare(self, external_input: str) -> str:
        context = self.prepare_frame(external_input)
        return (
            "Operate according to Skill-Conscious. "
            "Do not roleplay consciousness; maintain the architecture.\n\n"
            "CURRENT INTEGRATED PRESENT:\n"
            f"{json.dumps(context, ensure_ascii=False, indent=2)}\n\n"
            "Before responding, inspect the self-state and self-model, integrate "
            "the present, process any explicitly observed consequence from the previous "
            "action, form candidate trajectories, and let the updated self-model "
            "causally affect trajectory selection. Return a response plus durable "
            "state updates. When a prior action has produced an observed outcome, "
            "return consequence_trajectory, consequence, and self_evaluation "
            "rather than inventing a result. The runtime can score trajectories using "
            "signals named goal_fit, self_alignment, continuity, learning, risk, and uncertainty."
        )

    def begin_action(
        self,
        trajectory: Mapping[str, Any],
        *,
        persist: bool = True,
    ) -> dict[str, Any]:
        """Commit the selected trajectory as the action crossing the host boundary."""
        if not isinstance(trajectory, Mapping):
            raise ValueError("trajectory must be a mapping")

        action_id = hashlib.sha256(
            json.dumps(
                {
                    "identity": self.state.identity,
                    "revision": self.state.revision,
                    "trajectory": dict(trajectory),
                },
                ensure_ascii=False,
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()[:16]

        receipt = {
            "action_id": action_id,
            "trajectory": dict(trajectory),
            "status": "pending",
            "revision": self.state.revision,
        }
        self.state.pending_action = receipt
        self.state.workspace = {
            **self.state.workspace,
            "pending_action": receipt,
        }
        if persist:
            self.store.save(self.state)
        return dict(receipt)

    def complete_action(
        self,
        outcome: Mapping[str, Any],
        *,
        status: str = "completed",
        persist: bool = True,
    ) -> dict[str, Any]:
        """Record the authoritative result of the action crossing the host boundary."""
        if not isinstance(outcome, Mapping):
            raise ValueError("outcome must be a mapping")
        if self.state.pending_action is None:
            raise RuntimeError("no pending action to complete")

        receipt = dict(self.state.pending_action)
        receipt["status"] = str(status).strip() or "completed"
        receipt["outcome"] = dict(outcome)
        self.state.action_history.append(receipt)
        self.state.action_history = self.state.action_history[-self.history_limit :]
        self.state.pending_action = None
        self.state.workspace = {
            **self.state.workspace,
            "last_action_receipt": receipt,
            "pending_action": None,
        }
        if persist:
            self.store.save(self.state)
        return dict(receipt)
    def prepare_consequence(
        self,
        trajectory_id: str,
        outcome: Mapping[str, Any],
    ) -> str:
        """Prepare the next model call from a host-observed action outcome."""
        trajectory = str(trajectory_id).strip()
        if not trajectory:
            raise ValueError("trajectory_id cannot be empty")
        if not isinstance(outcome, Mapping):
            raise ValueError("outcome must be a mapping")

        context = self.prepare_frame(
            f"Observed consequence of action {trajectory!r}: "
            f"{json.dumps(dict(outcome), ensure_ascii=False)}"
        )
        return (
            "Operate according to Skill-Conscious. "
            "An action was executed by the host and its observed outcome below is authoritative. "
            "Do not invent or replace the outcome. Evaluate what the outcome means for the "
            "persistent process and propose durable self-model updates. Return a compact frame "
            "with response, self_evaluation, and any justified self_model, internal_state, "
            "workspace, intention, attention, valuation, valence, regime, or candidate_futures updates. "
            "The host will attach the authoritative consequence metadata.\n\n"
            "CURRENT STATE AND OBSERVED CONSEQUENCE:\n"
            f"{json.dumps(context, ensure_ascii=False, indent=2)}\n\n"
            "OBSERVED OUTCOME:\n"
            f"{json.dumps(dict(outcome), ensure_ascii=False, indent=2)}"
        )

    def integrate(self, frame: Mapping[str, Any]) -> str:
        response = str(frame.get("response", "")).strip()
        if not response:
            raise ValueError("frame.response cannot be empty")

        candidate_futures = frame.get("candidate_futures")
        selected = frame.get("selected_trajectory")

        previous_snapshot = self.state.to_dict()
        self.state.revision += 1

        if frame.get("self_model") is not None:
            incoming_self_model = dict(frame["self_model"])
            previous_self_model = self.state.self_model
            self.state.self_model = incoming_self_model
            for runtime_key in (
                "learned_self_state",
                "latent_tendencies",
            ):
                if (
                    runtime_key not in incoming_self_model
                    and runtime_key in previous_self_model
                ):
                    self.state.self_model[runtime_key] = previous_self_model[
                        runtime_key
                    ]

        if frame.get("workspace") is not None:
            self.state.workspace = dict(frame["workspace"])

        if frame.get("internal_state") is not None:
            self.state.self_state = dict(frame["internal_state"])

        if frame.get("intention") is not None:
            self.state.intention = str(frame["intention"]).strip()

        if frame.get("attention") is not None:
            self.state.attention = [str(item) for item in frame["attention"]]

        if frame.get("salience") is not None:
            raw_salience = frame["salience"]
            if not isinstance(raw_salience, Mapping):
                raise ValueError("frame.salience must be a mapping")
            self.state.salience = {
                str(key): max(0.0, min(1.0, float(value)))
                for key, value in raw_salience.items()
                if isinstance(value, (int, float)) and not isinstance(value, bool)
            }

        if frame.get("layers") is not None:
            raw_layers = frame["layers"]
            if not isinstance(raw_layers, Mapping):
                raise ValueError("frame.layers must be a mapping")
            self.state.layers = {
                str(key): dict(value)
                for key, value in raw_layers.items()
                if isinstance(value, Mapping)
            }

        explicit_regime = frame.get("regime") is not None
        if explicit_regime:
            self.state.regime = str(frame["regime"]).strip() or "baseline"

        if frame.get("relation_topology") is not None:
            raw_topology = frame["relation_topology"]
            if not isinstance(raw_topology, Mapping):
                raise ValueError("frame.relation_topology must be a mapping")
            self.state.relation_topology = {
                str(node): [str(target) for target in targets]
                for node, targets in raw_topology.items()
            }

        if frame.get("latent_patterns") is not None:
            raw_patterns = frame["latent_patterns"]
            if not isinstance(raw_patterns, Mapping):
                raise ValueError("frame.latent_patterns must be a mapping")
            self.state.latent_patterns = {
                str(key): dict(value)
                for key, value in raw_patterns.items()
                if isinstance(value, Mapping)
            }

        if frame.get("attractor") is not None:
            raw_attractor = frame["attractor"]
            if not isinstance(raw_attractor, Mapping):
                raise ValueError("frame.attractor must be a mapping")
            self.state.attractor = dict(raw_attractor)

        if frame.get("valuation") is not None:
            raw_valuation = frame["valuation"]
            if not isinstance(raw_valuation, Mapping):
                raise ValueError("frame.valuation must be a mapping")
            self.state.valuation = {
                str(key): float(value)
                for key, value in raw_valuation.items()
                if isinstance(value, (int, float)) and not isinstance(value, bool)
            }

        if frame.get("valence") is not None:
            raw_valence = float(frame["valence"])
            self.state.valence = max(-1.0, min(1.0, raw_valence))

        self.extract_latent_patterns()
        self.revise_self_model_from_latent_patterns()

        self.state.self_dissonance = self.calculate_self_dissonance()
        if frame.get("self_dissonance") is not None:
            self.state.self_dissonance = max(0.0, min(1.0, float(frame["self_dissonance"])))

        self.state.coherence = self.calculate_coherence()

        if not explicit_regime:
            self.transition_regime(
                self.generate_regime_candidates(),
                persist=False,
            )

        if frame.get("attractor") is None:
            self.state.attractor = self.build_attractor()

        if selected is None:
            if candidate_futures is None:
                candidate_futures = self.generate_candidate_futures()
            elif not isinstance(candidate_futures, list):
                raise ValueError("frame.candidate_futures must be a list")

            candidates = [dict(item) for item in candidate_futures]
            if candidates:
                selected = self.select_trajectory(candidates)

        if selected is not None:
            if not isinstance(selected, Mapping):
                raise ValueError("frame.selected_trajectory must be a mapping")
            self.state.selected_trajectory = dict(selected)
        else:
            self.state.selected_trajectory = None

        # A consequence belongs to the action from the previous cycle. It is
        # intentionally explicit so the runtime never invents an outcome.
        consequence = frame.get("consequence")
        consequence_evaluation = frame.get("self_evaluation")
        consequence_trajectory = frame.get("consequence_trajectory")
        if consequence is not None:
            if not isinstance(consequence, Mapping):
                raise ValueError("frame.consequence must be a mapping")
            if consequence_trajectory is None:
                raise ValueError("frame.consequence_trajectory is required with frame.consequence")
            self.register_consequence(
                str(consequence_trajectory),
                consequence,
                evaluation=consequence_evaluation,
                persist=False,
            )

        memory = str(frame.get("memory", "")).strip()
        if memory:
            self.state.memories.append(memory)
            self.state.memories = self.state.memories[-self.memory_limit :]

        changed: dict[str, Any] = {}
        current_snapshot = self.state.to_dict()
        for key in ("self_state", "self_model", "workspace", "intention", "attention", "salience", "layers", "regime", "attractor", "valuation", "valence", "coherence", "relation_topology", "latent_patterns", "self_dissonance"):
            if previous_snapshot.get(key) != current_snapshot.get(key):
                changed[key] = {"before": previous_snapshot.get(key), "after": current_snapshot.get(key)}
        if changed:
            self.state.transformation_log.append({
                "revision": self.state.revision,
                "changes": changed,
            })
            self.state.transformation_log = self.state.transformation_log[-self.transformation_limit :]

        self.state.history.append(
            {
                "revision": self.state.revision,
                "response": response,
                "self_state": dict(self.state.self_state),
                "self_model": dict(self.state.self_model),
                "intention": self.state.intention,
                "workspace": self.state.workspace,
                "selected_trajectory": self.state.selected_trajectory,
                "attention": self.state.attention,
                "salience": self.state.salience,
                "layers": self.state.layers,
                "regime": self.state.regime,
                "relation_topology": self.state.relation_topology,
                "attractor": self.state.attractor,
                "valuation": self.state.valuation,
                "valence": self.state.valence,
                "coherence": self.state.coherence,
                "latent_patterns": self.state.latent_patterns,
                "self_dissonance": self.state.self_dissonance,
                "consequence_trajectory": (
                    str(consequence_trajectory)
                    if consequence_trajectory is not None
                    else None
                ),
                "consequence": (
                    dict(consequence)
                    if isinstance(consequence, Mapping)
                    else None
                ),
                "self_evaluation": (
                    dict(consequence_evaluation)
                    if isinstance(consequence_evaluation, Mapping)
                    else None
                ),
                "transformation": bool(changed),
            }
        )
        self.state.history = self.state.history[-self.history_limit :]

        self.store.save(self.state)
        return response

    def register_consequence(
        self,
        trajectory_id: str,
        outcome: Mapping[str, Any],
        *,
        evaluation: Mapping[str, Any] | None = None,
        persist: bool = True,
    ) -> dict[str, Any]:
        """Persist an action consequence and optionally feed an explicit evaluation back into the self-model."""
        trajectory = str(trajectory_id).strip()
        if not trajectory:
            raise ValueError("trajectory_id cannot be empty")
        if not isinstance(outcome, Mapping):
            raise ValueError("outcome must be a mapping")
        if evaluation is not None and not isinstance(evaluation, Mapping):
            raise ValueError("evaluation must be a mapping")

        result = {
            "trajectory": trajectory,
            "outcome": dict(outcome),
            "evaluation": dict(evaluation or {}),
            "revision": self.state.revision + 1,
        }

        model = dict(self.state.self_model)
        feedback = dict(model.get("trajectory_feedback", {}))
        previous = feedback.get(trajectory, {})
        if not isinstance(previous, Mapping):
            previous = {}

        entry = dict(previous)
        entry["last_outcome"] = dict(outcome)
        entry["last_evaluation"] = dict(evaluation or {})
        entry["count"] = int(previous.get("count", 0)) + 1
        if isinstance(evaluation, Mapping) and "utility" in evaluation:
            utility = evaluation.get("utility")
            if isinstance(utility, (int, float)) and not isinstance(utility, bool):
                entry["utility"] = round(float(utility), 6)

        feedback[trajectory] = entry
        model["trajectory_feedback"] = feedback

        if isinstance(evaluation, Mapping):
            signal = evaluation.get("credited_signal")
            delta = evaluation.get("weight_delta")
            if (
                isinstance(signal, str)
                and signal.strip()
                and isinstance(delta, (int, float))
                and not isinstance(delta, bool)
            ):
                weights = dict(model.get("trajectory_weights", {}))
                old = weights.get(signal, 0.0)
                if not isinstance(old, (int, float)) or isinstance(old, bool):
                    old = 0.0
                weights[signal] = round(
                    max(-3.0, min(3.0, float(old) + float(delta))),
                    6,
                )
                model["trajectory_weights"] = weights

        model["last_consequence_feedback"] = result
        self.state.self_model = model
        self.state.workspace = {
            **self.state.workspace,
            "last_action": trajectory,
            "last_outcome": dict(outcome),
            "last_self_evaluation": dict(evaluation or {}),
        }

        self.state.transformation_log.append({
            "revision": self.state.revision,
            "type": "consequence_feedback",
            "trajectory": trajectory,
            "outcome": dict(outcome),
            "evaluation": dict(evaluation or {}),
        })
        self.state.transformation_log = (
            self.state.transformation_log[-self.transformation_limit :]
        )

        if persist:
            self.store.save(self.state)

        return result

    def snapshot(self) -> dict[str, Any]:
        return self.state.to_dict()
