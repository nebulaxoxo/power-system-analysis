from linetool.electrical import inductance_capacitance


def test_inductance_capacitance_ex4_2():
    # Example 4.2: GMD=44.097 ft, GMRL=0.0444 ft, GMRC=0.056 ft -> L=1.38, C=0.0083
    L, C = inductance_capacitance(44.097, 0.0444, 0.056)
    assert round(L, 2) == 1.38
    assert round(C, 4) == 0.0083


def test_inductance_capacitance_ex4_4():
    # Example 4.4: GMD=56.06649, GMRL=0.65767, GMRC=0.69696 ft -> L=0.8891, C=0.0127
    L, C = inductance_capacitance(56.06649, 0.65767, 0.69696)
    assert round(L, 4) == 0.8891
    assert round(C, 4) == 0.0127