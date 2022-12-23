# This file serves to test mupliple interactions of the three different
# functionalities of the Repeat step. We will denote them in this file,
# for brevity, as the Loop, Measure, and Variable functionality, and abbreviate
# them L M V, which puts them both in alphabetical order and in chronological
# order of implementation: The original functionality that repeated the number
# of 'repeats' is "Loop". The dynamic functionality that requires a sensor
# feedback is "Measure", and the one iterating over a set of loop variables
# is "Variable". We begin by testing pairwise, and triple nestings of those.
# A constellation denoted LM descibes an outer L-Repeat and an inner M-Repeat.

import os

import ChemputerAPI
import pytest
from chempiler.chempiler import Chempiler
from chemputerxdl.platform import ChemputerPlatform

from tests.utils import generic_chempiler_test
from xdl import XDL
from xdl.errors import XDLAttrDuplicateID, XDLSanityCheckError
from xdl.utils.tracer import tracer_tester

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "..", "files/repeat_iteration_files")


@pytest.mark.chemputer
def test_iterative_repeat_solvents_basic():
    """Test Repeat will iterate through available solvents for second Add"""

    xdl_f = os.path.join(FOLDER, "iterative_repeat_solvents_basic.xdl")
    graph_f = os.path.join(FOLDER, "Mitsunobu_graph.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, testing=True, interactive=False)

    generic_chempiler_test(xdl_f, graph_f)


@pytest.mark.chemputer
def test_iterative_repeat_solvents_basic_duplicate_ID():
    """Test error will be raised if loop variable is the same as a Parameter,
    Hardware or Component ID.
    """
    xdl_files = [
        "iterative_repeat_solvents_basic_duplicate_param_ID.xdl",
        "iterative_repeat_solvents_basic_duplicate_hardware_ID.xdl",
        "iterative_repeat_solvents_basic_duplicate_reagent_ID.xdl",
    ]

    for f in xdl_files:
        xdl_f = os.path.join(FOLDER, f)
        graph_f = os.path.join(FOLDER, "Mitsunobu_graph.json")
        with pytest.raises(XDLAttrDuplicateID):
            generic_chempiler_test(xdl_f, graph_f)


FILE_NAMES_REPEAT_VARIABLES = [
    "repeat_variables_53_ex1.xdl",
    "repeat_variables_53_ex2.xdl",
    "repeat_variables_53_ex3.xdl",
    "repeat_variables_53_ex4.xdl",
    "repeat_variables_53_ex5.xdl",
]

STEP_LISTS_REPEAT_VARIABLES = [
    [("Add", {"reagent": "water"}), ("Add", {"reagent": "ether"})],
    [
        ("Add", {"vessel": "buffer_flask", "reagent": "ether"}),
        ("Add", {"vessel": "buffer_flask2", "reagent": "water"}),
    ],
    [
        ("Add", {"vessel": "buffer_flask", "reagent": "ether"}),
        ("Add", {"vessel": "buffer_flask2", "reagent": "ether"}),
        ("Add", {"vessel": "buffer_flask", "reagent": "water"}),
        ("Add", {"vessel": "buffer_flask2", "reagent": "water"}),
    ],
    [
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
    ],
    [
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
    ],
]


@pytest.mark.chemputer
@pytest.mark.parametrize(
    argnames="test_case",
    argvalues=zip(
        FILE_NAMES_REPEAT_VARIABLES,
        STEP_LISTS_REPEAT_VARIABLES,
    ),
    ids=FILE_NAMES_REPEAT_VARIABLES,
)
def test_iterative_repeat_advanced(test_case):
    """Testing getting right steps from the tracer."""
    # Each file has it's own designated step list
    examplefile, test_list = test_case

    xdl_file = os.path.join(FOLDER, examplefile)
    xdl_graph = os.path.join(FOLDER, "bigrig.json")

    x = XDL(xdl_file, platform=ChemputerPlatform)
    x.prepare_for_execution(xdl_graph, testing=True)
    c = Chempiler(
        experiment_code="test",
        output_dir=".",
        graph_file=xdl_graph,
        simulation=True,
        device_modules=[ChemputerAPI],
    )
    x.execute(platform_controller=c)
    tracer = x.tracer

    tracer_tester(tracer, test_list)


FILE_NAMES_REPEAT_VARIABLES_ALL_MATCHES = [
    # matches all reagents
    "repeat_variables_53_ex1_all_reagents.xdl",
    # matches all reagents and all components zipped
    "repeat_variables_53_ex2_all_reagents_all_hardware.xdl",
    # adds all reagents into all components
    "repeat_variables_53_ex3_all_reagent_hardware_combos.xdl",
    # adds all reagents twice
    "repeat_variables_53_ex4_all_reagents_twice.xdl",
    # adds all reagents twice, 3 times (6 times total)
    "repeat_variables_53_ex5_all_reagents_twice_thrice.xdl",
]


@pytest.mark.chemputer
@pytest.mark.parametrize(
    argnames="test_case",
    argvalues=zip(
        FILE_NAMES_REPEAT_VARIABLES_ALL_MATCHES,
        STEP_LISTS_REPEAT_VARIABLES,
    ),
    ids=FILE_NAMES_REPEAT_VARIABLES_ALL_MATCHES,
)
def test_iterative_repeat_match_all_hardware_and_reagents(test_case):
    """
    Test that providing a loop variable of 'Hardware' or 'Reagents'
    within Repeat step will repeat the procedure in all Components or for all
    Reagents within XDL file.
    """
    examplefile, test_list = test_case

    xdl_file = os.path.join(FOLDER, examplefile)
    xdl_graph = os.path.join(FOLDER, "bigrig.json")

    x = XDL(xdl_file, platform=ChemputerPlatform)
    x.prepare_for_execution(xdl_graph, testing=True)
    c = Chempiler(
        experiment_code="test",
        output_dir=".",
        graph_file=xdl_graph,
        simulation=True,
        device_modules=[ChemputerAPI],
    )
    x.execute(platform_controller=c)
    tracer = x.tracer

    tracer_tester(tracer, test_list)


FILE_NAMES_PAIRS = [
    "repeat_pairs_LM.xdl",
    "repeat_pairs_ML.xdl",
    "repeat_pairs_MV.xdl",
    "repeat_pairs_VM.xdl",
    "repeat_pairs_VL.xdl",
    "repeat_pairs_LV.xdl",
]

STEP_LISTS_PAIRS = [
    [  # LM
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "water"}),
    ],
    [  # ML
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "water"}),
    ],
    [  # MV
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
    ],
    [  # VM
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
    ],
    [  # VL
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
    ],
    [  # LV
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
    ],
]


@pytest.mark.chemputer
@pytest.mark.parametrize(
    argnames="test_case",
    argvalues=zip(
        FILE_NAMES_PAIRS,
        STEP_LISTS_PAIRS,
    ),
    ids=FILE_NAMES_PAIRS,
)
def test_iterative_repeat_pairs(test_case):
    """Testing the following combinations in order: LM ML MV VM VL LV,
    where the first (outer) Repeat has 3 iterations, and the inner has 2"""
    examplefile, test_list = test_case

    xdl_file = os.path.join(FOLDER, examplefile)
    xdl_graph = os.path.join(FOLDER, "biggerrig.json")

    x = XDL(xdl_file, platform=ChemputerPlatform)
    x.prepare_for_execution(xdl_graph, testing=True)
    c = Chempiler(
        experiment_code="test",
        output_dir=".",
        graph_file=xdl_graph,
        simulation=True,
        device_modules=[ChemputerAPI],
    )
    x.execute(platform_controller=c)
    tracer = x.tracer
    tracer_tester(tracer, test_list)


FILE_NAMES_TRIPLES = [
    "repeat_triples_LVM.xdl",
    "repeat_triples_LMV.xdl",
    "repeat_triples_MLV.xdl",
    "repeat_triples_MVL.xdl",
    "repeat_triples_VLM.xdl",
    "repeat_triples_VML.xdl",
]

STEP_LISTS_TRIPLES = [
    [  # LVM
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
    ],
    [  # LMV
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
    ],
    [  # MLV
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
    ],
    [  # MVL
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
    ],
    [  # VLM
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "chloroacetyl chloride"}),
        ("Add", {"reagent": "chloroacetyl chloride"}),
        ("Add", {"reagent": "chloroacetyl chloride"}),
        ("Add", {"reagent": "chloroacetyl chloride"}),
        ("Add", {"reagent": "chloroacetyl chloride"}),
        ("Add", {"reagent": "chloroacetyl chloride"}),
    ],
    [  # VML
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "water"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "ether"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "THF"}),
        ("Add", {"reagent": "chloroacetyl chloride"}),
        ("Add", {"reagent": "chloroacetyl chloride"}),
        ("Add", {"reagent": "chloroacetyl chloride"}),
        ("Add", {"reagent": "chloroacetyl chloride"}),
        ("Add", {"reagent": "chloroacetyl chloride"}),
        ("Add", {"reagent": "chloroacetyl chloride"}),
    ],
]


@pytest.mark.chemputer
@pytest.mark.parametrize(
    argnames="test_case",
    argvalues=zip(
        FILE_NAMES_TRIPLES,
        STEP_LISTS_TRIPLES,
    ),
    ids=FILE_NAMES_TRIPLES,
)
def test_iterative_repeat_triples(test_case):
    """Testing the following combinations in order: LMV LVM MLV MVL VLM VML,
    where the first (outer) Repeat has 4 iterations, the middle one  3
    and the inner has 2"""
    examplefile, test_list = test_case

    xdl_file = os.path.join(FOLDER, examplefile)
    xdl_graph = os.path.join(FOLDER, "biggerrig.json")

    x = XDL(xdl_file, platform=ChemputerPlatform)
    x.prepare_for_execution(xdl_graph, testing=True)
    c = Chempiler(
        experiment_code="test",
        output_dir=".",
        graph_file=xdl_graph,
        simulation=True,
        device_modules=[ChemputerAPI],
    )
    x.execute(platform_controller=c)
    tracer = x.tracer
    tracer_tester(tracer, test_list)


XDL_FILES = [
    # Parameter and Reagent duplicated
    "duplicate_ID_reagent_parameter.xdl",
    # Reagent and Hardware duplicated
    "duplicate_ID_reagent_hardware.xdl",
    # Hardware and Parameter duplicated
    "duplicate_ID_hardware_parameter.xdl",
    # Parameter, Hardware and Reagent duplicated
    "duplicate_ID_hardware_parameter_reagent.xdl",
    # Parameter and Reagent duplicated in BP
    "duplicate_ID_reagent_parameter_BP.xdl",
    # Reagent and Hardware duplicated in BP
    "duplicate_ID_reagent_hardware_BP.xdl",
    # Hardware and Parameter duplicated in BP
    "duplicate_ID_parameter_hardware_BP.xdl",
    # Parameter, Hardware and Reagent duplicated in BP
    "duplicate_ID_parameter_hardware_reagents_BP.xdl",
]


@pytest.mark.unit
@pytest.mark.parametrize(
    argnames="xdl_file",
    argvalues=XDL_FILES,
)
def test_duplicate_ID_error(xdl_file):
    """
    Tests an error is raised when IDs of Parameters, Reagents and
    Hardware are not unique.
    """
    xdl_file = os.path.join(FOLDER, xdl_file)
    with pytest.raises(XDLAttrDuplicateID):
        XDL(xdl_file, platform=ChemputerPlatform)


TEST_FILE_DIR = os.path.join(FOLDER, "ECK_repeat_iteration_hardware_test_files")
SECTIONS = ["Synthesis section tests", "BP tests", "Nested BP tests"]
TEST_CASES = []
for section in SECTIONS:
    section_folder = os.path.join(TEST_FILE_DIR, section)
    xdl_files = [f for f in os.listdir(section_folder) if f.endswith(".xdl")]
    for xdl_file in xdl_files:
        TEST_CASES.append([section, xdl_file])


@pytest.mark.chemputer
@pytest.mark.parametrize(
    argnames="test_case", argvalues=TEST_CASES, ids=[item[0] for item in TEST_CASES]
)
def test_iterative_repeat_blueprints(test_case):
    """Tests the following scenarios:

    1. one loop variable in one Repeat child step
    2. two loop variables in the same Repeat child step
    3. multiple loop variables across multiple child steps (nested repeats)
    4. all Reagents as loop variables
    5. all Hardware as loop variables
    6. all Hardware and all Reagents as loop variables (nested)
    7. use of parameter and loop variable in the same step

    within the Synthesis section, inside Blueprints and inside nested Blueprints
    """
    section, xdl_file = test_case
    section_folder = os.path.join(TEST_FILE_DIR, section)
    graph_f = os.path.join(TEST_FILE_DIR, "miniputer.json")

    generic_chempiler_test(
        xdl_file=os.path.join(section_folder, xdl_file), graph_file=graph_f
    )


@pytest.mark.chemputer
def test_loop_variable_step_replacement():
    """
    Tests that all substeps variables are replaced when a loop variable is
    used. Example step is Dissolve as it expands to have a decent number of
    substeps.

    Both vessel and solvent are loop variables in the test files
    (2 loop variables in one step).
    Loop variables should match reactor with reagent 15 and UVVis with
    solvent.
    """

    test_files = os.path.join(FOLDER, "ECK_repeat_iteration_hardware_test_files")

    graph_f = os.path.join(test_files, "miniputer.json")

    xdl_files = [
        "two_GV_substeps_synthesis.xdl",
        "two_GV_substeps_BP.xdl",
        "two_GV_substeps_nested_BP.xdl",
    ]

    for xdl_f in xdl_files:

        xdl_file = os.path.join(test_files, xdl_f)

        generic_chempiler_test(xdl_file=xdl_file, graph_file=graph_f)

        x = XDL(xdl_file, platform=ChemputerPlatform)
        x.prepare_for_execution(graph_f, testing=True)
        c = Chempiler(
            experiment_code="test",
            output_dir=".",
            graph_file=graph_f,
            simulation=True,
            device_modules=[ChemputerAPI],
        )
        x.execute(platform_controller=c)
        tracer = x.tracer

        dissolve_starts = [
            i for i, s in enumerate(tracer) if s[0].__name__ == "Dissolve"
        ]

        # tracer now records step properties once it's finished executing
        # so dissolve step will be last to be recorded amongst all it's substeps
        dissolve_1 = tracer[0 : dissolve_starts[0] + 1]

        # make sure prepare for execution worked and Dissolve was expanded
        # out into substeps
        # different files have different number of steps but they should always
        # be above 23 (the number of steps for two_GV_substeps_synthesis.xdl)
        assert len(dissolve_1) >= 23

        # check all appropriate properties have correct value from general
        # variables
        for step in dissolve_1:

            # stirring controllers are set for all reactors at the same time
            if "stir" not in step[0].__name__.lower():
                properties = step[1]
                for prop, val in properties.items():

                    try:
                        if prop in ["vessel", "to_vessel"]:
                            assert val in ["reactor", "waste1", "rctdigital"]
                        if prop in ["reagent", "reagent_vessel", "from_vessel"]:
                            assert val == "reagent_15"
                    except AssertionError:
                        pass

        # same checks as above but also checks that all substep properites
        # have been replace with second set of loop variables
        # ie step was prepared for execution again with new set of GVs
        dissolve_2 = tracer[dissolve_starts[0] + 1 :]
        assert len(dissolve_2) >= 22

        for step in dissolve_2:

            # stirring controllers are set for all reactors at the same time
            if "stir" not in step[0].__name__.lower():
                properties = step[1]
                for prop, val in properties.items():
                    if prop in ["vessel", "to_vessel"]:
                        assert val in ["UVVis", "waste2", "rctdigital"]
                    if prop in ["reagent", "reagent_vessel", "from_vessel"]:
                        assert val == "solvent"


SANITY_CHECK_FILES = [
    "repeat_sanity_LV.xdl",
    "repeat_sanity_MV.xdl",
    "repeat_sanity_ML.xdl",
]


@pytest.mark.chemputer
def test_repeat_sanity_checks():
    """Testing the that the sanity checks catch when multiple functionalities
    of repeat are being used at the same time. Following the notation of the
    pair- and triplet-checks, M V L denote which functionalities are used
    at the same time."""
    for sanity_check_file in SANITY_CHECK_FILES:

        xdl_file = os.path.join(FOLDER, sanity_check_file)
        xdl_graph = os.path.join(FOLDER, "biggerrig.json")

        with pytest.raises(XDLSanityCheckError):
            generic_chempiler_test(xdl_file, xdl_graph)


@pytest.mark.chemputer
def test_blueprint_repeat_scope():
    """
    Checks that iterative Repeat step in blueprint only has access to reagents
    and hardware mapped in blueprint declaration and not XDL object reagents
    and hardware.

    Also checks that loop variables are matched on the original properties
    of the blueprint steps. In this example, the iteration occurs for solvents
    of role "solvent" i.e. reagent reagent_33 within the blueprint.

    reagent_33 is a default blueprint reagent.
    reagent_33 is mapped to solvent (which has role='acid') but the general
    variables should match based on the original properties of reagent_33
    instead.

    It also checks the same mechanism for hardware, where reactor_BP is mapped
    (type = flask) to 'reactor' (type = reactor).
    """
    xdl_file = os.path.join(FOLDER, "two_GV_BP_scope.xdl")
    graph_f = os.path.join(
        FOLDER, "ECK_repeat_iteration_hardware_test_files", "miniputer.json"
    )
    x = XDL(xdl_file, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, testing=True)
    c = Chempiler(
        experiment_code="test",
        output_dir=".",
        graph_file=graph_f,
        simulation=True,
        device_modules=[ChemputerAPI],
    )
    x.execute(platform_controller=c)
    tracer = x.tracer
    dissolve_starts = [i for i, s in enumerate(tracer) if s[0].__name__ == "Dissolve"]
    assert len(dissolve_starts) == 1

    dissolve = tracer[dissolve_starts[0] :]

    # check all appropriate properties have correct value from general
    # variables
    for step in dissolve:
        properties = step[1]
        for prop, val in properties.items():
            if prop in ["vessel", "to_vessel"]:
                assert val in ["reactor", "waste2", "rctdigital"]
            if prop in ["reagent", "reagent_vessel", "from_vessel"]:
                assert val == "solvent"


@pytest.mark.chemputer
def test_blueprint_repeat_PFE_delay():
    """
    Checks that prepare for execution is delayed for steps which use loop
    variables. Including Separate, which also requires extra steps that are
    added during prepare for execution to be delayed: adding implied steps and
    cleaning schedule - both of which use iter_vessel_contents (this function
    requires all properties to be resolved at prepare_for_execution, which is
    not possible when using loop variables).
    """
    xdl_file = os.path.join(FOLDER, "repeat_PFE_delay.xdl")
    graph_f = os.path.join(FOLDER, "MSC_separators.json")
    generic_chempiler_test(xdl_file, graph_f)


MULTIPLE_CLAUSE_FILES = [
    "multiple_loop_variable_syn.xdl",
    "multiple_loop_variable_BP.xdl",
    "multiple_loop_variable_BP_inside_repeat.xdl",
]


@pytest.mark.chemputer
@pytest.mark.parametrize(
    argnames="xdl_f", argvalues=MULTIPLE_CLAUSE_FILES, ids=MULTIPLE_CLAUSE_FILES
)
def test_loop_variable_multiple_clauses(xdl_f):
    """
    Checks that loop variables can be matched by multiple clauses for the
    same loop variable. In this example, the iteration occurs for solvents
    which have BOTH role "substrate" AND solid = "False"
    i.e. reagent_14_BP, reagent_12_BP.
    """
    xdl_file = os.path.join(FOLDER, xdl_f)
    graph_f = os.path.join(
        FOLDER, "ECK_repeat_iteration_hardware_test_files", "miniputer.json"
    )

    add_props = [
        {"vessel": "reactor", "reagent": "reagent_12"},
        {"vessel": "UVVis", "reagent": "reagent_14"},
    ]

    x = XDL(xdl_file, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, testing=True)
    c = Chempiler(
        experiment_code="test",
        output_dir=".",
        graph_file=graph_f,
        simulation=True,
        device_modules=[ChemputerAPI],
    )
    x.execute(platform_controller=c)
    tracer = x.tracer

    adds = [s[1] for s in tracer if s[0].__name__ == "Add"]

    for real_props, desired_props in zip(adds, add_props):
        for prop in desired_props:
            assert desired_props[prop] == real_props[prop]
