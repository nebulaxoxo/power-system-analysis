from linetool.geometry import single_circuit_gmd


def test_single_circuit_gmd_ex4_2():
    # Example 4.2: D12=35, D23=35, D13=70 ft -> GMD = 44.097 ft
    gmd = single_circuit_gmd(35, 35, 70)
    assert round(gmd, 3) == 44.097