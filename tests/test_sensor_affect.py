from skill_conscious.sensor_affect import appraise_sensory_field, causal_localization_index, modality_causal_attribution, score_action_with_affect


def test_neutral_sensory_state_has_zero_operational_affect():
    snapshot = appraise_sensory_field(
        {"vision": 1.0, "audio": 0.0}, {"vision": 1.0, "audio": 0.0},
        affective_weights={"vision": 1.0, "audio": 1.0},
        self_relevance_weights={"vision": 1.0, "audio": 1.0},
    )
    assert snapshot.prediction_error == 0.0
    assert snapshot.valence == 0.0
    assert snapshot.arousal == 0.0
    assert snapshot.coherence == 1.0


def test_single_modality_perturbation_is_causally_localized():
    snapshot = appraise_sensory_field(
        {"vision": 1.0, "audio": 0.0, "touch": 0.0},
        {"vision": 0.0, "audio": 0.0, "touch": 0.0},
        scales={"vision": 1.0, "audio": 1.0, "touch": 1.0},
        affective_weights={"vision": 1.0, "audio": 1.0, "touch": 1.0},
        self_relevance_weights={"vision": 1.0, "audio": 1.0, "touch": 1.0},
    )
    attribution = modality_causal_attribution(snapshot)
    assert attribution["vision"] == 1.0
    assert causal_localization_index(snapshot) == 1.0
    assert abs(snapshot.self_relevance - 1.0 / 3.0) < 1e-6


def test_opposing_modalities_reduce_cross_modal_coherence():
    aligned = appraise_sensory_field({"vision": 1.0, "audio": 1.0}, {"vision": 0.0, "audio": 0.0})
    opposed = appraise_sensory_field({"vision": 1.0, "audio": -1.0}, {"vision": 0.0, "audio": 0.0})
    assert aligned.coherence > opposed.coherence


def test_affective_appraisal_changes_action_score():
    pleasant_score, pleasant = score_action_with_affect(
        0.5, {"vision": 1.0}, {"vision": 0.0},
        affective_weights={"vision": 1.0}, affect_weight=1.0,
    )
    unpleasant_score, unpleasant = score_action_with_affect(
        0.5, {"vision": -1.0}, {"vision": 0.0},
        affective_weights={"vision": 1.0}, affect_weight=1.0,
    )
    assert pleasant.valence > unpleasant.valence
    assert pleasant_score > unpleasant_score


def test_appraisal_is_deterministic():
    args = dict(
        observation={"vision": 0.8, "audio": -0.2},
        expected={"vision": 0.1, "audio": 0.0},
        scales={"vision": 1.0, "audio": 1.0},
        affective_weights={"vision": 1.0, "audio": -0.5},
        self_relevance_weights={"vision": 2.0, "audio": 1.0},
    )
    assert appraise_sensory_field(**args) == appraise_sensory_field(**args)
