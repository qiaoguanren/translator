"""
Tests for resolving XDL XML blueprints in locations other
than the XDL file that invokes them.
"""
#  std
import os

import pytest
from chemputerxdl import ChemputerPlatform

#  relative
from xdl import XDL

from .blueprint_fixtures import check_props, flatten_steps, mitsunobu_props

HERE = os.path.dirname(__file__)
FILES = os.path.join(HERE, "..", "..", "files")


@pytest.fixture
def mitsunobu_fixture():
    return mitsunobu_props()


@pytest.mark.chemputer
def test_blueprint_resolution_same_folder(mitsunobu_fixture):
    """
    Validates that blueprints can be resolved when they are located in a file
    in the same folder as the file that invokes them.

    Uses split_Mitsunobu_blueprint_synthesis_only.xdl, which has only a
    Synthesis section which uses the blueprints:
    'Cyclic_Mitsunobu_Split' and 'Single_Add_Split'.

    These blueprints are present and resolved from
    'split_Mitsunobu_blueprint_bp_only.xdl'

    Args:
        mitsunobu_fixture (List[Tuple[str, Dict[str, Any]]]): list of step name
            tuples and their associated props and values. Spawned from
            'Mitsunobu_blueprint.xdl'
    """
    synthesis_file = os.path.join(
        FILES,
        "test_blueprint_resolution",
        "split_Mitsunobu_blueprint_synthesis_only.xdl",
    )
    graph_file = os.path.join(FILES, "Chemify149_Mitsunobu.json")
    x = XDL(synthesis_file, platform=ChemputerPlatform)

    x.prepare_for_execution(
        graph_file=graph_file,
        interactive=False,
        equiv_reference="PPh3",
        equiv_amount="2 mol",
    )

    mitsunobu_fixture[3] = ("Cyclic_Mitsunobu_Split", {"id": "Cyclic_Mitsunobu_Split"})
    mitsunobu_fixture[-2] = ("Single_Add_Split", {"id": "Single_Add_Split"})
    check_props(steps=flatten_steps(x.steps), prop_list=mitsunobu_fixture)


@pytest.mark.chemputer
def test_blueprint_resolution_working_directory(mitsunobu_fixture):
    """
    Validates that blueprints can be resolved when they are located in a file
    in a different folder as the file that invokes them, provided the
    blueprint-containing folder is passed as 'working_directory' to the
    XDL constructor.

    Uses split_Mitsunobu_blueprint_synthesis_only.xdl, which has only a
    Synthesis section which uses the blueprints:
    'Cyclic_Mitsunobu_Split' and 'Single_Add_Split'.

    These blueprints are present and resolved from
    'split_Mitsunobu_blueprint_bp_only.xdl'.

    Args:
        mitsunobu_fixture (List[Tuple[str, Dict[str, Any]]]): list of step name
            tuples and their associated props and values. Spawned from
            'Mitsunobu_blueprint.xdl'
    """
    synthesis_file = os.path.join(
        FILES,
        "test_blueprint_resolution",
        "working_directory_test",
        "split_Mitsunobu_blueprint_synthesis_only_wd.xdl",
    )
    graph_file = os.path.join(FILES, "Chemify149_Mitsunobu.json")
    x = XDL(
        synthesis_file,
        platform=ChemputerPlatform,
        working_directory=os.path.join(FILES, "test_blueprint_resolution"),
    )

    x.prepare_for_execution(
        graph_file=graph_file,
        interactive=False,
        equiv_reference="PPh3",
        equiv_amount="2 mol",
    )
    mitsunobu_fixture[3] = ("Cyclic_Mitsunobu_Split", {"id": "Cyclic_Mitsunobu_Split"})
    mitsunobu_fixture[-2] = ("Single_Add_Split", {"id": "Single_Add_Split"})
    check_props(steps=flatten_steps(x.steps), prop_list=mitsunobu_fixture)


@pytest.mark.chemputer
def test_recursive_blueprint_resolution_same_folder(mitsunobu_fixture):
    """
    Validates that blueprints containing blueprint substeps can be resolved when
    they are located in a file in the same folder as the file that invokes them.

    Uses split_Mitsunobu_blueprint_synthesis_only.xdl, which has only a
    Synthesis section which uses the blueprint
    'Cyclic_Mitsunobu_Split' which uses the bp 'Single_Add_Split' as a step.

    These blueprints are present and resolved from
    'split_Mitsunobu_blueprint_bp_only.xdl'

    Args:
        mitsunobu_fixture (List[Tuple[str, Dict[str, Any]]]): list of step name
            tuples and their associated props and values. Spawned from
            'Mitsunobu_blueprint.xdl'
    """
    synthesis_file = os.path.join(
        FILES,
        "test_blueprint_resolution",
        "split_Mitsunobu_recursive_blueprint_synthesis_only.xdl",
    )
    graph_file = os.path.join(FILES, "Chemify149_Mitsunobu.json")
    x = XDL(synthesis_file, platform=ChemputerPlatform)

    x.prepare_for_execution(
        graph_file=graph_file,
        interactive=False,
        equiv_reference="PPh3",
        equiv_amount="2 mol",
    )
    mitsunobu_fixture[3] = (
        "Cyclic_Mitsunobu_Recursive_Split",
        {"id": "Cyclic_Mitsunobu_Recursive_Split"},
    )
    mitsunobu_fixture.insert(
        4,
        (
            "Dissolve_Reagents_Recursive_Split",
            {"id": "Dissolve_Reagents_Recursive_Split"},
        ),
    )
    del mitsunobu_fixture[-2]

    check_props(steps=flatten_steps(x.steps), prop_list=mitsunobu_fixture)


@pytest.mark.chemputer
def test_recursive_blueprint_resolution_working_directory(mitsunobu_fixture):
    """
    Validates that blueprints containing blueprint substeps can be resolved
    when they are located in a file in a different folder as the file that
    invokes them, provided the blueprint-containing folder is passed as
    'working_directory' to the XDL constructor.

    Uses split_Mitsunobu_blueprint_synthesis_only_wd.xdl, which has only a
    Synthesis section which uses the blueprint
    'Cyclic_Mitsunobu_Split' which uses the bp 'Single_Add_Split' as a step.

    These blueprints are present and resolved from
    'split_Mitsunobu_blueprint_bp_only.xdl'

    Args:
        mitsunobu_fixture (List[Tuple[str, Dict[str, Any]]]): list of step name
            tuples and their associated props and values. Spawned from
            'Mitsunobu_blueprint.xdl'
    """
    synthesis_file = os.path.join(
        FILES,
        "test_blueprint_resolution",
        "working_directory_test",
        "split_Mitsunobu_recursive_blueprint_synthesis_only_wd.xdl",
    )
    graph_file = os.path.join(FILES, "Chemify149_Mitsunobu.json")
    x = XDL(
        synthesis_file,
        platform=ChemputerPlatform,
        working_directory=os.path.join(FILES, "test_blueprint_resolution"),
    )

    x.prepare_for_execution(
        graph_file=graph_file,
        interactive=False,
        equiv_reference="PPh3",
        equiv_amount="2 mol",
    )
    mitsunobu_fixture[3] = (
        "Cyclic_Mitsunobu_Recursive_Split",
        {"id": "Cyclic_Mitsunobu_Recursive_Split"},
    )
    mitsunobu_fixture.insert(
        4,
        (
            "Dissolve_Reagents_Recursive_Split",
            {"id": "Dissolve_Reagents_Recursive_Split"},
        ),
    )
    del mitsunobu_fixture[-2]

    check_props(steps=flatten_steps(x.steps), prop_list=mitsunobu_fixture)
