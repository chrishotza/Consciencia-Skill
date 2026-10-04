from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

from skill_conscious import ConsciousRuntime


def _candidate_set() -> list[dict[str, Any]]:
    return [
        {
            "id": "exploit",
            "signals": {"goal_fit": 1.0},
            "epistemic_value": 0.0,
        },
        {
            "id": "explore",
            "signals": {},
            "epistemic_value": 1.0,
        },
    ]


def run_longitudinal_uncertainty_probe(
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
            "metacognitive-uncertainty-longitudinal",
            state_path=path,
            metacognitive_uncertainty_weight=2.0,
        )
        runtime.state.self_model["metacognitive_prediction_expected_accuracy"] = 0.9
        runtime.state.self_model["metacognitive_uncertainty"] = 0.1
        runtime.store.save(runtime.state)
        baseline = runtime.snapshot_metacognitive_prediction()

        selections: list[str] = []
        uncertainties: list[float] = []
        contributions: list[float] = []
        restart_checks: list[bool] = []

        for cycle in range(cycles):
            if cycle == intervention_cycle:
                runtime.intervene_metacognitive_prediction_expected_accuracy(
                    0.1,
                    persist=True,
                    intervention_id="longitudinal-uncertainty-intervention",
                )

            if cycle == restoration_cycle:
                runtime.restore_metacognitive_prediction(
                    baseline,
                    persist=True,
                    intervention_id="longitudinal-uncertainty-restoration",
                )

            if cycle == restart_cycle:
                restarted = ConsciousRuntime(
                    "metacognitive-uncertainty-longitudinal",
                    state_path=path,
                    metacognitive_uncertainty_weight=2.0,
                )
                restart_checks.append(
                    restarted.metacognitive_uncertainty()
                    == runtime.metacognitive_uncertainty()
                )
                runtime = restarted

            selected = runtime.select_trajectory(_candidate_set())
            runtime.state.selected_trajectory = selected

            diagnostics = selected["metacognition"]["metacognitive_uncertainty"]
            selections.append(str(selected["id"]))
            uncertainties.append(float(diagnostics["uncertainty"]))
            contributions.append(float(diagnostics["contribution"]))

            # Persist the causal state between cycles just as the host runtime does.
            runtime.store.save(runtime.state)

        return {
            "protocol": "metacognitive-uncertainty-longitudinal-v1",
            "cycles": cycles,
            "intervention_cycle": intervention_cycle,
            "restoration_cycle": restoration_cycle,
            "selections": selections,
            "uncertainties": uncertainties,
            "epistemic_contributions": contributions,
            "restart_checks": restart_checks,
            "intervention_persisted": uncertainties[restart_cycle] == 0.9,
            "selection_shifted": (
                selections[0] == "exploit"
                and selections[intervention_cycle] == "explore"
            ),
            "selection_restored": all(
                value == "exploit" for value in selections[restoration_cycle:]
            ),
        }


def main() -> None:
    report = run_longitudinal_uncertainty_probe()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    assert report["intervention_persisted"]
    assert report["selection_shifted"]
    assert report["selection_restored"]
    assert all(report["restart_checks"])
    print("METACOGNITIVE_UNCERTAINTY_LONGITUDINAL_PASS")


if __name__ == "__main__":
    main()
