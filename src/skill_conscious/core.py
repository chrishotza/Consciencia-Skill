from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping

from .ontology import CONSCIOUSNESS_DEFINITION


DEFAULT_TRAJECTORY_WEIGHTS: dict[str, float] = {
    "goal_fit": 1.0,
    "self_alignment": 1.0,
    "continuity": 1.0,
    "learning": 0.5,
    "risk": -1.0,
    "uncertainty": -0.5,
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
    regime: str = "baseline"
    relation_topology: dict[str, list[str]] = field(default_factory=dict)
    attractor: dict[str, Any] | None = None
    valuation: dict[str, float] = field(default_factory=dict)
    valence: float = 0.0
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
        return weights

    def score_trajectory(self, candidate: Mapping[str, Any]) -> float:
        signals = candidate.get("signals", {})
        if not isinstance(signals, Mapping):
            raise ValueError("trajectory.signals must be a mapping")

        weights = self.trajectory_weights()
        score = 0.0
        for key, value in signals.items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                score += weights.get(str(key), 0.0) * float(value)
        return score

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
        external_input = str(external_input).strip()
        if not external_input:
            raise ValueError("external_input cannot be empty")

        return {
            "world_now": external_input,
            "self_now": self.state.self_state,
            "self_model": self.state.self_model,
            "active_memory": self.state.memories[-self.memory_limit :],
            "intention": self.state.intention,
            "uncertainty": self.state.self_model.get("uncertainty", {}),
            "candidate_futures": [],
            "selected_trajectory": self.state.selected_trajectory,
            "attention": self.state.attention,
            "regime": self.state.regime,
            "relation_topology": self.state.relation_topology,
            "attractor": self.state.attractor,
            "valuation": self.state.valuation,
            "valence": self.state.valence,
            "transformation_log": self.state.transformation_log[-self.transformation_limit :],
            "revision": self.state.revision,
        }

    def prepare_frame(
        self,
        external_input: str,
        *,
        candidate_futures: list[Mapping[str, Any]] | None = None,
    ) -> dict[str, Any]:
        frame = self.present(external_input)
        if candidate_futures:
            frame["candidate_futures"] = [dict(item) for item in candidate_futures]

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

        if candidate_futures is not None:
            if not isinstance(candidate_futures, list):
                raise ValueError("frame.candidate_futures must be a list")
            candidates = [dict(item) for item in candidate_futures]
            if selected is None and candidates:
                selected = self.select_trajectory(candidates)

        if selected is not None:
            if not isinstance(selected, Mapping):
                raise ValueError("frame.selected_trajectory must be a mapping")
            self.state.selected_trajectory = dict(selected)
        else:
            self.state.selected_trajectory = None

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

        memory = str(frame.get("memory", "")).strip()
        if memory:
            self.state.memories.append(memory)
            self.state.memories = self.state.memories[-self.memory_limit :]

        changed: dict[str, Any] = {}
        current_snapshot = self.state.to_dict()
        for key in ("self_state", "self_model", "workspace", "intention", "attention", "regime", "attractor", "valuation", "valence", "relation_topology"):
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
                "regime": self.state.regime,
                "relation_topology": self.state.relation_topology,
                "attractor": self.state.attractor,
                "valuation": self.state.valuation,
                "valence": self.state.valence,
                "transformation": bool(changed),
            }
        )
        self.state.history = self.state.history[-self.history_limit :]

        self.store.save(self.state)
        return response

    def snapshot(self) -> dict[str, Any]:
        return self.state.to_dict()
