# CADET: X-ray Cavity Detection Pipeline


![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-2.15-D00000?style=flat-square&logo=keras&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-013243?style=flat-square&logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-1.11%2B-8CAAE6?style=flat-square&logo=scipy&logoColor=white)
![Astropy](https://img.shields.io/badge/Astropy-6.0%2B-FF6700?style=flat-square&logo=astropy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8%2B-11557C?style=flat-square&logo=matplotlib&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.1%2B-150458?style=flat-square&logo=pandas&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.7%2B-E92063?style=flat-square&logo=pydantic&logoColor=white)
![YAML](https://img.shields.io/badge/Config-YAML-CB171E?style=flat-square&logo=yaml&logoColor=white)

---

## Overview

**CADET: An Automated Pipeline for X-ray Cavity Detection in Galactic and Cluster Environments Using DBSCAN Clustering** notebook. The codebase wraps the `pycadet` inference workflow into modular Python components with a CLI interface, YAML-driven configuration, structured outputs, and a test suite — suitable for reproducible scientific pipelines and further engineering.

---

## Pipeline

The pipeline executes the following sequence:

```
FITS Image → Preprocessing → CADET Inference → DBSCAN Post-processing
          → Geometry Estimation → 3D Volume Reconstruction → Structured Export
```

1. **Load** a FITS image from disk.
2. **Rebin / center** the image to CADET-compatible dimensions.
3. **Infer** cavity probability maps using the CADET deep learning model.
4. **Decompose** the probability map into labeled cavity masks via DBSCAN-based post-processing.
5. **Estimate geometry** — rotation angle, ellipticity, semi-major and semi-minor axes.
6. **Reconstruct** 3D cavity volumes from the 2D projections.
7. **Export** plots, masks, and structured metadata.

---

## Project Structure

```
CADET_Xray_Pipeline/
├── configs/
│   └── config.example.yaml          # Example YAML configuration
├── scripts/
│   └── run_pipeline.py              # Standalone runner script
├── src/
│   └── cadet_xray_pipeline/
│       ├── __init__.py
│       ├── cli.py                   # CLI entry point
│       ├── config.py                # Pydantic config models
│       ├── evaluation.py            # Baseline evaluation utilities
│       ├── inference.py             # CADET model inference
│       ├── io.py                    # FITS I/O helpers
│       ├── pipeline.py              # Orchestration logic
│       ├── postprocessing.py        # DBSCAN cavity decomposition
│       ├── preprocessing.py         # Rebinning and centering
│       ├── visualization.py         # Plot generation
│       └── utils.py                 # Shared utilities
├── tests/
│   ├── test_config.py
│   └── test_postprocessing.py
├── pyproject.toml
├── requirements.txt
└── requirements-dev.txt
```

---

## Installation

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows PowerShell
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Or install as a package

```bash
pip install -e .
```

---

## Quick Start

Place your FITS file in `data/raw/`, then run the pipeline via script:

```bash
python scripts/run_pipeline.py \
  --input data/raw/NGC4649.fits \
  --output outputs/ngc4649 \
  --scale 2 \
  --ra "12:43:40.0057" \
  --dec "11:33:10.456" \
  --th1 0.4 \
  --th2 0.6 \
  --shift
```

Or use the installed CLI entry point:

```bash
cadet-xray \
  --input data/raw/NGC4649.fits \
  --output outputs/ngc4649 \
  --scale 2 \
  --ra "12:43:40.0057" \
  --dec "11:33:10.456"
```

---

## Configuration

For repeatable runs, use a YAML configuration file:

```bash
cadet-xray --config configs/config.example.yaml
```

See `configs/config.example.yaml` for all available parameters and inline documentation.

---

## Outputs

| File | Description |
|------|-------------|
| `prediction.npy` | Raw CADET cavity probability map |
| `cavity_labels.npy` | Integer-labeled cavity mask |
| `summary.json` | Structured metadata and per-cavity measurements |
| `prediction_overlay.png` | Input image overlaid with prediction contours |
| `cavity_labels.png` | Color-coded labeled cavity map |

---

## Notes on Evaluation

Computed a simple accuracy metric against an intensity-threshold-derived pseudo-ground-truth mask. This is **not** a scientifically validated evaluation protocol. In this repository, that logic is isolated in `evaluation.py` and explicitly documented as a baseline utility, not a benchmark. For real validation, expert-labeled cavity masks should be used.

---

## Recommendations for Production Use

- Pin exact dependency versions using a lock file (e.g., `pip-compile` or `uv lock`).
- Extend the test suite with FITS fixtures covering edge cases.
- Validate against expert-annotated cavity masks before drawing scientific conclusions.
- Integrate structured logging and experiment tracking (e.g., MLflow, W&B).
- Add CI workflows for linting, testing, and packaging on push.

---

## Attribution

All deep learning inference and cavity analysis functionality is provided by the external [`pycadet`](https://github.com/JunaidZaman03/CADET-Xray-Cavity-Detection) package. Please cite the original CADET work if you use this pipeline in a scientific context.
