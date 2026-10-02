import json
import sys
from pathlib import Path

from experiments.i5_2_state_dependent_query import main

def test_query_experiment_contract(tmp_path: Path, monkeypatch):
    out = tmp_path / 'i5_2'
    monkeypatch.setattr(sys, 'argv', ['i5_2_state_dependent_query.py','--episodes','16','--out',str(out)])
    main()
    summary=json.loads((out/'summary.json').read_text(encoding='utf-8'))
    assert summary['episodes']==16
    assert 0.0 <= summary['endpoints']['full_query_accuracy'] <= 1.0
    assert 0.0 <= summary['endpoints']['state_dependent_query_change_rate'] <= 1.0
    assert summary['endpoints']['full_minus_shuffled_p'] >= 0.0