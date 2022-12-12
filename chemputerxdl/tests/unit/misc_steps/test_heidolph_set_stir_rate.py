import os
import pytest
from xdl import XDL
from chemputerxdl.steps import SetStirRate, CStopStir

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')

@pytest.mark.unit
def test_heidolph_set_stir_rate():
    """Test that SetStirRate with Heidolph stops the stirring after setting
    the stir speed, because Heidolph starts stirring when stir speed is set so
    need this for consistent behaviour across all stirrers.
    """
    xdl_f = os.path.join(FOLDER, 'lidocaine.xdl')
    graph_f = os.path.join(FOLDER, 'lidocaine_graph.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, testing=True)

    # Test Heidolph set stir rate stops stirring after stir rate set.
    tested = False
    for step in x.steps:
        if type(step) == SetStirRate and step.vessel == 'flask_separator':
            assert len(step.steps) == 2
            assert type(step.steps[1]) == CStopStir
            tested = True
            break

    assert tested
