from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Sequence


class ReconciliationStatus(str, Enum):
    NO_CHECKPOINT = "NO_CHECKPOINT"
    ALIGNED = "ALIGNED"
    LOCAL_AHEAD = "LOCAL_AHEAD"
    LOCAL_BEHIND = "LOCAL_BEHIND"
    DIVERGED = "DIVERGED"


@dataclass(frozen=True)
class ReconciliationReport:
    status: ReconciliationStatus
    checkpoint_id: str | None
    local_state_fingerprint: str
    remote_state_fingerprint: str | None
    local_trajectory_fingerprint: str
    remote_trajectory_fingerprint: str | None
    local_event_count: int
    remote_event_count: int | None
    local_memory_count: int
    remote_memory_count: int | None
    state_match: bool
    trajectory_match: bool
    event_count_delta: int | None
    memory_count_delta: int | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "checkpoint_id": self.checkpoint_id,
            "local_state_fingerprint": self.local_state_fingerprint,
            "remote_state_fingerprint": self.remote_state_fingerprint,
            "local_trajectory_fingerprint": self.local_trajectory_fingerprint,
            "remote_trajectory_fingerprint": self.remote_trajectory_fingerprint,
            "local_event_count": self.local_event_count,
            "remote_event_count": self.remote_event_count,
            "local_memory_count": self.local_memory_count,
            "remote_memory_count": self.remote_memory_count,
            "state_match": self.state_match,
            "trajectory_match": self.trajectory_match,
            "event_count_delta": self.event_count_delta,
            "memory_count_delta": self.memory_count_delta,
        }


def latest_checkpoint(
    checkpoints: Sequence[Mapping[str, Any]],
) -> Mapping[str, Any] | None:
    return checkpoints[-1] if checkpoints else None


def reconcile(
    *,
    local_state_fingerprint: str,
    local_trajectory_fingerprint: str,
    local_event_count: int,
    local_memory_count: int,
    checkpoints: Sequence[Mapping[str, Any]],
) -> ReconciliationReport:
    checkpoint = latest_checkpoint(checkpoints)

    if checkpoint is None:
        return ReconciliationReport(
            status=ReconciliationStatus.NO_CHECKPOINT,
            checkpoint_id=None,
            local_state_fingerprint=local_state_fingerprint,
            remote_state_fingerprint=None,
            local_trajectory_fingerprint=local_trajectory_fingerprint,
            remote_trajectory_fingerprint=None,
            local_event_count=int(local_event_count),
            remote_event_count=None,
            local_memory_count=int(local_memory_count),
            remote_memory_count=None,
            state_match=False,
            trajectory_match=False,
            event_count_delta=None,
            memory_count_delta=None,
        )

    payload = checkpoint.get("payload") or {}
    remote_state = str(payload.get("state_fingerprint", ""))
    remote_trajectory = str(payload.get("trajectory_fingerprint", ""))
    remote_events = int(payload.get("event_count", 0))
    remote_memories = int(payload.get("memory_count", 0))

    state_match = remote_state == local_state_fingerprint
    trajectory_match = remote_trajectory == local_trajectory_fingerprint
    event_delta = int(local_event_count) - remote_events
    memory_delta = int(local_memory_count) - remote_memories

    if state_match and trajectory_match and event_delta == 0 and memory_delta == 0:
        status = ReconciliationStatus.ALIGNED
    elif event_delta >= 0 and memory_delta >= 0 and (
        event_delta > 0 or memory_delta > 0
    ):
        status = ReconciliationStatus.LOCAL_AHEAD
    elif event_delta <= 0 and memory_delta <= 0 and (
        event_delta < 0 or memory_delta < 0
    ):
        status = ReconciliationStatus.LOCAL_BEHIND
    else:
        status = ReconciliationStatus.DIVERGED

    return ReconciliationReport(
        status=status,
        checkpoint_id=str(checkpoint.get("checkpoint_id")),
        local_state_fingerprint=local_state_fingerprint,
        remote_state_fingerprint=remote_state,
        local_trajectory_fingerprint=local_trajectory_fingerprint,
        remote_trajectory_fingerprint=remote_trajectory,
        local_event_count=int(local_event_count),
        remote_event_count=remote_events,
        local_memory_count=int(local_memory_count),
        remote_memory_count=remote_memories,
        state_match=state_match,
        trajectory_match=trajectory_match,
        event_count_delta=event_delta,
        memory_count_delta=memory_delta,
    )
