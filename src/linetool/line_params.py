import cmath


def rlc_to_zy(r, L_mH, C_uF, g, freq_hz, length=1) -> tuple:
    """
    Convert r/L/C/g per-unit-length parameters to complex z, y per unit length.
    r: ohm/length, L_mH: mH/length, C_uF: uF/length, g: siemens/length
    Returns (z_per_length, y_per_length) as complex ohm/length, siemens/length.
    """
    w = 2 * cmath.pi * freq_hz
    x = w * L_mH * 1e-3
    b = w * C_uF * 1e-6
    z = complex(r, x)
    y = complex(g, b)
    return z, y


def short_line_abcd(z_per_length: complex, length: float) -> tuple:
    """
    Short line model: series impedance only, no shunt admittance.
    Returns (Z, Y, A, B, C, D).
    """
    Z = z_per_length * length
    Y = complex(0, 0)
    A = complex(1, 0)
    B = Z
    C = complex(0, 0)
    D = complex(1, 0)
    return Z, Y, A, B, C, D


def medium_line_abcd(z_per_length: complex, y_per_length: complex, length: float) -> tuple:
    """
    Medium line model: nominal pi.
    Returns (Z, Y, A, B, C, D).
    """
    Z = z_per_length * length
    Y = y_per_length * length
    A = D = 1 + Z * Y / 2
    B = Z
    C = Y * (1 + Z * Y / 4)
    return Z, Y, A, B, C, D


def long_line_abcd(z_per_length: complex, y_per_length: complex, length: float) -> tuple:
    """
    Long line model: exact solution via hyperbolic functions.
    Returns (Zc, gamma, A, B, C, D, Z_eq, Y_eq) where Z_eq/Y_eq are the
    equivalent-pi parameters.
    """
    z, y = z_per_length, y_per_length
    gamma = cmath.sqrt(z * y)
    Zc = cmath.sqrt(z / y)
    gl = gamma * length

    A = D = cmath.cosh(gl)
    B = Zc * cmath.sinh(gl)
    C = cmath.sinh(gl) / Zc

    Z_eq = B
    Y_eq = 2 / Zc * cmath.tanh(gl / 2)

    return Zc, gamma, A, B, C, D, Z_eq, Y_eq