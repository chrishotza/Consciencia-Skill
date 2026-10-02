from __future__ import annotations

import pytest

from src.consciousness_server.core import ConsciousnessStore


def test_event_identity_is_deterministic(tmp_path):
    store = ConsciousnessStore(tmp_path / "events.db")

    event_id_a = store.deterministic_event_id(
        "ci_identity",
        "DYNAMIC_UPDATE",
        {"delta": 0.25, "source": "test"},
        2,
        None,
    )
    event_id_b = store.deterministic_event_id(
        "ci_identity",
        "DYNAMIC_UPDATE",
        {"source": "test", "delta": 0.25},
        2,
        None,
    )

    assert event_id_a == event_id_b
    assert len(event_id_a) == 64
    store.close()


def test_delta_export_and_exact_replay_match_source(tmp_path):
    source = ConsciousnessStore(tmp_path / "source.db")
    target = ConsciousnessStore(tmp_path / "target.db")

    source_state = source.create_instance("replay-ai", "ci_replay")
    target.create_instance("replay-ai", "ci_replay")

    source.append_event(
        source_state.instance_id,
        "WAKE",
        {"cycle": 1},
        created_at="2026-10-02T03:00:00+00:00",
    )
    source.append_event(
        source_state.instance_id,
        "DYNAMIC_UPDATE",
        {"delta": 0.75},
        created_at="2026-10-02T03:00:01+00:00",
    )

    delta = source.list_events_after("ci_replay", after_revision=1)
    assert len(delta) == 2
    assert delta[0]["logical_revision"] == 2
    assert delta[1]["logical_revision"] == 3
    assert delta[1]["parent_event_id"] == delta[0]["event_id"]

    replayed = target.replay_events(
        "ci_replay",
        delta,
        base_revision=1,
        base_state_hash=target.state_hash("ci_replay"),
    )

    assert replayed.revision == source.get_state("ci_replay").revision
    assert target.state_hash("ci_replay") == source.state_hash("ci_replay")
    assert target.list_events("ci_replay") == source.list_events("ci_replay")

    # Exact retransmission is idempotent.
    target.replay_events(
        "ci_replay",
        delta,
        base_revision=1,
        base_state_hash=target.state_hash("ci_replay"),
    )
    assert target.state_hash("ci_replay") == source.state_hash("ci_replay")

    source.close()
    target.close()


def test_replay_blocks_revision_divergence(tmp_path):
    source = ConsciousnessStore(tmp_path / "source.db")
    target = ConsciousnessStore(tmp_path / "target.db")

    source.create_instance("replay-ai", "ci_diverge")
    target.create_instance("replay-ai", "ci_diverge")

    source.append_event(
        "ci_diverge",
        "WAKE",
        {"cycle": 1},
        created_at="2026-10-02T03:00:00+00:00",
    )
    delta = source.list_events_after("ci_diverge", after_revision=1)

    target.append_event(
        "ci_diverge",
        "DYNAMIC_UPDATE",
        {"delta": 99.0},
        created_at="2026-10-02T03:00:05+00:00",
    )

    with pytest.raises(ValueError, match="base_revision_mismatch"):
        target.replay_events(
            "ci_diverge",
            delta,
            base_revision=1,
            base_state_hash=None,
        )

    source.close()
    target.close()


def test_replay_requires_matching_parent_chain(tmp_path):
    store = ConsciousnessStore(tmp_path / "chain.db")
    store.create_instance("chain-ai", "ci_chain")

    event = {
        "event_id": "bad-event",
        "event_type": "WAKE",
        "payload": {"cycle": 1},
        "logical_revision": 2,
        "parent_event_id": "wrong-parent",
        "created_at": "2026-10-02T03:00:00+00:00",
    }

    with pytest.raises(ValueError, match="replay_parent_mismatch"):
        store.replay_events(
            "ci_chain",
            [event],
            base_revision=1,
            base_state_hash=store.state_hash("ci_chain"),
        )

    store.close()
