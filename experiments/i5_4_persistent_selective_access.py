from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import numpy as np

from src.ontto.bridge import DynamicStateBridge
from src.ontto.dynamics import Config as DynamicsConfig
from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.provider import LLMResponse
from src.ontto.storage import MemoryStore

CANDIDATE_SIGNALS = (-1.0, 1.0)


class FakeProvider:
    def chat(self, messages, temperature=0.7):
        return LLMResponse(
            text="Calibration response.\nMEMORY: retain dynamic continuity.\nSELF_MODEL: internal state follows trajectory.",
            raw={"fake": True},
        )


def sign_flip(values: np.ndarray, seed: int, permutations: int = 20000) -> float:
    values = np.asarray(values, dtype=float)
    if values.size == 0:
        return 1.0
    observed = abs(float(values.mean()))
    rng = np.random.default_rng(seed)
    signs = rng.choice((-1.0, 1.0), size=(permutations, values.size))
    null = np.abs((signs * values[None, :]).mean(axis=1))
    return float((np.count_nonzero(null >= observed) + 1) / (permutations + 1))


def warmup(db_path: Path, seed: int, cycles: int) -> None:
    store = MemoryStore(db_path)
    cfg = OrganismConfig(
        agent_id="receiver",
        dynamic_seed=seed,
        dream_every_cycles=10000,
        event_limit=0,
        self_observer_enabled=True,
        self_selection_enabled=False,
        workspace_enabled=False,
        workspace_selective_access_enabled=False,
    )
    organism = PersistentOrganism(cfg, store, FakeProvider(), lambda _: None)
    for i in range(cycles):
        organism.wake_cycle(f"calibration {i}")
        organism.autonomous_wake_cycle()
    store.conn.close()


def oracle_for_state(state, seed: int, step_index: int) -> dict[str, object]:
    bridge = DynamicStateBridge(DynamicsConfig(), seed=seed)
    outcomes = {}
    for signal in CANDIDATE_SIGNALS:
        snap = bridge.advance(
            previous_state=state.dynamic_prev_state,
            state=state.dynamic_state,
            memory=state.dynamic_memory,
            pressure=state.dynamic_pressure,
            signal=signal,
            steps=1,
            step_index=step_index,
        )
        outcomes[signal] = {"state": float(snap.state), "distance": float(abs(snap.state - 0.0))}
    oracle_signal = min(CANDIDATE_SIGNALS, key=lambda s: (abs(outcomes[s]["state"] - 0.0), abs(s)))
    return {
        "oracle_signal": oracle_signal,
        "oracle_distance": abs(outcomes[oracle_signal]["state"] - 0.0),
    }


def run_arm(
    db_path: Path,
    *,
    seed: int,
    query_mode: str,
    attention_mode: str,
    access_weight: float,
) -> dict[str, object]:
    store = MemoryStore(db_path)
    cfg = OrganismConfig(
        agent_id="receiver",
        dynamic_seed=seed,
        dream_every_cycles=10000,
        event_limit=0,
        self_observer_enabled=True,
        self_selection_enabled=True,
        self_selection_policy="self_model",
        self_selection_signals=CANDIDATE_SIGNALS,
        workspace_enabled=False,
        workspace_selective_access_enabled=True,
        workspace_selective_access_query_mode=query_mode,
        workspace_selective_access_attention_mode=attention_mode,
        workspace_selective_access_weight=access_weight,
    )
    organism = PersistentOrganism(cfg, store, FakeProvider(), lambda _: None)
    before = store.load_state("receiver")
    oracle = oracle_for_state(before, seed, before.dynamic_steps)
    organism.autonomous_wake_cycle()
    after = store.load_state("receiver")
    event = store.recent_events("receiver", 1)[0]
    selection = event["payload"]["self_selection"]
    selective = selection["workspace_selective_access"]
    chosen = float(selection["chosen_signal"])
    regret = float(abs(after.dynamic_state) - oracle["oracle_distance"])
    persistence_before = {
        "query_module": after.workspace_last_query_module,
        "query_distance": after.workspace_last_query_distance,
        "attention_weights": list(after.workspace_last_attention_weights),
        "access_steps": after.workspace_selective_access_steps,
    }
    store.conn.close()

    restored = MemoryStore(db_path)
    restored_state = restored.load_state("receiver")
    persistence_after = {
        "query_module": restored_state.workspace_last_query_module,
        "query_distance": restored_state.workspace_last_query_distance,
        "attention_weights": list(restored_state.workspace_last_attention_weights),
        "access_steps": restored_state.workspace_selective_access_steps,
    }
    restored.conn.close()

    return {
        "chosen_signal": chosen,
        "oracle_signal": oracle["oracle_signal"],
        "regret": regret,
        "selective": selective,
        "persistence_equal": persistence_before == persistence_after,
    }


def run(seed: int, replicates: int, warmup_cycles: int, access_weight: float, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    controls = {
        "full": ("full", "full"),
        "shuffled_query": ("shuffled", "full"),
        "shuffled_attention": ("full", "shuffled"),
        "zero_query": ("zero", "full"),
        "random_query": ("random", "full"),
        "lesion_query": ("lesion", "full"),
    }
    rows = []
    for rep in range(replicates):
        rep_seed = seed + rep
        base = out / f"base_{rep}.db"
        warmup(base, rep_seed, warmup_cycles)
        for name, (query_mode, attention_mode) in controls.items():
            db = out / f"{name}_{rep}.db"
            shutil.copy2(base, db)
            row = run_arm(
                db,
                seed=rep_seed,
                query_mode=query_mode,
                attention_mode=attention_mode,
                access_weight=access_weight,
            )
            rows.append({"replicate": rep, "seed": rep_seed, "control": name, **row})
            db.unlink(missing_ok=True)
        base.unlink(missing_ok=True)

    by_name = {}
    for row in rows:
        by_name.setdefault(row["control"], []).append(row)
    full = {r["replicate"]: r for r in by_name["full"]}
    endpoints = {}
    for name in controls:
        if name == "full":
            continue
        values = np.asarray(
            [
                by_name[name][i]["regret"] - full[by_name[name][i]["replicate"]]["regret"]
                for i in range(replicates)
            ],
            dtype=float,
        )
        p = sign_flip(values, seed + len(endpoints) + 1)
        endpoints[f"{name}_regret_cost_mean"] = float(values.mean())
        endpoints[f"{name}_regret_cost_p"] = p
        endpoints[f"{name}_action_change_rate"] = float(
            np.mean(
                [
                    int(by_name[name][i]["chosen_signal"] != full[by_name[name][i]["replicate"]]["chosen_signal"])
                    for i in range(replicates)
                ]
            )
        )
    endpoints["full_persistence_rate"] = float(
        np.mean([r["persistence_equal"] for r in by_name["full"]])
    )
    endpoints["full_attention_mass_mean"] = float(
        np.mean([r["selective"]["attention_mass"] for r in by_name["full"]])
    )
    endpoints["full_access_strength_mean"] = float(
        np.mean([r["selective"]["access_strength"] for r in by_name["full"]])
    )

    summary = {
        "experiment": "i5_4_persistent_selective_access",
        "seed": seed,
        "replicates": replicates,
        "warmup_cycles": warmup_cycles,
        "candidate_signals": list(CANDIDATE_SIGNALS),
        "access_weight": access_weight,
        "controls": controls,
        "endpoints": endpoints,
        "boundary": "I5.4 integrates state-dependent query and attention allocation into PersistentOrganism. It tests computational selective access and causal action modulation, not consciousness.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "runs.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261004)
    ap.add_argument("--replicates", type=int, default=24)
    ap.add_argument("--warmup", type=int, default=24)
    ap.add_argument("--access-weight", type=float, default=0.35)
    ap.add_argument("--out", default="results/i5_4_persistent_selective_access")
    args = ap.parse_args()
    print(json.dumps(run(args.seed, args.replicates, args.warmup, args.access_weight, Path(args.out)), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
