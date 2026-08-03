def voltage_regulation(Vs_LL: float, Vr_LL: float, A: complex) -> float:
    """
    Percent voltage regulation.
    Vs_LL, Vr_LL: line-to-line voltage magnitudes (kV) at rated receiving-end load.
    A: the ABCD 'A' constant (complex). For a short line A=1, so this
    reduces to the simple (Vs-Vr)/Vr form automatically.

    Returns percent regulation.
    """
    Vr_nl = Vs_LL / abs(A)
    return (Vr_nl - Vr_LL) / Vr_LL * 100


def transmission_efficiency(P_receiving: float, P_sending: float) -> float:
    """
    Percent transmission efficiency = Pr / Ps * 100
    P_receiving, P_sending: real power (MW) at each end.
    """
    return P_receiving / P_sending * 100