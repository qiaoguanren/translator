import os
import sys
import shutil
from xdl import XDL
from xdl.steps import Step, AbstractBaseStep, UnimplementedStep
from chempiler import Chempiler
import ChemputerAPI
import commanduinolabware

HERE = os.path.abspath(os.path.dirname(__file__))

def get_chempiler(graph_file: str) -> Chempiler:
    if os.path.isdir(os.path.join(HERE, 'chempiler_output')):
        shutil.rmtree(os.path.join(HERE, 'chempiler_output'))
    return Chempiler(
        experiment_code='test',
        output_dir=os.path.join(HERE, 'chempiler_output'),
        simulation=True,
        graph_file=graph_file,
        device_modules=[ChemputerAPI, commanduinolabware])


def generic_chempiler_test(xdl_file: str, graph_file: str) -> None:
    """Given XDL file and graph file, try and execute Chempiler simulation
    of XDL.

    Args:
        xdl_file (str): Path to XDL file.
        graph_file (str): Path to graph file.
    """
    x = XDL(xdl_file)
    for i in reversed(range(len(x.steps))):
        if isinstance(x.steps[i], UnimplementedStep):
            x.steps.pop(i)
    x.prepare_for_execution(graph_file, testing=True)
    x.steps = [
        remove_confirm_steps(step) for step in x.steps]
    old_stdout = sys.stdout
    with open(os.devnull, 'w') as devnull:
        sys.stdout = devnull
        chempiler = get_chempiler(graph_file)
        x.execute(chempiler)
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
        for i in reversed(range(len(step.steps))):
            if step.steps[i].name == 'Confirm':
                step.steps.pop(i)
            else:
                step.steps[i] = remove_confirm_steps(step.steps[i])
        return step

def test_step(step, correct_step_info):
    assert type(step) == correct_step_info[0]
    for k, v in correct_step_info[1].items():
        assert k in step.properties
        assert step.properties[k] == v
