import os
import pytest
from xdl import XDL
from chemputerxdl.steps import MWAddAndTurn, CTurnMotor, Transfer
from ...utils import generic_chempiler_test

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')

@pytest.mark.unit
def test_modular_wheel_execution():
    xdl_f = os.path.join(FOLDER, "modular_wheel_transfer.xdl")
    graph_f = os.path.join(FOLDER, "modular_wheel.json")
    generic_chempiler_test(xdl_f, graph_f)

    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, interactive=False)

    assert isinstance(x.steps[0], MWAddAndTurn)

    for step in x.steps:
        if isinstance(step, MWAddAndTurn):
            assert len(step.steps) == 2
            assert isinstance(step.steps[0], Transfer)
            assert isinstance(step.steps[-1], CTurnMotor)
