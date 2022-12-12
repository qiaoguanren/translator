import os
import os
import pytest
from ..integration.test_info.lidocaine import LIDOCAINE_TEXT
from synthreader import text_to_xdl

HERE = os.path.abspath(os.path.dirname(__file__))

LIDOCAINE_NEUTRALIZATION_VOLUME = 20

@pytest.mark.unit
def test_guess_neutralization_volumes():
    x = text_to_xdl(LIDOCAINE_TEXT)
    for step in x.steps:
        if step.name == 'Add' and 'hydroxide' in step.reagent:
            assert step.volume == LIDOCAINE_NEUTRALIZATION_VOLUME
