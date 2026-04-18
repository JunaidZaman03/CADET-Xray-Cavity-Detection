from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from .config import PipelineConfig
from .pipeline import run_pipeline
from .utils import setup_logging


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Production CLI for CADET X-ray cavity detection.")
    parser.add_argument("--config", type=str, help="Path to YAML config file.")
    parser.add_argument("--input", dest="input_path", type=str, help="Input FITS file path.")
    parser.add_argument("--output", dest="output_dir", type=str, help="Output directory.")
    parser.add_argument("--scale", type=int, default=2, help="Rebin scale.")
    parser.add_argument("--ra", type=str, default=None, help="Right ascension for centering.")
    parser.add_argument("--dec", type=str, default=None, help="Declination for centering.")
    parser.add_argument("--shift", action="store_true", help="Enable shifted CADET inference.")
    parser.add_argument("--th1", type=float, default=0.4, help="Lower cavity threshold.")
    parser.add_argument("--th2", type=float, default=0.6, help="Upper cavity threshold.")
    parser.add_argument("--prediction-threshold", type=float, default=0.5, help="Binary prediction threshold for evaluation helpers.")
    parser.add_argument("--no-plots", action="store_true", help="Disable plot generation.")
    return parser


def parse_config(args: argparse.Namespace) -> PipelineConfig:
    if args.config:
        return PipelineConfig.from_yaml(args.config)
    if not args.input_path:
        raise SystemExit("Either --config or --input must be provided.")
    return PipelineConfig(
        input_path=Path(args.input_path),
        output_dir=Path(args.output_dir or "outputs/run"),
        scale=args.scale,
        ra=args.ra,
        dec=args.dec,
        shift=args.shift,
        th1=args.th1,
        th2=args.th2,
        prediction_threshold=args.prediction_threshold,
        save_plots=not args.no_plots,
    )


def main() -> None:
    setup_logging(logging.INFO)
    parser = build_parser()
    args = parser.parse_args()
    config = parse_config(args)
    summary = run_pipeline(config)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
