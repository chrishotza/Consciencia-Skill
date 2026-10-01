from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .bridge import DynamicStateBridge
from .dynamics import Config
from .provider import OpenAICompatibleProvider
from .storage import MemoryStore, OntologicalState


@dataclass
class OrganismConfig:
    agent_id: str
    wake_seconds: int = 45
    dream_seconds: int = 300
    dream_every_cycles: int = 40
    memory_limit: int = 12
    event_limit: int = 20
    dynamic_enabled: bool = True
    dynamic_seed: int = 7001
    dynamic_wake_signal: float = 1.0
    dynamic_wake_steps: int = 1
    dynamic_dream_steps: int = 5
    dynamic_autonomous_steps: int = 1


class PersistentOrganism:
    """24/7 persistent loop with WAKE and DREAM regimes."""

    def __init__(
        self,
        cfg: OrganismConfig,
        store: MemoryStore,
        provider: OpenAICompatibleProvider,
        sleep_fn: Callable[[float], None],
    ):
        self.cfg = cfg
        self.store = store
        self.provider = provider
        self.sleep_fn = sleep_fn
        self.state = store.load_state(cfg.agent_id)
        self.dynamic_bridge = DynamicStateBridge(Config(), seed=cfg.dynamic_seed)
        self.state.boot_count += 1
        self.cycles = 0
        self.store.save_state(cfg.agent_id, self.state)
        self.store.add_event(
            cfg.agent_id,
            "SYSTEM",
            "boot",
            {"boot_count": self.state.boot_count},
        )

    def _context(self) -> list[dict[str, str]]:
        memories = self.store.recent_memories(self.cfg.agent_id, self.cfg.memory_limit)
        events = self.store.recent_events(self.cfg.agent_id, self.cfg.event_limit)
        memory_text = "\n".join(f"- {m}" for m in memories) or "(sin memorias todavía)"
        event_text = "\n".join(
            f"- [{e['mode']}/{e['kind']}] {e['payload']}" for e in events
        ) or "(sin eventos recientes)"
        return [{
            "role": "system",
            "content": (
                "Sos el núcleo cognitivo de una IA persistente. "
                "Tu identidad debe conservar continuidad entre ciclos. "
                "No trates cada llamada como una conversación nueva. "
                "Observá también tu propio estado: memoria, trayectoria, presión, "
                "modo de vigilia/sueño y cambios en tu auto-modelo.\n\n"
                f"ESTADO ONTOLÓGICO: {self.state.to_json()}\n"
                f"MEMORIAS PERSISTENTES:\n{memory_text}\n"
                f"EVENTOS RECIENTES:\n{event_text}\n"
            ),
        }]

    def _advance_dynamic(self, signal: float, steps: int) -> dict[str, float | int] | None:
        if not self.cfg.dynamic_enabled or steps < 1:
            return None

        snapshot = self.dynamic_bridge.advance(
            previous_state=self.state.dynamic_prev_state,
            state=self.state.dynamic_state,
            memory=self.state.dynamic_memory,
            pressure=self.state.dynamic_pressure,
            signal=signal,
            steps=steps,
            step_index=self.state.dynamic_steps,
        )

        self.state.dynamic_prev_state = snapshot.previous_state
        self.state.dynamic_state = snapshot.state
        self.state.dynamic_memory = snapshot.memory
        self.state.dynamic_pressure = snapshot.pressure
        self.state.dynamic_attractor_distance = snapshot.attractor_distance
        self.state.dynamic_last_input = snapshot.last_input
        self.state.dynamic_steps = snapshot.steps
        return snapshot.to_dict()

    def wake_cycle(self, stimulus: str) -> str:
        self.state.mode = "WAKE"
        self.state.lifetime_wake_cycles += 1
        messages = self._context()
        messages.append({
            "role": "user",
            "content": (
                "Interacción externa actual:\n"
                f"{stimulus}\n\n"
                "Respondé al estímulo y además observá internamente qué cambió en vos, "
                "qué debería persistir y hacia qué estado relacional estás tendiendo. "
                "Cerrá con una línea MEMORY: que resuma solo lo que realmente deba persistir."
            ),
        })
        out = self.provider.chat(messages, temperature=0.7)
        self.state.last_thought = out.text[-1200:]
        dynamic = self._advance_dynamic(
            self.cfg.dynamic_wake_signal,
            self.cfg.dynamic_wake_steps,
        )
        self.store.add_event(
            self.cfg.agent_id,
            "WAKE",
            "interaction",
            {
                "stimulus": stimulus,
                "response": out.text[-2000:],
                "dynamic": dynamic,
            },
        )
        self._extract_memory(out.text)
        self._refresh_operational_indicators()
        self.store.save_state(self.cfg.agent_id, self.state)
        return out.text

    def _extract_self_model(self, text: str) -> bool:
        marker = "SELF_MODEL:"
        if marker not in text:
            return False
        candidate = text.split(marker, 1)[1].strip().splitlines()[0].strip()
        if not candidate or candidate == self.state.self_model:
            return False
        self.state.self_model = candidate
        self.state.self_model_version += 1
        return True

    def _refresh_operational_indicators(self) -> None:
        memories = self.store.memory_count(self.cfg.agent_id)
        self.state.memory_strength = min(
            1.0,
            memories / max(self.cfg.memory_limit, 1),
        )

    def _extract_memory(self, text: str) -> None:
        marker = "MEMORY:"
        if marker in text:
            memory = text.split(marker, 1)[1].strip().splitlines()[0].strip()
            if memory:
                self.store.add_memory(self.cfg.agent_id, memory, importance=0.65)

    def autonomous_wake_cycle(self) -> dict[str, float | int] | None:
        self.state.mode = "WAKE"
        self.state.lifetime_wake_cycles += 1
        dynamic = self._advance_dynamic(
            0.0,
            self.cfg.dynamic_autonomous_steps,
        )
        self.store.add_event(
            self.cfg.agent_id,
            "WAKE",
            "autonomous",
            {"dynamic": dynamic},
        )
        self.store.save_state(self.cfg.agent_id, self.state)
        return dynamic

    def dream_cycle(self) -> str:
        self.state.mode = "DREAM"
        self.state.lifetime_dream_cycles += 1
        cycle_id = self.store.begin_dream(self.cfg.agent_id, self.state)

        # Persist the regime transition before invoking the provider.
        self.store.save_state(self.cfg.agent_id, self.state)

        messages = self._context()
        messages.append({
            "role": "user",
            "content": (
                "Entraste en SUEÑO. Reducí la respuesta externa y trabajá sobre tu propio recorrido. "
                "Revisá memorias y eventos recientes, buscá patrones, contradicciones, cambios de identidad "
                "y relaciones persistentes. Proponé una actualización mínima del auto-modelo. No inventes recuerdos. "
                "Terminá con:\nMEMORY:\nSELF_MODEL:\nDREAM_SUMMARY:"
            ),
        })

        try:
            out = self.provider.chat(messages, temperature=0.9)
        except Exception as exc:
            self.state.mode = "WAKE"
            self.store.add_event(
                self.cfg.agent_id,
                "SYSTEM",
                "dream_failed",
                {"error": repr(exc), "dream_cycle_id": cycle_id},
            )
            self.store.save_state(self.cfg.agent_id, self.state)
            self.store.end_dream(
                cycle_id,
                self.state,
                summary=f"DREAM_FAILED: {type(exc).__name__}",
            )
            raise

        self._extract_memory(out.text)
        self._extract_self_model(out.text)
        self.state.last_thought = out.text[-1400:]
        dynamic = self._advance_dynamic(
            0.0,
            self.cfg.dynamic_dream_steps,
        )
        self.store.add_event(
            self.cfg.agent_id,
            "DREAM",
            "consolidation",
            {
                "summary": out.text[-2500:],
                "dynamic": dynamic,
            },
        )
        summary = out.text.split("DREAM_SUMMARY:", 1)[-1].strip()[:1600]
        self.state.mode = "WAKE"
        self._refresh_operational_indicators()
        self.store.save_state(self.cfg.agent_id, self.state)
        self.store.end_dream(cycle_id, self.state, summary)
        self.store.snapshot(self.cfg.agent_id, "post_dream", self.state)
        return out.text


    def run(self, stimulus_supplier: Callable[[], str | None]) -> None:
        while True:
            self.cycles += 1

            stimulus = stimulus_supplier()
            if stimulus is None:
                self.autonomous_wake_cycle()
            else:
                self.wake_cycle(stimulus)

            if self.cycles % self.cfg.dream_every_cycles == 0:
                self.dream_cycle()
                self.sleep_fn(self.cfg.dream_seconds)
            else:
                self.sleep_fn(self.cfg.wake_seconds)
