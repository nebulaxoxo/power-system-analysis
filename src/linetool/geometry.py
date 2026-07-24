def single_circuit_gmd(D12: float, D23: float, D13: float) -> float:
    """
    Geometric Mean Distance for a single-circuit transposed line.

    D12, D23, D13: phase spacings (any consistent unit, e.g. m or ft)
    Returns GMD in the same unit.
    """
    return (D12 * D23 * D13) ** (1 / 3)