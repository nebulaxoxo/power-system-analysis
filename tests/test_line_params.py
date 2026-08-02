import cmath
from linetool.line_params import rlc_to_zy, short_line_abcd, medium_line_abcd, long_line_abcd


def test_short_line_ex5_1():
    # Example 5.1: Z = 6 + j20 ohm (given directly, not per-length)
    Z, Y, A, B, C, D = short_line_abcd(complex(6, 20), length=1)
    assert Z == complex(6, 20)
    assert Y == 0
    assert A == 1 and D == 1
    assert B == complex(6, 20)
    assert C == 0


def test_medium_line_ex5_2():
    # Example 5.2: r=0.036 ohm/km, L=0.8 mH/km, C=0.0112 uF/km, g=0, f=60Hz, length=130km
    z, y = rlc_to_zy(r=0.036, L_mH=0.8, C_uF=0.0112, g=0, freq_hz=60)
    Z, Y, A, B, C, D = medium_line_abcd(z, y, length=130)

    assert round(Z.real, 2) == 4.68
    assert round(Z.imag, 3) == 39.207
    assert round(Y.imag, 8) == round(0.000548899, 8)
    assert round(A.real, 5) == 0.98924
    assert round(A.imag, 4) == 0.0013


def test_long_line_ex5_4():
    # Example 5.4: z=0.045+j0.4 ohm/km, y=j4.0e-6 siemens/km, length=250km
    # Expected ABCD: A=0.9504+j0.0055, B=10.8778+j98.3624
    z = complex(0.045, 0.4)
    y = complex(0, 4.0e-6)
    Zc, gamma, A, B, C, D, Z_eq, Y_eq = long_line_abcd(z, y, length=250)

    assert round(A.real, 4) == 0.9504
    assert round(A.imag, 4) == 0.0055
    assert round(B.real, 4) == 10.8778
    assert round(B.imag, 4) == 98.3624