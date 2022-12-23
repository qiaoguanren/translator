import os
import re

import pytest

try:
    from chemputerxdl import ChemputerPlatform
    from chemputerxdl.steps import (
        CleanVessel,
        Dry,
        Evaporate,
        HeatChill,
        HeatChillToTemp,
        StartHeatChill,
    )
except ModuleNotFoundError:
    pass

from xdl import XDL
from xdl.utils.prop_limits import (
    PRESSURE_PROP_LIMIT,
    ROTATION_SPEED_PROP_LIMIT,
    TEMP_PROP_LIMIT,
)

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "..", "files")

TEMP_STEPS = [
    HeatChillToTemp,
    HeatChill,
    StartHeatChill,
    Evaporate,
    Dry,
    CleanVessel,
]


@pytest.mark.chemputer
def test_human_readable():
    """Test human readable strings are outputted correctly."""
    xdl_f = os.path.join(FOLDER, "Chemify008_epoxidation.xdl")
    graph_f = os.path.join(FOLDER, "Chemify008_epoxidation.json")

    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, interactive=False)
    for step in x.steps:
        human_readable = step.human_readable()
        verify_human_readable(step, human_readable)


def verify_no_none(step, human_readable):
    """Verify `None` is never outputted anywhere."""
    assert " None " not in human_readable


def verify_max_four_decimal_points(step, human_readable):
    """Verify no more than 4 decimal points are ever outputted."""
    assert not re.search(r"[0-9]+\.[0-9]{5}", human_readable)


def verify_no_trailing_decimal_zeroes(step, human_readable):
    """Verify there are no trailing 0s on a decimal number, e.g. "250.0" should
    be "250".
    """
    assert not re.search(r"[0-9]+\.[0]+(?![0-9])", human_readable)


def verify_temps_have_units(step, human_readable):
    """Verify all temperatures have units."""
    for prop, val in step.properties.items():
        if step.PROP_LIMITS.get(prop, None) is TEMP_PROP_LIMIT:
            if prop == "temp":
                assert f"{format_number(val)} °C" in human_readable


def verify_pressures_have_units(step, human_readable):
    """Verify all temperatures have units."""
    for prop, val in step.properties.items():
        if step.PROP_LIMITS.get(prop, None) is PRESSURE_PROP_LIMIT:
            assert f"{format_number(val)} mbar" in human_readable


def verify_rotation_speeds_have_units(step, human_readable):
    """Verify all rotation speeds have units."""
    for prop, val in step.properties.items():
        if step.PROP_LIMITS.get(prop, None) is ROTATION_SPEED_PROP_LIMIT:
            if step.properties.get("stir", None):
                assert f"{format_number(val)} RPM" in human_readable


def verify_full_stop_at_end(step, human_readable):
    """Verify all sentences end with a full stop, and only one full stop."""
    assert human_readable[-1] == "." and human_readable[-2] != "."


def format_number(number):
    """Format number to 4 decimal places with no trailing zeros."""
    return f"{number:.4f}".rstrip("0").rstrip(".")


TESTS = {
    "NO_NONE": verify_no_none,
    "FULL_STOP_AT_END": verify_full_stop_at_end,
    "MAX_FOUR_DECIMAL_POINTS": verify_max_four_decimal_points,
    "NO_TRAILING_DECIMAL_ZEROS": verify_no_trailing_decimal_zeroes,
    "TEMPS_HAVE_UNITS": verify_temps_have_units,
    "ROTATION_SPEEDS_HAVE_UNITS": verify_rotation_speeds_have_units,
    "PRESSURES_HAVE_UNITS": verify_pressures_have_units,
}


def verify_human_readable(step, human_readable):
    """Verify human readable with collection of tests."""
    for _, test in TESTS.items():
        test(step, human_readable)
