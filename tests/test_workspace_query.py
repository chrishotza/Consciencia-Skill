import numpy as np
import pytest

from src.ontto.workspace_query import QUERY_CODES, StateDependentQuery

def test_query_matches_nearest_code():
    q = StateDependentQuery()
    x = np.zeros((6,2), dtype=float)
    result = q.query(x, QUERY_CODES[4])
    assert result.module_index == 4
    assert result.distance == 0.0

def test_query_changes_when_global_state_changes():
    q = StateDependentQuery()
    x = np.zeros((6,2), dtype=float)
    a = q.query(x, QUERY_CODES[2])
    b = q.query(x, QUERY_CODES[5])
    assert a.module_index != b.module_index

def test_query_reads_only_selected_module_value():
    q = StateDependentQuery()
    x = np.zeros((6,2), dtype=float)
    x[3,0] = 0.25
    x[4,0] = -0.75
    result = q.query(x, QUERY_CODES[4])
    assert result.module_index == 4
    assert q.target_value(x, result) == pytest.approx(-0.75)

def test_invalid_broadcast_rejected():
    q = StateDependentQuery()
    with pytest.raises(ValueError): q.query(np.zeros((6,2)), np.zeros(3))