from __future__ import annotations

import numpy as np


def create_threshold_ground_truth(data: np.ndarray, threshold: float) -> np.ndarray:
    return (data > threshold).astype(np.uint8)


def resize_mask_to_prediction_shape(mask: np.ndarray, target_shape: tuple[int, int]) -> np.ndarray:
    try:
        from scipy.ndimage import zoom
    except ImportError as exc:
        raise ImportError("scipy is required for mask resizing.") from exc

    zoom_factors = (target_shape[0] / mask.shape[0], target_shape[1] / mask.shape[1])
    return zoom(mask, zoom_factors, order=0)


def binary_accuracy(prediction: np.ndarray, target: np.ndarray, threshold: float = 0.5) -> float:
    pred_binary = prediction > threshold
    return float(np.mean(pred_binary == target))
