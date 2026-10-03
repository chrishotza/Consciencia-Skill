import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from experiments.coupled_ablation import run_ablation


def test_ablation_shows_causal_policy_shift():
    result = run_ablation()
    assert result["A_baseline"]["selected"] == "preserve"
    assert result["B_sensory_affect"]["selected"] == "explore"
    assert result["C_sensory_plus_dynamics"]["selected"] == "explore"


def test_ablation_reports_dynamic_field():
    result = run_ablation()
    assert result["C_sensory_plus_dynamics"]["dynamic_repertoire"] >= 0.0
    assert 0.0 <= result["C_sensory_plus_dynamics"]["field_coherence"] <= 1.0
