import os

import pytest

from xdl import XDL

try:
    from chemputerxdl import ChemputerPlatform
except ModuleNotFoundError:
    pass

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "..", "files")


@pytest.mark.chemputer
def test_scaling():
    """Test that dry step at specific pressure works in filter."""
    xdl_f = os.path.join(FOLDER, "scale_procedure.xdl")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.scale_procedure(0.5)
    assert x.steps[0].volume == 10  # Add step changed
    assert x.steps[1].volume == 10  # CleanVessel unchanged
