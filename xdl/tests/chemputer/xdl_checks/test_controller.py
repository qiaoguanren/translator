import os

import pytest

from xdl import XDLController

from ...utils import get_chempiler

try:
    from chemputerxdl import ChemputerPlatform
except ModuleNotFoundError:
    pass

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "..", "files")


@pytest.mark.chemputer
def test_controller():
    """Test that XDL controller works in simulation mode."""
    graph_f = os.path.join(FOLDER, "bigrig.json")
    c = get_chempiler(graph_f)
    controller = XDLController(ChemputerPlatform, c, graph_f)
    controller.add(reagent="water", vessel="reactor", volume=10)
