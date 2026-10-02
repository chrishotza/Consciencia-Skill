import numpy as np

from experiments.lattice_v1 import _pattern, _run_trace
from src.ontto.lattice import LatticeComputer, LatticeConfig

def test_temporal_trace_returns_requested_delays():
    pattern = _pattern(np.random.default_rng(10), 5)
    result = _run_trace(size=12, coupling=0.22, noise_std=0.0, pattern=pattern, seed=10, delays=[0,1,3,5], perturb_at=None, perturb_amplitude=0.5)
    assert set(result["scores"]) == {"0","1","3","5"}
    assert all(-1.0 <= v <= 1.0 for v in result["scores"].values())

def test_temporal_trace_is_deterministic_for_zero_noise():
    pattern = _pattern(np.random.default_rng(11), 5)
    kwargs = dict(size=12, coupling=0.22, noise_std=0.0, pattern=pattern, seed=11, delays=[0,2,4], perturb_at=2, perturb_amplitude=0.5)
    assert _run_trace(**kwargs) == _run_trace(**kwargs)

def test_perturbed_arm_preserves_initial_memory_readout():
    pattern = _pattern(np.random.default_rng(12), 5)
    clean = _run_trace(size=12, coupling=0.22, noise_std=0.0, pattern=pattern, seed=12, delays=[0,2,4], perturb_at=None, perturb_amplitude=0.5)
    pert = _run_trace(size=12, coupling=0.22, noise_std=0.0, pattern=pattern, seed=12, delays=[0,2,4], perturb_at=2, perturb_amplitude=0.5)
    assert clean["scores"]["0"] == pert["scores"]["0"]

def test_existing_lattice_roundtrip_still_works():
    lattice = LatticeComputer(LatticeConfig(size=8), seed=13)
    lattice.write(np.ones((8,8)))
    restored = LatticeComputer.from_dict(lattice.to_dict())
    assert np.array_equal(restored.state, lattice.state)
    assert restored.step_count == lattice.step_count