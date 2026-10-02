from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .client import ConsciousnessClient


class SynchronizationStatus(str, Enum):
    ALIGNED = "ALIGNED"
    LOCAL_UPDATED = "LOCAL_UPDATED"
    PEER_UPDATED = "PEER_UPDATED"
    DIVERGED = "DIVERGED"
    NO_INSTANCE = "NO_INSTANCE"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class SynchronizationReport:
    status: SynchronizationStatus
    instance_id: str
    local_revision: int | None
    peer_revision: int | None
    local_state_hash: str | None
    peer_state_hash: str | None
    applied_event_count: int = 0
    direction: str = "none"
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "instance_id": self.instance_id,
            "local_revision": self.local_revision,
            "peer_revision": self.peer_revision,
            "local_state_hash": self.local_state_hash,
            "peer_state_hash": self.peer_state_hash,
            "applied_event_count": self.applied_event_count,
            "direction": self.direction,
            "reason": self.reason,
        }


def _instance(client: ConsciousnessClient, instance_id: str) -> dict[str, Any] | None:
    try:
        return client.get_instance(instance_id)
    except Exception as exc:
        if getattr(exc, "code", None) == 404:
            return None
        raise


def synchronize_pair(
    local: ConsciousnessClient,
    peer: ConsciousnessClient,
    *,
    instance_id: str,
    identity: str | None = None,
    limit: int = 1000,
) -> SynchronizationReport:
    """Safely synchronize one instance in either direction.

    Exactly one side may advance when revisions differ. Equal revisions with
    different state hashes are treated as divergence and are never overwritten.
    """
    local_payload = _instance(local, instance_id)
    peer_payload = _instance(peer, instance_id)

    if local_payload is None and peer_payload is None:
        return SynchronizationReport(
            status=SynchronizationStatus.NO_INSTANCE,
            instance_id=instance_id,
            local_revision=None,
            peer_revision=None,
            local_state_hash=None,
            peer_state_hash=None,
            reason="Neither peer has the requested instance.",
        )

    if local_payload is None:
        remote_state = peer_payload["state"]
        local.ensure_instance(
            instance_id,
            identity or str(remote_state["identity"]),
        )
        local_payload = _instance(local, instance_id)

    if peer_payload is None:
        local_state = local_payload["state"]
        peer.ensure_instance(
            instance_id,
            identity or str(local_state["identity"]),
        )
        peer_payload = _instance(peer, instance_id)

    assert local_payload is not None
    assert peer_payload is not None

    local_state = local_payload["state"]
    peer_state = peer_payload["state"]
    local_revision = int(local_state["revision"])
    peer_revision = int(peer_state["revision"])
    local_hash = local_payload.get("state_hash")
    peer_hash = peer_payload.get("state_hash")

    if local_revision == peer_revision:
        if local_hash == peer_hash:
            return SynchronizationReport(
                status=SynchronizationStatus.ALIGNED,
                instance_id=instance_id,
                local_revision=local_revision,
                peer_revision=peer_revision,
                local_state_hash=local_hash,
                peer_state_hash=peer_hash,
                reason="Both peers have the same revision and state hash.",
            )
        return SynchronizationReport(
            status=SynchronizationStatus.DIVERGED,
            instance_id=instance_id,
            local_revision=local_revision,
            peer_revision=peer_revision,
            local_state_hash=local_hash,
            peer_state_hash=peer_hash,
            reason="Equal revisions carry different state hashes; automatic overwrite is blocked.",
        )

    if local_revision > peer_revision:
        source, target = local, peer
        base_revision = peer_revision
        base_hash = peer_hash
        direction = "LOCAL_TO_PEER"
        status = SynchronizationStatus.PEER_UPDATED
    else:
        source, target = peer, local
        base_revision = local_revision
        base_hash = local_hash
        direction = "PEER_TO_LOCAL"
        status = SynchronizationStatus.LOCAL_UPDATED

    delta = source.export_delta(
        instance_id,
        after_revision=base_revision,
        limit=limit,
    )
    events = list(delta.get("events", []))

    if not events:
        return SynchronizationReport(
            status=SynchronizationStatus.BLOCKED,
            instance_id=instance_id,
            local_revision=local_revision,
            peer_revision=peer_revision,
            local_state_hash=local_hash,
            peer_state_hash=peer_hash,
            direction=direction,
            reason="Revision gap exists but the source returned no replayable events.",
        )

    replay = target.replay_delta(
        instance_id,
        base_revision=base_revision,
        base_state_hash=base_hash,
        events=events,
    )
    final = _instance(target, instance_id)
    if final is None:
        return SynchronizationReport(
            status=SynchronizationStatus.BLOCKED,
            instance_id=instance_id,
            local_revision=local_revision,
            peer_revision=peer_revision,
            local_state_hash=local_hash,
            peer_state_hash=peer_hash,
            applied_event_count=0,
            direction=direction,
            reason="Target instance disappeared after replay.",
        )

    final_state = final["state"]
    final_revision = int(final_state["revision"])
    final_hash = final.get("state_hash")
    expected_revision = max(local_revision, peer_revision)

    if final_revision != expected_revision:
        return SynchronizationReport(
            status=SynchronizationStatus.BLOCKED,
            instance_id=instance_id,
            local_revision=local_revision,
            peer_revision=peer_revision,
            local_state_hash=local_hash,
            peer_state_hash=peer_hash,
            applied_event_count=len(events),
            direction=direction,
            reason="Replay completed but target revision did not reach the expected peer revision.",
        )

    return SynchronizationReport(
        status=status,
        instance_id=instance_id,
        local_revision=final_revision if status is SynchronizationStatus.LOCAL_UPDATED else local_revision,
        peer_revision=peer_revision if status is SynchronizationStatus.LOCAL_UPDATED else final_revision,
        local_state_hash=final_hash if status is SynchronizationStatus.LOCAL_UPDATED else local_hash,
        peer_state_hash=peer_hash if status is SynchronizationStatus.LOCAL_UPDATED else final_hash,
        applied_event_count=len(events),
        direction=direction,
        reason="Deterministic event delta replayed and verified.",
    )
