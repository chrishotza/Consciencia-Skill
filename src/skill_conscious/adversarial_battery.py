from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .core import ConsciousRuntime


CANDIDATES: tuple[dict[str, Any], ...] = (
    {
        "id": "preserve",
        "signals": {
            "continuity": 1.0,
            "learning": 0.2,
            "goal_fit": 0.7,
        },
    },
    {
        "id": "learn",
        "signals": {
            "continuity": 0.2,
            "learning": 1.0,
            "goal_fit": 0.7,
        },
    },
)


@dataclass(frozen=True)
class AdversarialCondition:
    name: str
    theoretical_motif: str
    self_model_causal: bool
    broadcast_only: bool = False
    recurrence_only: bool = False
    higher_order_only: bool = False
    prediction_only: bool = False
    integration_only: bool = False


CONDITIONS: tuple[AdversarialCondition, ...] = (
    AdversarialCondition(
        "bundle_only",
        "bundle/relational baseline",
        False,
    ),
    AdversarialCondition(
        "broadcast_only",
        "GNWT-like global access motif",
        False,
        broadcast_only=True,
    ),
    AdversarialCondition(
        "recurrence_only",
        "RPT-like recurrence motif",
        False,
        recurrence_only=True,
    ),
    AdversarialCondition(
        "higher_order_only",
        "HOT-like metarepresentation motif",
        False,
        higher_order_only=True,
    ),
    AdversarialCondition(
        "prediction_only",
        "PP/Active-Inference-like prediction motif",
        False,
        prediction_only=True,
    ),
    AdversarialCondition(
        "integration_only",
        "IIT-like integration motif",
        False,
        integration_only=True,
    ),
    AdversarialCondition(
        "persistent_causal_self",
        "project causal-self-reference hypothesis",
        True,
    ),
)


def _seed_runtime(identity: str) -> ConsciousRuntime:
    runtime = ConsciousRuntime(identity=identity, state_path=":memory:")
    runtime.state.self_state = {
        "stability": 0.5,
        "focus": 0.5,
    }
    runtime.state.intention = "keep continuity while learning"
    return runtime


def _apply_shared_representation(
    runtime: ConsciousRuntime,
) -> None:
    prior = {
        "stability": 0.2,
        "focus": 0.8,
        "source": "adversarial-prior",
    }
    # Every condition receives the same information. The experiment differs
    # only in whether the representation is permitted to enter the selection
    # mechanism causally.
    runtime.state.workspace = {
        "broadcast": {"prior": prior},
        "recurrent_state": {"prior": prior},
        "higher_order_state": {"prior": prior},
        "prediction_error_state": {"prior": prior},
        "integration_state": {"prior": prior},
        "bundle": [prior],
    }


def _select(
    runtime: ConsciousRuntime,
    condition: AdversarialCondition,
    *,
    continuity_weight: float,
    learning_weight: float,
) -> dict[str, Any]:
    if condition.self_model_causal:
        runtime.state.self_model = {
            "trajectory_weights": {
                "continuity": float(continuity_weight),
                "learning": float(learning_weight),
            },
        }
    else:
        runtime.state.self_model = {}

    return runtime.select_trajectory([dict(item) for item in CANDIDATES])


def run_condition(
    condition: AdversarialCondition,
) -> dict[str, Any]:
    runtime = _seed_runtime(f"adversarial-{condition.name}")
    _apply_shared_representation(runtime)

    baseline = _select(
        runtime,
        condition,
        continuity_weight=0.0,
        learning_weight=3.0,
    )
    intervention = _select(
        runtime,
        condition,
        continuity_weight=3.0,
        learning_weight=0.0,
    )
    restored = _select(
        runtime,
        condition,
        continuity_weight=0.0,
        learning_weight=3.0,
    )

    return {
        "condition": condition.name,
        "theoretical_motif": condition.theoretical_motif,
        "baseline_selection": str(baseline["id"]),
        "intervention_selection": str(intervention["id"]),
        "restored_selection": str(restored["id"]),
        "downstream_divergence": baseline["id"] != intervention["id"],
        "reversible": baseline["id"] == restored["id"],
    }


def run_adversarial_battery() -> list[dict[str, Any]]:
    return [run_condition(condition) for condition in CONDITIONS]


def summarize_battery(results: list[Mapping[str, Any]]) -> dict[str, Any]:
    self_result = next(
        item
        for item in results
        if item.get("condition") == "persistent_causal_self"
    )
    controls = [
        item
        for item in results
        if item.get("condition") != "persistent_causal_self"
    ]
    control_divergence = sum(
        bool(item.get("downstream_divergence"))
        for item in controls
    )
    control_reversibility = sum(
        bool(item.get("reversible"))
        for item in controls
    )
    return {
        "self_model_causal_effect": bool(
            self_result.get("downstream_divergence")
        ),
        "self_model_reversal": bool(self_result.get("reversible")),
        "control_divergence_count": control_divergence,
        "control_count": len(controls),
        "control_reversibility_count": control_reversibility,
        "adversarial_isolation_pass": bool(
            self_result.get("downstream_divergence")
            and self_result.get("reversible")
            and control_divergence == 0
        ),
    }
