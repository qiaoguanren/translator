import os

from xdl.steps import *
from synthreader import text_to_xdl

def test_correct_vessels(test_info, x=None):
    """Test that the type of every step in outputted XDL is correct."""
    if not x:
        x = text_to_xdl(test_info['text'])
    correct_vessels = test_info['vessels']
    for i, step in enumerate(x.steps):
        if type(step) == Repeat:
            for j, substep in enumerate(step.children):
                for prop, vessel in correct_vessels[i]['children'][j].items():
                    assert substep.properties[prop] == vessel
        else:
            for prop, vessel in correct_vessels[i].items():
                assert step.properties[prop] == vessel

def test_correct_properties(test_info, x=None):
    """Test that the type of every step in outputted XDL is correct."""
    if not x:
        x = text_to_xdl(test_info['text'])
    correct_properties = test_info['properties']
    for i, step in enumerate(x.steps):
        if type(step) == Repeat:
            for j, substep in enumerate(step.children):
                for prop, val in correct_properties[i]['children'][j].items():
                    if type(substep.properties[prop]) == float:
                        assert f'{substep.properties[prop]:.4f}' == f'{val:.4f}'
                    else:
                        assert substep.properties[prop] == val

        else:
            try:
                for prop, val in correct_properties[i].items():
                    if type(step.properties[prop]) == float:
                        assert f'{step.properties[prop]:.4f}' == f'{val:.4f}'
                    else:
                        assert step.properties[prop] == val
            except AssertionError:
                raise AssertionError(f'{step.name}\n\n{step.properties}')
