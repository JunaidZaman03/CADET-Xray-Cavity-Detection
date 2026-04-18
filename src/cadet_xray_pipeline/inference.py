from __future__ import annotations

import numpy as np


def make_cadet_prediction(data: np.ndarray, shift: bool = False) -> np.ndarray:
    try:
        from pycadet import make_prediction
    except ImportError as exc:
        raise ImportError("pycadet is required for inference.") from exc

    return make_prediction(data, shift=shift)
