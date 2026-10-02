from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .reconciliation import ReconciliationReport, ReconciliationStatus


class RecoveryAction(str, Enum):
    NO_ACTION = "NO_ACTION"
    INITIALIZE_CHECKPOINT = "INITIALIZE_CHECKPOINT"
    EXPORT_LOCAL_DELTA = "EXPORT_LOCAL_DELTA"
    REQUEST_REMOTE_REPLAY = "REQUEST_REMOTE_REPLAY"
    BLOCK_DIVERGENCE = "BLOCK_DIVERGENCE"


@dataclass(frozen=True)
class RecoveryPlan:
    action: RecoveryAction
    checkpoint_id: str | None
    reason: str
    event_delta: int | None
    memory_delta: int | None
    state_match: bool
    trajectory_match: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action.value,
            "checkpoint_id": self.checkpoint_id,
            "reason": self.reason,
            "event_delta": self.event_delta,
            "memory_delta": self.memory_delta,
            "state_match": self.state_match,
            "trajectory_match": self.trajectory_match,
        }


def plan_recovery(report: ReconciliationReport) -> RecoveryPlan:
    if report.status is ReconciliationStatus.NO_CHECKPOINT:
        return RecoveryPlan(
            action=RecoveryAction.INITIALIZE_CHECKPOINT,
            checkpoint_id=None,
            reason="No server checkpoint exists yet; establish a continuity boundary before replay.",
            event_delta=None,
            memory_delta=None,
            state_match=False,
            trajectory_match=False,
        )

    if report.status is ReconciliationStatus.ALIGNED:
        return RecoveryPlan(
            action=RecoveryAction.NO_ACTION,
            checkpoint_id=report.checkpoint_id,
            reason="Local organism matches the latest server checkpoint.",
            event_delta=report.event_count_delta,
            memory_delta=report.memory_count_delta,
            state_match=report.state_match,
            trajectory_match=report.trajectory_match,
        )

    if report.status is ReconciliationStatus.LOCAL_AHEAD:
        return RecoveryPlan(
            action=RecoveryAction.EXPORT_LOCAL_DELTA,
            checkpoint_id=report.checkpoint_id,
            reason="Local continuity has advanced beyond the latest server checkpoint; export the local delta before transfer.",
            event_delta=report.event_count_delta,
            memory_delta=report.memory_count_delta,
            state_match=report.state_match,
            trajectory_match=report.trajectory_match,
        )

    if report.status is ReconciliationStatus.LOCAL_BEHIND:
        return RecoveryPlan(
            action=RecoveryAction.REQUEST_REMOTE_REPLAY,
            checkpoint_id=report.checkpoint_id,
            reason="Local continuity is behind the latest server checkpoint; a remote replay boundary is required before advancing locally.",
            event_delta=report.event_count_delta,
            memory_delta=report.memory_count_delta,
            state_match=report.state_match,
            trajectory_match=report.trajectory_match,
        )

    return RecoveryPlan(
        action=RecoveryAction.BLOCK_DIVERGENCE,
        checkpoint_id=report.checkpoint_id,
        reason="Local and remote continuity diverged; do not overwrite either side automatically.",
        event_delta=report.event_count_delta,
        memory_delta=report.memory_count_delta,
        state_match=report.state_match,
        trajectory_match=report.trajectory_match,
    )
