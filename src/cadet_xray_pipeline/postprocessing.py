from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np


@dataclass
class CavityMeasurement:
    cavity_id: int
    area_px2: float
    angle_deg: float
    ellipticity: float
    semi_major_px: float
    semi_minor_px: float
    volume_px3: float | None = None
    area_arcsec2: float | None = None
    volume_arcsec3: float | None = None


def decompose_cavities(prediction: np.ndarray, th1: float, th2: float):
    try:
        from pycadet import decompose
    except ImportError as exc:
        raise ImportError("pycadet is required for cavity decomposition.") from exc

    return decompose(prediction, th1=th1, th2=th2)


def build_label_map(cavities: list[np.ndarray]) -> np.ndarray:
    if not cavities:
        return np.zeros((128, 128), dtype=int)
    label_map = np.zeros_like(cavities[0], dtype=int)
    for idx, cav in enumerate(cavities, start=1):
        label_map = np.where(cav > 0, idx, label_map)
    return label_map


def _compute_axes(area_px2: float, ellipticity: float) -> tuple[float, float]:
    semi_major = (area_px2 / np.pi / max(1e-8, (1 - ellipticity))) ** 0.5
    semi_minor = semi_major * (1 - ellipticity)
    return semi_major, semi_minor


def measure_cavities(cavities: list[np.ndarray], wcs: Any | None = None) -> tuple[list[CavityMeasurement], list[np.ndarray]]:
    try:
        from pycadet import make_3D_cavity, rotangle_and_ellip
    except ImportError as exc:
        raise ImportError("pycadet is required for cavity measurement.") from exc

    angular_scale = None
    if wcs is not None and hasattr(wcs, "pixel_scale_matrix"):
        angular_scale = float(wcs.pixel_scale_matrix[1, 1]) * 3600.0

    measurements: list[CavityMeasurement] = []
    cubes: list[np.ndarray] = []

    for idx, cav in enumerate(cavities, start=1):
        angle_rad, ellipticity = rotangle_and_ellip(cav.T)
        area_px2 = float(np.sum(cav))
        semi_major, semi_minor = _compute_axes(area_px2, float(ellipticity))
        cube = make_3D_cavity(cav, rotate_back=True)
        cubes.append(cube)
        volume_px3 = float(np.sum(cube))

        measurement = CavityMeasurement(
            cavity_id=idx,
            area_px2=area_px2,
            angle_deg=float(np.degrees(angle_rad)),
            ellipticity=float(ellipticity),
            semi_major_px=float(semi_major),
            semi_minor_px=float(semi_minor),
            volume_px3=volume_px3,
        )

        if angular_scale is not None:
            measurement.area_arcsec2 = area_px2 * angular_scale**2
            measurement.volume_arcsec3 = volume_px3 * angular_scale**3

        measurements.append(measurement)

    return measurements, cubes


def measurements_to_dict(measurements: list[CavityMeasurement]) -> list[dict[str, Any]]:
    return [asdict(item) for item in measurements]
