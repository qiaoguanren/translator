#  std
import os

import ChemputerAPI
import pytest
from chempiler import Chempiler

from tests.utils import remove_confirm_steps

#  relative
from xdl import XDL
from xdl.errors import XDLError

try:
    from chemputerxdl import ChemputerPlatform
except ModuleNotFoundError:
    pass

HERE = os.path.dirname(__file__)
FILES = os.path.join(HERE, "..", "..", "files")


@pytest.mark.chemputer
def test_blueprint_default_reagents():
    """
    - Tests blueprint default reagents are set correctly and used.
    - Tests that a combination of default reagents and mapped reagents
        is valid.
    - Reagent properties for resolving equivalent amount in blueprint steps
        should come from blueprint Reagent default.
    """
    xdl_file = os.path.join(FILES, "default_bp_reagents.xdl")
    graph_file = os.path.join(FILES, "Chemify149_Mitsunobu.json")

    x = XDL(xdl_file, platform=ChemputerPlatform)
    x.prepare_for_execution(
        graph_file=graph_file,
        interactive=False,
        equiv_reference="PPh3",
        equiv_amount="2 mol",
    )

    x.steps = [remove_confirm_steps(step) for step in x.steps]

    c = Chempiler(
        experiment_code="test",
        output_dir="out",
        graph_file=graph_file,
        simulation=True,
        device_modules=[ChemputerAPI],
    )

    x.execute(c)

    mitsunobu_step = x.steps[3]
    mitsunobu_reagents = {r.name: r for r in mitsunobu_step.reagents}

    default_reagent = {
        "name": "THF",
        "molecular_weight": "72.11 g/mol",
        "density": "0.889 g/mL",
        "role": "solvent",
    }

    # check default blueprint reagent THF has been parsed and is present in
    # mapped reagents
    assert "THF" in mitsunobu_reagents

    for prop, value in default_reagent.items():

        val = value.split(" ")[0]
        assert str(mitsunobu_reagents["THF"].properties[prop]) == val

    # check that step using equivalence reference is correct
    third_add = mitsunobu_step.steps[2]
    assert third_add.context.equiv_reference == "THF"
    assert third_add.context.equiv_amount == "1 mL"
    assert round(third_add.volume, 2) == 12.94
    assert round(third_add.context._equiv_moles, 4) == 0.0123

    fourth_add = mitsunobu_step.steps[3]
    assert fourth_add.context.equiv_reference == "THF"
    assert fourth_add.context.equiv_amount == "1 mL"
    assert round(fourth_add.volume, 2) == 10.00
    assert round(fourth_add.context._equiv_moles, 4) == 0.0123


@pytest.mark.chemputer
def test_blueprint_default_insufficient_props():
    """
    - Tests that an error is raise when blueprint default reagent has
        insufficient props for use (e.g. no molecular weight or density for
        equivalence calculations), even if a Reagent with the same name and
        correct properties is in the Synthesis section.
    """
    xdl_file = os.path.join(FILES, "default_bp_reagents_insufficient_props.xdl")
    graph_file = os.path.join(FILES, "Chemify149_Mitsunobu.json")

    x = XDL(xdl_file, platform=ChemputerPlatform)

    with pytest.raises(XDLError):
        x.prepare_for_execution(
            graph_file=graph_file,
            interactive=False,
            equiv_reference="PPh3",
            equiv_amount="2 mol",
        )


@pytest.mark.chemputer
def test_blueprint_overwrite_default_reagents():
    """
    - Tests that blueprint default reagents are overwritten by explicit
        mapping of reagents during blueprint using default reagent ids.
    - Reagent properties for resolving equivalent amount in blueprint steps
        should come from mapped Reagent.
    """
    xdl_file = os.path.join(FILES, "overwrite_default_bp_reagents.xdl")
    graph_file = os.path.join(FILES, "Chemify149_Mitsunobu.json")

    x = XDL(xdl_file, platform=ChemputerPlatform)
    x.prepare_for_execution(
        graph_file=graph_file,
        interactive=False,
        equiv_reference="PPh3",
        equiv_amount="2 mol",
    )

    x.steps = [remove_confirm_steps(step) for step in x.steps]

    c = Chempiler(
        experiment_code="test",
        output_dir="out",
        graph_file=graph_file,
        simulation=True,
        device_modules=[ChemputerAPI],
    )

    x.execute(c)

    # test first use of blueprint with default overwritten
    test_add = x.steps[3].steps[2]
    blueprint_context = test_add.context.parent_context

    # check default blueprint reagent THF has been parsed
    assert blueprint_context.reagents[0].id == "THF"

    # check that default has been overwritten in blueprint reagents
    mapped_THF_props = blueprint_context.reagents[0].properties
    assert mapped_THF_props["role"] == "substrate"
    assert mapped_THF_props["molecular_weight"] == 216.33
    assert mapped_THF_props["density"] == 1.778

    # check that step using equivalence reference is correct
    assert test_add.context.equiv_reference == "THF"
    assert test_add.context.equiv_amount == "1 mL"

    ref_reag = test_add.context._reference_reagent
    assert ref_reag.properties["role"] == "substrate"
    assert ref_reag.properties["molecular_weight"] == 216.33
    assert ref_reag.properties["density"] == 1.778
    assert round(test_add.context._equiv_moles, 4) == 0.0082
    assert round(test_add.volume, 2) == 8.63


@pytest.mark.chemputer
def test_blueprint_overwrite_default_reagents_diff_reagent():
    """
    - Tests that blueprint default reagents are overwritten by explicit
        mapping of reagents using default reagent ids during blueprint when the
        mapped reagent name is different to the default name (Methanol).
    - There's a reagent in the synthesis section that has the same name (THF)
        as the default reagent. This is used as the precipitate solvent in
        the Grignard blueprint.
    """
    xdl_file = os.path.join(FILES, "overwrite_default_bp_reagents_diff_reagent.xdl")
    graph_file = os.path.join(FILES, "Chemify149_Mitsunobu.json")

    x = XDL(xdl_file, platform=ChemputerPlatform)
    x.prepare_for_execution(
        graph_file=graph_file,
        interactive=False,
        equiv_reference="PPh3",
        equiv_amount="2 mol",
    )

    x.steps = [remove_confirm_steps(step) for step in x.steps]

    c = Chempiler(
        experiment_code="test",
        output_dir="out",
        graph_file=graph_file,
        simulation=True,
        device_modules=[ChemputerAPI],
    )

    x.execute(c)

    test_dissolves = x.steps[3].steps[3:5]
    blueprint_context = test_dissolves[0].context.parent_context

    # check that precipitate solvent is mapped to Synthesis section THF
    mapped_THF_props = [r for r in blueprint_context.reagents if r.name == "THF"][
        0
    ].properties
    assert mapped_THF_props["id"] == "THF"
    assert mapped_THF_props["role"] == "substrate"
    assert mapped_THF_props["molecular_weight"] == 216.33
    assert mapped_THF_props["density"] == 1.778

    # check that step using methanol and steps using THF (precipitate_solvent)
    # are correct
    for dissolve_step in test_dissolves:
        assert dissolve_step.solvent == "methanol"

    assert x.steps[3].steps[7].solvent == "methanol"
    assert x.steps[3].steps[8].solvent == "THF"
    assert x.steps[3].steps[11].solvent == "THF"


@pytest.mark.chemputer
def test_blueprint_use_default_reagents_twice():
    """
    Tests using the same blueprint with defaults twice: the first time with
        defaults overwritten, the second time just using the default.
    """
    xdl_file = os.path.join(FILES, "use_default_bp_reagents_twice.xdl")
    graph_file = os.path.join(FILES, "Chemify149_Mitsunobu.json")

    x = XDL(xdl_file, platform=ChemputerPlatform)
    x.prepare_for_execution(
        graph_file=graph_file,
        interactive=False,
        equiv_reference="PPh3",
        equiv_amount="2 mol",
    )

    x.steps = [remove_confirm_steps(step) for step in x.steps]

    c = Chempiler(
        experiment_code="test",
        output_dir="out",
        graph_file=graph_file,
        simulation=True,
        device_modules=[ChemputerAPI],
    )

    x.execute(c)

    # check that step using equivalence reference is correct when mapped
    # reagent is used
    test_add = x.steps[3].steps[2]
    assert test_add.context.equiv_reference == "THF"
    assert test_add.context.equiv_amount == "1 mL"

    ref_reag = test_add.context._reference_reagent
    assert ref_reag.properties["role"] == "substrate"
    assert ref_reag.properties["molecular_weight"] == 216.33
    assert ref_reag.properties["density"] == 1.778
    assert round(test_add.context._equiv_moles, 4) == 0.0082
    assert round(test_add.volume, 2) == 8.63

    # check that step using equivalence reference is correct when default
    # reagent is used (different reagent properties)
    test_add = x.steps[9].steps[2]
    assert test_add.context.equiv_reference == "THF"
    assert test_add.context.equiv_amount == "1 mL"

    ref_reag = test_add.context._reference_reagent
    assert ref_reag.properties["role"] == "solvent"
    assert ref_reag.properties["molecular_weight"] == 72.11
    assert ref_reag.properties["density"] == 0.889
    assert round(test_add.context._equiv_moles, 4) == 0.0123
    assert round(test_add.volume, 2) == 12.94


@pytest.mark.chemputer
def test_blueprint_use_default_reagents_nested():
    """Testing all four ways of nested blueprints overwriting as follows:
    The XDL files have 3 Procedures: The main Procedure, the outer Mitsunobu
    blueprint and the inner Mitsunobu blueprint. Main calls outer, outer calls
    inner. In each of these calls, overwriting can either happen, or not.
    That leads to four scenarios, and we will use the following four reagents
    from the original Mitsunobu blueprint:
                                            Main overrides Outer
                                                     |  Outer overrides Inner
                                                     |           |
    reagent:Z-Hyp-OH                                True        True
    Phosphine:PPh3                                  True        False
    reaction_solvent:THF                            False       True
    precipitate_solvent:diethyl_ether               False       False

    Main overrides Outer:
        True:
            Reagent in Main has name = reagent_name
            call has name_outer = reagent_name
        False:
            Reagent does not appear in Main
            call omits variable
    Outer overrides Inner:
        True:
            Reagent in Outer has name = name_outer
            call has name_inner = name_outer
        False:
            Reagent in Outer has id = name_outer
            call omits variable

    """
    xdl_file = os.path.join(FILES, "overwrite_default_bp_reagents_nested.xdl")
    graph_file = os.path.join(FILES, "Chemify149_Mitsunobu_nested_bp.json")
    x = XDL(xdl_file, platform=ChemputerPlatform)

    x.prepare_for_execution(
        graph_file=graph_file,
        interactive=False,
        equiv_reference="Z-Hyp-OH",
        equiv_amount="2 mol",
    )

    x.steps = [remove_confirm_steps(step) for step in x.steps]

    c = Chempiler(
        experiment_code="test",
        output_dir="out",
        graph_file=graph_file,
        simulation=True,
        device_modules=[ChemputerAPI],
    )
    tracer = []
    x.execute(c, tracer=tracer)

    added_reagents_list = [
        tracestep[1]["reagent"]
        for tracestep in tracer
        if tracestep[0].__name__ == "Add"
    ]

    expected_list = [
        "Z-Hyp-OH",  # Main overrides outer overrides inner: No index
        "THF_o",  # Outer overrides inner:                index 'o'
        "diethyl_ether_i",  # Nothing overwritten, take inner:      index 'i'
        "PPh3_i",  # Main overrides outer, but not inner:  index 'i'
    ]

    forbidden_list = [
        "Z-Hyp-OH_o",  # Overwritten by Main
        "Z-Hyp-OH_i",  # Overwritten by Main
        "THF",  # Doesn't exist
        "THF_i",  # Overwritten by Outer
        "diethyl_ether",  # Doesn't exist
        "diethyl_ether_o",  # Doesn't exist
        "PPh3_o",  # Doesn't exist
        "PPh3",  # Overwrites what doesn't exist and is ignored
    ]

    for good_reagent in expected_list:
        assert good_reagent in added_reagents_list
    for bad_reagent in forbidden_list:
        assert bad_reagent not in added_reagents_list
