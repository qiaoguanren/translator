import os

import pytest
from chemputerxdl import ChemputerPlatform

from xdl.blueprints import Blueprint
from xdl.context import Context
from xdl.readwrite.xml_interpreter import retrieve_blueprint

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "..", "files", "test_blueprint_resolution")


@pytest.mark.unit
def test_retrieve_blueprint():
    """Tests retrieve_blueprint function works correctly."""
    bp = retrieve_blueprint(
        name="Cyclic_Mitsunobu_only",
        context=Context(platform=ChemputerPlatform()),
        folder=FOLDER,
    )

    assert issubclass(bp, Blueprint)
    assert bp.id, bp.name == "Cyclic_Mitsunobu_only"
