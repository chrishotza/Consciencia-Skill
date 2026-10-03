from __future__ import annotations

import json
import tempfile
from dataclasses import replace
from pathlib import Path

from skill_conscious import ConsciousRuntime, ExperienceFieldProfile, run_reversible_intervention


def profile(offset: float = 0.0) -> ExperienceFieldProfile:
    base = ExperienceFieldProfile(
        0.10, 0.90, 0.20, 0.50, 0.70, 0.80,
        0.10, 0.40, 0.20, 0.85, 0.25,
    )
    return replace(
        base,
        prediction_error=max(0.0, min(1.0, base.prediction_error + offset)),
        sensory_coherence=max(0.0, min(1.0, base.sensory_coherence - offset)),
        valence=max(-1.0, min(1.0, base.valence + offset)),
        self_relevance=max(0.0, min(1.0, base.self_relevance + offset)),
        dynamic_persistence=max(0.0, min(1.0, base.dynamic_persistence - offset)),
        dynamic_synchrony=max(0.0, min(1.0, base.dynamic_synchrony - offset)),
        dynamic_metastability=max(0.0, min(1.0, base.dynamic_metastability + abs(offset))),
        dynamic_complexity=max(0.0, min(1.0, base.dynamic_complexity + offset)),
        avalanche_activity=max(0.0, min(1.0, base.avalanche_activity + abs(offset))),
        field_coherence=max(0.0, min(1.0, base.field_coherence - abs(offset))),
        dynamic_repertoire=max(0.0, min(1.0, base.dynamic_repertoire + abs(offset))),
    )


def run() -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="skill-conscious-causal-") as directory:
        root = Path(directory)
        runtime = ConsciousRuntime(
            "causal-experiment",
            state_path=root / "runtime.json",
            dynamic_core_enabled=True,
            dynamic_core_state_path=root / "dynamic",
            dynamic_core_return_weight=0.50,
        )
        baseline = profile()
        for index, observed in enumerate((baseline, profile(0.01), profile(-0.01)), 1):
            runtime.observe_experience_field(
                observed,
                evidence_id=f"observation-{index}",
                persist=False,
            )
        runtime.record_experience_recovery(
            baseline,
            profile(0.35),
            profile(0.01),
            evidence_id="recovery-1",
            persist=False,
        )

        candidates = [
            {
                "id": "preserve",
                "signals": {"goal_fit": 0.49},
                "predicted_experience_field": profile(0.01).to_dict(),
            },
            {
                "id": "explore",
                "signals": {"goal_fit": 0.52},
                "predicted_experience_field": profile(0.35).to_dict(),
            },
        ]
        result = run_reversible_intervention(
            runtime,
            candidates,
            intervention_center=profile(0.35).to_dict(),
        )
        return result.to_dict()


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False, sort_keys=True))
