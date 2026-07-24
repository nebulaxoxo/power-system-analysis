import math


def inductance_capacitance(GMD: float, GMRL: float, GMRC: float) -> tuple[float, float]:
    """
    Per-phase inductance and capacitance from geometric mean values.

    GMD, GMRL, GMRC must already be in consistent units (all m or all ft).

    Returns (L, C):
        L: inductance in mH/km
        C: capacitance in uF/km
    """
    L = 0.2 * math.log(GMD / GMRL)
    C = 0.0556 / math.log(GMD / GMRC)
    return L, C