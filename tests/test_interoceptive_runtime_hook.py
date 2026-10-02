from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.storage import MemoryStore


class FakeProvider:
    def chat(self, messages, temperature=0.7):
        raise AssertionError("provider should not be called by autonomous wake")


def test_interoceptive_control_hook_is_default_off(tmp_path):
    store = MemoryStore(tmp_path / 'default.db')
    try:
        cfg = OrganismConfig(agent_id='agent-default')
        organism = PersistentOrganism(cfg, store, FakeProvider(), lambda _: None)
        result = organism.autonomous_wake_cycle()
        assert result is not None
        event = store.recent_events('agent-default', 1)[-1]
        assert event['payload']['interoceptive_control'] is None
    finally:
        store.conn.close()


def test_interoceptive_control_hook_can_run_autonomously(tmp_path):
    store = MemoryStore(tmp_path / 'enabled.db')
    try:
        cfg = OrganismConfig(
            agent_id='agent-enabled',
            interoceptive_control_enabled=True,
            interoceptive_control_mode='full',
        )
        organism = PersistentOrganism(cfg, store, FakeProvider(), lambda _: None)
        result = organism.autonomous_wake_cycle()
        assert result is not None
        event = store.recent_events('agent-enabled', 1)[-1]
        control = event['payload']['interoceptive_control']
        assert control['mode'] == 'full'
        assert len(control['candidates']) == 3
        assert control['chosen_signal'] in (-1.0, 0.0, 1.0)
    finally:
        store.conn.close()
