import pytest
from linetool.acsr_data import get_conductor, ACSR_TABLE


def test_rail_matches_ex4_4():
    # Example 4.4: RAIL diameter=2.959 cm, GMR=1.173 cm
    rail = get_conductor("RAIL")
    assert rail.diameter_cm == 2.9590
    assert rail.gmr_cm == 1.1730


def test_bittern_matches_ex4_2():
    # Example 4.2: BITTERN diameter=1.345 in -> 1.345*2.54 = 3.4163 cm (table: 3.4160, rounding)
    bittern = get_conductor("bittern")  # lowercase, checks case-insensitivity
    assert round(bittern.diameter_cm / 2.54, 3) == 1.345


def test_unknown_conductor_raises():
    with pytest.raises(KeyError):
        get_conductor("not_a_real_conductor")


def test_table_size():
    assert len(ACSR_TABLE) == 52