import asyncio
import os

import pytest

from xdl import XDL
from xdl.blueprints import Blueprint
from xdl.errors import XDLError

from ..blueprints.blueprint_fixtures import flatten_steps

try:
    from chemputerxdl import ChemputerPlatform

    from ...utils import get_chempiler
except ModuleNotFoundError:
    pass

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "..", "files")
INTEGRATION_FOLDER = os.path.join(os.path.dirname(HERE), "..", "files")

TESTS = [
    ("lidocaine.xdl", "lidocaine_graph.json"),
    ("DMP.xdl", "DMP_graph.json"),
]


@pytest.mark.chemputer
@pytest.mark.parametrize(
    argnames="test_case",
    argvalues=TESTS,
    ids=[item[0] for item in TESTS],
)
def test_xdlexe(test_case):
    test_xdl_f, test_graph_f = test_case
    test_xdl_f = os.path.join(INTEGRATION_FOLDER, test_xdl_f)
    test_graph_f = os.path.join(INTEGRATION_FOLDER, test_graph_f)

    x = XDL(test_xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(
        test_graph_f, testing=True, save_path=test_xdl_f + "exe", interactive=False
    )
    xexe = XDL(test_xdl_f + "exe", platform=ChemputerPlatform)

    x_flat_steps = [s for s in flatten_steps(x.steps) if not isinstance(s, Blueprint)]
    xexe_flat_steps = flatten_steps(xexe.steps)
    assert len(x_flat_steps) == len(xexe_flat_steps)
    for i, step in enumerate(x_flat_steps):
        check_steps_identical(step, xexe_flat_steps[i], test_xdl_f)


def check_steps_identical(step1, step2, test_file):
    assert type(step1) == type(step2)
    for prop, val in step1.properties.items():
        if prop == "children":
            step1_children_no_bp = [
                s for s in step1.children if not isinstance(s, Blueprint)
            ]
            step2_children_no_bp = [
                s for s in step2.children if not isinstance(s, Blueprint)
            ]
            for j, child in enumerate(step1_children_no_bp):
                assert child.name == step2_children_no_bp[j].name
                for child_prop, child_val in child.properties.items():

                    if child_prop != "context":
                        step2_child_prop = step2_children_no_bp[j].properties[
                            child_prop
                        ]
                        if child_val or step2_child_prop:
                            assert child_val == step2_child_prop

        elif (val or step2.properties[prop]) and (prop != "context"):
            try:
                if type(val) == float:
                    assert f"{step2.properties[prop]:.4f}" == f"{val:.4f}"
                else:
                    assert step2.properties[prop] == val
            except AssertionError:
                raise AssertionError(
                    f'Property "{prop}": {val} != {step2.properties[prop]}\n'
                    f"{test_file}"
                )
    # if not isinstance(step1, (AbstractBaseStep, AbstractDynamicStep)):
    #     assert len(step1.steps) == len(step2.steps)
    #     for j, step in enumerate(step1.steps):
    #         test_steps_identical(step, step2.steps[j], test_file)


@pytest.mark.chemputer
@pytest.mark.parametrize(
    argnames="test_case", argvalues=TESTS, ids=[item[0] for item in TESTS]
)
def test_xdlexe_execute_wrong_graph(test_case):
    test_xdl_f, test_graph_f = test_case
    test_xdl_f = os.path.join(INTEGRATION_FOLDER, test_xdl_f)
    test_graph_f = os.path.join(INTEGRATION_FOLDER, test_graph_f)

    with pytest.raises(XDLError):
        x = XDL(test_xdl_f, platform=ChemputerPlatform)
        x.prepare_for_execution(test_graph_f, testing=True, interactive=False)
        x = XDL(test_xdl_f + "exe", platform=ChemputerPlatform)
        c = get_chempiler(os.path.join(FOLDER, "bigrig.json"))
        x.execute(c)


@pytest.mark.chemputer
def test_xdlexe_decodes_symbols():
    test_path = os.path.join(FOLDER, "xdlexe_test_iso8891.xdlexe")
    XDL(test_path, platform=ChemputerPlatform)


@pytest.mark.chemputer
def test_xdlexe_missing_properties():
    test_path = os.path.join(FOLDER, "xdlexe_test_missing_properties.xdlexe")

    # Test misses the `max_retries` property in SeparatePhases step
    with pytest.raises(XDLError):
        XDL(test_path, platform=ChemputerPlatform)


@pytest.mark.skip(reason="Use of DynamicStep is discouraged")
@pytest.mark.chemputer
def test_execute_dynamic_steps_individually():
    x = XDL(
        os.path.join(INTEGRATION_FOLDER, "lidocaine.xdlexe"), platform=ChemputerPlatform
    )
    graph = os.path.join(INTEGRATION_FOLDER, "lidocaine_graph.json")
    c = get_chempiler(graph)
    steps = [(i, step) for i, step in enumerate(x.steps) if step.name == "Separate"]
    assert len(steps) > 0
    for _idx, step in steps[:1]:
        with pytest.raises(XDLError):
            asyncio.run(step.execute_step(c, locks=[], tracer=[], step_indexes=[0]))

    x2 = XDL(
        os.path.join(INTEGRATION_FOLDER, "lidocaine.xdlexe"), platform=ChemputerPlatform
    )
    x2.prepare_for_execution(graph, interactive=False)
    for i, _step in x2.steps[2:1]:
        x.execute(c, i)


@pytest.mark.chemputer
def test_xdlexe_with_repeat():
    x = XDL(os.path.join(FOLDER, "repeat_parent.xdl"), platform=ChemputerPlatform)
    x.prepare_for_execution(os.path.join(FOLDER, "bigrig.json"), testing=True)
    xexe = XDL(os.path.join(FOLDER, "repeat_parent.xdlexe"), platform=ChemputerPlatform)
    for i, step in enumerate(x.steps):
        if step.name == "Repeat":
            xexe_step = xexe.steps[i]
            assert len(step.children) == len(xexe_step.children)
            assert len(step.steps) == len(xexe_step.steps)
