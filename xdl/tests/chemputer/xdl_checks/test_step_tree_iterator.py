import pytest

try:
    from chemputerxdl.steps import (
        CSetRecordingSpeed,
        CStirringControllerSetSpeed,
        CStirringControllerStart,
        CStirringControllerStop,
        CWait,
        StartStir,
        Stir,
        StopStir,
        Wait,
    )
except ModuleNotFoundError:
    pass


@pytest.mark.chemputer
def test_step_tree_iterator():
    """Test step tree iterator goes through step tree in a depth first
    manner.
    """
    step = Stir(vessel="reactor", time="60 min", stir_speed=250)
    expected_step_tree = [
        StartStir,
        CStirringControllerSetSpeed,
        CStirringControllerStart,
        Wait,
        CSetRecordingSpeed,
        CWait,
        CSetRecordingSpeed,
        StopStir,
        CStirringControllerStop,
    ]
    for i, substep in enumerate(step.step_tree):
        assert type(substep) == expected_step_tree[i]
