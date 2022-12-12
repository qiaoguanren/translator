import os
import os
import pytest
from ..integration.test_info.dmp_step3  import DMP_STEP3_TEXT
from ..integration.test_info.alkyl_fluor_step3 import ALKYL_FLUOR_STEP3_TEXT
from ..integration.test_info.alkyl_fluor_step4 import ALKYL_FLUOR_STEP4_TEXT
from synthreader import text_to_xdl

HERE = os.path.abspath(os.path.dirname(__file__))

DMP_STEP3_ROTAVAP_PRESSURE = [768.5]
ALKYL_FLUOR_STEP4_ROTAVAP_PRESSURES = [426, 699]
ALKYL_FLUOR_STEP3_ROTAVAP_PRESSURES = [699]
tests = [
    (DMP_STEP3_TEXT, DMP_STEP3_ROTAVAP_PRESSURE),
    (ALKYL_FLUOR_STEP4_TEXT, ALKYL_FLUOR_STEP4_ROTAVAP_PRESSURES),
    (ALKYL_FLUOR_STEP3_TEXT, ALKYL_FLUOR_STEP3_ROTAVAP_PRESSURES),
]

@pytest.mark.unit
def test_guess_rotavap_pressures():
    for text, pressures in tests:
        x = text_to_xdl(text)
        for step in x.steps:
            if step.name == 'Evaporate':
                assert step.pressure == pressures.pop(0)
                assert step.temp == 50
                assert step.mode == 'auto'
