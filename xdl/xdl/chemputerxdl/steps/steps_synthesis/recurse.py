"""
.. module:: steps_synthesis.recurse
    :platforms: Unix, Windows
    :synopsis: XDL step for performing the A-Life classification of 'Recursion'
            Remove X% liquid from vessel and replenish with new stock up to
            100% volume.

"""

from typing import List, Union, Optional, Dict
import copy

# XDL
from xdl.steps.base_steps import Step, AbstractStep
from xdl.utils.prop_limits import VOLUME_PROP_LIMIT, TIME_PROP_LIMIT

# Relative
from ..steps_synthesis import Add
from ..steps_utility.liquid_handling import Transfer
from ..steps_utility.cleaning import CleanBackbone
# from ..steps_utility.modular_wheel import MWAddAndTurn
from ..steps_base.general import CWait
from ..base_step import ChemputerStep

# List of steps to adjust for recursive cycles
APPLY_RECURSION_TO_STEPS = [
    Add,
    Transfer
    #MWAddAndTurn
]

class Recurse(ChemputerStep, AbstractStep):
    """
    Carry out simple recursion for ALife Chemputers. Similar to XDL repeat
    step but with modifications to Add, Transfer and MwAddAndTurn steps to
    adjust for recursive volumes.

    Args:
        n_cycles (int): Specifies number of recursive cycles (including first
            cycle).
        children (List[Step]): List of child steps to apply recursion.
        sampling_volume (float): Amount to harvest from each reactor at the
            end of cycles 2+ (sampling volumes for first cycle are set by
            child steps)
        replenishment_volume (float): Total volume of inputs used to replenish
            each reactor at the start of recursive cycles. Ratio of inputs will
            be kepts consistent between cycles, with individual volumes scaled
            appropriately.
        clean_after_n_cycles (int): Optional. Inserts backbone cleans between
            recursive cycles.
        cleaning_solvents (List[str]): Optional. Specifies list of solvents to
            use in extra backbone cleans. After n cycles, backbone will be
            cleaned using each of these solvents in order.
    """
    DEFAULT_PROPS = {
        'replenishment_volume': None,  # mL
        'cycle_time': 6,   # hours
        'clean_after_n_cycles': None,
        'cleaning_solvents': ["ipa", "water"]
    }

    PROP_TYPES = {
        'n_cycles': int,
        'sampling_volume': float,
        'replenishment_volume': float,
        'children': Union[Step, List[Step]],
        'cycle_time': float,  # hours
        'clean_after_n_cycles': int,  # cycles
        'cleaning_solvents': List[str]  # list of strings
    }

    PROP_LIMITS = {
        'sampling_volume': VOLUME_PROP_LIMIT,
        'replenishment_volume': VOLUME_PROP_LIMIT,
        'cycle_time': TIME_PROP_LIMIT,
    }

    def __init__(
        self,
        n_cycles: int,
        children: Union[Step, List[Step]],
        sampling_volume: float,
        replenishment_volume: Optional[float] = 'default',
        cycle_time: Optional[float] = 'default',
        clean_after_n_cycles: int = 'default',
        cleaning_solvents: List[str] = 'default',
        **kwargs
    ) -> None:
        super().__init__(locals())

        # Convert `children` to list if not already
        if type(children) != list:
            self.children = [children]

        # Set replenishment volume
        if not self.replenishment_volume:
            self.replenishment_volume = self.sampling_volume

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        # Get all child steps
        steps = [step for step in self.children]

        # Add a Wait step with time set to Recursion cycle time
        steps.append(CWait(time=self.cycle_time * 60 * 60))

        # Get volumes to use for recursion
        recursion_volumes = self.return_to_vessel_recursion_volumes()

        # Iterate over n-1 cycles
        for i in range(0, self.n_cycles - 1):
            # Iterate over all child steps
            for step in self.children:
                # Get the recursive step
                recursive_step = copy.deepcopy(step)

                # Step name is present in recursion volumes
                if step.name in recursion_volumes:
                    # Obtain the total volume
                    total_volume = recursion_volumes[step.name][step.vessel]

                    # Calculate the relative volume
                    relative_volume = recursive_step.volume / total_volume

                    # Set recursive step volume
                    recursive_step.volume = (
                        relative_volume * self.replenishment_volume
                    )

                # Step is a Modular Wheel add and turn step
                elif type(step) == MWAddAndTurn:
                    # Set recursion volume to the defualt sampling volume
                    recursive_step.volume = self.sampling_volume

                # Add recursive step to current list of steps
                steps.append(recursive_step)

            # Clean after X cycles
            if (self.clean_after_n_cycles
                    and not (i - 1) % self.clean_after_n_cycles):

                # CLeaning solvent are defined
                if self.cleaning_solvents:
                    # Add CleanBackbone step for every cleaning solvent
                    for solvent in self.cleaning_solvents:
                        steps.append(CleanBackbone(solvent=solvent))

            # Wait if on the second to last cycle
            if i < self.n_cycles - 2:
                steps.append(CWait(time=self.cycle_time * 60 * 60))

        return steps

    def return_to_vessel_recursion_volumes(self) -> Dict[str, Dict[str, float]]:
        """
        Return default cycle 1 Transfer and Add volume specified to each
        reactor. This is to work out recursion volumes after the first cycle.

        Returns:
            Dict[str, Dict[str, float]]: Vessels and volumes
        """

        recursion_volumes = {}

        # Iterate through all child steps
        for step in self.children:
            # Step is valid for recursion and not a MW step
            if (type(step) in APPLY_RECURSION_TO_STEPS
                    and type(step) != MWAddAndTurn):

                # Set empty dict if step name not already in recursion_volumes
                if step.name not in recursion_volumes:
                    recursion_volumes[step.name] = {}

                # Vessel not present, update to add to recursion_volumes
                if step.vessel not in recursion_volumes[step.name]:
                    recursion_volumes[step.name].update({
                        step.vessel: step.volume
                    })

                # Present, increment volume
                else:
                    recursion_volumes[step.name][step.vessel] += step.volume

        return recursion_volumes

    def human_readable(self, language: Optional[str] = 'en') -> str:
        """Gets the human-readable text for this step.

        Args:
            language (Optional[str], optional): Localisation language.
                                                Defaults to 'en'.

        Returns:
            str: Human-readable text for the step
        """

        human_readable = f'Recurse for {self.n_cycles} cycles:\n'

        # Add human readable text for each child step
        for step in self.children:
            human_readable += f'    {step.human_readable()}\n'

        return human_readable
