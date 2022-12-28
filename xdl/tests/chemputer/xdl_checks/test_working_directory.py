import json
import os

import pytest

from xdl import XDL
from xdl.readwrite.utils import read_file

try:
    from chemputerxdl import ChemputerPlatform
except ModuleNotFoundError:
    pass

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "..", "files")
INTEGRATION_FOLDER = os.path.join(os.path.dirname(HERE), "..", "files")


@pytest.mark.chemputer
def test_set_working_directory_from_file():
    xdl_f = os.path.join(INTEGRATION_FOLDER, "lidocaine.xdl")
    graph_f = os.path.join(INTEGRATION_FOLDER, "lidocaine_graph.json")

    # check working directory is set to folder of xdl file when no other option
    # for working directory given
    x1 = XDL(xdl_f, platform=ChemputerPlatform)
    x1.prepare_for_execution(graph_f, interactive=False)

    assert x1.working_directory == os.path.abspath(INTEGRATION_FOLDER)

    # check working directory is overwritten for xdl file when working directory
    # is supplied
    x2 = XDL(xdl=xdl_f, working_directory=HERE, platform=ChemputerPlatform)
    x2.prepare_for_execution(graph_f, interactive=False)

    assert x2.working_directory == HERE

    # check working directory is set to XDLPATH when XDLPATH exists in
    # environment variables
    os.environ["XDLPATH"] = FOLDER
    x3 = XDL(xdl=xdl_f, platform=ChemputerPlatform)
    x3.prepare_for_execution(graph_f, interactive=False)

    assert x3.working_directory == FOLDER

    # check working directory is overwritten for xdl file when working directory
    # is supplied, even when environment variable is set
    x4 = XDL(xdl=xdl_f, working_directory=HERE, platform=ChemputerPlatform)
    x4.prepare_for_execution(graph_f, interactive=False)

    assert x4.working_directory == HERE
    os.environ.pop("XDLPATH")


@pytest.mark.chemputer
def test_set_working_directory_from_dict():
    xdl_f = os.path.join(INTEGRATION_FOLDER, "xdl_jsons", "lidocaine.json")
    graph_f = os.path.join(INTEGRATION_FOLDER, "lidocaine_graph.json")

    with open(xdl_f) as j:
        xdl_d = json.load(j)

    # check working directory is to current working directory when xdl format
    # is json dict
    x1 = XDL(xdl_d, platform=ChemputerPlatform)
    x1.prepare_for_execution(graph_f, interactive=False)

    assert x1.working_directory == os.getcwd()


@pytest.mark.chemputer
def test_set_working_directory_from_xdl_str():
    xdl_f = os.path.join(INTEGRATION_FOLDER, "lidocaine.xdl")
    graph_f = os.path.join(INTEGRATION_FOLDER, "lidocaine_graph.json")

    xdl_s = read_file(xdl_f)

    # check working directory is set to current working directory when xdl
    # format is xml string
    x1 = XDL(xdl_s, platform=ChemputerPlatform)
    x1.prepare_for_execution(graph_f, interactive=False)

    assert x1.working_directory == os.getcwd()
