import os

import pytest

from xdl import XDL
from xdl.variables import Variable

try:
    from chemputerxdl import ChemputerPlatform
except ModuleNotFoundError:
    pass

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "files")


@pytest.mark.chemputer
def test_variables_parsing():
    x = XDL(os.path.join(FOLDER, "variables_parse.xdl"), platform=ChemputerPlatform)
    assert hasattr(x, "variables")
    assert len(x.variables) == 5
    for var in x.variables:
        assert isinstance(var, Variable)
