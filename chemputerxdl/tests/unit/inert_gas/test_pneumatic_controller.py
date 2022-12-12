import os
import pytest
from xdl import XDL
from ...utils import generic_chempiler_test

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')

@pytest.mark.unit
def test_pneumatic_controller():
    """Test pneumatic controller works correctly."""
    xdl_f = os.path.join(FOLDER, 'pneumatic_controller.xdl')
    graph_f = os.path.join(FOLDER, 'pneumatic_controller.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, testing=True)

    # Ignores the shutdown at the end
    check_steps = x.steps[:-1]
    for step in check_steps:
        assert step.pneumatic_controller == 'pneumatic_controller'

        if step.vessel == 'flask':
            assert str(step.pneumatic_controller_port) == '2'

        elif step.vessel == 'filter':

            if step.port == 'bottom':
                assert str(step.pneumatic_controller_port) == '1'

            elif step.port == 'top':
                assert str(step.pneumatic_controller_port) == '3'

    generic_chempiler_test(xdl_f, graph_f)

@pytest.mark.unit
def test_pneumatic_controller_ports():
    """This file was causing an error, see issue #22."""
    xdl_f = os.path.join(FOLDER, 'MIDA-Deprotection.xdl')
    graph_f = os.path.join(FOLDER, 'MIDA-Deprotection.json')
    generic_chempiler_test(xdl_f, graph_f)
