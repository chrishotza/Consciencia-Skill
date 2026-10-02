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


def test_assemble_summary_freezes_replication_metadata():
    from experiments.i5_19_independent_bridge_replication import assemble_summary

    raw = {
        "seed": 20261019,
        "replicates": 24,
        "warmup_cycles": 24,
        "cycles": 15,
        "lags": [-3, -2, -1, 1, 2, 3],
    }
    analysis = {
        "source_seed": 20261019,
        "permutations": 20_000,
        "metrics": {"signed_auc_delta": {"global_bridge_effect": {"mean_across_lags": -1.0}}},
    }
    result = assemble_summary(raw, analysis, 20261019)

    assert result["experiment"] == "i5_19_independent_bridge_replication"
    assert result["source_i5_17_seed"] == 20261019
    assert result["source_i5_18_source_seed"] == 20261019
    assert result["replicates"] == 24
    assert result["warmup_cycles"] == 24
    assert result["cycles"] == 15
    assert result["permutations"] == 20_000
    assert result["new_trajectories_collected"] is True
