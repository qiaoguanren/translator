import os

import pytest

from xdl import XDL

try:
    from chemputerxdl import ChemputerPlatform
except ModuleNotFoundError:
    pass

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "..", "files")


@pytest.mark.chemputer
def test_global_comment_prop():
    """Check comment prop works and survives saving and reloading."""
    x = XDL(os.path.join(FOLDER, "comment-prop.xdl"), platform=ChemputerPlatform)
    assert x.steps[0].comment == "this is a comment"

    # Check XML save and reload works
    os.makedirs(os.path.join(FOLDER, "chempiler_output"), exist_ok=True)
    save_path = os.path.join(FOLDER, "chempiler_output", "comment-prop-saved.xdl")
    x.save(save_path)
    x = XDL(save_path, platform=ChemputerPlatform)
    os.remove(save_path)
    assert x.steps[0].comment == "this is a comment"

    # Check JSON save and reload works
    save_json_path = os.path.join(FOLDER, "chempiler_output", "comment-prop-saved.json")
    x.save(save_json_path, file_format="json")
    x = XDL(save_json_path, platform=ChemputerPlatform)
    os.remove(save_json_path)
    assert x.steps[0].comment == "this is a comment"
