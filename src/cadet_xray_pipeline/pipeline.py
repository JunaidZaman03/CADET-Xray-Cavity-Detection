from __future__ import annotations

import logging
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np

from .config import PipelineConfig
from .io import load_fits_data
from .inference import make_cadet_prediction
from .postprocessing import build_label_map, decompose_cavities, measure_cavities, measurements_to_dict
from .preprocessing import rebin_fits
from .utils import ensure_dir, write_json
from .visualization import save_label_map, save_prediction_overlay

logger = logging.getLogger(__name__)


def run_pipeline(config: PipelineConfig) -> dict[str, Any]:
    output_dir = ensure_dir(config.output_dir)

    logger.info("Loading raw FITS data from %s", config.input_path)
    raw_data = load_fits_data(config.input_path)

    logger.info("Rebinning input image")
    rebinned_data, wcs = rebin_fits(
        config.input_path,
        scale=config.scale,
        ra=config.ra,
        dec=config.dec,
        shift=config.shift,
    )

    logger.info("Running CADET prediction")
    prediction = make_cadet_prediction(rebinned_data, shift=config.shift)

    logger.info("Decomposing cavity candidates")
    cavities = decompose_cavities(prediction, th1=config.th1, th2=config.th2)
    label_map = build_label_map(cavities)

    logger.info("Measuring cavities")
    measurements, _ = measure_cavities(cavities, wcs=wcs)

    np.save(Path(output_dir) / "prediction.npy", prediction)
    np.save(Path(output_dir) / "cavity_labels.npy", label_map)

    if config.save_plots:
        save_prediction_overlay(rebinned_data, prediction, Path(output_dir) / "prediction_overlay.png")
        save_label_map(label_map, Path(output_dir) / "cavity_labels.png")

    summary = {
        "input_path": str(config.input_path),
        "output_dir": str(output_dir),
        "scale": config.scale,
        "shift": config.shift,
        "thresholds": {"th1": config.th1, "th2": config.th2},
        "rebinned_shape": list(rebinned_data.shape),
        "raw_shape": list(raw_data.shape),
        "num_cavities": len(cavities),
        "cavities": measurements_to_dict(measurements),
    }
    write_json(Path(output_dir) / "summary.json", summary)
    return summary
