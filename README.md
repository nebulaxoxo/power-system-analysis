# Transmission Line Parameters Tool

A Python/PyQt reimplementation of classic MATLAB power-systems teaching code
(H. Saadat, *Power System Analysis*, Chapter 4) for computing transmission
line geometric mean distance (GMD), geometric mean radius (GMRL/GMRC), and
per-phase inductance/capacitance — for single-circuit and double-circuit
(vertical or horizontal) transposed lines, with bundled conductors and ACSR
conductor lookup.

This is not a line-by-line port of the original textbook exercises — it's a
generalized calculator. The textbook's worked examples (4.2–4.6) are used as
regression tests, not as the program's structure.

## Status

✅ Chapter 4 (Examples 4.2–4.6) core pipeline and GUI complete and validated.

## Background

The original MATLAB code this project modernizes:
- `gmd.m` — interactive, menu-driven computation of GMD/GMRL/GMRC
- `acsr.m` — ACSR conductor lookup table
- `AcsrGui.m` — GUIDE-based GUI for browsing ACSR conductors

## Architecture

```
src/linetool/
├── geometry.py    # GMD calculations for single/double-circuit configs
├── bundling.py     # bundle conductor GMR calculations
├── electrical.py   # inductance / capacitance formulas
├── acsr_data.py    # ACSR conductor lookup table + image
└── main.py         # PyQt6 GUI
```

## Setup

```bash
pip install -r requirements.txt
```

## Running the GUI

```bash
# from repo root
export PYTHONPATH=src   # PowerShell: $env:PYTHONPATH="src"
python -m linetool.main
```

## Reference formulas

- Inductance: `L = 0.2 * ln(GMD / GMRL)` mH/km
- Capacitance: `C = 0.0556 / ln(GMD / GMRC)` µF/km

## Running tests

```bash
export PYTHONPATH=src   # PowerShell: $env:PYTHONPATH="src"
pytest tests/ -v
```

## Roadmap

- [x] Design: module split, GUI plan, platform choice
- [x] Geometry engine + tests (single-circuit, double-vertical, double-horizontal)
- [x] Bundling engine + tests
- [x] Electrical formulas + tests
- [x] ACSR data module + tests
- [x] PyQt6 GUI (config selector, dynamic inputs, ACSR listbox + image, Calculate button, popup errors)
- [x] `requirements.txt` pinning / packaging polish
- [ ] Future chapters (beyond Ch. 4)