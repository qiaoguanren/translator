import pytest

try:
    from chemputerxdl.steps import Dissolve, Filter
except ModuleNotFoundError:
    pass


@pytest.mark.chemputer
def test_default_props():
    # Step DEFAULT_PROPS dict
    step = Dissolve(vessel="reactor", solvent="water", volume="20 mL")
    assert step.temp is None
    assert step.time == 20 * 60
    assert step.stir_speed == 400
    step = Filter(vessel="filter")
    assert step.wait_time == 60 * 2
