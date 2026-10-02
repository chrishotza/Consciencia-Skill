from experiments.i5_19_independent_bridge_replication import (
    CYCLES,
    INDEPENDENT_SEED,
    PERMUTATIONS,
    REPLICATES,
    SOURCE_SEED,
    WARMUP_CYCLES,
    validate_frozen_protocol,
)


def test_protocol_is_independent_and_frozen():
    assert INDEPENDENT_SEED != SOURCE_SEED
    assert REPLICATES == 24
    assert WARMUP_CYCLES == 24
    assert CYCLES == 15
    assert PERMUTATIONS == 20_000


def test_protocol_validator_rejects_source_seed():
    try:
        validate_frozen_protocol(
            seed=SOURCE_SEED,
            replicates=REPLICATES,
            warmup_cycles=WARMUP_CYCLES,
            cycles=CYCLES,
            permutations=PERMUTATIONS,
        )
    except ValueError as exc:
        assert "independent seed" in str(exc)
    else:
        raise AssertionError("source I5.17 seed must be rejected")


def test_protocol_validator_accepts_independent_frozen_configuration():
    validate_frozen_protocol(
        seed=INDEPENDENT_SEED,
        replicates=REPLICATES,
        warmup_cycles=WARMUP_CYCLES,
        cycles=CYCLES,
        permutations=PERMUTATIONS,
    )
