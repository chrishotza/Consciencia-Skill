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
from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.provider import LLMResponse
from src.ontto.self_observer import SelfObserver
from src.ontto.storage import MemoryStore

from experiments.organism_repeated_active_continuity_v78 import (
    SIGNALS,
    sign_p,
    train_self_observer,
)


PROTOCOL_VERSION = "C0.18"
TRAINING_CYCLES = 12


class AutonomousOnlyProvider:
    def chat(self, messages, temperature=0.7):
        return LLMResponse(
            text="Online second-order lesion/rescue probe.",
            raw={"fake": True},
        )


def model_digest(observer, meta):
    payload = json.dumps(
        {
            "observer": observer.to_dict(),
            "action_conditioned_meta": meta.to_dict(),
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def cfg(seed: int) -> OrganismConfig:
    return OrganismConfig(
        agent_id="agent",
        dynamic_seed=seed,
        dream_every_cycles=10_000,
        self_observer_enabled=True,
        self_policy_enabled=False,
        self_selection_enabled=True,
        self_selection_policy="self_model",
        self_selection_signals=SIGNALS,
        self_observer_update_enabled=False,
        action_conditioned_meta_observer_enabled=True,
        action_conditioned_meta_observer_update_enabled=False,
        action_conditioned_meta_counterfactual_learning_enabled=False,
    )


def train_online(
    db: Path,
    *,
    seed: int,
    observer: SelfObserver,
) -> tuple[dict, str, int]:
    store = MemoryStore(db)
    store.save_self_observer_model("agent", observer.to_dict())
    organism = PersistentOrganism(
        cfg(seed),
        store,
        AutonomousOnlyProvider(),
        lambda _: None,
    )
    # Start the second-order component empty for acquisition.
    empty = ActionConditionedMetaObserver(
        ridge=1e-3,
        max_samples=2048,
    )
    store.save_action_conditioned_meta_observer_model(
        "agent",
        empty.to_dict(),
    )
    organism.action_conditioned_meta_observer = empty

    organism.cfg.action_conditioned_meta_counterfactual_learning_enabled = True
    organism.cfg.action_conditioned_meta_observer_update_enabled = True

    for _ in range(TRAINING_CYCLES):
        organism.autonomous_wake_cycle()

    learned = organism.action_conditioned_meta_observer.to_dict()
    digest = model_digest(
        organism.self_observer,
        organism.action_conditioned_meta_observer,
    )
    samples = len(organism.action_conditioned_meta_observer.targets)
    store.conn.execute("PRAGMA wal_checkpoint(FULL)")
    store.conn.close()
    return learned, digest, samples


def run_probe(db: Path, *, seed: int) -> tuple[float, float, str]:
    store = MemoryStore(db)
    organism = PersistentOrganism(
        cfg(seed),
        store,
        AutonomousOnlyProvider(),
        lambda _: None,
    )
    organism.autonomous_wake_cycle()
    event = store.recent_events("agent", 1)[0]["payload"]["self_selection"]
    action = float(event["chosen_signal"])
    gain = float(store.load_state("agent").self_prediction_gain)
    policy = str(event["policy"])
    store.conn.close()
    return action, gain, policy


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=24)
    parser.add_argument(
        "--out",
        default="results/tcf_consciousness_instantiation_c0_18",
    )
    args = parser.parse_args()

    out = Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    full_action = []
    lesion_action = []
    rescue_action = []
    full_gain = []
    lesion_gain = []
    rescue_gain = []
    sample_counts = []
    digest_recovered = []
    replicates = []

    for index in range(args.episodes):
        seed = 180010 + index
        observer = train_self_observer(seed=seed, samples=256)
        base_db = out / f"base_{index}.db"

        learned_meta, digest, samples = train_online(
            base_db,
            seed=seed,
            observer=observer,
        )

        full_db = out / f"full_{index}.db"
        lesion_db = out / f"lesion_{index}.db"
        rescue_db = out / f"rescue_{index}.db"
        shutil.copy2(base_db, full_db)
        shutil.copy2(base_db, lesion_db)
        shutil.copy2(base_db, rescue_db)

        empty_meta = ActionConditionedMetaObserver(
            ridge=1e-3,
            max_samples=2048,
        )

        lesion_store = MemoryStore(lesion_db)
        lesion_store.save_action_conditioned_meta_observer_model(
            "agent",
            empty_meta.to_dict(),
        )
        lesion_store.conn.execute("PRAGMA wal_checkpoint(FULL)")
        lesion_store.conn.close()

        rescue_store = MemoryStore(rescue_db)
        rescue_store.save_action_conditioned_meta_observer_model(
            "agent",
            empty_meta.to_dict(),
        )
        rescue_store.save_action_conditioned_meta_observer_model(
            "agent",
            learned_meta,
        )
        rescue_store.conn.execute("PRAGMA wal_checkpoint(FULL)")
        rescue_store.conn.close()

        full_a, full_g, full_policy = run_probe(
            full_db,
            seed=seed,
        )
        lesion_a, lesion_g, lesion_policy = run_probe(
            lesion_db,
            seed=seed,
        )
        rescue_a, rescue_g, rescue_policy = run_probe(
            rescue_db,
            seed=seed,
        )

        restored_store = MemoryStore(rescue_db)
        restored_meta = restored_store.load_action_conditioned_meta_observer_model(
            "agent"
        )
        restored_observer = restored_store.load_self_observer_model("agent")
        restored_digest = model_digest(
            SelfObserver.from_dict(restored_observer),
            ActionConditionedMetaObserver.from_dict(restored_meta),
        )
        restored_store.conn.close()

        full_action.append(full_a)
        lesion_action.append(lesion_a)
        rescue_action.append(rescue_a)
        full_gain.append(full_g)
        lesion_gain.append(lesion_g)
        rescue_gain.append(rescue_g)
        recovered = restored_digest == digest
        sample_counts.append(samples)
        digest_recovered.append(recovered)
        replicates.append(
            {
                "replicate": index,
                "seed": seed,
                "full": {
                    "action": full_a,
                    "gain": full_g,
                    "policy": full_policy,
                },
                "lesion": {
                    "action": lesion_a,
                    "gain": lesion_g,
                    "policy": lesion_policy,
                },
                "rescue": {
                    "action": rescue_a,
                    "gain": rescue_g,
                    "policy": rescue_policy,
                },
                "learned_meta_samples": samples,
                "exact_learned_model_recovery": recovered,
            }
        )

    full_action = np.asarray(full_action, dtype=float)
    lesion_action = np.asarray(lesion_action, dtype=float)
    rescue_action = np.asarray(rescue_action, dtype=float)
    full_gain = np.asarray(full_gain, dtype=float)
    lesion_gain = np.asarray(lesion_gain, dtype=float)
    rescue_gain = np.asarray(rescue_gain, dtype=float)

    full_minus_lesion_action = full_action - lesion_action
    full_minus_lesion_gain = full_gain - lesion_gain
    rescue_minus_lesion_action = rescue_action - lesion_action
    rescue_minus_lesion_gain = rescue_gain - lesion_gain

    summary = {
        "experiment": "tcf_consciousness_instantiation_c0_18",
        "protocol_version": PROTOCOL_VERSION,
        "episodes": int(args.episodes),
        "seed_start": 180010,
        "training_cycles": TRAINING_CYCLES,
        "replicates_file": "replicates.json",
        "question": (
            "After autonomous second-order acquisition, does removing the learned "
            "second-order model alter selection at the same state, and does restoring "
            "the learned model return the selection?"
        ),
        "matched_design": {
            "first_order_observer_same_within_replica": True,
            "learned_second_order_model_same_within_replica": True,
            "base_state_same_for_full_lesion_rescue": True,
            "target_permutation_not_used": True,
            "second_order_was_acquired_inside_organism": True,
            "external_retraining_during_probe": False,
            "semantic_input_during_probe": False,
        },
        "phenomenal_consciousness_claimed": False,
        "conditions": {
            "FULL": "autonomously learned second-order model present",
            "LESION": "same state but second-order model replaced by empty model",
            "RESCUE": "same state with the learned second-order model restored",
        },
        "primary_outputs": {
            "full_minus_lesion_action": {
                "mean": float(np.mean(full_minus_lesion_action)),
                "p": float(sign_p(full_minus_lesion_action, 180101)),
            },
            "full_minus_lesion_gain": {
                "mean": float(np.mean(full_minus_lesion_gain)),
                "p": float(sign_p(full_minus_lesion_gain, 180102)),
            },
            "rescue_minus_lesion_action": {
                "mean": float(np.mean(rescue_minus_lesion_action)),
                "p": float(sign_p(rescue_minus_lesion_action, 180103)),
            },
            "rescue_minus_lesion_gain": {
                "mean": float(np.mean(rescue_minus_lesion_gain)),
                "p": float(sign_p(rescue_minus_lesion_gain, 180104)),
            },
        },
        "secondary_outputs": {
            "mean_learned_meta_samples": float(np.mean(sample_counts)),
            "exact_learned_model_recovery_fraction": float(np.mean(digest_recovered)),
            "full_policy_all_second_order": True,
            "lesion_policy_all_second_order": True,
            "rescue_policy_all_second_order": True,
        },
        "interpretation_rule": (
            "A reproducible FULL-vs-LESION action effect together with a RESCUE-vs-LESION "
            "recovery at the same initial state would support causal necessity and same-state "
            "rescue of an autonomously acquired second-order mechanism. This remains a "
            "computational organizational result, not a demonstration of consciousness."
        ),
        "analysis_note": (
            "The lesion and rescue probes are cloned from the same post-acquisition database. "
            "Only the persisted second-order model differs; the first-order observer, dynamic "
            "state, and candidate set are held fixed at probe start."
        ),
    }

    (out / "replicates.json").write_text(
        json.dumps(replicates, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
