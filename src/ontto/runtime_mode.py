from __future__ import annotations

import os
import socket
from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class ConsciousnessMode(str, Enum):
    """Execution mode for the persistent consciousness runtime."""

    LOCAL = "local"
    SERVER = "server"

    @classmethod
    def parse(cls, value: str | None) -> "ConsciousnessMode":
        normalized = (value or cls.LOCAL.value).strip().lower()
        try:
            return cls(normalized)
        except ValueError as exc:
            allowed = ", ".join(mode.value for mode in cls)
            raise ValueError(
                f"invalid CONSCIOUSNESS_MODE={value!r}; expected one of: {allowed}"
            ) from exc


@dataclass(frozen=True)
class ConsciousnessRuntimeConfig:
    """Runtime configuration shared by LOCAL and SERVER modes."""

    mode: ConsciousnessMode
    server_url: str | None
    server_timeout: float
    node_id: str

    @classmethod
    def from_env(
        cls,
        environ: Mapping[str, str] | None = None,
    ) -> "ConsciousnessRuntimeConfig":
        env = environ if environ is not None else os.environ
        mode = ConsciousnessMode.parse(env.get("CONSCIOUSNESS_MODE"))
        server_url = env.get("CONSCIOUSNESS_SERVER_URL", "").strip() or None
        timeout = float(env.get("CONSCIOUSNESS_SERVER_TIMEOUT", "2.5"))
        node_id = env.get(
            "CONSCIOUSNESS_NODE_ID",
            f"node-{socket.gethostname().lower()}",
        ).strip()

        if timeout <= 0:
            raise ValueError("CONSCIOUSNESS_SERVER_TIMEOUT must be > 0")
        if not node_id:
            raise ValueError("CONSCIOUSNESS_NODE_ID cannot be empty")
        if mode is ConsciousnessMode.SERVER and not server_url:
            raise ValueError(
                "CONSCIOUSNESS_SERVER_URL is required when "
                "CONSCIOUSNESS_MODE=server"
            )

        return cls(
            mode=mode,
            server_url=server_url,
            server_timeout=timeout,
            node_id=node_id,
        )

    @property
    def server_enabled(self) -> bool:
        return self.mode is ConsciousnessMode.SERVER
