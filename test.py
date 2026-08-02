"""
Example 4.2 (Saadat) -- Single-circuit line, one Bittern conductor per phase.
D12=35, D23=35, D13=70 ft. Diameter=1.345 in, GMR=0.5328 in.
Expected: GMD=44.097 ft, L=1.38 mH/km, C=0.0083 uF/km
"""
from linetool.geometry import single_circuit_gmd
from linetool.bundling import bundle_gmr
from linetool.electrical import inductance_capacitance

# Geometry (ft)
D12, D23, D13 = 35, 35, 70
GMD = single_circuit_gmd(D12, D23, D13)

# Conductor (Bittern), no bundling (nb=1)
diameter_in = 1.345
GMR_in = 0.5328
r_ft = (diameter_in / 2) / 12
Ds_ft = GMR_in / 12

GMRL, GMRC = bundle_gmr(Ds=Ds_ft, r=r_ft, nb=1)

L, C = inductance_capacitance(GMD, GMRL, GMRC)

print(f"GMD  = {GMD:.5f} ft")
print(f"GMRL = {GMRL:.5f} ft   GMRC = {GMRC:.5f} ft")
print(f"L = {L:.4f} mH/km")
print(f"C = {C:.4f} uF/km")