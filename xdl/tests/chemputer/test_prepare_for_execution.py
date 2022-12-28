import os

import pytest

from xdl import XDL

try:
    from chemputerxdl import ChemputerPlatform
except ModuleNotFoundError:
    pass

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "files")


@pytest.mark.chemputer
def test_lidocaine_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, "lidocaine.xdl")
    graph_f = os.path.join(FOLDER, "lidocaine_graph.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, interactive=False)


@pytest.mark.chemputer
def test_add_amount_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, "add_amount.xdl")
    graph_f = os.path.join(FOLDER, "bigrig.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, interactive=False)


@pytest.mark.chemputer
def test_orgsyn_v83p0184a_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, "orgsyn_v83p0184a.xdl")
    graph_f = os.path.join(FOLDER, "orgsyn_v83p0184a_graph.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, interactive=False)


@pytest.mark.chemputer
def test_orgsyn_v83p0193_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, "orgsyn_v83p0193.xdl")
    graph_f = os.path.join(FOLDER, "orgsyn_v83p0193_graph.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, interactive=False)


@pytest.mark.chemputer
def test_orgsyn_v80p0129_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, "orgsyn_v80p0129.xdl")
    graph_f = os.path.join(FOLDER, "orgsyn_v80p0129_graph.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, interactive=False)


@pytest.mark.chemputer
def test_orgsyn_v88p0152_a_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, "orgsyn_v88p0152_a.xdl")
    graph_f = os.path.join(FOLDER, "orgsyn_v88p0152_a_graph.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, interactive=False)


@pytest.mark.chemputer
def test_orgsyn_v81p0262_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, "orgsyn_v81p0262.xdl")
    graph_f = os.path.join(FOLDER, "orgsyn_v81p0262_graph.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, interactive=False)


@pytest.mark.chemputer
def test_orgsyn_v87p0016_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, "orgsyn_v87p0016.xdl")
    graph_f = os.path.join(FOLDER, "orgsyn_v87p0016_graph.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, interactive=False)


@pytest.mark.chemputer
def test_equivalents_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, "lidocaine.xdl")
    graph_f = os.path.join(FOLDER, "lidocaine_graph.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(
        graph_f,
        interactive=False,
        equiv_amount="1 g",
        equiv_reference="2,6-Dimethylaniline",
    )


@pytest.mark.chemputer
def test_blueprint_scaling_prepare_for_execution():
    xdl_file = os.path.join(FOLDER, "Mitsunobu_blueprint_scaled_equivalents.xdl")
    graph_file = os.path.join(FOLDER, "Mitsunobu_graph.json")
    x = XDL(xdl_file, platform=ChemputerPlatform)
    x.prepare_for_execution(
        graph_file, interactive=False, equiv_reference="Z-Hyp-OH", equiv_amount="1 g"
    )
