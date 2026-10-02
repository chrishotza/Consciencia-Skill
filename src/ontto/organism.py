from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from .bridge import DynamicStateBridge
from .dynamics import Config
from .provider import OpenAICompatibleProvider
from .storage import OntologicalState
from .persistence_backend import PersistenceBackend
from .self_observer import SelfObserver
from .trajectory_selector import TrajectorySelector
from .memory_policy import ContinuityMemoryPolicy
from .self_policy import SelfPolicy
from .meta_observer import MetaSelfObserver
from .action_conditioned_meta_observer import ActionConditionedMetaObserver


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
    self_observer_enabled: bool = True
    self_observer_update_enabled: bool = True
    self_observer_ridge: float = 1e-3
    self_observer_max_samples: int = 2048
    meta_self_observer_enabled: bool = False
    meta_self_observer_ridge: float = 1e-3
    meta_self_observer_max_samples: int = 2048
    action_conditioned_meta_observer_enabled: bool = False
    action_conditioned_meta_observer_ridge: float = 1e-3
    action_conditioned_meta_observer_max_samples: int = 2048
    action_conditioned_meta_observer_update_enabled: bool = True
    action_conditioned_meta_counterfactual_learning_enabled: bool = False
    self_selection_enabled: bool = True
    self_selection_attractor_weight: float = 0.70
    self_selection_coherence_weight: float = 0.30
    self_selection_meta_error_weight: float = 0.0
    self_selection_policy: str = "self_model"
    self_selection_signals: tuple[float, ...] = (-1.0, 0.0, 1.0)
    self_policy_enabled: bool = False
    self_policy_ridge: float = 1e-3
    semantic_dynamic_bridge_enabled: bool = False
    semantic_dynamic_scale: float = 1.0
    semantic_dynamic_importance: float = 0.65
    semantic_self_model_bridge_enabled: bool = False
    semantic_self_model_scale: float = 1.0
    semantic_self_model_importance: float = 0.65
    dream_semantic_bridge_enabled: bool = False
    dream_semantic_bridge_scale: float = 1.0
    dream_semantic_bridge_importance: float = 0.65


class PersistentOrganism:
    """24/7 persistent loop with WAKE and DREAM regimes."""

    def __init__(
        self,
        cfg: OrganismConfig,
        store: PersistenceBackend,
        provider: OpenAICompatibleProvider,
        sleep_fn: Callable[[float], None],
    ):
        self.cfg = cfg
        self.store = store
        self.provider = provider
        self.sleep_fn = sleep_fn
        self.state = store.load_state(cfg.agent_id)
        self.dynamic_bridge = DynamicStateBridge(Config(), seed=cfg.dynamic_seed)
        persisted_self_model = store.load_self_observer_model(cfg.agent_id)
        self.self_observer = (
            SelfObserver.from_dict(persisted_self_model)
            if persisted_self_model is not None
            else SelfObserver(
                ridge=cfg.self_observer_ridge,
                max_samples=cfg.self_observer_max_samples,
            )
        )
        self.meta_observer = MetaSelfObserver(
            ridge=cfg.meta_self_observer_ridge,
            max_samples=cfg.meta_self_observer_max_samples,
        )
        persisted_action_meta = (
            store.load_action_conditioned_meta_observer_model(cfg.agent_id)
        )
        self.action_conditioned_meta_observer = (
            ActionConditionedMetaObserver.from_dict(persisted_action_meta)
            if persisted_action_meta is not None
            else ActionConditionedMetaObserver(
                ridge=cfg.action_conditioned_meta_observer_ridge,
                max_samples=cfg.action_conditioned_meta_observer_max_samples,
            )
        )
        self.trajectory_selector = TrajectorySelector(
            attractor_weight=cfg.self_selection_attractor_weight,
            coherence_weight=cfg.self_selection_coherence_weight,
            meta_error_weight=cfg.self_selection_meta_error_weight,
        )
        persisted_self_policy = store.load_self_policy_model(cfg.agent_id)
        self.self_policy = (
            SelfPolicy.from_dict(persisted_self_policy)
            if persisted_self_policy is not None
            else SelfPolicy(ridge=cfg.self_policy_ridge)
        )
        self.memory_policy = ContinuityMemoryPolicy()
        if cfg.self_observer_enabled and persisted_self_model is None:
            for row in store.self_observer_trajectory(cfg.agent_id):
                features = np.asarray(row["features"], dtype=float)
                self.self_observer.observe(
                    features=features,
                    actual_state=float(row["actual_state"]),
                )
                if cfg.meta_self_observer_enabled:
                    self.meta_observer.observe(
                        features=features,
                        prediction_error=float(row["prediction_error"]),
                    )
            if self.self_observer.targets:
                self.store.save_self_observer_model(
                    cfg.agent_id,
                    self.self_observer.to_dict(),
                )
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

        step_start = self.state.dynamic_steps
        pre_previous_state = self.state.dynamic_prev_state
        pre_state = self.state.dynamic_state
        pre_memory = self.state.dynamic_memory
        pre_pressure = self.state.dynamic_pressure
        pre_attractor_distance = self.state.dynamic_attractor_distance
        observer_features = None
        prediction = None
        if self.cfg.self_observer_enabled:
            observer_features = SelfObserver.features_for(
                previous_state=self.state.dynamic_prev_state,
                state=self.state.dynamic_state,
                memory=self.state.dynamic_memory,
                pressure=self.state.dynamic_pressure,
                last_input=signal,
                attractor_distance=self.state.dynamic_attractor_distance,
                steps_delta=steps,
            )
            prediction = self.self_observer.predict(
                previous_state=self.state.dynamic_prev_state,
                state=self.state.dynamic_state,
                memory=self.state.dynamic_memory,
                pressure=self.state.dynamic_pressure,
                last_input=signal,
                attractor_distance=self.state.dynamic_attractor_distance,
                steps_delta=steps,
            )

        snapshot = self.dynamic_bridge.advance(
            previous_state=self.state.dynamic_prev_state,
            state=self.state.dynamic_state,
            memory=self.state.dynamic_memory,
            pressure=self.state.dynamic_pressure,
            signal=signal,
            steps=steps,
            step_index=step_start,
        )

        self.state.dynamic_prev_state = snapshot.previous_state
        self.state.dynamic_state = snapshot.state
        self.state.dynamic_memory = snapshot.memory
        self.state.dynamic_pressure = snapshot.pressure
        self.state.dynamic_attractor_distance = snapshot.attractor_distance
        self.state.dynamic_last_input = snapshot.last_input
        self.state.dynamic_steps = snapshot.steps

        if self.cfg.self_observer_enabled and prediction is not None and observer_features is not None:
            prediction_error = abs(snapshot.state - prediction.predicted_state)
            baseline_error = abs(snapshot.state - prediction.baseline_state)
            gain = baseline_error - prediction_error
            if self.cfg.self_observer_update_enabled:
                self.self_observer.observe(
                    features=observer_features,
                    actual_state=snapshot.state,
                )
                self.store.save_self_observer_model(
                    self.cfg.agent_id,
                    self.self_observer.to_dict(),
                )
            if self.cfg.meta_self_observer_enabled:
                self.meta_observer.observe(
                    features=observer_features,
                    prediction_error=prediction_error,
                )
            if (
                self.cfg.action_conditioned_meta_observer_enabled
                and self.cfg.action_conditioned_meta_observer_update_enabled
            ):
                action_meta_features = (
                    ActionConditionedMetaObserver.features_for(
                        previous_state=pre_previous_state,
                        state=pre_state,
                        memory=pre_memory,
                        pressure=pre_pressure,
                        last_input=signal,
                        attractor_distance=pre_attractor_distance,
                        steps_delta=steps,
                        predicted_state=prediction.predicted_state,
                        predicted_displacement=abs(
                            prediction.predicted_state - pre_state
                        ),
                    )
                )
                self.action_conditioned_meta_observer.observe(
                    features=action_meta_features,
                    prediction_error=prediction_error,
                )
                self.store.save_action_conditioned_meta_observer_model(
                    self.cfg.agent_id,
                    self.action_conditioned_meta_observer.to_dict(),
                )
            samples = len(self.self_observer.targets)
            confidence = min(1.0, samples / 32.0)
            self.state.self_prediction = prediction.predicted_state
            self.state.self_prediction_error = prediction_error
            self.state.self_prediction_gain = gain
            self.state.self_prediction_confidence = confidence
            self.state.self_prediction_samples = samples
            self.store.record_self_observer_snapshot(
                self.cfg.agent_id,
                mode=self.state.mode,
                label="self-observation",
                step_start=step_start,
                step_end=snapshot.steps,
                features=observer_features.tolist(),
                predicted_state=prediction.predicted_state,
                baseline_state=prediction.baseline_state,
                actual_state=snapshot.state,
                prediction_error=prediction_error,
                baseline_error=baseline_error,
                gain=gain,
                confidence=confidence,
                samples=samples,
            )
        label = {
            "DREAM": "dream",
            "WAKE": "autonomous" if signal == 0.0 else "wake",
        }.get(self.state.mode, self.state.mode.lower())
        self.store.record_dynamic_snapshot(
            self.cfg.agent_id,
            mode=self.state.mode,
            label=label,
            step_start=step_start,
            step_end=snapshot.steps,
            signal=signal,
            previous_state=snapshot.previous_state,
            state=snapshot.state,
            memory=snapshot.memory,
            pressure=snapshot.pressure,
            attractor_distance=snapshot.attractor_distance,
        )
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

        memory_candidate = self._extract_memory_candidate(out.text)
        self_model_candidate = self._extract_self_model_candidate(out.text)

        semantic_bridge = None
        semantic_self_model_bridge = None
        wake_signal = self.cfg.dynamic_wake_signal

        if self.cfg.semantic_dynamic_bridge_enabled and memory_candidate:
            semantic_bridge = self._semantic_dynamic_signal(memory_candidate)
            wake_signal = float(semantic_bridge["signal"])

        if (
            self.cfg.semantic_self_model_bridge_enabled
            and self_model_candidate
        ):
            semantic_self_model_bridge = self._semantic_self_model_signal(
                self_model_candidate
            )
            if self.cfg.semantic_dynamic_bridge_enabled and semantic_bridge:
                wake_signal = float(
                    0.5
                    * (
                        float(semantic_bridge["signal"])
                        + float(semantic_self_model_bridge["signal"])
                    )
                )
            else:
                wake_signal = float(semantic_self_model_bridge["signal"])

        self._extract_self_model(out.text)

        dynamic = self._advance_dynamic(
            wake_signal,
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
                "semantic_bridge": semantic_bridge,
                "semantic_self_model_bridge": semantic_self_model_bridge,
            },
        )
        self._extract_memory(out.text)
        self._refresh_operational_indicators()
        self.store.save_state(self.cfg.agent_id, self.state)
        return out.text

    def _extract_self_model_candidate(self, text: str) -> str | None:
        marker = "SELF_MODEL:"
        if marker not in text:
            return None
        candidate = text.split(marker, 1)[1].strip().splitlines()[0].strip()
        return candidate or None

    def _extract_self_model(self, text: str) -> bool:
        candidate = self._extract_self_model_candidate(text)
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

    def _extract_memory_candidate(self, text: str) -> str | None:
        marker = "MEMORY:"
        if marker not in text:
            return None
        memory = text.split(marker, 1)[1].strip().splitlines()[0].strip()
        return memory or None

    def _semantic_dynamic_signal(self, memory: str) -> dict[str, float | bool | str]:
        recent = self.store.recent_memories(
            self.cfg.agent_id,
            self.cfg.memory_limit,
        )
        admission = self.memory_policy.admit(
            memory,
            recent,
            importance=self.cfg.semantic_dynamic_importance,
        )
        omega = float(admission.decision.omega)
        signal = float(np.tanh(self.cfg.semantic_dynamic_scale * omega))
        return {
            "memory": memory,
            "novelty": float(admission.novelty),
            "coupling": float(admission.coupling),
            "persistence": float(admission.persistence),
            "omega": omega,
            "signal": signal,
            "admissible": bool(admission.decision.exists),
        }

    def _semantic_self_model_signal(self, self_model: str) -> dict[str, float | bool | str]:
        recent = [self.state.self_model] if self.state.self_model else []
        admission = self.memory_policy.admit(
            self_model,
            recent,
            importance=self.cfg.semantic_self_model_importance,
        )
        omega = float(admission.decision.omega)
        signal = float(np.tanh(self.cfg.semantic_self_model_scale * omega))
        return {
            "self_model": self_model,
            "novelty": float(admission.novelty),
            "coupling": float(admission.coupling),
            "persistence": float(admission.persistence),
            "omega": omega,
            "signal": signal,
            "admissible": bool(admission.decision.exists),
        }

    def _extract_memory(self, text: str) -> None:
        memory = self._extract_memory_candidate(text)
        if memory:
            self.store.add_memory(
                self.cfg.agent_id,
                memory,
                importance=self.cfg.semantic_dynamic_importance,
            )

    def _calibrate_action_conditioned_meta_candidates(
        self,
        candidates: tuple,
    ) -> int:
        if not (
            self.cfg.action_conditioned_meta_observer_enabled
            and self.cfg.action_conditioned_meta_counterfactual_learning_enabled
        ):
            return 0

        step_start = self.state.dynamic_steps
        bridge = DynamicStateBridge(
            self.dynamic_bridge.cfg,
            seed=self.dynamic_bridge.seed,
        )
        for candidate in candidates:
            predicted_state = float(candidate.prediction.predicted_state)
            snapshot = bridge.advance(
                previous_state=self.state.dynamic_prev_state,
                state=self.state.dynamic_state,
                memory=self.state.dynamic_memory,
                pressure=self.state.dynamic_pressure,
                signal=float(candidate.signal),
                steps=self.cfg.dynamic_autonomous_steps,
                step_index=step_start,
            )
            prediction_error = abs(
                float(snapshot.state) - predicted_state
            )
            features = ActionConditionedMetaObserver.features_for(
                previous_state=self.state.dynamic_prev_state,
                state=self.state.dynamic_state,
                memory=self.state.dynamic_memory,
                pressure=self.state.dynamic_pressure,
                last_input=float(candidate.signal),
                attractor_distance=self.state.dynamic_attractor_distance,
                steps_delta=self.cfg.dynamic_autonomous_steps,
                predicted_state=predicted_state,
                predicted_displacement=float(candidate.displacement),
            )
            self.action_conditioned_meta_observer.observe(
                features=features,
                prediction_error=prediction_error,
            )

        self.store.save_action_conditioned_meta_observer_model(
            self.cfg.agent_id,
            self.action_conditioned_meta_observer.to_dict(),
        )
        return len(candidates)

    def autonomous_wake_cycle(self) -> dict[str, float | int] | None:
        self.state.mode = "WAKE"
        self.state.lifetime_wake_cycles += 1

        chosen_signal = 0.0
        candidates = ()
        counterfactual_meta_samples_added = 0
        if self.cfg.self_selection_enabled and self.cfg.self_observer_enabled:
            candidates = self.trajectory_selector.evaluate(
                self.self_observer,
                current_state=self.state.dynamic_state,
                current_memory=self.state.dynamic_memory,
                current_pressure=self.state.dynamic_pressure,
                current_input=self.state.dynamic_last_input,
                current_attractor=self.dynamic_bridge.cfg.attractor,
                steps_delta=self.cfg.dynamic_autonomous_steps,
                signals=self.cfg.self_selection_signals,
                meta_observer=(
                    self.meta_observer
                    if self.cfg.meta_self_observer_enabled
                    else None
                ),
            )
            counterfactual_meta_samples_added = (
                self._calibrate_action_conditioned_meta_candidates(candidates)
            )
            if self.cfg.action_conditioned_meta_observer_enabled:
                scored = []
                for candidate in candidates:
                    prediction_error = self.action_conditioned_meta_observer.predict_error(
                        previous_state=self.state.dynamic_prev_state,
                        state=self.state.dynamic_state,
                        memory=self.state.dynamic_memory,
                        pressure=self.state.dynamic_pressure,
                        last_input=float(candidate.signal),
                        attractor_distance=self.state.dynamic_attractor_distance,
                        steps_delta=self.cfg.dynamic_autonomous_steps,
                        predicted_state=float(candidate.prediction.predicted_state),
                        predicted_displacement=float(candidate.displacement),
                    )
                    scored.append(
                        (
                            float(prediction_error),
                            abs(float(candidate.signal)),
                            candidate,
                            float(prediction_error),
                        )
                    )
                _, _, chosen, _ = min(
                    scored,
                    key=lambda row: (row[0], row[1]),
                )
            elif self.cfg.self_policy_enabled:
                policy_candidates = [
                    {
                        "current_state": float(self.state.dynamic_state),
                        "attractor_distance": float(candidate.attractor_distance),
                        "predicted_state": float(candidate.prediction.predicted_state),
                        "predicted_displacement": float(candidate.displacement),
                        "signal": float(candidate.signal),
                    }
                    for candidate in candidates
                ]
                chosen_row = self.self_policy.choose(policy_candidates)
                chosen = next(
                    candidate
                    for candidate in candidates
                    if candidate.signal == float(chosen_row["signal"])
                )
            elif self.cfg.self_selection_policy == "self_model":
                chosen = self.trajectory_selector.choose(candidates)
            elif self.cfg.self_selection_policy == "random":
                import random
                rng = random.Random(self.cfg.dynamic_seed + self.state.dynamic_steps)
                chosen = rng.choice(list(candidates))
            else:
                raise ValueError(
                    f"unknown self_selection_policy={self.cfg.self_selection_policy!r}"
                )
            chosen_signal = chosen.signal

        dynamic = self._advance_dynamic(
            chosen_signal,
            self.cfg.dynamic_autonomous_steps,
        )
        self.store.add_event(
            self.cfg.agent_id,
            "WAKE",
            "autonomous",
            {
                "dynamic": dynamic,
                "self_selection": {
                    "enabled": bool(self.cfg.self_selection_enabled and self.cfg.self_observer_enabled),
                    "policy": (
                        "action_conditioned_second_order"
                        if self.cfg.action_conditioned_meta_observer_enabled
                        else (
                            "learned_self_policy"
                            if self.cfg.self_policy_enabled
                            else self.cfg.self_selection_policy
                        )
                    ),
                    "candidate_signals": list(self.cfg.self_selection_signals),
                    "self_policy_enabled": bool(self.cfg.self_policy_enabled),
                    "self_policy_samples": len(self.self_policy.targets),
                    "meta_self_model_enabled": bool(self.cfg.meta_self_observer_enabled),
                    "action_conditioned_meta_model_enabled": bool(
                        self.cfg.action_conditioned_meta_observer_enabled
                    ),
                    "action_conditioned_meta_model_updates_enabled": bool(
                        self.cfg.action_conditioned_meta_observer_update_enabled
                    ),
                    "action_conditioned_meta_model_samples": len(
                        self.action_conditioned_meta_observer.targets
                    ),
                    "action_conditioned_meta_counterfactual_learning_enabled": bool(
                        self.cfg.action_conditioned_meta_counterfactual_learning_enabled
                    ),
                    "counterfactual_meta_samples_added": counterfactual_meta_samples_added,
                    "chosen_signal": chosen_signal,
                    "candidates": [
                        {
                            "signal": candidate.signal,
                            "predicted_state": candidate.prediction.predicted_state,
                            "predicted_attractor_distance": candidate.attractor_distance,
                            "predicted_displacement": candidate.displacement,
                            "predicted_error": candidate.predicted_error,
                            "score": candidate.score,
                            "action_conditioned_predicted_error": (
                                float(
                                    self.action_conditioned_meta_observer.predict_error(
                                        previous_state=self.state.dynamic_prev_state,
                                        state=self.state.dynamic_state,
                                        memory=self.state.dynamic_memory,
                                        pressure=self.state.dynamic_pressure,
                                        last_input=float(candidate.signal),
                                        attractor_distance=self.state.dynamic_attractor_distance,
                                        steps_delta=self.cfg.dynamic_autonomous_steps,
                                        predicted_state=float(candidate.prediction.predicted_state),
                                        predicted_displacement=float(candidate.displacement),
                                    )
                                )
                                if self.cfg.action_conditioned_meta_observer_enabled
                                else None
                            ),
                            "samples": candidate.prediction.samples,
                            "confidence": candidate.prediction.confidence,
                        }
                        for candidate in candidates
                    ],
                },
            },
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

        memory_candidate = self._extract_memory_candidate(out.text)
        self_model_candidate = self._extract_self_model_candidate(out.text)

        dream_semantic_bridge = None
        dream_self_model_bridge = None
        dream_signal = 0.0

        if self.cfg.dream_semantic_bridge_enabled and memory_candidate:
            recent = self.store.recent_memories(
                self.cfg.agent_id,
                self.cfg.memory_limit,
            )
            admission = self.memory_policy.admit(
                memory_candidate,
                recent,
                importance=self.cfg.dream_semantic_bridge_importance,
            )
            omega = float(admission.decision.omega)
            signal = float(
                np.tanh(self.cfg.dream_semantic_bridge_scale * omega)
            )
            dream_semantic_bridge = {
                "memory": memory_candidate,
                "omega": omega,
                "signal": signal,
                "novelty": float(admission.novelty),
                "coupling": float(admission.coupling),
                "persistence": float(admission.persistence),
                "admissible": bool(admission.decision.exists),
            }

        if self.cfg.dream_semantic_bridge_enabled and self_model_candidate:
            dream_self_model_bridge = self._semantic_self_model_signal(
                self_model_candidate
            )

        signals = []
        if dream_semantic_bridge is not None:
            signals.append(float(dream_semantic_bridge["signal"]))
        if dream_self_model_bridge is not None:
            signals.append(float(dream_self_model_bridge["signal"]))
        if signals:
            dream_signal = float(np.mean(signals))

        self._extract_memory(out.text)
        self._extract_self_model(out.text)
        self.state.last_thought = out.text[-1400:]
        dynamic = self._advance_dynamic(
            dream_signal,
            self.cfg.dynamic_dream_steps,
        )
        self.store.add_event(
            self.cfg.agent_id,
            "DREAM",
            "consolidation",
            {
                "summary": out.text[-2500:],
                "dynamic": dynamic,
                "semantic_bridge": dream_semantic_bridge,
                "semantic_self_model_bridge": dream_self_model_bridge,
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
