import os
import shutil
import stat
import sys
from typing import Dict, List, Tuple

import ChemputerAPI
import commanduinolabware
from chempiler import Chempiler
from chemputerxdl import ChemputerPlatform

from xdl import XDL
from xdl.steps import AbstractBaseStep, Step, UnimplementedStep

HERE = os.path.abspath(os.path.dirname(__file__))
CHEMPILER_OUTPUT = os.path.join(HERE, "chempiler_output")


def remove_dir(path):
    """
    Recursively remove all files in a directory or a single target file.
    Should be ompatible with both Windows and Unix os.

    Args:
        path (str): full path to directory.
    """
    if os.path.isdir(path):
        shutil.rmtree(path, onerror=_error_handler)

    else:
        if os.path.exists(path):
            os.remove(path)


def _error_handler(func, path, exc_info):
    """
    Error handler for error caused by ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.
    Otherwise, it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=_error_handler)``
    Adapted from StackOverflow solution:
    ```https://stackoverflow.com/questions/2656322/
            shutil-rmtree-fails-on-windows-with-access-is-denied```
    """
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)


def get_chempiler(graph_file: str) -> Chempiler:
    remove_dir(CHEMPILER_OUTPUT)

    return Chempiler(
        experiment_code="test",
        output_dir=CHEMPILER_OUTPUT,
        simulation=True,
        graph_file=graph_file,
        device_modules=[ChemputerAPI, commanduinolabware],
    )


def generic_chempiler_test(
    xdl_file: str, graph_file: str, tracer: List[Tuple[type, Dict]] = None
) -> None:
    """Given XDL file and graph file, try and execute Chempiler simulation
    of XDL.

    Args:
        xdl_file (str): Path to XDL file.
        graph_file (str): Path to graph file.
    """
    x = XDL(xdl_file, platform=ChemputerPlatform)
    for i in reversed(range(len(x.steps))):
        if isinstance(x.steps[i], UnimplementedStep):
            x.steps.pop(i)
    x.prepare_for_execution(graph_file, testing=True)
    x.steps = [remove_confirm_steps(step) for step in x.steps]
    old_stdout = sys.stdout
    with open(os.devnull, "w") as devnull:
        sys.stdout = devnull
        chempiler = get_chempiler(graph_file)
        x.execute(chempiler, interactive=False, tracer=tracer)
    sys.stdout = old_stdout


def remove_confirm_steps(step: Step) -> None:
    """Recursively remove Confirm steps from given step, going all the way down
    step tree. This needs to be done as you can't ask for input during an
    automated test.

    Args:
        step (Step): Step to remove Confirm steps from.
    """
    # If step is base step just return step.
    if isinstance(step, AbstractBaseStep):
        return step
    else:
        for i, _ in reversed(list(enumerate(step.steps))):
            if step.steps[i].name == "Confirm":
                step.steps.pop(i)
            else:
                step.steps[i] = remove_confirm_steps(step.steps[i])
        return step


def test_step(step, correct_step_info):
    assert type(step) == correct_step_info[0]  # nosec B101
    for k, v in correct_step_info[1].items():
        assert k in step.properties  # nosec B101
        assert step.properties[k] == v  # nosec B101
