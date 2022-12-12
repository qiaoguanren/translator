import os
import pytest
from chemputerxdl.steps import Add
from chemputerxdl.steps.steps_utility import PrimePumpForAdd
from xdl.steps.special_steps import Repeat

from xdl import XDL

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')

@pytest.mark.unit
def test_prime_n_times():
    """Test that Repeat in PrimePumpForAdd with prime_n_times works."""

    x = XDL(os.path.join(FOLDER, 'prime_n_times.xdl'))
    x.prepare_for_execution(os.path.join(FOLDER, 'bigrig.json'), testing=True)
    prime_n_times = 5

    for step in x.steps:
        if type(step) == Add:
            for add_step in step.steps:
                if type(add_step) == PrimePumpForAdd:
                    for prime_step in add_step.steps:
                        if type(prime_step) == Repeat:
                            assert len(prime_step.steps) == prime_n_times
