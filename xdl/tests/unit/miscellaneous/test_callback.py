from xdl.steps.base_steps import AbstractStep
from xdl.steps.special_steps import Callback
from chemputerxdl.steps import Wait
from ...utils import get_chempiler

import os
import pytest
from typing import Callable

HERE = os.path.abspath(os.path.dirname(__file__))

class TestStep(AbstractStep):

    __test__ = False

    PROP_TYPES = {
        'on_finish': Callable,
    }

    def __init__(self, on_finish: Callable):
        super().__init__(locals())

    def get_steps(self):
        return [
            Wait(50),
            Callback(self.on_finish, args=[0], keyword_args={'result': 1}),
        ]

@pytest.mark.unit
def test_callback():
    c = get_chempiler(os.path.join(HERE, '..', 'files', 'bigrig.json'))
    step = TestStep(on_finish)
    step.execute(c)

@pytest.mark.unit
def on_finish(item, result=None):
    assert item == 0
    assert result == 1
