from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class PipelineConfig(BaseModel):
    input_path: Path
    output_dir: Path = Field(default=Path("outputs/run"))
    scale: int = Field(default=2, ge=1)
    ra: Optional[str] = None
    dec: Optional[str] = None
    shift: bool = False
    th1: float = Field(default=0.4, ge=0.0, le=1.0)
    th2: float = Field(default=0.6, ge=0.0, le=1.0)
    prediction_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    save_plots: bool = True


    @classmethod
    def from_yaml(cls, path: str | Path) -> "PipelineConfig":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return cls(**data)
