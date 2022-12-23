import os
from typing import List

import pytest

try:
    from chemputerxdl import ChemputerPlatform
except ModuleNotFoundError:
    pass

from xdl import XDL
from xdl.constants import JSON_PROP_TYPE
from xdl.steps import AbstractStep, Step

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "..", "files")


class TestStep(AbstractStep):
    __test__ = False

    PROP_TYPES = {"test_prop": JSON_PROP_TYPE}

    def __init__(self, test_prop, **kwargs):
        super().__init__(locals())

    def get_steps(self) -> List[Step]:
        return []


class TestPlatform(ChemputerPlatform):
    __test__ = False

    @property
    def step_library(self):
        step_library = super().step_library
        step_library["TestStep"] = TestStep
        return step_library


@pytest.mark.chemputer
def test_json_prop_types():
    save_path = os.path.join(FOLDER, "json-prop-type.xdl")

    x = XDL(
        steps=[TestStep({"a": "b", "1": 2})],
        reagents=[],
        hardware=[],
        platform=TestPlatform,
    )
    x.save(save_path)
    x = XDL(save_path, platform=TestPlatform)
    test_prop = x.steps[0].test_prop
    assert type(test_prop) == dict
    assert test_prop["a"] == "b"
    assert test_prop["1"] == 2
