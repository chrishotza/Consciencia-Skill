from __future__ import annotations

import json
import tempfile
from pathlib import Path

from skill_conscious.core import ConsciousRuntime


CURRENT_STATE = {"stability": 0.5, "focus": 0.5}
CURRENT_INTENTION = "Maintain continuity while learning from new evidence."

CANDIDATES = [
    {
        "id": "preserve_continuity",
        "signals": {
            "goal_fit": 1.0,
            "self_alignment": 0.8,
            "continuity": 1.0,
            "learning": 0.2,
            "risk": 0.1,
        },
    },
    {
        "id": "learn",
        "signals": {
            "goal_fit": 0.8,
            "self_alignment": 0.6,
            "continuity": 0.7,
            "learning": 1.0,
            "risk": 0.2,
        },
    },
]

def same_present(runtime: ConsciousRuntime) -> None:
    runtime.state.self_state = dict(CURRENT_STATE)
    runtime.state.intention = CURRENT_INTENTION


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        persistent_path = root / "persistent.json"
        bundle_path = root / "bundle.json"

        # The two systems receive the same current state and intention.
        persistent = ConsciousRuntime(
            identity="hume-adversarial",
            state_path=persistent_path,
        )
        same_present(persistent)

        bundle = ConsciousRuntime(
            identity="hume-adversarial-bundle",
            state_path=bundle_path,
        )
        same_present(bundle)

        # Same prior information, represented differently.
        prior_perception = {
            "stability": 0.2,
            "focus": 0.8,
            "source": "prior_bundle",
        }
        bundle.state.workspace = {
            "perception_bundle": [prior_perception],
        }

        # Persistent-self condition: the prior evidence has entered a
        # durable self-model and therefore changes trajectory weights.
        persistent.state.self_model = {
            "trajectory_weights": {
                "continuity": 0.0,
                "learning": 3.0,
            },
            "last_bundle_evidence": prior_perception,
        }
        persistent.store.save(persistent.state)

        # Bundle-only condition: the same evidence remains available as a
        # perception record, but no persistent self-model preference is used.
        bundle.store.save(bundle.state)

        persistent_selected = persistent.select_trajectory(CANDIDATES)
        bundle_selected = bundle.select_trajectory(CANDIDATES)

        print("HUME_BUNDLE_AB")
        print(json.dumps({
            "same_present": True,
            "persistent_self_model": persistent.state.self_model,
            "bundle_perceptions": bundle.state.workspace["perception_bundle"],
            "persistent_selected": persistent_selected,
            "bundle_selected": bundle_selected,
        }, ensure_ascii=False))

        assert persistent_selected["id"] != bundle_selected["id"]

        # Reverse intervention: change only the persistent self-model.
        persistent.state.self_model["trajectory_weights"] = {
            "continuity": 3.0,
            "learning": 0.0,
        }
        persistent.store.save(persistent.state)
        reversed_selected = persistent.select_trajectory(CANDIDATES)
        assert reversed_selected["id"] != persistent_selected["id"]
        assert reversed_selected["id"] == "preserve_continuity"

        # The reversed intervention must survive a restart.
        restarted = ConsciousRuntime(
            identity="hume-adversarial",
            state_path=persistent_path,
        )
        assert restarted.state.self_model["trajectory_weights"] == {
            "continuity": 3.0,
            "learning": 0.0,
        }

        print("INTERVENTION_REVERSAL")
        print(json.dumps({
            "before": persistent_selected["id"],
            "after": reversed_selected["id"],
            "restart_selected_weight": restarted.state.self_model["trajectory_weights"],
        }, ensure_ascii=False))
        print("HUME_BUNDLE_AB_PASS")


if __name__ == "__main__":
    main()