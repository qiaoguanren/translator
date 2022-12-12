from typing import Callable
import time
import os
import pytest
import ChemputerAPI
from chempiler import Chempiler

from ...utils import generic_chempiler_test

from xdl import XDL
from xdl.steps.base_steps import AbstractAsyncStep
from xdl.steps.special_steps import Async
from chemputerxdl.steps import Wait

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')

class TestAsyncStep(AbstractAsyncStep):

    __test__ = False

    PROP_TYPES = {
        'callback': Callable,
        'on_finish': Callable,
    }

    def __init__(self, callback: Callable, on_finish: Callable):
        super().__init__(locals())

    def async_execute(self, chempiler, logger=None, level=0):
        for i in range(5):
            time.sleep(1)
            self.callback(i)
        self.on_finish()

class TestAsyncStepManager(object):

    __test__ = False

    def __init__(self):
        self.async_step = TestAsyncStep(
            self.test_async_step_callback, self.test_async_step_on_finish)
        self.vals = []

    def test_async_step_callback(self, i):
        self.vals.append(i)

    def test_async_step_on_finish(self):
        assert tuple(self.vals) == (0, 1, 2, 3, 4)
        self.vals = 'donedone'

    def execute(self):
        self.async_step.execute(None, None)

@pytest.mark.unit
def test_async_step():
    mgr = TestAsyncStepManager()
    mgr.execute()
    waits = 0
    while len(mgr.vals) < 5:
        time.sleep(1)
        waits += 1
        assert waits < 7
    assert mgr.vals == 'donedone'

class TestAsyncWrapperManager(object):

    __test__ = False

    def __init__(self, steps):
        self.async_steps = Async(steps, on_finish=self.on_finish)
        self.done = False

    def execute(self, chempiler):
        self.async_steps.execute(chempiler, None)

    def on_finish(self):
        self.done = True

@pytest.mark.unit
def test_async_wrapper():
    chempiler = Chempiler(
        experiment_code='test',
        output_dir=os.path.join(HERE, 'chempiler_output'),
        simulation=True,
        graph_file=os.path.join(HERE, '..', 'files', 'bigrig.json'),
        device_modules=[ChemputerAPI])

    mgr = TestAsyncWrapperManager(Wait(5))
    mgr.execute(chempiler)
    time.sleep(2)
    assert mgr.done is True

    mgr = TestAsyncWrapperManager([Wait(5)])
    mgr.execute(chempiler)
    time.sleep(2)
    assert mgr.done is True

@pytest.mark.unit
def test_async_wrapper_in_file():
    xdl_f = os.path.join(FOLDER, 'async.xdl')
    graph_f = os.path.join(FOLDER, 'bigrig.json')

    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, testing=True)
    for step in x.steps:
        if step.name == 'Async':
            assert step.steps[0].reagent_vessel == 'flask_water'

    generic_chempiler_test(xdl_f, graph_f)

@pytest.mark.unit
def test_advanced_async_case():
    xdl_f = os.path.join(FOLDER, 'async_advanced.xdl')
    graph_f = os.path.join(FOLDER, 'async_advanced.json')
    generic_chempiler_test(xdl_f, graph_f)
