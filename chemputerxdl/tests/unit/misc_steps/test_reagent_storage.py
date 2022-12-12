import os
import pytest
from xdl import XDL
from chemputerxdl.steps import (
    StartStir, StopStir, StartHeatChill, StopHeatChill, Wait, Add)
from chemputerxdl.constants import DEFAULT_STIR_REAGENT_FLASK_SPEED

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')

@pytest.mark.unit
def test_stirred_reagents():
    """Test reagent flasks needing stirring work."""
    xdl_f = os.path.join(FOLDER, 'stirred_reagents.xdl')
    graph_f = os.path.join(FOLDER, 'bigrig.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, testing=True)

    check_steps = x.steps[:-1]
    assert type(check_steps[1]) == StartStir
    assert check_steps[1].vessel == 'flask_water'
    assert check_steps[1].stir_speed == DEFAULT_STIR_REAGENT_FLASK_SPEED
    assert type(check_steps[-1]) == StopStir

@pytest.mark.unit
def test_temp_controlled_reagents():
    """Test reagent flasks needing stirring work."""
    xdl_f = os.path.join(FOLDER, 'temp_controlled_reagents.xdl')
    graph_f = os.path.join(FOLDER, 'bigrig.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, testing=True)

    check_steps = x.steps[:-1]
    assert type(check_steps[0]) == StartHeatChill
    assert check_steps[0].vessel == 'flask_water'
    assert check_steps[0].temp == 5
    assert type(check_steps[-1]) == StopHeatChill

@pytest.mark.unit
def test_last_minute_addition():
    """Test that last minute addition works."""
    xdl_f = os.path.join(FOLDER, 'reagent_flask_last_minute_addition.xdl')
    graph_f = os.path.join(FOLDER, 'bigrig.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, testing=True)

    check_steps = x.steps[:-1]
    for i, step in enumerate(check_steps):
        if type(step) == Wait:
            last_minute_step = check_steps[i + 1]
            add_step = check_steps[i + 2]
            assert type(last_minute_step) == Add
            assert type(add_step) == Add
            assert last_minute_step.volume == 50
            assert last_minute_step.reagent == 'ether'
            assert add_step.reagent == 'water'
