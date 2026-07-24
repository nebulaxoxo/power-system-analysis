def single_circuit_gmd(D12: float, D23: float, D13: float) -> float:
    """
    Geometric Mean Distance for a single-circuit transposed line.

    D12, D23, D13: phase spacings (any consistent unit, e.g. m or ft)
    Returns GMD in the same unit.
    """
    return (D12 * D23 * D13) ** (1 / 3)

def double_vertical_gmd(S11, S22, S33, H12, H23, variant: int):
    """
    GMD for a double-circuit line with vertical conductor configuration.

    S11, S22, S33: vertical spacings between phases within a circuit
    H12, H23: horizontal offsets between the two circuits
    variant: 1 = abc-c'b'a', 2 = abc-a'b'c'

    Returns (GMD, Da1a2, Db1b2, Dc1c2) -- the phase distances are needed
    later by the bundling module for double-circuit GMR calculations.
    """
    a1 = complex(-S11 / 2, H12)
    b1 = complex(-S22 / 2, 0)
    c1 = complex(-S33 / 2, -H23)

    if variant == 1:
        a2 = complex(S33 / 2, -H23)
        b2 = complex(S22 / 2, 0)
        c2 = complex(S11 / 2, H12)
    elif variant == 2:
        a2 = complex(S11 / 2, H12)
        b2 = complex(S22 / 2, 0)
        c2 = complex(S33 / 2, -H23)
    else:
        raise ValueError("variant must be 1 or 2")

    Da1b1 = abs(a1 - b1); Da1b2 = abs(a1 - b2)
    Da2b1 = abs(a2 - b1); Da2b2 = abs(a2 - b2)
    Db1c1 = abs(b1 - c1); Db1c2 = abs(b1 - c2)
    Db2c1 = abs(b2 - c1); Db2c2 = abs(b2 - c2)
    Da1c1 = abs(a1 - c1); Da1c2 = abs(a1 - c2)
    Da2c1 = abs(a2 - c1); Da2c2 = abs(a2 - c2)

    DAB = (Da1b1 * Da1b2 * Da2b1 * Da2b2) ** 0.25
    DBC = (Db1c1 * Db1c2 * Db2c1 * Db2c2) ** 0.25
    DCA = (Da1c1 * Da1c2 * Da2c1 * Da2c2) ** 0.25
    GMD = (DAB * DBC * DCA) ** (1 / 3)

    Da1a2 = abs(a1 - a2)
    Db1b2 = abs(b1 - b2)
    Dc1c2 = abs(c1 - c2)

    return GMD, Da1a2, Db1b2, Dc1c2

def double_horizontal_gmd(D12, D23, D13, S11, variant: int):
    """
    GMD for a double-circuit line with horizontal conductor configuration.

    D12, D23, D13: spacings between phases a-b, b-c, a-c within a circuit
    S11: distance between the two circuits
    variant: 1 = abc-a'b'c', 2 = abc-c'b'a'

    Returns (GMD, Da1a2, Db1b2, Dc1c2) -- as with double_vertical_gmd, needed
    later by the bundling module.
    """
    a1 = -(D13 + S11 / 2)
    b1 = -(D23 + S11 / 2)
    c1 = -S11 / 2

    if variant == 1:
        a2 = S11 / 2
        b2 = D12 + S11 / 2
        c2 = D13 + S11 / 2
    elif variant == 2:
        a2 = D13 + S11 / 2
        b2 = D12 + S11 / 2
        c2 = S11 / 2
    else:
        raise ValueError("variant must be 1 or 2")

    Da1b1 = abs(a1 - b1); Da1b2 = abs(a1 - b2)
    Da2b1 = abs(a2 - b1); Da2b2 = abs(a2 - b2)
    Db1c1 = abs(b1 - c1); Db1c2 = abs(b1 - c2)
    Db2c1 = abs(b2 - c1); Db2c2 = abs(b2 - c2)
    Da1c1 = abs(a1 - c1); Da1c2 = abs(a1 - c2)
    Da2c1 = abs(a2 - c1); Da2c2 = abs(a2 - c2)

    DAB = (Da1b1 * Da1b2 * Da2b1 * Da2b2) ** 0.25
    DBC = (Db1c1 * Db1c2 * Db2c1 * Db2c2) ** 0.25
    DCA = (Da1c1 * Da1c2 * Da2c1 * Da2c2) ** 0.25
    GMD = (DAB * DBC * DCA) ** (1 / 3)

    Da1a2 = abs(a1 - a2)
    Db1b2 = abs(b1 - b2)
    Dc1c2 = abs(c1 - c2)

    return GMD, Da1a2, Db1b2, Dc1c2

