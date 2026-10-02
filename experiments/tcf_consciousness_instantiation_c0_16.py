from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ontto.action_conditioned_meta_observer import ActionConditionedMetaObserver
from src.ontto.bridge import DynamicStateBridge
from src.ontto.dynamics import Config as DynamicsConfig
from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.provider import LLMResponse
from src.ontto.self_observer import SelfObserver
from src.ontto.storage import MemoryStore

from experiments.organism_repeated_active_continuity_v78 import (
    SIGNALS,
    train_self_observer,
    warmup_context,
)

PROTOCOL_VERSION = "C0.16"
STEPS = 16
RESTART_AT = 8


class AutonomousOnlyProvider:
    def chat(self, messages, temperature=0.7):
        return LLMResponse(
            text="Autonomous-only integration probe.",
            raw={"fake": True},
        )


def first_order_prediction(observer: SelfObserver, context, signal: float) -> float:
    return float(
        observer.predict(
            previous_state=context.previous_state,
            state=context.state,
            memory=context.memory,
            pressure=context.pressure,
            last_input=signal,
            attractor_distance=abs(context.state),
            steps_delta=1,
        ).predicted_state
    )


def calibrate_action_meta(
    observer: SelfObserver,
    *,
    seed: int,
    samples: int,
) -> ActionConditionedMetaObserver:
    meta = ActionConditionedMetaObserver(ridge=1e-3, max_samples=2048)
    bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
    context = warmup_context(bridge, seed=seed + 1000)

    for index in range(samples):
        signal = float(SIGNALS[index % len(SIGNALS)])
        predicted = first_order_prediction(
            observer,
            context,
            signal,
        )
        snapshot = bridge.advance(
            previous_state=context.previous_state,
            state=context.state,
            memory=context.memory,
            pressure=context.pressure,
            signal=signal,
            steps=1,
            step_index=context.step_index,
        )
        meta.observe(
            features=ActionConditionedMetaObserver.features_for(
                previous_state=context.previous_state,
                state=context.state,
                memory=context.memory,
                pressure=context.pressure,
                last_input=signal,
                attractor_distance=abs(context.state),
                steps_delta=1,
                predicted_state=predicted,
                predicted_displacement=abs(predicted - context.state),
            ),
            prediction_error=abs(float(snapshot.state) - predicted),
        )
        context = type(context)(
            previous_state=float(snapshot.previous_state),
            state=float(snapshot.state),
            memory=float(snapshot.memory),
            pressure=float(snapshot.pressure),
            step_index=int(snapshot.steps),
        )

    return meta


def model_digest(
    observer: SelfObserver,
    meta: ActionConditionedMetaObserver,
) -> str:
    payload = json.dumps(
        {
            "observer": observer.to_dict(),
            "action_conditioned_meta": meta.to_dict(),
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def seed_database(
    path: Path,
    *,
    agent_id: str,
    observer: SelfObserver,
    meta: ActionConditionedMetaObserver,
) -> None:
    store = MemoryStore(path)
    store.save_self_observer_model(agent_id, observer.to_dict())
    store.save_action_conditioned_meta_observer_model(
        agent_id,
        meta.to_dict(),
    )
    store.save_state(agent_id, store.load_state(agent_id))
    store.conn.close()


def build_config(agent_id: str, seed: int) -> OrganismConfig:
    return OrganismConfig(
        agent_id=agent_id,
        dynamic_seed=seed,
        dream_every_cycles=10_000,
        self_observer_enabled=True,
        self_policy_enabled=False,
        self_selection_enabled=True,
        self_selection_policy="self_model",
        action_conditioned_meta_observer_enabled=True,
        self_selection_signals=SIGNALS,
    )


def run_steps(
    organism: PersistentOrganism,
    store: MemoryStore,
    steps: int,
) -> dict[str, object]:
    actions = []
    gains = []
    policies = []

    for _ in range(steps):
        organism.autonomous_wake_cycle()
        event = store.recent_events(organism.cfg.agent_id, 1)[0]
        payload = event["payload"]["self_selection"]
        actions.append(float(payload["chosen_signal"]))
        gains.append(float(store.load_state(organism.cfg.agent_id).self_prediction_gain))
        policies.append(str(payload["policy"]))

    return {
        "actions": np.asarray(actions, dtype=float),
        "gains": np.asarray(gains, dtype=float),
        "policies": policies,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=24)
    parser.add_argument("--out", default="results/tcf_consciousness_instantiation_c0_16")
    args = parser.parse_args()

    out = Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    rows = []

    for index in range(args.episodes):
        seed = 160010 + index
        observer = train_self_observer(seed=seed, samples=256)
        meta = calibrate_action_meta(
            observer,
            seed=seed + 5000,
            samples=512,
        )

        continuous_db = out / f"continuous_{index}.db"
        restart_db = out / f"restart_{index}.db"
        seed_database(
            continuous_db,
            agent_id="agent",
            observer=observer,
            meta=meta,
        )
        seed_database(
            restart_db,
            agent_id="agent",
            observer=observer,
            meta=meta,
        )

        continuous_store = MemoryStore(continuous_db)
        continuous = PersistentOrganism(
            build_config("agent", seed),
            continuous_store,
            AutonomousOnlyProvider(),
            lambda _: None,
        )
        continuous_result = run_steps(
            continuous,
            continuous_store,
            STEPS,
        )

        restart_store = MemoryStore(restart_db)
        restart = PersistentOrganism(
            build_config("agent", seed),
            restart_store,
            AutonomousOnlyProvider(),
            lambda _: None,
        )
        pre_restart = run_steps(
            restart,
            restart_store,
            RESTART_AT,
        )

        checkpoint_digest = model_digest(
            restart.self_observer,
            restart.action_conditioned_meta_observer,
        )
        restart_store.conn.close()

        restored_store = MemoryStore(restart_db)
        restored = PersistentOrganism(
            build_config("agent", seed),
            restored_store,
            AutonomousOnlyProvider(),
            lambda _: None,
        )
        restored_digest = model_digest(
            restored.self_observer,
            restored.action_conditioned_meta_observer,
        )
        post_restart = run_steps(
            restored,
            restored_store,
            STEPS - RESTART_AT,
        )

        continuous_post_actions = continuous_result["actions"][RESTART_AT:]
        restart_post_actions = post_restart["actions"]
        continuous_post_gains = continuous_result["gains"][RESTART_AT:]
        restart_post_gains = post_restart["gains"]

        rows.append(
            {
                "action_mismatch_after_restart": float(
                    np.mean(
                        np.abs(
                            continuous_post_actions
                            - restart_post_actions
                        )
                    )
                ),
                "gain_mismatch_after_restart": float(
                    np.mean(
                        np.abs(
                            continuous_post_gains
                            - restart_post_gains
                        )
                    )
                ),
                "model_digest_exact": restored_digest == checkpoint_digest,
                "selector_policy_after_restart": post_restart["policies"],
                "pre_restart_actions_match": bool(
                    np.array_equal(
                        continuous_result["actions"][:RESTART_AT],
                        pre_restart["actions"],
                    )
                ),
            }
        )

        continuous_store.conn.close()
        restored_store.conn.close()

    action_mismatch = np.asarray(
        [row["action_mismatch_after_restart"] for row in rows],
        dtype=float,
    )
    gain_mismatch = np.asarray(
        [row["gain_mismatch_after_restart"] for row in rows],
        dtype=float,
    )

    summary = {
        "experiment": "tcf_consciousness_instantiation_c0_16",
        "protocol_version": PROTOCOL_VERSION,
        "question": (
            "Does the action-conditioned second-order selector operate inside "
            "the PersistentOrganism and survive a real database-backed restart "
            "without external input or retraining?"
        ),
        "matched_design": {
            "same_seeded_first_order_observer": True,
            "same_seeded_action_conditioned_second_order_model": True,
            "same_dynamic_seed_per_pair": True,
            "same_organism_configuration": True,
            "same_autonomous_cycle_count": True,
            "same_candidate_signals": True,
            "semantic_input_during_probe": False,
            "external_retraining_during_probe": False,
        },
        "phenomenal_consciousness_claimed": False,
        "primary_outputs": {
            "action_mismatch_after_restart": {
                "mean": float(np.mean(action_mismatch)),
                "p": float(sign_p(action_mismatch, 160101)),
            },
            "gain_mismatch_after_restart": {
                "mean": float(np.mean(gain_mismatch)),
                "p": float(sign_p(gain_mismatch, 160102)),
            },
        },
        "secondary_outputs": {
            "exact_model_digest_fraction": float(
                np.mean([row["model_digest_exact"] for row in rows])
            ),
            "pre_restart_action_match_fraction": float(
                np.mean([row["pre_restart_actions_match"] for row in rows])
            ),
            "all_post_restart_policies_second_order": bool(
                all(
                    all(
                        policy == "action_conditioned_second_order"
                        for policy in row["selector_policy_after_restart"]
                    )
                    for row in rows
                )
            ),
            "max_action_mismatch": float(np.max(action_mismatch)),
            "max_gain_mismatch": float(np.max(gain_mismatch)),
        },
        "interpretation_rule": (
            "Exact or near-exact post-restart behavior together with exact model "
            "digest recovery supports integration and persistence of the "
            "action-conditioned second-order selector inside the persistent "
            "organism. This is a computational persistence result, not a "
            "demonstration of phenomenal consciousness."
        ),
        "analysis_note": (
            "The experiment seeds both model layers into SQLite, runs autonomous "
            "organism cycles, closes the database, reconstructs the organism, "
            "reloads both persisted models, and continues with no external input."
        ),
    }

    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
