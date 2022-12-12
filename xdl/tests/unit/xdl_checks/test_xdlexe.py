import os
import pytest
from xdl import XDL
from xdl.steps.base_steps import AbstractBaseStep, AbstractDynamicStep
from xdl.errors import XDLError
from ...utils import get_chempiler, generic_chempiler_test

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, '..', 'files')
INTEGRATION_FOLDER = os.path.join(
    os.path.dirname(HERE), '..', 'integration', 'files'
)

TESTS = [
    (os.path.join(INTEGRATION_FOLDER, 'lidocaine.xdl'),
     os.path.join(INTEGRATION_FOLDER, 'lidocaine_graph.json')),

    (os.path.join(INTEGRATION_FOLDER, 'DMP.xdl'),
     os.path.join(INTEGRATION_FOLDER, 'DMP_graph.json')),

    (os.path.join(INTEGRATION_FOLDER, 'AlkylFluor.xdl'),
     os.path.join(INTEGRATION_FOLDER, 'AlkylFluor_graph.graphml')),
]

@pytest.mark.unit
def test_xdlexe():
    for test_xdl_f, test_graph_f in TESTS:
        print(test_xdl_f)
        x = XDL(test_xdl_f)
        x.prepare_for_execution(
            test_graph_f, testing=True, save_path=test_xdl_f + 'exe')
        xexe = XDL(test_xdl_f + 'exe')
        assert len(x.steps) == len(xexe.steps)
        for i, step in enumerate(x.steps):
            test_steps_identical(step, xexe.steps[i], test_xdl_f)
    generic_chempiler_test(test_xdl_f, test_graph_f)

@pytest.mark.skip(reason="Not an actual test")
def test_steps_identical(step1, step2, test_file):
    assert type(step1) == type(step2)
    for prop, val in step1.properties.items():
        if prop == 'children':
            for j, child in enumerate(step1.children):
                assert child.name == step2.children[j].name
                for child_prop, child_val in child.properties.items():
                    if child_val or step2.children[j].properties[child_prop]:
                        assert (
                            child_val
                            == step2.children[j].properties[child_prop]
                        )

        elif val or step2.properties[prop]:
            try:
                if type(val) == float:
                    assert f'{step2.properties[prop]:.4f}' == f'{val:.4f}'
                else:
                    assert step2.properties[prop] == val
            except AssertionError:
                raise AssertionError(
                    f'Property "{prop}": {val} != {step2.properties[prop]}\n\
 {test_file}'
                )
    if not isinstance(step1, (AbstractBaseStep, AbstractDynamicStep)):
        assert len(step1.steps) == len(step2.steps)
        for j, step in enumerate(step1.steps):
            test_steps_identical(step, step2.steps[j], test_file)

@pytest.mark.unit
def test_xdlexe_execute_wrong_graph():
    for test_xdl_f, test_graph_f in TESTS:
        with pytest.raises(XDLError):
            x = XDL(test_xdl_f)
            x.prepare_for_execution(test_graph_f, testing=True)
            x = XDL(test_xdl_f + 'exe')
            c = get_chempiler(os.path.join(FOLDER, 'bigrig.json'))
            x.execute(c)

        x = XDL(test_xdl_f)
        x.prepare_for_execution(test_graph_f, testing=True)
        x = XDL(test_xdl_f + 'exe')
        c = get_chempiler(test_graph_f)
        x.execute(c)

@pytest.mark.unit
def test_xdlexe_decodes_symbols():
    test_path = os.path.join(FOLDER, "xdlexe_test_iso8891.xdlexe")
    XDL(test_path)

@pytest.mark.unit
def test_xdlexe_missing_properties():
    test_path = os.path.join(FOLDER, "xdlexe_test_missing_properties.xdlexe")

    # Test misses the `max_retries` property in SeparatePhases step
    with pytest.raises(XDLError):
        XDL(test_path)

@pytest.mark.unit
def test_execute_dynamic_steps_inidividually():
    x = XDL(os.path.join(FOLDER, 'xdlexe_test_dynamic_steps.xdlexe'))
    graph = os.path.join(FOLDER, 'bigrig.json')
    c = get_chempiler(graph)
    steps = [
        (i, step)
        for i, step in enumerate(x.steps)
        if step.name == 'Separate'
    ]
    assert len(steps) > 0
    for i, step in steps[:1]:
        with pytest.raises(XDLError):
            step.execute(c)

    for i, step in steps[:1]:
        x.execute(c, i)

@pytest.mark.unit
def test_xdlexe_with_repeat():
    x = XDL(os.path.join(FOLDER, 'repeat_parent.xdl'))
    x.prepare_for_execution(os.path.join(FOLDER, 'bigrig.json'), testing=True)
    xexe = XDL(os.path.join(FOLDER, 'repeat_parent.xdlexe'))
    for i, step in enumerate(x.steps):
        if step.name == 'Repeat':
            xexe_step = xexe.steps[i]
            assert len(step.children) == len(xexe_step.children)
            assert len(step.steps) == len(xexe_step.steps)
