import cmath
from linetool.line_params import rlc_to_zy, medium_line_abcd
from linetool.two_port import solve_two_port, current_from_power


def test_solve_given_Vr_Ir_ex5_2():
    # Example 5.2: given receiving end (Vr, Sr), find sending end
    z, y = rlc_to_zy(r=0.036, L_mH=0.8, C_uF=0.0112, g=0, freq_hz=60)
    Z, Y, A, B, C, D = medium_line_abcd(z, y, length=130)

    Vr = complex(325 / (3 ** 0.5), 0)  # kV, phase voltage
    AR_book = cmath.acos(0.8)
    Sr = 270 * (cmath.cos(AR_book) + 1j * cmath.sin(AR_book))

    Ir = current_from_power(Vr, Sr)
    result = solve_two_port(A, B, C, D, Vr=Vr, Ir=Ir)

    Vs = result["Vs"]
    Is = result["Is"]
    Vs3ph_LL = (3 ** 0.5) * abs(Vs)
    Ism = 1000 * abs(Is)

    assert round(Vs3ph_LL, 1) == 345.0
    assert round(Ism, 0) == 421.0


def test_solve_given_Vs_Is_ex5_3():
    # Example 5.3: given sending end (Vs, Is), find receiving end
    z = complex(0.036, 0.3)
    y = complex(0, 4.22e-6)
    Z, Y, A, B, C, D = medium_line_abcd(z, y, length=130)

    Vs3ph = 345
    Ism = 0.4  # kA
    As = -cmath.acos(0.95)
    Vs = complex(Vs3ph / (3 ** 0.5), 0)
    Is = Ism * (cmath.cos(As) + 1j * cmath.sin(As))

    result = solve_two_port(A, B, C, D, Vs=Vs, Is=Is)
    Vr = result["Vr"]
    Ir = result["Ir"]

    Vr3ph = (3 ** 0.5) * abs(Vr)
    Irm = 1000 * abs(Ir)

    assert round(Vr3ph, 2) == 330.68
    assert round(Irm, 1) == 441.8