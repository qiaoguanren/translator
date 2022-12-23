import pytest

import xdl.utils.prop_limits as pl


@pytest.mark.unit
def test_prop_limit_addition():
    """Testing to see that the __add__ method works as expected,
    and testing the MEASUREMENT_PROP_LIMIT"""

    # Addition tests
    temp_and_ph = pl.TEMP_PROP_LIMIT + pl.PH_RANGE_PROP_LIMIT
    assert temp_and_ph.validate("10 °C")
    assert temp_and_ph.validate("8.777")
    assert temp_and_ph.validate("55.777")
    with pytest.raises(AssertionError):
        assert temp_and_ph.validate("55.777 kJ/mol")
    with pytest.raises(AssertionError):
        assert pl.PH_RANGE_PROP_LIMIT.validate("75")
    with pytest.raises(AssertionError):
        assert pl.PH_RANGE_PROP_LIMIT.validate("55.777 kJ/mol")
    temp_and_colour_and_power = (
        pl.TEMP_PROP_LIMIT + pl.COLOR_PROP_LIMIT + pl.POWER_PROP_LIMIT
    )
    assert temp_and_colour_and_power.validate("10 °C")
    assert temp_and_colour_and_power.validate("green")
    assert temp_and_colour_and_power.validate("1210 MW")
    with pytest.raises(AssertionError):
        assert temp_and_colour_and_power.validate("55.777 kJ/mol")

    measurement = pl.MEASUREMENT_PROP_LIMIT
    assert measurement.validate("10 °C")
    assert measurement.validate("8.777")
    assert measurement.validate("55.777")
    with pytest.raises(AssertionError):
        assert measurement.validate("55.777 kJ/mol")
    with pytest.raises(AssertionError):
        assert measurement.validate("1210 MW")
    with pytest.raises(AssertionError):
        assert measurement.validate("green")
