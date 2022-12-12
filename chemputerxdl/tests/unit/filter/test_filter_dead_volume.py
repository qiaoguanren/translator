import os
import pytest
from xdl import XDL

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')

@pytest.mark.unit
def test_remove_filter_dead_volume():
    """Test that RemoveFilterDeadVolume is only added before Filter steps,
    otherwise dead volume should just become part of reaction mixture."""
    xdl_f = os.path.join(FOLDER, 'AlkylFluor.xdl')
    graph_f = os.path.join(FOLDER, 'AlkylFluor_graph.graphml')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, interactive=False)
    for i, step in enumerate(x.steps):
        if step.name == 'RemoveFilterDeadVolume':
            if i + 2 < len(x.steps):
                assert x.steps[i + 2].name == 'Filter'
        elif step.name == 'Filter':
            if i - 2 >= 0:
                assert x.steps[i - 2].name == 'RemoveFilterDeadVolume'
