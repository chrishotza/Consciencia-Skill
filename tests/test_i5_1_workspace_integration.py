from pathlib import Path

from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.provider import LLMResponse
from src.ontto.storage import MemoryStore

class FakeProvider:
    def chat(self, messages, temperature=0.7):
        return LLMResponse(
            text="Calibration response.\nMEMORY: retain dynamic continuity.\nSELF_MODEL: internal state follows trajectory.",
            raw={"fake": True},
        )

def test_workspace_changes_autonomous_event_when_enabled(tmp_path: Path):
    db = tmp_path / "workspace.db"
    store = MemoryStore(db)
    base_cfg = OrganismConfig(agent_id="workspace", dream_every_cycles=10000, event_limit=0, self_observer_enabled=True, self_selection_enabled=False, workspace_enabled=False)
    organism = PersistentOrganism(base_cfg, store, FakeProvider(), lambda _: None)
    for i in range(12): organism.wake_cycle(f"warmup {i}")
    store.conn.close()
    store = MemoryStore(db)
    cfg = OrganismConfig(agent_id="workspace", dream_every_cycles=10000, event_limit=0, self_observer_enabled=True, self_selection_enabled=True, self_selection_signals=(-1.0,1.0), workspace_enabled=True)
    organism = PersistentOrganism(cfg, store, FakeProvider(), lambda _: None)
    organism.autonomous_wake_cycle()
    event = store.recent_events("workspace", 1)[0]
    control = event["payload"]["self_selection"]["workspace_control"]
    assert control["enabled"] is True
    assert len(control["selected_modules"]) == 2
    assert len(control["broadcast"]) == 2
    assert store.persistence_observables("workspace")["workspace_steps"] == 1

def test_workspace_runtime_observables_survive_restart(tmp_path: Path):
    db = tmp_path / "restart.db"
    store = MemoryStore(db)
    cfg = OrganismConfig(agent_id="restart", dream_every_cycles=10000, event_limit=0, self_observer_enabled=True, self_selection_enabled=True, self_selection_signals=(-1.0,1.0), workspace_enabled=True)
    organism = PersistentOrganism(cfg, store, FakeProvider(), lambda _: None)
    for i in range(10):
        organism.wake_cycle(f"warmup {i}")
        organism.autonomous_wake_cycle()
    before = store.persistence_observables("restart")
    store.conn.close()
    restored_store = MemoryStore(db)
    after = restored_store.persistence_observables("restart")
    assert after["workspace_last_selected_module"] == before["workspace_last_selected_module"]
    assert after["workspace_last_broadcast"] == before["workspace_last_broadcast"]
    assert after["workspace_steps"] == before["workspace_steps"]