from __future__ import annotations

from pathlib import Path

import numpy as np


def save_prediction_overlay(data: np.ndarray, prediction: np.ndarray, output_path: str | Path) -> None:
    import matplotlib.pyplot as plt

    plt.figure(figsize=(6, 6))
    plt.imshow(np.log10(data + 1e-10), origin="lower")
    plt.contour(prediction, levels=[0.4, 0.6, 0.9], colors="white")
    plt.title("CADET contours on X-ray image")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def save_label_map(label_map: np.ndarray, output_path: str | Path) -> None:
    import matplotlib.pyplot as plt

    plt.figure(figsize=(6, 6))
    plt.imshow(label_map, origin="lower")
    plt.title("Detected cavity labels")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
