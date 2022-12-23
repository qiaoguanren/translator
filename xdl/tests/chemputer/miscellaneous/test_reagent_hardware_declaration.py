import os

import pytest

from xdl.errors import XDLReagentNotDeclaredError, XDLVesselNotDeclaredError

try:
    from tests.utils import generic_chempiler_test

except ModuleNotFoundError:
    pass

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "..", "files")


@pytest.mark.chemputer
def test_reagent_declaration():
    """Test XDLReagentNotDeclaredError is raised when reagent is used
    in Procedure section XDL, but not declared in Reagent section."""
    xdl_f = os.path.join(FOLDER, "missing_reagent_declaration.xdl")
    graph_f = os.path.join(FOLDER, "xdl_declarations.json")

    with pytest.raises(
        XDLReagentNotDeclaredError,
        match='"acetone" used as reagent in procedure but not declared in \
<Reagents> section of XDL',
    ):
        generic_chempiler_test(xdl_f, graph_f)


@pytest.mark.chemputer
def test_vessel_declaration():
    """Test XDLVesselNotDeclaredError is raised when vessel is used
    in Procedure section XDL, but not declared in Hardware section."""
    xdl_f = os.path.join(FOLDER, "missing_hardware_declaration.xdl")
    graph_f = os.path.join(FOLDER, "xdl_declarations.json")

    with pytest.raises(
        XDLVesselNotDeclaredError,
        match='"reactor2" used as vessel in procedure but not declared in \
<Hardware> section of XDL',
    ):
        generic_chempiler_test(xdl_f, graph_f)
