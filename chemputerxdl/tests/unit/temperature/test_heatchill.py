import os
import pytest
from ...utils import generic_chempiler_test
from xdl import XDL
from chemputerxdl.constants import (
    CHILLER_MIN_TEMP,
    CHILLER_MAX_TEMP,
    HEATER_MAX_TEMP
)
from chemputerxdl.steps import CChillerSetTemp, CStirrerSetTemp

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')

@pytest.mark.unit
def test_start_stop_heatchill():
    """Test that StartHeatChill and StopHeatChill work."""
    xdl_f = os.path.join(FOLDER, 'heatchill.xdl')
    graph_f = os.path.join(FOLDER, 'bigrig.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, testing=True)
    generic_chempiler_test(xdl_f, graph_f)

@pytest.mark.unit
def test_inactive_heatchill():
    xdl_f = os.path.join(FOLDER, 'inactive_heatchill.xdl')
    graph_f = os.path.join(FOLDER, 'bigrig.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, testing=True)
    generic_chempiler_test(xdl_f, graph_f)

@pytest.mark.unit
def test_heatchill_return_to_rt():
    xdl_f = os.path.join(FOLDER, 'heatchill_return_to_rt.xdl')
    graph_f = os.path.join(FOLDER, 'heatchill_return_to_rt.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, testing=True)
    generic_chempiler_test(xdl_f, graph_f)

@pytest.mark.unit
def test_heatchill_reactor_with_heater_and_chiller():
    xdl_f = os.path.join(FOLDER, 'heater_chiller_reactor.xdl')
    graph_f = os.path.join(FOLDER, 'heater_chiller_reactor.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, testing=True)
    assert len([
        step
        for step in x.base_steps
        if type(step) in [CChillerSetTemp, CStirrerSetTemp]
    ]) == 9
    for step in x.base_steps:
        if type(step) == CChillerSetTemp:
            assert CHILLER_MIN_TEMP < step.temp < CHILLER_MAX_TEMP

        elif type(step) == CStirrerSetTemp:
            assert CHILLER_MAX_TEMP < step.temp < HEATER_MAX_TEMP
    generic_chempiler_test(xdl_f, graph_f)
