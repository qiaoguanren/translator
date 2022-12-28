import os

import pytest

from xdl import XDL

try:
    from chemputerxdl import ChemputerPlatform
except ModuleNotFoundError:
    pass

HERE = os.path.abspath(os.path.dirname(__file__))
FILES = os.path.join(HERE, "..", "..", "files")


@pytest.fixture
def source_xdl() -> XDL:
    return XDL(os.path.join(FILES, "add_equivalents.xdl"), platform=ChemputerPlatform)


@pytest.mark.chemputer
def test_add_XDL(source_xdl):
    # add two xdl files and check that reagents, steps and components
    # are combined
    xdl_1 = source_xdl
    xdl_2 = source_xdl
    combined = xdl_1 + xdl_2

    manual_reagent_add = list({*xdl_1.reagents, *xdl_2.reagents})
    manual_step_add = list(xdl_1.steps) + list(xdl_2.steps)
    manual_hardware_add = list({*xdl_1.hardware, *xdl_2.hardware})

    assert manual_reagent_add == combined.reagents
    assert manual_step_add == combined.steps
    assert manual_hardware_add == combined.hardware


@pytest.mark.chemputer
def test_eq_XDL(source_xdl):

    xdl_1 = source_xdl
    xdl_2 = source_xdl
    xdl_3 = XDL(os.path.join(FILES, "add_amount.xdl"), platform=ChemputerPlatform)

    assert xdl_1 == xdl_2
    assert xdl_1 != xdl_3
