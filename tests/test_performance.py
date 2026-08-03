import cmath
from linetool.performance import voltage_regulation, transmission_efficiency
from linetool.line_params import rlc_to_zy, medium_line_abcd
from linetool.two_port import solve_two_port, current_from_power


def test_regulation_efficiency_ex5_1a():
    # Example 5.1(a): short line, Z=6+j20, VR=220kV LL, SR=304.8+j228.6 MVA lagging
    VRLL = 220
    VR = VRLL / (3 ** 0.5)
    Z = complex(6, 20)
    SR = complex(304.8, 228.6)
    IR = SR.conjugate() / (3 * VR)
    VS = VR + Z * IR
    VSLL = (3 ** 0.5) * abs(VS)
    SS = 3 * VS * IR.conjugate()

    reg = voltage_regulation(VSLL, VRLL, A=complex(1, 0))
    eff = transmission_efficiency(SR.real, SS.real)

    assert round(reg, 1) == 13.6
    assert round(eff, 1) == 94.4


def test_regulation_ex5_2():
    z, y = rlc_to_zy(r=0.036, L_mH=0.8, C_uF=0.0112, g=0, freq_hz=60)
    Z, Y, A, B, C, D = medium_line_abcd(z, y, length=130)

    Vr = complex(325 / (3 ** 0.5), 0)
    AR = cmath.acos(0.8)
    Sr = 270 * (cmath.cos(AR) + 1j * cmath.sin(AR))
    Ir = current_from_power(Vr, Sr)

    result = solve_two_port(A, B, C, D, Vr=Vr, Ir=Ir)
    Vs3ph_LL = (3 ** 0.5) * abs(result["Vs"])

    reg = voltage_regulation(Vs3ph_LL, 325, A)
    assert round(reg, 3) == 7.309