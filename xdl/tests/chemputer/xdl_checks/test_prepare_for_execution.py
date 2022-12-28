import os

import pytest

from xdl import XDL

try:
    from chemputerxdl import ChemputerPlatform
except ModuleNotFoundError:
    pass

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "..", "files")
INTEGRATION_FOLDER = os.path.join(os.path.dirname(HERE), "..", "files")


@pytest.mark.chemputer
def test_equivalents_prepare_for_execution_context():
    xdl_f = os.path.join(INTEGRATION_FOLDER, "lidocaine.xdl")
    graph_f = os.path.join(INTEGRATION_FOLDER, "lidocaine_graph.json")

    # check equivalence amount and reference passed onto Context correctly
    x1 = XDL(xdl_f, platform=ChemputerPlatform)
    x1.prepare_for_execution(
        graph_f,
        interactive=False,
        equiv_amount="1 g",
        equiv_reference="2,6-Dimethylaniline",
    )

    assert x1.context.equiv_amount == "1 g"
    assert x1.context.equiv_reference == "2,6-Dimethylaniline"

    # check equivalence amount and reference is None by default
    x2 = XDL(xdl_f, platform=ChemputerPlatform)
    x2.prepare_for_execution(graph_f, interactive=False)

    assert x2.context.equiv_amount is None
    assert x2.context.equiv_reference is None


def context_step_tree_test(compiled_xdl: XDL):
    """
    Make sure hierarichical context resolution is working (substeps can
    recursively search up their step tree until the variable is resolved)
    """
    context = compiled_xdl.context

    for step in compiled_xdl.steps:

        # top level steps should have parent context as XDL context
        assert step.context.parent_context == context

        if hasattr(step, "steps"):
            # substeps should have independent Context but still be able to
            # resolve variables from top level of Context
            for substep in step.steps:

                assert substep.context is not context
                assert substep.context.root_context is context

                for var in context._context_params:
                    if var != "parent_context":
                        assert getattr(substep.context, var) == (
                            context._context_params[var]
                        )


@pytest.mark.chemputer
def test_prepare_for_execution_context():
    xdl_f = os.path.join(INTEGRATION_FOLDER, "lidocaine.xdl")
    graph_f = os.path.join(INTEGRATION_FOLDER, "lidocaine_graph.json")

    # check equivalence amount and reference passed onto Context correctly
    x1 = XDL(xdl_f, platform=ChemputerPlatform)

    x1.prepare_for_execution(graph_f, interactive=False)

    context_step_tree_test(x1)

    # test all steps and substeps have context before execution and can be used
    # to calculate equivalent amounts
    x2 = XDL(xdl_f, platform=ChemputerPlatform)

    x2.prepare_for_execution(
        graph_f,
        interactive=False,
        equiv_amount="1 g",
        equiv_reference="2,6-Dimethylaniline",
    )

    context_step_tree_test(x2)
