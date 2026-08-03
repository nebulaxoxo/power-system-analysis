def current_from_power(V: complex, S: complex) -> complex:
    """
    I = conj(S) / (3 * conj(V)) -- per-phase current from per-phase voltage
    and 3-phase complex power S = P + jQ.
    """
    return S.conjugate() / (3 * V.conjugate())


def current_from_impedance(V: complex, Z: complex) -> complex:
    """I = V / Z"""
    return V / Z


def solve_two_port(A: complex, B: complex, C: complex, D: complex, **known) -> dict:
    """
    Given ABCD and exactly two of {Vs, Is, Vr, Ir} as keyword args
    (complex numbers), solve for all four.

    Returns {"Vs":..., "Is":..., "Vr":..., "Ir":...}
    """
    keys = set(known.keys())

    if keys == {"Vr", "Ir"}:
        Vr, Ir = known["Vr"], known["Ir"]
        Vs = A * Vr + B * Ir
        Is = C * Vr + D * Ir

    elif keys == {"Vs", "Is"}:
        Vs, Is = known["Vs"], known["Is"]
        det = A * D - B * C
        Vr = (D * Vs - B * Is) / det
        Ir = (-C * Vs + A * Is) / det

    elif keys == {"Vs", "Vr"}:
        Vs, Vr = known["Vs"], known["Vr"]
        Ir = (Vs - A * Vr) / B
        Is = C * Vr + D * Ir

    elif keys == {"Vs", "Ir"}:
        Vs, Ir = known["Vs"], known["Ir"]
        Vr = (Vs - B * Ir) / A
        Is = C * Vr + D * Ir

    elif keys == {"Is", "Vr"}:
        Is, Vr = known["Is"], known["Vr"]
        Ir = (Is - C * Vr) / D
        Vs = A * Vr + B * Ir

    elif keys == {"Is", "Ir"}:
        Is, Ir = known["Is"], known["Ir"]
        Vr = (Is - D * Ir) / C
        Vs = A * Vr + B * Ir

    else:
        raise ValueError(
            f"Must provide exactly two of Vs, Is, Vr, Ir; got {sorted(keys)}"
        )

    return {"Vs": Vs, "Is": Is, "Vr": Vr, "Ir": Ir}