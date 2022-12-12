import os
import pytest
from xdl import XDL

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')

@pytest.mark.unit
def test_loop():
    """Test Loop step works correctly."""
    xdl_f = os.path.join(FOLDER, 'loop_parent.xdl')
    graph_f = os.path.join(FOLDER, 'bigrig.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, testing=True)

    for step in x.steps:
        if step.name == 'Loop':
            assert len(step.children) == 2
