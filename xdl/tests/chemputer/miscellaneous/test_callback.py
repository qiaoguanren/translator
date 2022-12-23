import asyncio

from xdl.steps import Callback
from xdl.steps.core import AbstractStep, Step

try:
    from chemputerxdl.steps import Wait
except ModuleNotFoundError:
    pass

import os
from typing import Callable, List

import pytest

from ...utils import get_chempiler

HERE = os.path.abspath(os.path.dirname(__file__))


class TestStep(AbstractStep):

    __test__ = False

    PROP_TYPES = {"on_finish": Callable, "context": None}

    def __init__(self, on_finish: Callable, context: None, **kwargs):
        super().__init__(locals())

    def get_steps(self) -> List[Step]:
        return [
            Wait(50),
            Callback(self.on_finish, args=[0], keyword_args={"result": 1}),
        ]


@pytest.mark.chemputer
def test_callback():
    c = get_chempiler(os.path.join(HERE, "..", "..", "files", "bigrig.json"))
    step = TestStep(on_finish=on_finish, context=None)
    asyncio.run(step.execute(c))


@pytest.mark.chemputer
def on_finish(item, result=None):
    assert item == 0
    assert result == 1
