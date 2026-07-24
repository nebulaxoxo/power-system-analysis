def bundle_gmr(Ds: float, r: float, nb: int, d: float = 0) -> tuple[float, float]:
    """
    Effective GMR for a bundled conductor.

    Ds: conductor's own GMR
    r: conductor radius
    nb: number of conductors in the bundle (1-4)
    d: bundle spacing (ignored if nb == 1)

    Returns (GMRL_bundle, GMRC_bundle) in the same unit as Ds/r/d.
    """
    if nb == 1:
        return Ds, r
    elif nb == 2:
        return (d * Ds) ** 0.5, (d * r) ** 0.5
    elif nb == 3:
        return (d ** 2 * Ds) ** (1 / 3), (d ** 2 * r) ** (1 / 3)
    elif nb == 4:
        factor = 2 ** 0.125
        return factor * (d ** 3 * Ds) ** (1 / 4), factor * (d ** 3 * r) ** (1 / 4)
    else:
        raise ValueError("nb must be 1, 2, 3, or 4")


def double_circuit_gmr(GMRL_bundle, GMRC_bundle, Da1a2, Db1b2, Dc1c2) -> tuple[float, float]:
    """
    Combines a bundle's GMR with inter-circuit phase distances for
    double-circuit configurations (not used for single-circuit).

    Returns (GMRL, GMRC).
    """
    DSA = (GMRL_bundle * Da1a2) ** 0.5
    DSB = (GMRL_bundle * Db1b2) ** 0.5
    DSC = (GMRL_bundle * Dc1c2) ** 0.5
    rA = (GMRC_bundle * Da1a2) ** 0.5
    rB = (GMRC_bundle * Db1b2) ** 0.5
    rC = (GMRC_bundle * Dc1c2) ** 0.5

    GMRL = (DSA * DSB * DSC) ** (1 / 3)
    GMRC = (rA * rB * rC) ** (1 / 3)
    return GMRL, GMRC