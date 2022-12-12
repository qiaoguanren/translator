import os
import pytest
from xdl import XDL

HERE = os.path.abspath(os.path.dirname(__file__))
INTEGRATION_FOLDER = os.path.join(
    os.path.dirname(HERE), '..', 'integration', 'files'
)

TESTS = [
    os.path.join(INTEGRATION_FOLDER, 'orgsyn_v83p0184a.xdl'),
    os.path.join(INTEGRATION_FOLDER, 'lidocaine.xdl'),
    os.path.join(INTEGRATION_FOLDER, 'AlkylFluor.xdl'),
]

def compare_xdls(xdl1, xdl2):
    for i, step in enumerate(xdl1.steps):
        assert step.name == xdl2.steps[i].name
        for prop, val in step.properties.items():
            if prop not in step.INTERNAL_PROPS and prop != 'children':
                assert val == xdl2.steps[i].properties[prop]

@pytest.mark.unit
def test_xdl_readwrite():
    for test in TESTS:
        x1 = XDL(test)
        x1.save('test.xdl')
        x2 = XDL('test.xdl')
        os.remove('test.xdl')
        compare_xdls(x1, x2)
