import os
import os
import pytest
from ..integration.test_info.lidocaine import LIDOCAINE_TEXT
from synthreader import text_to_xdl

HERE = os.path.abspath(os.path.dirname(__file__))

LIDOCAINE_PRODUCT_BOTTOMS = [False, True, True]

@pytest.mark.unit
def test_guess_separation_phases():
    x = text_to_xdl(LIDOCAINE_TEXT)
    i = 0
    for step in x.steps:
        if step.name == 'Separate':
            assert step.product_bottom == LIDOCAINE_PRODUCT_BOTTOMS[i]
            i += 1
