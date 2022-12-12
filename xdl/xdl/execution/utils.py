from networkx import MultiDiGraph

from ..steps import Step, AbstractDynamicStep, NON_RECURSIVE_ABSTRACT_STEPS

def do_sanity_check(graph: MultiDiGraph, step: Step) -> None:
    """Perform sanity checks on the given step

    Args:
        graph (MultiDiGraph): Graph to use when performing sanity checks.
        step (Step): Step to perform sanity checks for.
    """

    # Perform step sanity check
    step.final_sanity_check(graph)

    # Iterate through any child steps
    if 'children' in step.properties:
        for child in step.children:
            do_sanity_check(graph, child)

    # Recursive step
    if not isinstance(step, NON_RECURSIVE_ABSTRACT_STEPS):
        # Iterate through substep and perform sanity check
        for substep in step.steps:
            do_sanity_check(graph, substep)

    # Dynamic step
    elif type(step) == AbstractDynamicStep:
        # Iterate through each substep in the steps current start block
        for substep in step.start_block:
            # Sanity check the substep
            do_sanity_check(graph, substep)
