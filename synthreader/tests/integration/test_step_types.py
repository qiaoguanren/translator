import os
from chemputerxdl.steps import Transfer
from synthreader import text_to_xdl

from .generator import get_reagents

HERE = os.path.abspath(os.path.dirname(__file__))

def test_correct_step_types(test_info, x=None):
    """Test that the type of every step in outputted XDL is correct."""
    if not x:
        x = text_to_xdl(test_info['text'])
    x.save(os.path.join(HERE, 'test_output', test_info['name'] + '.xdl'))
    correct_steps = test_info['steps']
    i = 0
    j = 0
    while j < len(correct_steps):
        # Ignore Transfer steps as these can just be artefacts of vessel
        # assignment and not core part of procedure.
        if type(x.steps[i]) == Transfer:
            i += 1
        assert j < len(correct_steps) and type(x.steps[i]) == correct_steps[j]
        i += 1
        j += 1
    assert i == len(x.steps)
