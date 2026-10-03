from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

from skill_conscious import ConsciousRuntime


def _candidates() -> list[dict[str, Any]]:
    return [
        {
            "id": "high-confidence",
            "signals": {"goal_fit": 0.5},
            "predicted_outcome": {"result": "A"},
            "predicted_outcome_confidence": 0.9,
        },
        {
            "id": "low-confidence",
            "signals": {"goal_fit": 0.5},
            "predicted_outcome": {"result": "B"},
            "predicted_outcome_confidence": 0.1,
        },
    ]


def run_longitudinal_confidence_probe(
    *,
    cycles: int = 12,
    restart_every: int = 6,
) -> dict[str, Any]:
    if cycles < 9:
        raise ValueError("cycles must be >= 9")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "runtime.json"
        runtime = ConsciousRuntime(
            "metacognitive-confidence-longitudinal",
            state_path=path,
            metacognitive_prediction_weight=2.0,
        )
        runtime.state.self_model["metacognitive_prediction_expected_accuracy"] = 0.9
        runtime.store.save(runtime.state)
        baseline_snapshot = runtime.snapshot_metacognitive_prediction()

        selections: list[str] = []
        expected_accuracy: list[float] = []
        contributions: list[float] = []
        restart_checks: list[bool] = []

        for cycle in range(cycles):
            if cycle == 4:
                runtime.intervene_metacognitive_prediction_expected_accuracy(
                    0.1,
                    persist=True,
                    intervention_id="longitudinal-confidence-intervention",
                )

            if cycle == 8:
                runtime.restore_metacognitive_prediction(
                    baseline_snapshot,
                    persist=True,
                    intervention_id="longitudinal-confidence-restoration",
                )

            if cycle and restart_every and cycle % restart_every == 0:
                restarted = ConsciousRuntime(
                    "metacognitive-confidence-longitudinal",
                    state_path=path,
                    metacognitive_prediction_weight=2.0,
                )
                restart_checks.append(
                    restarted.snapshot_metacognitive_prediction()
                    == runtime.snapshot_metacognitive_prediction()
                )
                runtime = restarted

            candidates = _candidates()
            runtime.integrate(
                {
                    "response": f"confidence longitudinal cycle {cycle}",
                    "candidate_futures": candidates,
                }
            )
            selected = dict(runtime.state.selected_trajectory or {})
            selections.append(str(selected["id"]))
            expected = runtime.snapshot_metacognitive_prediction()["expected_accuracy"]
            expected_accuracy.append(float(expected))

            meta = dict(selected.get("metacognition", {}))
            diagnostics = dict(meta.get("metacognitive_prediction", {}))
            contributions.append(float(diagnostics.get("contribution", 0.0)))

        return {
            "protocol": "metacognitive-confidence-longitudinal-v1",
            "cycles": cycles,
            "intervention_cycle": 4,
            "restoration_cycle": 8,
            "selections": selections,
            "expected_accuracy": expected_accuracy,
            "confidence_contributions": contributions,
            "restart_checks": restart_checks,
            "intervention_persisted": expected_accuracy[6] == 0.1,
            "selection_flipped": (
                selections[0] == "high-confidence"
                and selections[4] == "low-confidence"
            ),
            "selection_restored": all(
                value == "high-confidence" for value in selections[8:]
            ),
            "final_state_hash": hashlib.sha256(
                json.dumps(
                    runtime.snapshot(),
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest(),
        }


def main() -> None:
    report = run_longitudinal_confidence_probe()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    assert report["intervention_persisted"]
    assert report["selection_flipped"]
    assert report["selection_restored"]
    assert all(report["restart_checks"])
    print("METACOGNITIVE_CONFIDENCE_LONGITUDINAL_PASS")


if __name__ == "__main__":
    main()
