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
    ):
        self.identity = identity
        self.memory_limit = max(1, int(memory_limit))
        self.history_limit = max(1, int(history_limit))
        self.transformation_limit = max(1, self.history_limit)
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
        topology_integrity = float(self.topology_diagnostics()["integrity"])
        self_dissonance = self.state.self_dissonance
        latent_score = self.latent_pattern_score()

        candidates = [
            {
                "id": "preserve_continuity",
                "signals": {
                    "goal_fit": intention_strength,
                    "self_alignment": coherence,
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
            "revision": self.state.revision,
        }

    def trajectory_weights(self) -> dict[str, float]:
        weights = dict(DEFAULT_TRAJECTORY_WEIGHTS)
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

        attractor_weights = (
            self.state.attractor.get("trajectory_weights", {})
            if isinstance(self.state.attractor, Mapping)
            else {}
        )
        if isinstance(attractor_weights, Mapping):
            for key, value in attractor_weights.items():
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

        weights = self.state.self_model.get("regime_weights", {})
        if not isinstance(weights, Mapping):
            weights = {}

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
        self, candidates: list[Mapping[str, Any]]
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
                "self_state": self.state.self_state,
                "self_model": self.state.self_model,
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
            "the present, form candidate trajectories, and let the self-model "
            "causally affect trajectory selection. Return a response plus durable "
            "state updates. The runtime can score trajectories using signals named "
            "goal_fit, self_alignment, continuity, learning, risk, and uncertainty."
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
            self.state.self_model = dict(frame["self_model"])

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

        if frame.get("regime") is not None:
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

        self.state.self_dissonance = self.calculate_self_dissonance()
        if frame.get("self_dissonance") is not None:
            self.state.self_dissonance = max(0.0, min(1.0, float(frame["self_dissonance"])))

        self.state.coherence = self.calculate_coherence()
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
                "transformation": bool(changed),
            }
        )
        self.state.history = self.state.history[-self.history_limit :]

        self.store.save(self.state)
        return response

    def snapshot(self) -> dict[str, Any]:
        return self.state.to_dict()
