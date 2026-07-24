from linetool.bundling import bundle_gmr, double_circuit_gmr
from linetool.geometry import double_vertical_gmd


def test_bundle_gmr_ex4_3():
    # Example 4.3: single-circuit, nb=2, Ds=0.3924 in, r=0.4885 in, d=18 in
    # GMRL = sqrt(18*0.3924)/12 = 0.22147 ft, GMRC = sqrt(18*0.4885)/12 = 0.2471 ft
    Dsb, rb = bundle_gmr(Ds=0.3924, r=0.4885, nb=2, d=18)
    GMRL_ft = Dsb / 12
    GMRC_ft = rb / 12
    assert round(GMRL_ft, 4) == 0.2215
    assert round(GMRC_ft, 4) == 0.2471


def test_double_circuit_gmr_ex4_5():
    # Example 4.5: double-circuit vertical, variant 1, nb=2
    # Conductor: diameter=1.427 in (r=0.7135 in), Ds=0.564 in, bundle spacing d=18 in
    # Expect GMRL = 1.18731 m, GMRC = 1.25920 m
    _, Da1a2, Db1b2, Dc1c2 = double_vertical_gmd(11, 16.5, 12.5, 7, 6.5, variant=1)

    # bundle_gmr works in inches, then convert to meters (1 in = 0.0254 m)
    Dsb_in, rb_in = bundle_gmr(Ds=0.564, r=0.7135, nb=2, d=18)
    Dsb_m = Dsb_in * 0.0254
    rb_m = rb_in * 0.0254

    GMRL, GMRC = double_circuit_gmr(Dsb_m, rb_m, Da1a2, Db1b2, Dc1c2)
    assert round(GMRL, 5) == 1.18731
    assert round(GMRC, 5) == 1.25920