import os

import pytest

try:
    from ..utils import generic_chempiler_test
except ModuleNotFoundError:
    pass

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "files")
JSON_FOLDER = os.path.join(FOLDER, "xdl_jsons")

TESTS = [
    ("lidocaine.xdl", "lidocaine_graph.json"),
    ("DMP.xdl", "DMP_graph.json"),
    ("DMP_with_parameters.xdl", "DMP_graph.json"),
    ("DMP_with_parameters_no_param_prefix.xdl", "DMP_graph.json"),
    # Removed as not easy to convert a graphml graph to SL2
    # ('AlkylFluor.xdl', 'AlkylFluor_graph.graphml'),
    ("orgsyn_v83p0184a.xdl", "orgsyn_v83p0184a_graph.json"),
    ("orgsyn_v83p0193.xdl", "orgsyn_v83p0193_graph.json"),
    ("orgsyn_v80p0129.xdl", "orgsyn_v80p0129_graph.json"),
    ("orgsyn_v88p0152_a.xdl", "orgsyn_v88p0152_a_graph.json"),
    ("orgsyn_v81p0262.xdl", "orgsyn_v81p0262_graph.json"),
    ("orgsyn_v87p0016.xdl", "orgsyn_v87p0016_graph.json"),
    ("repeat_until_done_basic.xdl", "Mitsunobu_graph.json"),
]

JSON_TESTS = [
    ("lidocaine.json", "lidocaine_graph.json"),
    ("DMP.json", "DMP_graph.json"),
    ("DMP_with_parameters.json", "DMP_graph.json"),
    ("orgsyn_v83p0184a.json", "orgsyn_v83p0184a_graph.json"),
    ("orgsyn_v83p0193.json", "orgsyn_v83p0193_graph.json"),
    ("orgsyn_v80p0129.json", "orgsyn_v80p0129_graph.json"),
    ("orgsyn_v88p0152_a.json", "orgsyn_v88p0152_a_graph.json"),
    ("orgsyn_v81p0262.json", "orgsyn_v81p0262_graph.json"),
    ("orgsyn_v87p0016.json", "orgsyn_v87p0016_graph.json"),
]


@pytest.mark.chemputer
@pytest.mark.parametrize(
    argnames="test_case",
    argvalues=TESTS,
    ids=[item[0] for item in TESTS],
)
def test_xdl(test_case):
    test_xdl_f, test_graph_f = test_case
    test_xdl_f = os.path.join(FOLDER, test_xdl_f)
    test_graph_f = os.path.join(FOLDER, test_graph_f)

    generic_chempiler_test(test_xdl_f, test_graph_f)


@pytest.mark.chemputer
@pytest.mark.parametrize(
    argnames="test_case",
    argvalues=JSON_TESTS,
    ids=[item[0] for item in JSON_TESTS],
)
def test_json(test_case):
    test_xdl_f, test_graph_f = test_case
    generic_chempiler_test(
        os.path.join(JSON_FOLDER, test_xdl_f), os.path.join(FOLDER, test_graph_f)
    )
