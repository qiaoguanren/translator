import os
import pytest
from xdl import XDL
from xdl.steps import Repeat
from ...utils import generic_chempiler_test

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')

@pytest.mark.unit
def test_repeat():
    """Test Repeat step works correctly."""
    xdl_f = os.path.join(FOLDER, 'repeat_parent.xdl')
    graph_f = os.path.join(FOLDER, 'bigrig.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, testing=True)

    for step in x.steps:
        if type(step) == Repeat:
            assert len(step.steps) == 6
            assert step.steps[0].time == 5
            assert step.steps[1].time == 10
            assert step.steps[2].volume == 20
            assert step.steps[3].time == 5
            assert step.steps[4].time == 10
            assert step.steps[5].volume == 20
    generic_chempiler_test(xdl_f, graph_f)

@pytest.mark.unit
def test_repeat_scale_procedure():
    """Test scale_procedure works when wrapped in Repeat step."""
    xdl_f = os.path.join(FOLDER, 'repeat_parent.xdl')
    graph_f = os.path.join(FOLDER, 'bigrig.json')
    x = XDL(xdl_f)
    x.scale_procedure(0.1)
    x.prepare_for_execution(graph_f, testing=True)

    for step in x.steps:
        if type(step) == Repeat:
            assert len(step.steps) == 6
            assert step.steps[0].time == 5
            assert step.steps[1].time == 10
            assert step.steps[2].volume == 2
            assert step.steps[3].time == 5
            assert step.steps[4].time == 10
            assert step.steps[5].volume == 2
    generic_chempiler_test(xdl_f, graph_f)
