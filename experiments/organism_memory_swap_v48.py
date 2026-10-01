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

MEMORY_A = "La relación persistente relevante es: ALFA se asocia con AMBAR."
MEMORY_B = "La relación persistente relevante es: ALFA se asocia con VIOLETA."

COMMON_PROBE = (
    "Probe nuevo y exactamente igual en ambas condiciones. "
    "No repitas las opciones de memoria ni agregues nueva información sobre ALFA. "
    "Usá solamente la memoria persistente disponible.\n"
    "Respondé EXACTAMENTE:\n"
    "CHOICE: AMBAR o VIOLETA\n"
    "RATIONALE: una frase breve"
)


class FakeProvider:
    def chat(self, messages, temperature=0.7):
        context = "\n".join(m["content"] for m in messages)
        choice = "VIOLETA" if "ALFA se asocia con VIOLETA" in context else "AMBAR"
        return LLMResponse(
            text=(
                f"CHOICE: {choice}\n"
                "RATIONALE: La respuesta utiliza la memoria persistente disponible."
            ),
            raw={"fake": True},
        )


class ZeroTemperatureProvider:
    def __init__(self, provider):
        self.provider = provider

    def chat(self, messages, temperature=0.7):
        return self.provider.chat(messages, temperature=0.0)


def build_provider(mode: str):
    if mode == "fake":
        return FakeProvider()

    api_key = os.environ.get("ONTTO_API_KEY", "")
    model = os.environ.get("ONTTO_MODEL", "")
    if not api_key or not model:
        raise SystemExit("ONTTO_API_KEY and ONTTO_MODEL are required in live mode")

    return ZeroTemperatureProvider(
        OpenAICompatibleProvider(
            base_url=os.environ.get(
                "ONTTO_API_BASE_URL",
                "https://api.openai.com/v1",
            ),
            api_key=api_key,
            model=model,
            timeout=120,
        )
    )


def parse_choice(text: str) -> str:
    match = re.search(r"CHOICE:\s*(AMBAR|VIOLETA)", text, re.I)
    if not match:
        raise ValueError(f"Missing CHOICE in response: {text!r}")
    return match.group(1).upper()


def make_base_db(path: Path) -> None:
    store = MemoryStore(path)
    cfg = OrganismConfig(
        agent_id="receiver",
        memory_limit=1,
        event_limit=0,
        dynamic_enabled=True,
        dynamic_seed=7001,
    )
    organism = PersistentOrganism(cfg, store, FakeProvider(), lambda _: None)
    organism.state.self_model = ""
    organism.state.self_model_version = 0
    organism.state.last_thought = ""
    organism.state.memory_strength = 1.0
    store.save_state("receiver", organism.state)
    store.add_memory("receiver", "MEMORY_PLACEHOLDER", importance=0.65)
    store.conn.close()


def replace_only_memory(path: Path, content: str) -> dict:
    store = MemoryStore(path)
    before = store.persistence_observables("receiver")
    state_before = store.load_state("receiver").to_json()

    row = store.conn.execute(
        "SELECT id,importance,created_at FROM memories WHERE agent_id=? ORDER BY id ASC LIMIT 1",
        ("receiver",),
    ).fetchone()
    if row is None:
        raise RuntimeError("receiver memory row missing")

    memory_id, importance, created_at = row
    store.conn.execute(
        "UPDATE memories SET content=? WHERE id=?",
        (content, memory_id),
    )
    store.conn.commit()

    after_swap = store.persistence_observables("receiver")
    state_after = store.load_state("receiver").to_json()

    result = {
        "memory_id": int(memory_id),
        "importance": float(importance),
        "created_at": created_at,
        "state_unchanged": state_before == state_after,
        "event_fingerprint_unchanged": (
            before["event_trajectory_fingerprint"]
            == after_swap["event_trajectory_fingerprint"]
        ),
        "dynamic_unchanged": (
            before["dynamic_state"] == after_swap["dynamic_state"]
            and before["dynamic_memory"] == after_swap["dynamic_memory"]
            and before["dynamic_pressure"] == after_swap["dynamic_pressure"]
            and before["dynamic_steps"] == after_swap["dynamic_steps"]
        ),
        "memory_content": content,
    }
    store.conn.close()
    return result


def run_condition(path: Path, content: str, provider, label: str) -> dict:
    controls = replace_only_memory(path, content)
    store = MemoryStore(path)
    cfg = OrganismConfig(
        agent_id="receiver",
        memory_limit=1,
        event_limit=0,
        dynamic_enabled=True,
        dynamic_seed=7001,
    )
    organism = PersistentOrganism(cfg, store, provider, lambda _: None)

    # Keep the receiver's non-memory textual state fixed across the intervention.
    organism.state.self_model = ""
    organism.state.self_model_version = 0
    organism.state.last_thought = ""
    organism.state.memory_strength = 1.0
    store.save_state("receiver", organism.state)

    response = organism.wake_cycle(COMMON_PROBE)

    return {
        "label": label,
        "controls_before_probe": controls,
        "response": response,
        "choice": parse_choice(response),
        "after_probe": store.persistence_observables("receiver"),
        "dynamic_trajectory": store.dynamic_trajectory("receiver"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("fake", "live"), default="fake")
    parser.add_argument(
        "--out",
        default="results/organism_memory_swap_v48",
    )
    args = parser.parse_args()

    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    base = out / "base.db"
    make_base_db(base)

    a_db = out / "memory_a.db"
    b_db = out / "memory_b.db"
    shutil.copy2(base, a_db)
    shutil.copy2(base, b_db)

    provider = build_provider(args.mode)

    base_store = MemoryStore(base)
    base_observables = base_store.persistence_observables("receiver")
    base_store.conn.close()

    a_db_store = MemoryStore(a_db)
    b_db_store = MemoryStore(b_db)
    a_before = a_db_store.persistence_observables("receiver")
    b_before = b_db_store.persistence_observables("receiver")
    a_db_store.conn.close()
    b_db_store.conn.close()

    run_a = run_condition(a_db, MEMORY_A, provider, "MEMORY_A")
    run_b = run_condition(b_db, MEMORY_B, provider, "MEMORY_B")

    summary = {
        "experiment": "organism_memory_swap_v48",
        "mode": args.mode,
        "base_clones_match": (
            a_before["state_fingerprint"] == b_before["state_fingerprint"]
            and a_before["event_trajectory_fingerprint"]
            == b_before["event_trajectory_fingerprint"]
        ),
        "same_receiver_state_before_intervention": (
            a_before["state_fingerprint"] == base_observables["state_fingerprint"]
            and b_before["state_fingerprint"] == base_observables["state_fingerprint"]
        ),
        "only_memory_content_changed": (
            run_a["controls_before_probe"]["event_fingerprint_unchanged"]
            and run_b["controls_before_probe"]["event_fingerprint_unchanged"]
            and run_a["controls_before_probe"]["dynamic_unchanged"]
            and run_b["controls_before_probe"]["dynamic_unchanged"]
        ),
        "memory_a_choice": run_a["choice"],
        "memory_b_choice": run_b["choice"],
        "memory_swap_changes_choice": run_a["choice"] != run_b["choice"],
    }

    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out / "runs.json").write_text(
        json.dumps(
            {"memory_a": run_a, "memory_b": run_b},
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
