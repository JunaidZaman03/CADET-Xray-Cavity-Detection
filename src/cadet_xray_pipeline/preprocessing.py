from __future__ import annotations

from pathlib import Path
from typing import Optional


def rebin_fits(
    input_path: str | Path,
    scale: int,
    ra: Optional[str] = None,
    dec: Optional[str] = None,
    shift: bool = False,
):
    try:
        from pycadet import rebin
    except ImportError as exc:
        raise ImportError("pycadet is required for rebinning.") from exc

    kwargs = {"scale": scale, "shift": shift}
    if ra is not None:
        kwargs["ra"] = ra
    if dec is not None:
        kwargs["dec"] = dec
    return rebin(str(input_path), **kwargs)
