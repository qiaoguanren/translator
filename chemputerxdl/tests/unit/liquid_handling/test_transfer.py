import os
import pytest
from ...utils import generic_chempiler_test
from xdl import XDL

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')

@pytest.mark.unit
def test_transfer_through():
    """Test that transfering through a cartridge works."""
    xdl_f = os.path.join(FOLDER, 'transfer_through.xdl')
    graph_f = os.path.join(FOLDER, 'bigrig.json')

    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, testing=True)
    generic_chempiler_test(xdl_f, graph_f)

@pytest.mark.unit
def test_transfer_all_stops_stirring():
    """Test that Transfer 'all' stops stirring, so that stirrer doesn't mess
    with tubing position inside flask.
    """
    xdl_f = os.path.join(FOLDER, 'transfer_all_stops_stirring.xdl')
    graph_f = os.path.join(FOLDER, 'bigrig.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, testing=True)

    transfer_steps = [step for step in x.steps if step.name == 'Transfer']

    # Transfer 10 mL
    assert transfer_steps[0].steps[0].name == 'CMove'

    # Transfer 'all'
    assert (
        transfer_steps[1].steps[0].name == 'StopStir'
        and transfer_steps[1].steps[0].vessel == transfer_steps[1].from_vessel
    )
    print(transfer_steps[1].properties)
    assert transfer_steps[1].steps[-1].name == 'StopHeatChill'
    assert transfer_steps[1].steps[-1].vessel == 'reactor'

    generic_chempiler_test(xdl_f, graph_f)
