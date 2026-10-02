from experiments.interoception_i1 import episode, make_dataset, TRAIN_MAGNITUDES, OOD_MAGNITUDES


def test_i1_episode_is_deterministic():
    a = episode(1201, 0.5)
    b = episode(1201, 0.5)
    assert a[0].tolist() == b[0].tolist()
    assert a[1] == b[1]


def test_i1_dataset_shapes_and_ood_protocol():
    x_train, y_train = make_dataset([1, 2, 3, 4, 5, 6], TRAIN_MAGNITUDES)
    x_ood, y_ood = make_dataset([11, 12, 13, 14, 15, 16], OOD_MAGNITUDES)
    assert x_train.shape == (6, 8)
    assert y_train.shape == (6,)
    assert x_ood.shape == (6, 8)
    assert y_ood.shape == (6,)
    assert all(0.0 < value <= 1.0 for value in y_train)
    assert all(0.0 < value <= 1.0 for value in y_ood)
