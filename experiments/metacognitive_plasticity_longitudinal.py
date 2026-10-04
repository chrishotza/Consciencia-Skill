from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

from skill_conscious import ConsciousRuntime


def _configure(runtime: ConsciousRuntime) -> None:
    runtime.state.self_model.update(
        {
            "trajectory_priority_adaptation": {
                "enabled": True,
                "min_samples": 1,
                "utility_threshold": 0.0,
                "learning_rate": 0.5,
                "max_step": 1.0,
                "cooldown": 0,
                "confidence_threshold": 0.0,
                "direction_consistency": 0.0,
                "bounds": {"continuity": [-6.0, 6.0]},
            },
            "trajectory_weights": {"continuity": 0.0},
        }
    )


def _candidate() -> dict[str, Any]:
    return {
        "id": "continuity-action",
        "signals": {"continuity": 1.0},
        "predicted_outcome": {"result": "expected"},
        "predicted_outcome_confidence": 0.9,
    }


def run_longitudinal_plasticity_probe(
    *,
    cycles: int = 9,
    restart_cycle: int = 4,
    intervention_cycle: int = 3,
    restoration_cycle: int = 6,
) -> dict[str, Any]:
    if cycles <= restoration_cycle:
        raise ValueError("cycles must extend beyond restoration_cycle")

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "runtime.json"
        runtime = ConsciousRuntime(
            "metacognitive-plasticity-longitudinal",
            state_path=path,
        )
        _configure(runtime)
        runtime.state.self_model["metacognitive_prediction_expected_accuracy"] = 0.9
        runtime.store.save(runtime.state)
        baseline_prediction = runtime.snapshot_metacognitive_prediction()

        expected: list[float] = []
        factors: list[float] = []
        deltas: list[float] = []
        restart_checks: list[bool] = []

        for cycle in range(cycles):
            if cycle == intervention_cycle:
                runtime.intervene_metacognitive_prediction_expected_accuracy(
                    0.1,
                    persist=True,
                    intervention_id="longitudinal-plasticity-intervention",
                )

            if cycle == restoration_cycle:
                runtime.restore_metacognitive_prediction(
                    baseline_prediction,
                    persist=True,
                    intervention_id="longitudinal-plasticity-restoration",
                )

            if cycle == restart_cycle:
                restarted = ConsciousRuntime(
                    "metacognitive-plasticity-longitudinal",
                    state_path=path,
                )
                restart_checks.append(
                    restarted.snapshot_metacognitive_prediction()
                    == runtime.snapshot_metacognitive_prediction()
                )
                runtime = restarted

            candidate = _candidate()
            runtime.state.selected_trajectory = candidate
            result = runtime.register_consequence(
                candidate["id"],
                {"result": "observed"},
                evaluation={
                    "credited_signal": "continuity",
                    "utility": 1.0,
                },
                persist=True,
            )
            update = result["priority_adaptation"]["update"]
            meta = update["metacognitive_plasticity"]

            expected.append(float(meta["expected_accuracy"]))
            factors.append(float(meta["factor"]))
            deltas.append(float(update["delta"]))

        return {
            "protocol": "metacognitive-plasticity-longitudinal-v1",
            "cycles": cycles,
            "intervention_cycle": intervention_cycle,
            "restoration_cycle": restoration_cycle,
            "expected_accuracy": expected,
            "plasticity_factors": factors,
            "deltas": deltas,
            "restart_checks": restart_checks,
            "intervention_persisted": expected[restart_cycle] == 0.1,
            "plasticity_suppressed": deltas[intervention_cycle] < deltas[0],
            "plasticity_restored": all(
                abs(value - deltas[0]) < 1e-9
                for value in deltas[restoration_cycle:]
            ),
        }


def main() -> None:
    report = run_longitudinal_plasticity_probe()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    assert report["intervention_persisted"]
    assert report["plasticity_suppressed"]
    assert report["plasticity_restored"]
    assert all(report["restart_checks"])
    print("METACOGNITIVE_PLASTICITY_LONGITUDINAL_PASS")


if __name__ == "__main__":
    main()
