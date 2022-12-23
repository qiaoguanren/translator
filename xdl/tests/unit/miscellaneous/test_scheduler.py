import os

import ChemputerAPI
import pytest
from chempiler import Chempiler
from chemputerxdl import ChemputerPlatform

from tests.utils import remove_confirm_steps
from xdl import XDL

HERE = os.path.abspath(os.path.dirname(__file__))
FOLDER = os.path.join(HERE, "..", "..", "files")


@pytest.mark.skip(reason="Test must be run manually")
@pytest.mark.manual
@pytest.mark.parametrize(
    argnames="xdl_file,timings",
    argvalues=[
        ("step_deps.xdl", [1.0, 3.0, 10.0, 5.0]),
        ("step_deps_bp_basic.xdl", [1.0, 2.0, 3.0]),
        ("step_deps_in_bp.xdl", [1.0, 3.0, 10.0, 5.0, 2.0]),
        ("step_deps_on_bp.xdl", [0.5, 1.0, 3.0, 10.0, 5.0, 2.0]),
        (
            "step_deps_bps_independent.xdl",
            [1.0, 2.0, 3.0, 6.0, 9.0, 10.0, 4.0, 5.0],
        ),
    ],
)
def test_step_deps(xdl_file, timings):
    """
    test that Step deps are awaited correctly
    """
    xdl_f = os.path.join(FOLDER, xdl_file)
    graph_f = os.path.join(FOLDER, "Mitsunobu_graph.json")
    x = XDL(xdl_f, platform=ChemputerPlatform)
    x.prepare_for_execution(graph_f, testing=True, interactive=False)

    x.steps = [remove_confirm_steps(step) for step in x.steps]

    c = Chempiler(
        experiment_code="test",
        output_dir="out",
        graph_file=graph_f,
        simulation=True,
        device_modules=[ChemputerAPI],
    )

    x.execute(c)

    step_finish_order = timings
    wait_steps = [s[1]["time"] for s in x.tracer if s[0] == "CWait"]
    assert step_finish_order == wait_steps
