import os
import pytest
from xdl import XDL

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, 'files')

@pytest.mark.integration
def test_lidocaine_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, 'lidocaine.xdl')
    graph_f = os.path.join(FOLDER, 'lidocaine_graph.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, interactive=False)

@pytest.mark.integration
def test_dmp_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, 'DMP.xdl')
    graph_f = os.path.join(FOLDER, 'DMP_graph.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, interactive=False)

@pytest.mark.integration
def test_alkyl_fluor_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, 'AlkylFluor.xdl')
    graph_f = os.path.join(FOLDER, 'AlkylFluor_graph.graphml')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, interactive=False)

@pytest.mark.integration
def test_orgsyn_v83p0184a_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, 'orgsyn_v83p0184a.xdl')
    graph_f = os.path.join(FOLDER, 'orgsyn_v83p0184a_graph.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, interactive=False)

@pytest.mark.integration
def test_orgsyn_v83p0193_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, 'orgsyn_v83p0193.xdl')
    graph_f = os.path.join(FOLDER, 'orgsyn_v83p0193_graph.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, interactive=False)

@pytest.mark.integration
def test_orgsyn_v80p0129_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, 'orgsyn_v80p0129.xdl')
    graph_f = os.path.join(FOLDER, 'orgsyn_v80p0129_graph.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, interactive=False)

@pytest.mark.integration
def test_orgsyn_v88p0152_a_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, 'orgsyn_v88p0152_a.xdl')
    graph_f = os.path.join(FOLDER, 'orgsyn_v88p0152_a_graph.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, interactive=False)

@pytest.mark.integration
def test_orgsyn_v81p0262_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, 'orgsyn_v81p0262.xdl')
    graph_f = os.path.join(FOLDER, 'orgsyn_v81p0262_graph.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, interactive=False)

@pytest.mark.integration
def test_orgsyn_v87p0016_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, 'orgsyn_v87p0016.xdl')
    graph_f = os.path.join(FOLDER, 'orgsyn_v87p0016_graph.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, interactive=False)

@pytest.mark.integration
def test_orgsyn_v90p0251_prepare_for_execution():
    xdl_f = os.path.join(FOLDER, 'orgsyn_v90p0251.xdl')
    graph_f = os.path.join(FOLDER, 'orgsyn_v90p0251_graph.json')
    x = XDL(xdl_f)
    x.prepare_for_execution(graph_f, interactive=False)
