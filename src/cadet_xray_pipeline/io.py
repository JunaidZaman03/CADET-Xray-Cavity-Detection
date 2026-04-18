from __future__ import annotations

from pathlib import Path


def load_fits_data(input_path: str | Path):
    try:
        from astropy.io import fits
    except ImportError as exc:
        raise ImportError("astropy is required to load FITS data.") from exc

    return fits.getdata(str(input_path))
