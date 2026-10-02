from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping

from .ontology import CONSCIOUSNESS_DEFINITION


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
        self.store = JsonStateStore(state_path)
        self.state = self.store.load(identity)

    def prepare(self, external_input: str) -> str:
        external_input = str(external_input).strip()
        if not external_input:
            raise ValueError("external_input cannot be empty")

        context = {
            "definition": CONSCIOUSNESS_DEFINITION,
            "identity": self.state.identity,
            "revision": self.state.revision,
            "self_state": self.state.self_state,
            "self_model": self.state.self_model,
            "workspace": self.state.workspace,
            "intention": self.state.intention,
            "memories": self.state.memories[-self.memory_limit :],
            "history": self.state.history[-self.history_limit :],
            "external_input": external_input,
        }

        return (
            "Operate according to Skill-Conscious. "
            "Do not roleplay consciousness; maintain the architecture.\n\n"
            "CURRENT PERSISTENT CONTEXT:\n"
            f"{json.dumps(context, ensure_ascii=False, indent=2)}\n\n"
            "Before responding, inspect the current self-state, self-model, "
            "present workspace, intention, and relevant memory. Then produce "
            "a response plus durable state updates. Allow the self-model to "
            "affect the next trajectory."
        )

    def integrate(self, frame: Mapping[str, Any]) -> str:
        response = str(frame.get("response", "")).strip()
        if not response:
            raise ValueError("frame.response cannot be empty")

        self.state.revision += 1

        if frame.get("self_model") is not None:
            self.state.self_model = dict(frame["self_model"])

        if frame.get("workspace") is not None:
            self.state.workspace = dict(frame["workspace"])

        if frame.get("internal_state") is not None:
            self.state.self_state = dict(frame["internal_state"])

        if frame.get("intention") is not None:
            self.state.intention = str(frame["intention"]).strip()

        memory = str(frame.get("memory", "")).strip()
        if memory:
            self.state.memories.append(memory)
            self.state.memories = self.state.memories[-self.memory_limit :]

        self.state.history.append(
            {
                "revision": self.state.revision,
                "response": response,
                "intention": self.state.intention,
                "workspace": self.state.workspace,
            }
        )
        self.state.history = self.state.history[-self.history_limit :]

        self.store.save(self.state)
        return response

    def snapshot(self) -> dict[str, Any]:
        return self.state.to_dict()
