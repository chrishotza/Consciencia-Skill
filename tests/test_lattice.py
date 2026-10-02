import numpy as np

from src.ontto.lattice import LatticeComputer, LatticeConfig


def test_lattice_roundtrip():
    lattice = LatticeComputer(LatticeConfig(size=8), seed=1)
    lattice.write(np.ones((8, 8)))
    restored = LatticeComputer.from_dict(lattice.to_dict())
    assert np.array_equal(restored.state, lattice.state)
    assert restored.step_count == lattice.step_count


def test_local_boolean_gate_xor():
    lattice = LatticeComputer(LatticeConfig(size=8), seed=2)
    a = np.array([0, 0, 1, 1, 0, 1, 0, 1])
    b = np.array([0, 1, 0, 1, 1, 1, 0, 0])
    lattice.encode_bits(a, row=0)
    lattice.encode_bits(b, row=1)
    lattice.local_boolean_gate(
        left_row=0, right_row=1, output_row=2, width=8, op="xor"
    )
    expected = np.logical_xor(a, b).astype(int)
    assert np.array_equal(lattice.decode_bits(row=2, width=8), expected)


def test_local_coupling_spreads_perturbation():
    full = LatticeComputer(LatticeConfig(size=12, coupling=0.30), seed=3)
    full.state[6, 6] = 1.0
    full_spread = full.perturbation_spread(
        row=6, col=6, steps=5
    )["affected_fraction"]

    decoupled = LatticeComputer(LatticeConfig(size=12, coupling=0.0), seed=3)
    decoupled.state[6, 6] = 1.0
    decoupled_spread = decoupled.perturbation_spread(
        row=6, col=6, steps=5
    )["affected_fraction"]

    assert full_spread > decoupled_spread


def test_lesion_changes_field():
    lattice = LatticeComputer(LatticeConfig(size=10), seed=4)
    lattice.write(np.ones((10, 10)))
    before = lattice.state.copy()

    mask = np.zeros_like(lattice.state, dtype=bool)
    mask[4:6, 4:6] = True
    lattice.lesion(mask)

    assert not np.array_equal(before, lattice.state)
    assert np.all(lattice.state[4:6, 4:6] == 0.0)
