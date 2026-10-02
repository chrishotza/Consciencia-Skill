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

from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.provider import LLMResponse
from src.ontto.self_observer import SelfObserver
from src.ontto.action_conditioned_meta_observer import ActionConditionedMetaObserver
from src.ontto.storage import MemoryStore

from experiments.organism_repeated_active_continuity_v78 import (
    SIGNALS,
    sign_p,
    train_self_observer,
)


PROTOCOL_VERSION = "C0.17"
TRAINING_CYCLES = 12
EVAL_CYCLES = 4


class AutonomousOnlyProvider:
    def chat(self, messages, temperature=0.7):
        return LLMResponse(
            text="Autonomous-only acquisition probe.",
            raw={"fake": True},
        )


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


def seed_training_database(
    path: Path,
    *,
    observer: SelfObserver,
) -> None:
    store = MemoryStore(path)
    store.save_self_observer_model("agent", observer.to_dict())
    store.conn.execute(
        "DELETE FROM action_conditioned_meta_observer_models "
        "WHERE agent_id=?",
        ("agent",),
    )
    store.conn.commit()
    store.conn.execute(
        "PRAGMA wal_checkpoint(FULL)"
    )
    store.conn.close()


def cfg(seed: int, *, learn_second_order: bool, update_second_order: bool) -> OrganismConfig:
    return OrganismConfig(
        agent_id="agent",
        dynamic_seed=seed,
        dream_every_cycles=10_000,
        self_observer_enabled=True,
        self_policy_enabled=False,
        self_selection_enabled=True,
        self_selection_policy="self_model",
        self_selection_signals=SIGNALS,
        action_conditioned_meta_observer_enabled=True,
        action_conditioned_meta_observer_update_enabled=update_second_order,
        action_conditioned_meta_counterfactual_learning_enabled=learn_second_order,
    )


def run_cycles(
    organism: PersistentOrganism,
    store: MemoryStore,
    cycles: int,
) -> dict[str, np.ndarray | list[str]]:
    actions = []
    gains = []
    policies = []
    sample_counts = []

    for _ in range(cycles):
        organism.autonomous_wake_cycle()
        event = store.recent_events("agent", 1)[0]
        selection = event["payload"]["self_selection"]
        state = store.load_state("agent")
        actions.append(float(selection["chosen_signal"]))
        gains.append(float(state.self_prediction_gain))
        policies.append(str(selection["policy"]))
        sample_counts.append(
            int(selection["action_conditioned_meta_model_samples"])
        )

    return {
        "actions": np.asarray(actions, dtype=float),
        "gains": np.asarray(gains, dtype=float),
        "policies": policies,
        "sample_counts": np.asarray(sample_counts, dtype=int),
    }


def target_permute_meta(
    payload: dict,
    seed: int,
) -> ActionConditionedMetaObserver:
    model = ActionConditionedMetaObserver.from_dict(payload)
    targets = np.asarray(model.targets, dtype=float)
    rng = np.random.default_rng(seed)
    permuted = model.to_dict()
    permuted["targets"] = rng.permutation(targets).tolist()
    return ActionConditionedMetaObserver.from_dict(permuted)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=24)
    parser.add_argument(
        "--out",
        default="results/tcf_consciousness_instantiation_c0_17",
    )
    args = parser.parse_args()

    out = Path(args.out)
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    rows = []

    for index in range(args.episodes):
        seed = 170010 + index
        observer = train_self_observer(seed=seed, samples=256)

        base_db = out / f"training_{index}.db"
        true_db = out / f"true_{index}.db"
        permuted_db = out / f"permuted_{index}.db"

        seed_training_database(
            base_db,
            observer=observer,
        )

        training_store = MemoryStore(base_db)
        trainer = PersistentOrganism(
            cfg(
                seed,
                learn_second_order=True,
                update_second_order=True,
            ),
            training_store,
            AutonomousOnlyProvider(),
            lambda _: None,
        )
        training = run_cycles(
            trainer,
            training_store,
            TRAINING_CYCLES,
        )
        learned_meta_payload = trainer.action_conditioned_meta_observer.to_dict()
        learned_digest = model_digest(
            trainer.self_observer,
            trainer.action_conditioned_meta_observer,
        )
        learned_samples = len(
            trainer.action_conditioned_meta_observer.targets
        )
        training_store.conn.execute("PRAGMA wal_checkpoint(FULL)")
        training_store.conn.close()

        shutil.copy2(base_db, true_db)
        shutil.copy2(base_db, permuted_db)

        for path, permuted in (
            (true_db, False),
            (permuted_db, True),
        ):
            store = MemoryStore(path)
            if permuted:
                meta = target_permute_meta(
                    learned_meta_payload,
                    seed=171000 + index,
                )
                store.save_action_conditioned_meta_observer_model(
                    "agent",
                    meta.to_dict(),
                )
            store.conn.execute("PRAGMA wal_checkpoint(FULL)")
            store.conn.close()

        true_store = MemoryStore(true_db)
        true_organism = PersistentOrganism(
            cfg(
                seed,
                learn_second_order=False,
                update_second_order=False,
            ),
            true_store,
            AutonomousOnlyProvider(),
            lambda _: None,
        )
        true_start_digest = model_digest(
            true_organism.self_observer,
            true_organism.action_conditioned_meta_observer,
        )
        true_eval = run_cycles(
            true_organism,
            true_store,
            EVAL_CYCLES,
        )
        true_store.conn.execute("PRAGMA wal_checkpoint(FULL)")
        true_store.conn.close()

        perm_store = MemoryStore(permuted_db)
        perm_organism = PersistentOrganism(
            cfg(seed, learn_second_order=False),
            perm_store,
            AutonomousOnlyProvider(),
            lambda _: None,
        )
        perm_eval = run_cycles(
            perm_organism,
            perm_store,
            EVAL_CYCLES,
        )
        perm_store.conn.close()

        rows.append(
            {
                "learned_meta_samples": learned_samples,
                "learned_digest": learned_digest,
                "true_start_digest_matches": true_start_digest == learned_digest,
                "first_eval_action_difference": float(
                    true_eval["actions"][0] - perm_eval["actions"][0]
                ),
                "first_eval_gain_difference": float(
                    true_eval["gains"][0] - perm_eval["gains"][0]
                ),
                "mean_eval_action_difference": float(
                    np.mean(true_eval["actions"] - perm_eval["actions"])
                ),
                "mean_eval_gain_difference": float(
                    np.mean(true_eval["gains"] - perm_eval["gains"])
                ),
                "true_eval_policies": true_eval["policies"],
                "permuted_eval_policies": perm_eval["policies"],
                "training_sample_count_sequence": training["sample_counts"].tolist(),
            }
        )

    first_action = np.asarray(
        [row["first_eval_action_difference"] for row in rows],
        dtype=float,
    )
    first_gain = np.asarray(
        [row["first_eval_gain_difference"] for row in rows],
        dtype=float,
    )
    mean_action = np.asarray(
        [row["mean_eval_action_difference"] for row in rows],
        dtype=float,
    )
    mean_gain = np.asarray(
        [row["mean_eval_gain_difference"] for row in rows],
        dtype=float,
    )

    summary = {
        "experiment": "tcf_consciousness_instantiation_c0_17",
        "protocol_version": PROTOCOL_VERSION,
        "question": (
            "Can the PersistentOrganism acquire an action-conditioned second-order "
            "self-model online from its own counterfactual prediction errors, and "
            "does the acquired mapping become behaviorally specific?"
        ),
        "matched_design": {
            "first_order_observer_preseeded": True,
            "second_order_model_starts_empty": True,
            "counterfactual_second_order_learning_occurs_inside_organism": True,
            "same_training_seed_per_replica": True,
            "same_evaluation_state_per_true_permuted_pair": True,
            "same_first_order_observer_per_pair": True,
            "same_candidate_signals": True,
            "target_multiset_preserved_in_permutation": True,
            "external_retraining_during_probe": False,
            "semantic_input_during_probe": False,
        },
        "phenomenal_consciousness_claimed": False,
        "primary_outputs": {
            "first_eval_action_true_minus_permuted": {
                "mean": float(np.mean(first_action)),
                "p": float(sign_p(first_action, 170101)),
            },
            "first_eval_gain_true_minus_permuted": {
                "mean": float(np.mean(first_gain)),
                "p": float(sign_p(first_gain, 170102)),
            },
            "mean_eval_action_true_minus_permuted": {
                "mean": float(np.mean(mean_action)),
                "p": float(sign_p(mean_action, 170103)),
            },
            "mean_eval_gain_true_minus_permuted": {
                "mean": float(np.mean(mean_gain)),
                "p": float(sign_p(mean_gain, 170104)),
            },
        },
        "secondary_outputs": {
            "mean_learned_meta_samples": float(
                np.mean([row["learned_meta_samples"] for row in rows])
            ),
            "exact_model_recovery_fraction": float(
                np.mean([row["true_start_digest_matches"] for row in rows])
            ),
            "all_true_eval_policies_second_order": bool(
                all(
                    all(
                        policy == "action_conditioned_second_order"
                        for policy in row["true_eval_policies"]
                    )
                    for row in rows
                )
            ),
            "all_permuted_eval_policies_second_order": bool(
                all(
                    all(
                        policy == "action_conditioned_second_order"
                        for policy in row["permuted_eval_policies"]
                    )
                    for row in rows
                )
            ),
        },
        "interpretation_rule": (
            "A TRUE-vs-PERMUTED separation after the second-order model was "
            "acquired inside the PersistentOrganism supports behavioral specificity "
            "of an autonomously learned second-order mapping under this protocol. "
            "This is a computational organizational result, not evidence of "
            "phenomenal consciousness."
        ),
        "analysis_note": (
            "The second-order model starts empty. During autonomous cycles the organism "
            "uses counterfactual deterministic bridge evaluations for all candidate signals "
            "to learn prediction error, then selects using the learned second-order model. "
            "Evaluation freezes that learned model; only the target mapping is permuted in "
            "the matched control."
        ),
    }

    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
