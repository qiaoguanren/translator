"""Tests for XDL XML blueprints (i.e. blueprints that can be declared
directly in XDL XML files)
"""
#  std
import os

import pytest

from tests.utils import generic_chempiler_test

#  relative
from xdl import XDL
from xdl.blueprints import Blueprint
from xdl.context import Context
from xdl.errors import (
    XDLError,
    XDLNoParameterValue,
    XDLReagentNotDeclaredError,
    XDLVesselNotDeclaredError,
)

from .blueprint_fixtures import (
    check_props,
    flatten_steps,
    mitsunobu_equivalence_props,
    mitsunobu_props,
    simple_blueprint_props,
    transfer_liquids_props,
)

try:
    from chemputerxdl import ChemputerPlatform
except ModuleNotFoundError:
    pass

HERE = os.path.dirname(__file__)
FILES = os.path.join(HERE, "..", "..", "files")


@pytest.fixture
def mitsunobu_fixture():
    return mitsunobu_props()


@pytest.fixture
def mitsunobu_equivs_fixture():
    return mitsunobu_equivalence_props()


@pytest.fixture
def simple_blueprint_fixture():
    return simple_blueprint_props()


@pytest.fixture
def transfer_liquids_fixture():
    return transfer_liquids_props()


@pytest.mark.chemputer
def test_equivalence_references_prepare_for_execution(mitsunobu_equivs_fixture):
    """Checks final amounts are correct for blueprint-specific
    equivalence references and blueprints / steps whos equivalence
    reference is provided upon prepare for execution.

    Args:
        ugi_heck_fixture (List[Tuple[str, Dict[str, Any]]]): list of step name
            tuples and their associated props and values. Spawned from
            'Mitsunobu_blueprint_equiv_references.xdl'
    """
    xdl_file = os.path.join(FILES, "Mitsunobu_blueprint_equiv_references.xdl")
    graph_file = os.path.join(FILES, "Chemify149_Mitsunobu.json")

    x = XDL(xdl_file, platform=ChemputerPlatform)

    x.prepare_for_execution(
        graph_file=graph_file,
        interactive=False,
        equiv_reference="PPh3",
        equiv_amount="1 g",
    )
    check_props(steps=flatten_steps(x.steps), prop_list=mitsunobu_equivs_fixture)


@pytest.mark.chemputer
def test_mitsunobu_blueprint(mitsunobu_fixture):
    """Validate Mitsunobu blueprint, which contains blueprint-specific
    equivalence reference.

    Args:
        mitsunobu_fixture (List[Tuple[str, Dict[str, Any]]]): list of step name
            tuples and their associated props and values. Spawned from
            'Mitsunobu_blueprint.xdl'
    """
    xdl_file = os.path.join(FILES, "Mitsunobu_blueprint.xdl")
    graph_file = os.path.join(FILES, "Chemify149_Mitsunobu.json")

    x = XDL(xdl_file, platform=ChemputerPlatform)

    x.prepare_for_execution(
        graph_file=graph_file,
        interactive=False,
        equiv_reference="PPh3",
        equiv_amount="2 mol",
    )
    all_steps = flatten_steps(x.steps)

    for i, _ in enumerate(mitsunobu_fixture):
        step = all_steps[i]
        assert type(step.context) == Context

        ref_reagent = step.context._reference_reagent.name

        # second BP does not have specific equiv_reference
        if isinstance(step.context.xdl(), Blueprint) and i < 18:
            assert ref_reagent == "Z-Hyp-OH"
        else:
            assert ref_reagent == "PPh3"

    check_props(steps=all_steps, prop_list=mitsunobu_fixture)


@pytest.mark.chemputer
def test_non_blueprint_xml_invalid_step_prop():
    """
    Tests non-blueprint step prop validation in a blueprint-containing XDL.
    """
    xdl_file = os.path.join(FILES, "Mitsunobu_blueprint_invalid_step_props.xdl")

    with pytest.raises(
        XDLError, match="flibits is not a valid attribute for ResetHandling"
    ):
        XDL(xdl_file, platform=ChemputerPlatform)


@pytest.mark.chemputer
def test_blueprint_xml_invalid_step_prop():
    """Tests blueprint step prop validation in a blueprint-containing XDL."""
    xdl_file = os.path.join(FILES, "Mitsunobu_blueprint_invalid_bp_step_props.xdl")

    with pytest.raises(
        XDLError, match="flibits is not a valid attribute for ResetHandling"
    ):
        XDL(xdl_file, platform=ChemputerPlatform)


@pytest.mark.chemputer
def test_blueprint_no_equivs(simple_blueprint_fixture):
    """Validate Mitsunobu blueprint, which contains blueprint-specific
    equivalence reference.

    Args:
        mitsunobu_fixture (List[Tuple[str, Dict[str, Any]]]): list of step name
            tuples and their associated props and values. Spawned from
            'Mitsunobu_blueprint.xdl'
    """
    xdl_file = os.path.join(FILES, "simple_blueprint_ALC3_no_equivs.xdl")
    graph_file = os.path.join(FILES, "ALC3_testing_graph_no_DF.json")

    x = XDL(xdl_file, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_file=graph_file, interactive=False)

    all_steps = flatten_steps(x.steps)

    for i, (step_name, _props) in enumerate(simple_blueprint_fixture):
        step = all_steps[i]

        assert step.name == step_name
        assert step.context._reference_reagent is None

        # check nothing funky is happening with context eq calculations
        assert step.context._equiv_moles is None
        assert step.context.equivalents_to_mass() is None
        assert step.context.amount_to_mass() is None
        assert step.context.moles_to_mass() is None
        assert step.context.moles_to_volume() is None
        assert step.context.equivalents_to_volume() is None

    check_props(steps=all_steps, prop_list=simple_blueprint_fixture)


@pytest.mark.chemputer
def test_blueprint_mapping_from_synthesis_error():
    """
    Test error is raised when hardware and reagents are not explicitly mapped
    / mapping of objects from main synthesis is not possible.
    """

    xdl_file = os.path.join(
        FILES, "simple_blueprint_ALC3_two_blueprint_refs_unmapped_params.xdl"
    )

    # make sure no random values are assigned when parameters are used but
    # not defined
    with pytest.raises(XDLNoParameterValue):
        XDL(xdl_file, platform=ChemputerPlatform)

    # check error is raised when reagent is used in BP but not explicitly
    # mapped
    xdl_file_2 = os.path.join(FILES, "simple_blueprint_ALC3_with_params.xdl")

    with pytest.raises(XDLReagentNotDeclaredError):
        XDL(xdl_file_2, platform=ChemputerPlatform)


@pytest.mark.chemputer
def test_recursive_blueprint(mitsunobu_fixture):
    """Validate Mitsunobu_recursive_blueprint, which contains blueprint-specific
    equivalence reference, recursive_blueprint,
    unique recursive blueprint equiv reference,
    use of equivalents and parameters resolution in all levels of blueprints.

    Args:
        mitsunobu_fixture (List[Tuple[str, Dict[str, Any]]]): list of step name
            tuples and their associated props and values. Spawned from
            'Mitsunobu_blueprint.xdl'
    """
    xdl_file = os.path.join(FILES, "Mitsunobu_recursive_blueprint.xdl")
    graph_file = os.path.join(FILES, "Chemify149_Mitsunobu.json")

    x = XDL(xdl_file, platform=ChemputerPlatform)
    x.prepare_for_execution(
        graph_file=graph_file,
        interactive=False,
        equiv_reference="PPh3",
        equiv_amount="2 mol",
    )
    # first three steps are set stir steps
    all_steps = flatten_steps(x.steps)
    mitsunobu_fixture.insert(4, ("Dissolve_Reagents", {"id": "Dissolve_Reagents"}))
    del mitsunobu_fixture[-2]

    for i, (step_name, _props) in enumerate(mitsunobu_fixture):
        step = all_steps[i]

        assert step.name == step_name
        assert type(step.context) == Context

        ref_reagent = step.context._reference_reagent.name

        if isinstance(step.context.xdl(), Blueprint):
            assert ref_reagent == "Z-Hyp-OH"
        else:
            assert ref_reagent == "PPh3"

    check_props(steps=all_steps, prop_list=mitsunobu_fixture)


TESTS = [
    ("async_inside_blueprint.xdl", False),  # 1
    ("blueprint_inside_async.xdl", False),  # 2
    ("add_async_blueprint.xdl", False),  # 3
    ("repeat_inside_blueprint.xdl", False),  # 4
    ("blueprint_inside_repeat.xdl", False),  # 5
    ("blueprint_inside_repeat_GV_hardware.xdl", False),  # 6
    ("blueprint_inside_repeat_GV.xdl", True),  # 7
]


@pytest.mark.chemputer
@pytest.mark.parametrize(
    argnames="xdl_file,do_extended_test",
    argvalues=TESTS,
    ids=[item[0] for item in TESTS],
)
def test_blueprint_substeps(xdl_file, do_extended_test):
    """
    Checks that steps containing substeps within blueprints are resolved
    correctly.

    Checks that equivalence references are passed down from parent steps.

    From XDL1.5 onwards, Context is no longer copied down the step tree.
    A recursive look-up mechanism for any unresolved properties is used:
    if the step can't resolve a property within it's own Context, it will look
    in the parent context, and so on.

    test files:

        1. Async step inside a blueprint - async_inside_blueprint.xdl.
            - Async child (Add) uses equivalents reference as a unit.
            - Requires equivalence reference from blueprint to be passed down
                to Async and then Add.
            - Requires Add to access reagent properties from XDL (working
                context inheritance tree).

        2. Blueprint inside an Async step - blueprint_inside_async.xdl.
            - same requirements as above from the inner Add step, but this time
                the blueprint is inside Async instead of Async inside BP.

        3. Async step inside a blueprint. Async step contains a solid addition.
            - add_async_blueprint.xdl.
            - Requires Add step to have access to reagent properties from XDL
                (working context inheritance tree).

        4. Repeat step inside a blueprint - repeat_inside_blueprint.xdl.
            - same requirements as 1.

        5. Blueprint inside a Repeat step - blueprint_inside_repeat.xdl.
            - same requirements as 2.

        6. Blueprint inside a Repeat step with loop variable for hardware
            - blueprint_inside_repeat_GV_hardware.xdl.
            - Iterates over hardware and reagents and sets that same reagent
                as the equivalent reference for the blueprint.

        7. Blueprint inside a Repeat step with loop variable for reagent
            - blueprint_inside_repeat_GV.xdl.
            - Iterates over reagents and sets that same reagent as the
                equivalence reference for the blueprint.
    """
    graph_file = os.path.join(FILES, "bp_substep_graph.json")

    tracer = []

    xdl_file = os.path.join(FILES, xdl_file)
    generic_chempiler_test(xdl_file, graph_file, tracer)

    if do_extended_test:
        x = XDL(xdl_file, platform=ChemputerPlatform)
        x.prepare_for_execution(
            graph_file=graph_file,
            interactive=False,
        )

        # test loop variable equiv references are correct
        equiv_references = ["reagent_2", "reagent_3"]
        add_steps = [s for s in flatten_steps(x.steps) if s.name == "Add"]

        for idx, equiv_ref in enumerate(equiv_references):
            add_step = add_steps[idx]

            # loop variables should replace equiv reference and step properties
            assert add_step.reagent == equiv_ref
            assert add_step.context.equiv_reference == equiv_ref
            assert add_step.context.equiv_amount == "10 mmol"


@pytest.mark.chemputer
def test_blueprint_hardware_mapping_error():
    """
    Checks that error is raised if hardware is not mapped
    / defined when blueprint step is used.

    Also checks that default reagents can be defined if they are in the
    XDL synthesis section.
    """
    xdl_file = os.path.join(FILES, "blueprint_no_hardware_mapping.xdl")
    graph_file = os.path.join(FILES, "hardware_mapping.json")

    with pytest.raises(XDLVesselNotDeclaredError):
        generic_chempiler_test(xdl_file, graph_file)
