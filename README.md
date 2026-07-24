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

🚧 Early development — core calculation modules are being built and tested
before the GUI.

## Background

The original MATLAB code this project modernizes:
- `gmd.m` — interactive, menu-driven computation of GMD/GMRL/GMRC
- `acsr.m` — ACSR conductor lookup table
- `AcsrGui.m` — GUIDE-based GUI for browsing ACSR conductors

## Planned architecture

```
src/linetool/
├── geometry.py    # GMD calculations for single/double-circuit configs
├── bundling.py     # bundle conductor GMR calculations
├── electrical.py   # inductance / capacitance formulas
└── acsr_data.py    # ACSR conductor lookup table + image
```

A PyQt GUI sits on top of these once they're validated against the
textbook's known example answers.

## Reference formulas

- Inductance: `L = 0.2 * ln(GMD / GMRL)` mH/km
- Capacitance: `C = 0.0556 / ln(GMD / GMRC)` µF/km

## Running tests

```bash
pytest tests/
```

## Roadmap

- [x] Design: module split, GUI plan, platform choice
- [ ] Geometry engine + tests
- [ ] Bundling engine + tests
- [ ] Electrical formulas + tests
- [ ] ACSR data module
- [ ] PyQt GUI
- [ ] Future chapters (beyond Ch. 4)
