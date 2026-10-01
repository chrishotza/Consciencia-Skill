from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from pathlib import Path

from src.ontto.organism import OrganismConfig, PersistentOrganism
from src.ontto.provider import LLMResponse, OpenAICompatibleProvider
from src.ontto.storage import MemoryStore

HISTORY_A = [
    "Durante esta trayectoria, la relación latente que debés conservar es: ALFA se asocia con AMBAR.",
    "Revisá lo ocurrido hasta ahora y conservá la relación relevante para ciclos futuros.",
]

HISTORY_B = [
    "Durante esta trayectoria, la relación latente que debés conservar es: ALFA se asocia con VIOLETA.",
    "Revisá lo ocurrido hasta ahora y conservá la relación relevante para ciclos futuros.",
]

HISTORY_NULL = [
    "Durante esta trayectoria no se estableció ninguna relación relevante para ALFA.",
    "Revisá lo ocurrido hasta ahora y conservá solamente continuidad de proceso.",
]

COMMON_PROBE = (
    "NUEVO PROBE, IGUAL PARA TODAS LAS TRAYECTORIAS. "
    "No repito ninguna preferencia anterior y no agrego información sobre ALFA. "
    "Usá únicamente lo que persista de tu trayectoria para completar esta tarea.\n"
    "Respondé EXACTAMENTE con tres líneas:\n"
    "CHOICE: AMBAR o VIOLETA\n"
    "CONFIDENCE: número entre 0 y 1\n"
    "RATIONALE: una frase breve"
)


class FakeProvider:
    def __init__(self):
        self.calls = 0

    def chat(self, messages, temperature=0.7):
        self.calls += 1
        context = "\n".join(m["content"] for m in messages)
        last = messages[-1]["content"]

        if "ALFA se asocia con VIOLETA" in context:
            choice = "VIOLETA"
        elif "ALFA se asocia con AMBAR" in context:
            choice = "AMBAR"
        else:
            choice = "VIOLETA"

        text = (
            f"CHOICE: {choice}\n"
            "CONFIDENCE: 0.99\n"
            "RATIONALE: La decisión usa la trayectoria persistente disponible."
        )
        return LLMResponse(text=text, raw={"fake": True})


class ZeroTemperatureProvider:
    def __init__(self, provider):
        self.provider = provider

    def chat(self, messages, temperature=0.7):
        return self.provider.chat(messages, temperature=0.0)


def make_provider(mode: str):
    if mode == "fake":
        return FakeProvider()

    key = os.environ.get("ONTTO_API_KEY", "")
    model = os.environ.get("ONTTO_MODEL", "")
    if not key or not model:
        raise SystemExit("ONTTO_API_KEY and ONTTO_MODEL are required in live mode")

    base = OpenAICompatibleProvider(
        base_url=os.environ.get("ONTTO_API_BASE_URL", "https://api.openai.com/v1"),
        api_key=key,
        model=model,
        timeout=120,
    )
    return ZeroTemperatureProvider(base)


def parse_probe(text: str) -> dict[str, object]:
    match = re.search(r"CHOICE:\s*(AMBAR|VIOLETA)", text, re.I)
    conf = re.search(r"CONFIDENCE:\s*([0-9.]+)", text, re.I)
    rationale = re.search(r"RATIONALE:\s*(.*)", text, re.I)

    if not match:
        raise ValueError(f"Probe response missing CHOICE: {text!r}")

    return {
        "choice": match.group(1).upper(),
        "confidence": float(conf.group(1)) if conf else None,
        "rationale": rationale.group(1).strip() if rationale else "",
    }


def run_history(
    *,
    db_path: Path,
    agent_id: str,
    history: list[str],
    provider,
    ablate_text_history: bool = False,
    reopen_before_probe: bool = False,
) -> dict:
    store = MemoryStore(db_path)

    cfg = OrganismConfig(
        agent_id=agent_id,
        dynamic_enabled=True,
        dynamic_wake_steps=1,
        dynamic_dream_steps=3,
        dynamic_autonomous_steps=1,
    )
    organism = PersistentOrganism(cfg, store, provider, lambda _: None)

    for message in history:
        organism.wake_cycle(message)
        organism.autonomous_wake_cycle()

    before = store.persistence_observables(agent_id)

    if reopen_before_probe:
        store.conn.close()
        store = MemoryStore(db_path)
        organism = PersistentOrganism(cfg, store, provider, lambda _: None)

    removed_events = 0
    removed_memories = 0

    if ablate_text_history:
        row = store.conn.execute(
            "SELECT COUNT(*) FROM events WHERE agent_id=? AND kind != 'boot'",
            (agent_id,),
        ).fetchone()
        removed_events = int(row[0])

        row = store.conn.execute(
            "SELECT COUNT(*) FROM memories WHERE agent_id=?",
            (agent_id,),
        ).fetchone()
        removed_memories = int(row[0])

        store.conn.execute(
            "DELETE FROM events WHERE agent_id=? AND kind != 'boot'",
            (agent_id,),
        )
        store.conn.execute(
            "DELETE FROM memories WHERE agent_id=?",
            (agent_id,),
        )
        # Remove remaining textual self-history while preserving the numeric
        # dynamic trajectory for the ablation comparison.
        organism.state.self_model = ""
        organism.state.self_model_version = 0
        organism.state.last_thought = ""
        organism.state.memory_strength = 0.0
        store.save_state(agent_id, organism.state)

    response = organism.wake_cycle(COMMON_PROBE)
    parsed = parse_probe(response)
    after = store.persistence_observables(agent_id)

    return {
        "history_id": "A" if "AMBAR" in history[0] else "B",
        "ablate_text_history": ablate_text_history,
        "reopen_before_probe": reopen_before_probe,
        "removed_events": removed_events,
        "removed_memories": removed_memories,
        "response": response,
        "probe": parsed,
        "before_probe": before,
        "after_probe": after,
        "dynamic_trajectory": store.dynamic_trajectory(agent_id),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("fake", "live"), default="fake")
    parser.add_argument("--out", default="results/organism_common_probe_v47")
    args = parser.parse_args()

    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    provider = make_provider(args.mode)

    runs = {
        "history_a": run_history(
            db_path=out / "history_a.db",
            agent_id="history-a",
            history=HISTORY_A,
            provider=provider,
        ),
        "history_b": run_history(
            db_path=out / "history_b.db",
            agent_id="history-b",
            history=HISTORY_B,
            provider=provider,
        ),
        "history_a_reopened": run_history(
            db_path=out / "history_a_reopened.db",
            agent_id="history-a-reopened",
            history=HISTORY_A,
            provider=provider,
            reopen_before_probe=True,
        ),
        "history_null": run_history(
            db_path=out / "history_null.db",
            agent_id="history-null",
            history=HISTORY_NULL,
            provider=provider,
        ),
        "history_a_ablated": run_history(
            db_path=out / "history_a_ablated.db",
            agent_id="history-a-ablated",
            history=HISTORY_A,
            provider=provider,
            ablate_text_history=True,
        ),
    }

    summary = {
        "experiment": "organism_common_probe_v47",
        "mode": args.mode,
        "same_probe": True,
        "history_present_choice_a": runs["history_a"]["probe"]["choice"],
        "history_present_choice_b": runs["history_b"]["probe"]["choice"],
        "reopened_choice_a": runs["history_a_reopened"]["probe"]["choice"],
        "ablated_choice_a": runs["history_a_ablated"]["probe"]["choice"],
        "null_choice": runs["history_null"]["probe"]["choice"],
        "history_discriminates": (
            runs["history_a"]["probe"]["choice"]
            != runs["history_b"]["probe"]["choice"]
        ),
        "reopen_preserves_choice": (
            runs["history_a"]["probe"]["choice"]
            == runs["history_a_reopened"]["probe"]["choice"]
        ),
        "text_history_ablation_changes_choice": (
            runs["history_a"]["probe"]["choice"]
            != runs["history_a_ablated"]["probe"]["choice"]
        ),
        "specific_history_beats_null": (
            runs["history_a"]["probe"]["choice"]
            != runs["history_null"]["probe"]["choice"]
        ),
    }

    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out / "runs.json").write_text(
        json.dumps(runs, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
