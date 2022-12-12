from typing import Dict, List
from networkx import MultiDiGraph

# XDL
from xdl.steps import Step, NON_RECURSIVE_ABSTRACT_STEPS
from xdl.hardware import Hardware

# Relative
from .utils import VesselContents
from .tracking import iter_vessel_contents
from .constants import (
    TRANSFER_ALL_VOLUME_FACTOR,
    CLEAN_VESSEL_BOILING_POINT_FACTOR,
    SOLVENT_BOILING_POINTS
)
from ..steps import Transfer, CMove, Filter, CleanVessel

def add_all_volumes_to_step(
    graph: MultiDiGraph,
    step: Step,
    vessel_contents: Dict[str, VesselContents],
    definite: bool
):
    """Adds volumes to each movement step

    Args:
        step (Step): Step to add volume to
        vessel_contents (dict): Contents of the vessel
        definite (bool): Definite flag from iter_vessel_contents, means that
            volumes in vessel_contents are definitely correct.

    Raises:
        XDLError: Missing desired flask
    """

    # Step is of the Transfer or CMove variety
    if type(step) in [Transfer, CMove]:
        # Volume is the total volume of the container
        if step.volume == 'all':
            step.transfer_all = True

            # Step from vessel is present in vessel contents
            if definite and step.from_vessel in vessel_contents:
                # Recalculate volume
                step.volume = (
                    vessel_contents[step.from_vessel].volume
                    * TRANSFER_ALL_VOLUME_FACTOR
                )

            # Not present in vessel contents, set from max volume of vessel
            # in the graph
            else:
                step.volume = graph.nodes[step.from_vessel]['max_volume']

    # Add all volumes to child steps assume at this point volume tracking can no
    # longer be trusted.
    if hasattr(step, 'children'):
        for child in step.children:
            add_all_volumes_to_step(graph, child, vessel_contents, False)

    # Apply method to substeps of recursive steps
    if not isinstance(step, NON_RECURSIVE_ABSTRACT_STEPS):
        for substep in step.steps:
            add_all_volumes_to_step(
                graph, substep, vessel_contents, definite)

def add_all_volumes(
    graph: MultiDiGraph,
    graph_hardware: Hardware,
    steps: List[Step]
) -> None:
    """When volumes in CMove commands are specified by 'all', change
    these to max_volume of vessel.
    """
    prev_vessel_contents = None

    # Iterate through the vessel contents
    for _, step, vessel_contents, definite in iter_vessel_contents(
        steps, graph_hardware
    ):
        # Apply volume additions
        add_all_volumes_to_step(graph, step, prev_vessel_contents, definite)
        prev_vessel_contents = vessel_contents

def add_filter_volumes(
    graph: MultiDiGraph,
    graph_hardware: Hardware,
    steps: List[Step]
) -> None:
    """
    Add volume of filter bottom (aka dead_volume) and volume of material
    added to filter top to Filter steps.
    """
    prev_vessel_contents = {}

    # Iterate through vessel contents
    for _, step, vessel_contents, _ in iter_vessel_contents(
            steps, graph_hardware):

        # Filter step and not using Inline filter
        if type(step) == Filter and not step.properties['inline_filter']:

            # Current filter vessel been seen before
            if step.filter_vessel in prev_vessel_contents:
                # Set the top volume of the Filter step
                step.filter_top_volume = max(prev_vessel_contents[
                    step.filter_vessel].volume, 0)

                # Impossible volume, default to max volume of filter vessel
                if step.filter_top_volume <= 0:
                    step.filter_top_volume = graph.nodes[
                        step.filter_vessel]['max_volume']

            # Not been seen before, set to max volume fo filter vessel
            else:
                step.filter_top_volume = graph.nodes[
                    step.filter_vessel]['max_volume']

            # Need this as setting max_volume reinitialises step and
            # ApplyVacuum internal properties are lost.
            for substep in step.steps:
                substep.on_prepare_for_execution(graph)

        prev_vessel_contents = vessel_contents

def add_clean_vessel_temps(steps: List[Step]) -> None:
    """Add temperatures to CleanVessel steps. Priority is:
    1) Use explicitly given temperature.
    2) If solvent boiling point known use 80% of the boiling point.
    3) Use 30°C.

    Args:
        steps (List[List[Step]]): List of steps to add temperatures to
            CleanVessel steps

    Returns:
        List[List[Step]]: List of steps with temperatures added to
            CleanVessel steps.
    """

    # Iterate through each XDL step
    for step in steps:
        # CleanVessel step
        if type(step) == CleanVessel:
            # Temperature is not set
            if step.temp is None:
                # Obtain the solvent from the step
                solvent = step.solvent.lower()

                # Set the temperature of the step to the solvent's boiling
                # point if present
                if solvent in SOLVENT_BOILING_POINTS:
                    step.temp = (
                        SOLVENT_BOILING_POINTS[solvent]
                        * CLEAN_VESSEL_BOILING_POINT_FACTOR
                    )

                # Default temperature to 30C
                else:
                    step.temp = 30
