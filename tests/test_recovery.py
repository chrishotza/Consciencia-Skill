from __future__ import annotations

from src.consciousness_server.reconciliation import (
    ReconciliationStatus,
    ReconciliationReport,
)
from src.consciousness_server.recovery import RecoveryAction, plan_recovery


def report(status, **kwargs):
    base = dict(
        status=status,
        checkpoint_id="cp-test",
        local_state_fingerprint="local",
        remote_state_fingerprint="remote",
        local_trajectory_fingerprint="local-traj",
        remote_trajectory_fingerprint="remote-traj",
        local_event_count=4,
        remote_event_count=3,
        local_memory_count=2,
        remote_memory_count=1,
        state_match=False,
        trajectory_match=False,
        event_count_delta=1,
        memory_count_delta=1,
    )
    base.update(kwargs)
    return ReconciliationReport(**base)


def test_recovery_plan_aligned():
    p = plan_recovery(
        report(
            ReconciliationStatus.ALIGNED,
            checkpoint_id="cp-aligned",
            local_state_fingerprint="same",
            remote_state_fingerprint="same",
            local_trajectory_fingerprint="same",
            remote_trajectory_fingerprint="same",
            local_event_count=3,
            remote_event_count=3,
            local_memory_count=1,
            remote_memory_count=1,
            state_match=True,
            trajectory_match=True,
            event_count_delta=0,
            memory_count_delta=0,
        )
    )
    assert p.action is RecoveryAction.NO_ACTION


def test_recovery_plan_local_ahead():
    p = plan_recovery(report(ReconciliationStatus.LOCAL_AHEAD))
    assert p.action is RecoveryAction.EXPORT_LOCAL_DELTA


def test_recovery_plan_local_behind():
    p = plan_recovery(
        report(
            ReconciliationStatus.LOCAL_BEHIND,
            local_event_count=2,
            remote_event_count=4,
            local_memory_count=1,
            remote_memory_count=2,
            event_count_delta=-2,
            memory_count_delta=-1,
        )
    )
    assert p.action is RecoveryAction.REQUEST_REMOTE_REPLAY


def test_recovery_plan_diverged():
    p = plan_recovery(report(ReconciliationStatus.DIVERGED))
    assert p.action is RecoveryAction.BLOCK_DIVERGENCE


def test_recovery_plan_without_checkpoint():
    p = plan_recovery(
        report(
            ReconciliationStatus.NO_CHECKPOINT,
            checkpoint_id=None,
            remote_state_fingerprint=None,
            remote_trajectory_fingerprint=None,
            remote_event_count=None,
            remote_memory_count=None,
            event_count_delta=None,
            memory_count_delta=None,
        )
    )
    assert p.action is RecoveryAction.INITIALIZE_CHECKPOINT
