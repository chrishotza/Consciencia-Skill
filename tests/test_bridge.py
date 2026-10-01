from pathlib import Path

from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.bridge import DynamicStateBridge
from src.ontto.storage import MemoryStore


class FakeProvider:
    def chat(self, messages, temperature=0.7):
        class Response:
            text = (
                "MEMORY: La trayectoria persistente debe conservar relaciones.\n"
                "SELF_MODEL: Tengo estado dinámico persistente."
            )
            raw = {"fake": True}

        return Response()


def test_bridge_advances_reproducibly():
    first = DynamicStateBridge(seed=9).advance(
        previous_state=0.0,
        state=0.0,
        memory=0.0,
        pressure=0.0,
        signal=1.0,
        steps=3,
        step_index=0,
    )
    second = DynamicStateBridge(seed=9).advance(
        previous_state=0.0,
        state=0.0,
        memory=0.0,
        pressure=0.0,
        signal=1.0,
        steps=3,
        step_index=0,
    )

    assert first == second
    assert first.steps == 3
    assert first.state != 0.0


def test_organism_persists_dynamic_state_and_autonomous_cycle(tmp_path: Path):
    store = MemoryStore(tmp_path / "organism.db")
    organism = PersistentOrganism(
        OrganismConfig(agent_id="test-agent"),
        store,
        FakeProvider(),
        lambda _: None,
    )

    organism.wake_cycle("Primera interacción")
    before = store.persistence_observables("test-agent")

    assert before["dynamic_steps"] == 1
    assert before["dynamic_state"] != 0.0

    organism.autonomous_wake_cycle()
    middle = store.persistence_observables("test-agent")
    assert middle["dynamic_steps"] == 2

    store.conn.close()

    reopened = MemoryStore(tmp_path / "organism.db")
    restored = reopened.load_state("test-agent")
    assert restored.dynamic_steps == 2
    assert restored.dynamic_state == middle["dynamic_state"]
