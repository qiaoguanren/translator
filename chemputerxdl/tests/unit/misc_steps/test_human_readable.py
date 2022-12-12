import os
import pytest
from xdl import XDL
from chemputerxdl.steps import AbstractBaseStep

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')

files = [
    (os.path.join(FOLDER, 'lidocaine.xdl'),
     os.path.join(FOLDER, 'lidocaine_graph.json')),

    (os.path.join(FOLDER, 'alkyl_fluor_step4.xdl'),
     os.path.join(FOLDER, 'alkyl_fluor_step4.graphml'))
]

@pytest.mark.unit
def test_human_readable():
    """Test that human_readable generation works."""
    for xdl_f, graph_f in files:
        x = XDL(xdl_f)
        x.prepare_for_execution(graph_f, testing=True)
        for step in x.steps:
            if not isinstance(step, AbstractBaseStep):
                # No language given
                assert step.human_readable() not in [step.name, None]

                # Default language
                assert (step.human_readable(language='en')
                        not in [step.name, None])

                # Unsupported language
                assert (step.human_readable(language='cz')
                        == step.__class__.__name__)

                # Non default language
                assert step.human_readable(language='zh') not in [
                    step.name, None]
                for prop in step.properties:
                    assert not '{' + prop + '}' in step.human_readable('en')
                    assert not '{' + prop + '}' in step.human_readable('zh')
        x.human_readable()
        x.human_readable('zh')
