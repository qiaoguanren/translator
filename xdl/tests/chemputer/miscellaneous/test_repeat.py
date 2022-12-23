import os

import pytest

from xdl import XDL
from xdl.steps import Repeat

try:
    import ChemputerAPI
    from chempiler import Chempiler
    from chemputerxdl import ChemputerPlatform

    from tests.utils import generic_chempiler_test, remove_confirm_steps

except ModuleNotFoundError:
    pass

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "..", "files")


@pytest.mark.chemputer
def test_repeat():
    """Test Repeat step works correctly.
    Repeat should only expand out steps fully during execution.
    """
    xdl_f = os.path.join(FOLDER, "repeat_parent.xdl")
    graph_f = os.path.join(FOLDER, "bigrig.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, testing=True)
    for step in x.steps:
        if type(step) == Repeat:
            assert len(step.steps) == 3
            assert step.steps[0].time == 5
            assert step.steps[1].time == 10
            assert step.steps[2].volume == 20
    generic_chempiler_test(xdl_f, graph_f)


@pytest.mark.chemputer
def test_repeat_scale_procedure():
    """Test scale_procedure works when wrapped in Repeat step."""
    xdl_f = os.path.join(FOLDER, "repeat_parent.xdl")
    graph_f = os.path.join(FOLDER, "bigrig.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.scale_procedure(0.1)
    x.prepare_for_execution(graph_f, testing=True)

    for step in x.steps:
        if type(step) == Repeat:
            assert len(step.steps) == 3
            assert step.steps[0].time == 5
            assert step.steps[1].time == 10
            assert step.steps[2].volume == 2
    generic_chempiler_test(xdl_f, graph_f)


@pytest.mark.chemputer
def test_repeat_until_DONE_basic():
    """Test DONE functionality with basic repeats"""
    xdl_f = os.path.join(FOLDER, "repeat_until_done_basic.xdl")

    graph_f = os.path.join(FOLDER, "Mitsunobu_graph.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, testing=True)
    x.steps = [remove_confirm_steps(step) for step in x.steps]

    c = Chempiler(
        experiment_code="test",
        output_dir="out",
        graph_file=graph_f,
        simulation=True,
        device_modules=[ChemputerAPI],
    )
    x.execute(c)
    tracer = x.tracer

    # NOTE: tracer records step properties after execution and Mock measure
    # counter is increased during execution so counter starts at 1 but
    # finishes at 0 (None).
    step_props = [
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "0.5 mL"}),
        # first Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 5}),
        # second Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 5}),
        # third Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 5}),
        # fourth Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 5}),
        # fifth Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 5}),
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1.5 mL"}),
    ]

    step_prop_names = [s[0] for s in step_props]
    tracer_steps = [t for t in tracer if t[0].__name__ in step_prop_names]
    assert len(step_prop_names) == len(tracer_steps)

    for step, props in zip(tracer_steps, step_props):

        assert step[0].__name__ == props[0]

        for prop in props[1]:
            assert step[1][prop] == props[1][prop]


@pytest.mark.chemputer
def test_repeat_until_DONE_logic():
    """Test DONE logic (AND) with 2 monitor steps within a repeat"""
    xdl_f = os.path.join(FOLDER, "repeat_until_done_logic.xdl")

    graph_f = os.path.join(FOLDER, "Mitsunobu_graph.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.scale_procedure(0.1)
    x.prepare_for_execution(graph_f, testing=True)
    x.steps = [remove_confirm_steps(step) for step in x.steps]

    c = Chempiler(
        experiment_code="test",
        output_dir="out",
        graph_file=graph_f,
        simulation=True,
        device_modules=[ChemputerAPI],
    )
    tracer = []
    x.execute(c, tracer=tracer)

    mockmeasure_steps_short = [
        step
        for step in tracer
        if step[0].__name__ == "MockMeasure" and step[1]["comment"] == "short"
    ]
    mockmeasure_steps_long = [
        step
        for step in tracer
        if step[0].__name__ == "MockMeasure" and step[1]["comment"] == "long"
    ]
    assert len(mockmeasure_steps_short) == len(mockmeasure_steps_long) == 4


@pytest.mark.chemputer
def test_repeat_until_DONE_nested_repeats():
    """Test DONE functionality with nested repeats"""
    xdl_f = os.path.join(FOLDER, "repeat_until_done_nested_repeats.xdl")
    graph_f = os.path.join(FOLDER, "Mitsunobu_graph.json")

    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, testing=True)

    x.steps = [remove_confirm_steps(step) for step in x.steps]

    c = Chempiler(
        experiment_code="test",
        output_dir="out",
        graph_file=graph_f,
        simulation=True,
        device_modules=[ChemputerAPI],
    )

    x.execute(platform_controller=c)
    tracer = x.tracer

    x.steps = [remove_confirm_steps(step) for step in x.steps]

    # NOTE: tracer records step properties after execution and Mock measure
    # counter is increased during execution so counter starts at 1 but
    # finishes at 0 (None).
    step_props = [
        # first outer Repeat, first inner Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "0.5 mL"}),
        (
            "MockMeasure",
            {
                "target_repeats": 2,
            },
        ),
        # first outer Repeat, second inner Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "0.5 mL"}),
        (
            "MockMeasure",
            {
                "target_repeats": 2,
            },
        ),
        # first outer Repeat Add and Mock Measure
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "0.5 mL"}),
        (
            "MockMeasure",
            {
                "target_repeats": 3,
            },
        ),
        # second outer Repeat, first inner Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "0.5 mL"}),
        (
            "MockMeasure",
            {
                "target_repeats": 2,
            },
        ),
        # second outer Repeat, second inner Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "0.5 mL"}),
        (
            "MockMeasure",
            {
                "target_repeats": 2,
            },
        ),
        # second outer Repeat Add and Mock Measure
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "0.5 mL"}),
        (
            "MockMeasure",
            {
                "target_repeats": 3,
            },
        ),
        # third outer Repeat, first inner Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "0.5 mL"}),
        (
            "MockMeasure",
            {
                "target_repeats": 2,
            },
        ),
        # third outer Repeat, second inner Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "0.5 mL"}),
        (
            "MockMeasure",
            {
                "target_repeats": 2,
            },
        ),
        # second outer Repeat Add and Mock Measure
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "0.5 mL"}),
        (
            "MockMeasure",
            {
                "target_repeats": 3,
            },
        ),
    ]

    step_prop_names = [s[0] for s in step_props]
    tracer_steps = [t for t in tracer if t[0].__name__ in step_prop_names]
    assert len(step_prop_names) == len(tracer_steps)

    for step, props in zip(tracer_steps, step_props):

        assert step[0].__name__ == props[0]

        for prop in props[1]:
            assert step[1][prop] == props[1][prop]


@pytest.mark.chemputer
def test_repeat_until_DONE_blueprints():
    """
    Test DONE functionality with blueprints.
    Also tests that default reagents can be set in blueprints.
    """
    xdl_f = os.path.join(FOLDER, "repeat_until_done_blueprints.xdl")

    graph_f = os.path.join(FOLDER, "Mitsunobu_graph.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, testing=True)
    x.steps = [remove_confirm_steps(step) for step in x.steps]

    c = Chempiler(
        experiment_code="test",
        output_dir="out",
        graph_file=graph_f,
        simulation=True,
        device_modules=[ChemputerAPI],
    )
    x.execute(c)
    tracer = x.tracer

    x.steps = [remove_confirm_steps(step) for step in x.steps]

    # NOTE: tracer records step properties after execution and Mock measure
    # counter is increased during execution so counter starts at 1 but
    # finishes at 0 (None).
    step_props = [
        # Procedure Add
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "0.5 mL"}),
        # Blueprint Add
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "0.5 mL"}),
        # first BP Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 3}),
        # second BP Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 3}),
        # second BP Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 3}),
        # third BP Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 5}),
        # first procedure Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 5}),
        # second procedure Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 5}),
        # third procedure Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 5}),
        # fourth procedure Repeat
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 5}),
        # Procedure Add
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1.5 mL"}),
    ]

    step_prop_names = [s[0] for s in step_props]
    tracer_steps = [t for t in tracer if t[0].__name__ in step_prop_names]
    assert len(step_prop_names) == len(tracer_steps)

    for step, props in zip(tracer_steps, step_props):

        assert step[0].__name__ == props[0]

        for prop in props[1]:
            assert step[1][prop] == props[1][prop]


@pytest.mark.chemputer
def test_repeat_until_DONE_nested_blueprints():
    """Test DONE functionality with nested blueprints"""
    xdl_f = os.path.join(FOLDER, "repeat_until_done_nested_blueprints.xdl")

    graph_f = os.path.join(FOLDER, "Mitsunobu_graph.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, testing=True)
    x.steps = [remove_confirm_steps(step) for step in x.steps]

    c = Chempiler(
        experiment_code="test",
        output_dir="out",
        graph_file=graph_f,
        simulation=True,
        device_modules=[ChemputerAPI],
    )

    x.execute(c)
    tracer = x.tracer

    x.steps = [remove_confirm_steps(step) for step in x.steps]

    # NOTE: tracer records step properties after execution and Mock measure
    # counter is increased during execution so counter starts at 1 but
    # finishes at 0 (None).
    step_props = [
        # Procedure Add
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "0.5 mL"}),
        # first BP Add
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "0.5 mL"}),
        # first BP, first Repeat (Add and MockMeasure)
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 2}),
        # first BP, second Repeat (Add and MockMeasure)
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 2}),
        # first Procedure MockMeasure
        ("MockMeasure", {"target_repeats": 3}),
        # second BP Add
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "0.5 mL"}),
        # second BP, first Repeat (Add and MockMeasure)
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 2}),
        # second BP, second Repeat (Add and MockMeasure)
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 2}),
        # second Procedure MockMeasure
        ("MockMeasure", {"target_repeats": 3}),
        # third BP Add
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "0.5 mL"}),
        # third BP, first Repeat (Add and MockMeasure)
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 2}),
        # third BP, second Repeat (Add and MockMeasure)
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1 mL"}),
        ("MockMeasure", {"target_repeats": 2}),
        # third Procedure MockMeasure
        ("MockMeasure", {"target_repeats": 3}),
        # Procedure Add
        ("Add", {"reagent": "THF", "vessel": "reactor", "amount": "1.5 mL"}),
    ]

    step_prop_names = [s[0] for s in step_props]
    tracer_steps = [t for t in tracer if t[0].__name__ in step_prop_names]
    assert len(step_prop_names) == len(tracer_steps)

    for step, props in zip(tracer_steps, step_props):

        assert step[0].__name__ == props[0]

        for prop in props[1]:
            assert step[1][prop] == props[1][prop]


@pytest.mark.chemputer
def test_repeat_loop():
    """Making sure that 0 repeats omits the step instead of triggering the
    'until'-functionaliy."""
    xdl_f = os.path.join(FOLDER, "Heck_loop.xdl")
    graph_f = os.path.join(FOLDER, "Heck_loop.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, testing=True)
    generic_chempiler_test(xdl_f, graph_f)
