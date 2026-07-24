from linetool.geometry import single_circuit_gmd
from linetool.geometry import single_circuit_gmd, double_vertical_gmd
from linetool.geometry import single_circuit_gmd, double_vertical_gmd, double_horizontal_gmd

def test_single_circuit_gmd_ex4_2():
    # Example 4.2: D12=35, D23=35, D13=70 ft -> GMD = 44.097 ft
    gmd = single_circuit_gmd(35, 35, 70)
    assert round(gmd, 3) == 44.097

def test_double_vertical_gmd_ex4_5():
    # Example 4.5: S11=11, S22=16.5, S33=12.5, H12=7, H23=6.5, variant 1 -> GMD = 11.21352 m
    gmd, da1a2, db1b2, dc1c2 = double_vertical_gmd(11, 16.5, 12.5, 7, 6.5, variant=1)
    assert round(gmd, 3) == 11.214

def test_double_horizontal_gmd_ex4_6():
    # Example 4.6: D12=8, D23=8, D13=16, S11=9, variant 1 -> GMD = 14.92093 m
    gmd, da1a2, db1b2, dc1c2 = double_horizontal_gmd(8, 8, 16, 9, variant=1)
    assert round(gmd, 3) == 14.921