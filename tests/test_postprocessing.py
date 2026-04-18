import numpy as np

from cadet_xray_pipeline.postprocessing import build_label_map


def test_build_label_map():
    a = np.zeros((4, 4), dtype=int)
    b = np.zeros((4, 4), dtype=int)
    a[0:2, 0:2] = 1
    b[2:4, 2:4] = 1
    label_map = build_label_map([a, b])
    assert label_map[0, 0] == 1
    assert label_map[3, 3] == 2
