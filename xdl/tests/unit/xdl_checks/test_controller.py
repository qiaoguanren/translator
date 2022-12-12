import os
import pytest
from ...utils import get_chempiler
from xdl import XDLController
from chemputerxdl import ChemputerPlatform

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')

@pytest.mark.unit
def test_controller():
    """Test that XDL controller works in simulation mode."""
    graph_f = os.path.join(FOLDER, 'bigrig.json')
    c = get_chempiler(graph_f)
    controller = XDLController(ChemputerPlatform, c, graph_f)
    controller.add(reagent='water', vessel='reactor', volume=10)
