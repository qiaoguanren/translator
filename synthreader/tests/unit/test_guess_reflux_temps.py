import os
import os
import pytest
from ..integration.test_info.lidocaine import LIDOCAINE_TEXT
from synthreader import text_to_xdl

HERE = os.path.abspath(os.path.dirname(__file__))

LIDOCAINE_REFLUX_TEMP = 110.6

@pytest.mark.unit
def test_guess_reflux_temps():
    x = text_to_xdl(LIDOCAINE_TEXT)
    i = 0
    for step in x.steps:
        if step.name == 'HeatChill':
            assert step.temp == 110.6
