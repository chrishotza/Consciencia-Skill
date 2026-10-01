from pathlib import Path

from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.provider import LLMResponse
from src.ontto.storage import MemoryStore


class FakeProvider:
    def __init__(self):
        self.calls = []

    def chat(self, messages, temperature=0.7):
        self.calls.append((messages, temperature))
        last = messages[-1]["content"]
        if "Entraste en SUEÑO" in last:
            text = (
                "Reorganicé mi trayectoria. "
                "MEMORY: La continuidad entre ciclos debe conservar relaciones, no solo texto.\n"
                "SELF_MODEL: Mantengo estado persistente y puedo cambiar de régimen.\n"
                "DREAM_SUMMARY: Consolidé una relación entre memoria y continuidad."
            )
        else:
            text = (
                "Procesé el estímulo. "
                "MEMORY: La interacción actual pertenece a una trayectoria continua.\n"
            )
        return LLMResponse(text=text, raw={"fake": True})


def test_wake_dream_wake_persistence(tmp_path: Path):
    store = MemoryStore(tmp_path / "organism.db")
    provider = FakeProvider()
    cfg = OrganismConfig(
        agent_id="test-agent",
        memory_limit=10,
        event_limit=10,
    )
    organism = PersistentOrganism(cfg, store, provider, lambda _: None)

    first = organism.wake_cycle("Primera interacción")
    assert "MEMORY:" in first
    assert len(store.recent_memories("test-agent")) == 1
    assert store.load_state("test-agent").dynamic_steps == 1
    assert len(store.recent_events("test-agent")) == 2
    assert store.load_state("test-agent").boot_count == 1

    organism.dream_cycle()
    state_after_dream = store.load_state("test-agent")
    assert state_after_dream.mode == "WAKE"
    assert state_after_dream.self_model_version == 1
    assert state_after_dream.self_model != ""
    assert len(store.recent_memories("test-agent")) >= 2

    organism.wake_cycle("Segunda interacción")
    events = store.recent_events("test-agent", 20)
    assert [e["kind"] for e in events if e["kind"] != "boot"] == [
        "interaction",
        "consolidation",
        "interaction",
    ]

    trajectory_before_reopen = store.persistence_observables("test-agent")

    restored_store = MemoryStore(tmp_path / "organism.db")
    restored = restored_store.load_state("test-agent")
    assert restored.self_model_version == 1
    assert restored.last_thought != ""
    assert restored.lifetime_wake_cycles == 2
    assert restored.lifetime_dream_cycles == 1
    assert restored.boot_count == 1

    trajectory_after_reopen = restored_store.persistence_observables("test-agent")
    assert trajectory_after_reopen["trajectory_fingerprint"] == trajectory_before_reopen["trajectory_fingerprint"]
    assert trajectory_after_reopen["state_fingerprint"] == trajectory_before_reopen["state_fingerprint"]
    assert restored_store.load_state("test-agent").dynamic_steps == 1

    organism.dream_cycle()
    repeated_dream = store.load_state("test-agent")
    assert repeated_dream.self_model_version == 1


class FailingDreamProvider:
    def chat(self, messages, temperature=0.7):
        last = messages[-1]["content"]
        if "Entraste en SUEÑO" in last:
            raise RuntimeError("synthetic dream provider failure")
        return LLMResponse(
            text="MEMORY: wake event survived provider failure.",
            raw={"fake": True},
        )


def test_dream_provider_failure_recovers_to_wake(tmp_path: Path):
    db = tmp_path / "dream-failure.db"
    store = MemoryStore(db)
    organism = PersistentOrganism(
        OrganismConfig(agent_id="failure-agent"),
        store,
        FailingDreamProvider(),
        lambda _: None,
    )

    try:
        organism.dream_cycle()
    except RuntimeError:
        pass
    else:
        raise AssertionError("dream provider failure was expected")

    state = store.load_state("failure-agent")
    events = store.recent_events("failure-agent", 20)

    assert state.mode == "WAKE"
    assert state.lifetime_dream_cycles == 1
    assert any(e["kind"] == "dream_failed" for e in events)
