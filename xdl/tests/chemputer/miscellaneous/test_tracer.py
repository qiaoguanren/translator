import os

import ChemputerAPI
import pytest
from chempiler.chempiler import Chempiler
from chemputerxdl.platform import ChemputerPlatform

from xdl import XDL
from xdl.errors import XDLTracerError
from xdl.utils.tracer import tracer_tester

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "..", "files")

###############################
# Test Lists that should pass #
###############################

# Empty list should be true
test_list_true_1 = []

# No dict or empty dict both count as "just the step"
test_list_true_2 = [
    ("Wait", {}),
    ("Wait"),
    ("Add", {}),
    ("Wait"),
    ("Wait", {}),
    ("Add"),
    ("Repeat"),
]

# testing with standard units
test_list_true_3 = [
    ("Wait", {"time": "5 secs"}),
    ("Wait", {"time": "10 secs"}),
    ("Add", {"vessel": "filter", "reagent": "ether", "volume": "20 mL"}),
    ("Wait", {"time": "5 secs"}),
    ("Wait", {"time": "10 secs"}),
    ("Add", {"vessel": "filter", "reagent": "ether", "volume": "20 mL"}),
    ("Repeat", {"repeats": "2"}),
]

# testing without units
test_list_true_4 = [
    ("Wait", {"time": "5"}),
    ("Wait", {"time": "10"}),
    ("Add", {"vessel": "filter", "reagent": "ether", "volume": "20"}),
    ("Wait", {"time": "5"}),
    ("Wait", {"time": "10"}),
    ("Add", {"vessel": "filter", "reagent": "ether", "volume": "20"}),
    ("Repeat", {"repeats": "2"}),
]

# testing with non-standard units
test_list_true_5 = [
    ("Wait", {"time": "5 s"}),
    ("Wait", {"time": "10 sec"}),
    ("Add", {"vessel": "filter", "reagent": "ether", "volume": "0.02 L"}),
    ("Wait", {"time": "5 second"}),
    ("Wait", {"time": "10 seconds"}),
    ("Add", {"vessel": "filter", "reagent": "ether", "volume": "20000 uL"}),
    ("Repeat", {"repeats": "2"}),
]

###############################
# Test Lists that should fail #
###############################

# Steps are case-sensitive
test_list_false_1 = [
    ("repeat", {"repeats": "2"}),
]

# wrong value
test_list_false_2 = [
    ("repeat", {"repeats": "3"}),
]

# non-existent property
test_list_false_3 = [
    ("repeat", {"pressure": "2"}),
]

# Vessels/Reagents are case-sensitive
test_list_false_4 = [
    ("Add", {"vessel": "Filter"}),
]
test_list_false_5 = [
    ("Add", {"reagent": "Ether"}),
]


@pytest.mark.chemputer
@pytest.mark.parametrize(
    argnames="test_list_pass, test_list_fail",
    argvalues=[
        (test_list_true_1, test_list_false_1),
        (test_list_true_2, test_list_false_2),
        (test_list_true_3, test_list_false_3),
        (test_list_true_4, test_list_false_4),
        (test_list_true_5, test_list_false_5),
    ]
)
def test_tracer_attributes(test_list_pass, test_list_fail):
    """Testing getting right steps from the tracer."""
    # Each file has it's own designated step list

    xdl_file = os.path.join(FOLDER, "repeat_parent.xdl")
    xdl_graph = os.path.join(FOLDER, "bigrig.json")

    x = XDL(xdl_file, platform=ChemputerPlatform)
    x.prepare_for_execution(xdl_graph, testing=True)
    tracer = []
    c = Chempiler(
        experiment_code="test",
        output_dir=".",
        graph_file=xdl_graph,
        simulation=True,
        device_modules=[ChemputerAPI],
    )
    x.execute(platform_controller=c, tracer=tracer)

    # remove setstirspeed steps from tracer
    tracer_tester(tracer, test_list_pass)

    with pytest.raises(XDLTracerError):
        tracer_tester(tracer, test_list_fail)


def test_tracer_precision():
    """Testing the precision functionality of the tracer."""
    # Each file has it's own designated step list

    xdl_file = os.path.join(FOLDER, "repeat_parent.xdl")
    xdl_graph = os.path.join(FOLDER, "bigrig.json")

    x = XDL(xdl_file, platform=ChemputerPlatform)
    x.prepare_for_execution(xdl_graph, testing=True)
    tracer = []
    c = Chempiler(
        experiment_code="test",
        output_dir=".",
        graph_file=xdl_graph,
        simulation=True,
        device_modules=[ChemputerAPI],
    )
    x.execute(platform_controller=c, tracer=tracer)

    # testing with the precision argument
    test_list_true_precision = [
        ("Add", {"vessel": "filter", "reagent": "ether", "volume": "0.02001 L"}),
        ("Add", {"vessel": "filter", "reagent": "ether", "volume": "20001 uL"}),
    ]

    # Precision turend off
    test_list_false_precision_a = [
        ("Add", {"vessel": "filter", "reagent": "ether", "volume": "0.02001 L"}),
        ("Add", {"vessel": "filter", "reagent": "ether", "volume": "20001 uL"}),
    ]

    # Precision too low
    test_list_false_precision_b = [
        ("Add", {"vessel": "filter", "reagent": "ether", "volume": "0.021 L"}),
        ("Add", {"vessel": "filter", "reagent": "ether", "volume": "21000 uL"}),
    ]

    tracer_tester(tracer, test_list_true_precision, precision=0.001)

    with pytest.raises(XDLTracerError):
        tracer_tester(tracer, test_list_false_precision_a)
    with pytest.raises(XDLTracerError):
        tracer_tester(tracer, test_list_false_precision_b, precision=0.001)
