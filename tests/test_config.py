from pathlib import Path

from cadet_xray_pipeline.config import PipelineConfig


def test_config_defaults():
    cfg = PipelineConfig(input_path=Path("demo.fits"))
    assert cfg.scale == 2
    assert cfg.th1 == 0.4
    assert cfg.th2 == 0.6
