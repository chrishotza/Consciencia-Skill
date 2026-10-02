import numpy as np
import pytest
from src.ontto.global_workspace import GlobalWorkspace, WorkspaceConfig

def test_capacity_and_deterministic_selection():
    ws = GlobalWorkspace(6, 2, WorkspaceConfig(capacity=2))
    x = np.asarray([[3,0],[0,1],[2,0],[0,0],[1,0],[0.5,0]], dtype=float)
    out, sel = ws.step(x, np.ones(6))
    assert len(sel.indices) == 2 and sel.indices == (0,2) and out.shape == x.shape

def test_broadcast_changes_non_selected_modules():
    ws = GlobalWorkspace(4,2,WorkspaceConfig(capacity=1))
    x = np.asarray([[1,0],[0,2],[0,0],[0,0]], dtype=float)
    out, sel = ws.step(x, np.ones(4))
    assert sel.indices == (1,) and not np.array_equal(out[0], x[0])

def test_broadcast_off_is_local_only():
    ws = GlobalWorkspace(4,2,WorkspaceConfig(capacity=1))
    x = np.random.default_rng(9).normal(size=(4,2))
    out, _ = ws.step(x, np.ones(4), broadcast_enabled=False)
    assert np.array_equal(out, x)

def test_selected_lesion_changes_global_content():
    ws = GlobalWorkspace(4,2,WorkspaceConfig(capacity=2))
    x = np.asarray([[4,0],[3,0],[0.1,0.1],[0.1,0.1]], dtype=float)
    rel = np.ones(4)
    _, sel = ws.step(x, rel)
    selected, _ = ws.step(x, rel, selected_lesion=sel.indices[0])
    unselected, _ = ws.step(x, rel, selected_lesion=3)
    assert not np.array_equal(selected, unselected)

def test_invalid_capacity_rejected():
    with pytest.raises(ValueError): GlobalWorkspace(3,2,WorkspaceConfig(capacity=4))