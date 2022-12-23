import pytest

from xdl.errors import XDLValueError

try:
    from chemputerxdl.steps import Add
except ModuleNotFoundError:
    pass


@pytest.mark.chemputer
def test_volume_prop_limit():
    Add(reagent="water", vessel="reactor", volume="10 mL")
    with pytest.raises(XDLValueError):
        Add(reagent="water", vessel="reactor", volume="10 mg")
    with pytest.raises(XDLValueError):
        Add(reagent="water", vessel="reactor", volume="-10 mL")
