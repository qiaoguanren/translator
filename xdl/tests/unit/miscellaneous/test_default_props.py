import pytest
from chemputerxdl.steps import Dissolve, Filter

@pytest.mark.unit
def test_default_props():
    # Step DEFAULT_PROPS dict
    step = Dissolve(vessel="reactor", solvent="water", volume="20 mL")
    assert step.temp == 25
    assert step.time == 20 * 60
    assert step.stir_speed == 400
    step = Filter(filter_vessel="filter")
    assert step.wait_time == 60 * 2
