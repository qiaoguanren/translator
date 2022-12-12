"""
.. module:: steps_synthesis.separate
    :platforms: Unix, Windows
    :synopsis: XDL step to extract contents from a vessel using a given amount
                of solvent.

"""

from typing import Optional, Dict, Any, List
import math

# XDL
from xdl.steps.base_steps import Step, AbstractStep
from xdl.errors import XDLError
from xdl.utils.misc import SanityCheck
from xdl.constants import REAGENT_PROP_TYPE, VESSEL_PROP_TYPE
from xdl.utils.prop_limits import (
    TIME_PROP_LIMIT,
    ROTATION_SPEED_PROP_LIMIT,
    VOLUME_PROP_LIMIT,
    SEPARATION_PURPOSE_PROP_LIMIT,
)

# Relative
from .add import Add
from ..base_step import ChemputerStep
from ..steps_utility import Transfer, Wait, Stir, SeparatePhases
from ...constants import (
    BOTTOM_PORT,
    DEFAULT_SEPARATION_SLOW_STIR_TIME,
    DEFAULT_SEPARATION_SLOW_STIR_SPEED
)
from ...localisation import HUMAN_READABLE_STEPS
from ...constants import CHEMPUTER_WASTE, PORT_PROP_TYPE
from ...utils.execution import (
    get_buffer_flask, get_nearest_node, get_cartridge)
from ...utils.prop_limits import PORT_PROP_LIMIT

class Separate(ChemputerStep, AbstractStep):
    """Extract contents of from_vessel using given amount of given solvent.
    NOTE: If n_separations > 1, to_vessel/to_port must be capable of giving
    and receiving material.

    Args:
        purpose (str): 'extract' or 'wash'. Used in iter_vessel_contents.
        from_vessel (str): Vessel name with contents to be separated.
        from_port (str): from_vessel port to use.
        separation_vessel (str): Separation vessel name.
        to_vessel (str): Vessel to send product phase to.
        to_port (str): to_vessel port to use.
        solvent (str): Solvent to extract with.
        solvent_volume (float): Volume of solvent to extract with.
        product_bottom (bool): True if product in bottom phase, otherwise False.
        through (str): Optional. Chemical to transfer product phase through
            on way to to_vessel.
        through_cartridge (str): Optional. Node name of cartridge to transfer
            product phase through on way to to_vessel. Supplied internally if
            through is given.
        mixing_stir_speed (float): Optional. Stirring speed for fast
            stirring step (slow stirring currently uses default in
            xdl/constants.py),
        mixing_time (float): Time spent stirring.
        settling_time (float): Optional. Time to allow for phase separation
            after stirring.
        n_separations (int): Number of separations to perform.
        waste_phase_to_vessel (str): Vessel to send waste phase to.
        waste_phase_to_port (str): waste_phase_to_vessel port to use.
        waste_vessel (str): Given internally. Vessel to send waste to.
    """

    DEFAULT_PROPS = {
        'solvent_volume': '30 mL',
        'remove_dead_volume': True,
        'mixing_stir_speed': '600 RPM',
        'mixing_time': '5 min',
        'settling_time': '5 min',
        'solvent': None,
        'through': None,
        'from_port': None,
        'to_port': None,
        'waste_phase_to_vessel': None,
        'waste_phase_to_port': None,
        'n_separations': 1,
    }

    PROP_TYPES = {
        'purpose': str,
        'from_vessel': VESSEL_PROP_TYPE,
        'separation_vessel': VESSEL_PROP_TYPE,
        'to_vessel': VESSEL_PROP_TYPE,
        'product_bottom': bool,
        'solvent': REAGENT_PROP_TYPE,
        'through': str,
        'from_port': PORT_PROP_TYPE,
        'to_port': PORT_PROP_TYPE,
        'solvent_volume': float,
        'n_separations': int,
        'waste_phase_to_vessel': VESSEL_PROP_TYPE,
        'waste_phase_to_port': PORT_PROP_TYPE,
        'remove_dead_volume': bool,
        'waste_vessel': str,
        'buffer_flasks': List[str],
        'through_cartridge': str,
        'mixing_stir_speed': float,
        'mixing_time': float,
        'settling_time': float,
        'waste_phase_to_vessel_to_use': str,
    }

    INTERNAL_PROPS = [
        'waste_vessel',
        'waste_phase_to_vessel_to_use',
        'buffer_flasks',
        'through_cartridge',
    ]

    PROP_LIMITS = {
        'purpose': SEPARATION_PURPOSE_PROP_LIMIT,
        'from_port': PORT_PROP_LIMIT,
        'to_port': PORT_PROP_LIMIT,
        'waste_phase_to_port': PORT_PROP_LIMIT,
        'solvent_volume': VOLUME_PROP_LIMIT,
        'mixing_stir_speed': ROTATION_SPEED_PROP_LIMIT,
        'mixing_time': TIME_PROP_LIMIT,
        'settling_time': TIME_PROP_LIMIT,
    }

    def __init__(
        self,
        purpose: str,
        from_vessel: str,
        separation_vessel: str,
        to_vessel: str,
        product_bottom: bool,
        solvent: Optional[str] = 'default',
        through: Optional[str] = 'default',
        from_port: Optional[str] = 'default',
        to_port: Optional[str] = 'default',
        solvent_volume: Optional[float] = 'default',
        n_separations: Optional[int] = 'default',
        waste_phase_to_vessel: Optional[str] = 'default',
        waste_phase_to_port: Optional[str] = 'default',
        remove_dead_volume: Optional[bool] = 'default',
        mixing_stir_speed: Optional[float] = 'default',
        mixing_time: Optional[float] = 'default',
        settling_time: Optional[float] = 'default',

        # Internal properties
        waste_vessel: Optional[str] = None,
        waste_phase_to_vessel_to_use: Optional[str] = None,
        buffer_flasks: Optional[List[str]] = [None, None],
        through_cartridge: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check

        Raises:
            XDLError: Buffer flasks required greater than those available in
                        the graph.
        """
        # Obtain buffer flasks if not defined
        if not self.buffer_flasks[0]:
            self.buffer_flasks = get_buffer_flask(
                graph, self.separation_vessel, return_single=False
            )
            # Make sure list always has at least two elements. None buffer flask
            # is raised later, let it pass here.
            if len(self.buffer_flasks) == 1:
                self.buffer_flasks.append(None)

        # Obtain the waste vessel if not defined
        if not self.waste_vessel:
            self.waste_vessel = get_nearest_node(
                graph, self.separation_vessel, CHEMPUTER_WASTE
            )

        self.waste_phase_to_vessel_to_use = self.waste_phase_to_vessel
        if not self.waste_phase_to_vessel_to_use and self.waste_vessel:
            self.waste_phase_to_vessel_to_use = self.waste_vessel

        # Get the though cartridge if required
        if not self.through_cartridge and self.through:
            self.through_cartridge = get_cartridge(graph, self.through)

        # Get total number of buffer flasks present
        n_buffer_flasks = len([
            buf for buf in self.buffer_flasks if buf is not None
        ])

        # Raise error if there is not enough buffer flasks present
        if n_buffer_flasks < self.buffer_flasks_required:
            raise XDLError(
                f'{self.buffer_flasks_required} buffer flasks required but\
 {n_buffer_flasks} buffer flasks found in graph.'
            )

        # Split the separations if required
        self.split_separations_if_necessary(graph)

    def split_separations_if_necessary(self, graph: Dict):
        """If solvent volume is greater than the separator max volume split the
        separation into multiple smaller separations.

        Args:
            graph (Dict): Chemputer graph to check
        """

        # Get maximum volume of the separator
        separator_max_volume = graph.nodes[self.separation_vessel]['max_volume']

        # Solvent needed greater than separator volume
        if self.solvent_volume and self.solvent_volume > separator_max_volume:
            # Calculate number of separations needed
            self.n_separations = math.ceil(
                self.solvent_volume / separator_max_volume
            )

            # Set volume accordingly
            self.solvent_volume = self.solvent_volume / self.n_separations

    @property
    def dead_volume_target(self) -> Optional[str]:
        """Get the target of the dead volume removal

        Returns:
            Optional[str]: Waste vessel or None
        """

        return self.waste_vessel if self.remove_dead_volume else None

    def get_steps(self) -> List[Step]:
        """It may seem mental having this many methods with lots of duplicate
        code but the condensed version with lots of if statements for different
        scenarios was took too long to see what was going on. Better just to
        have clear routines for every scenario.

        Raises:
            XDLError: Invalid purpose for the step given

        Returns:
            List[Step]: List of XDL steps to execute
        """
        # Set separations to 1 if not defined
        if not self.n_separations:
            self.n_separations = 1

        # Set location of waste phase in this variable, so that it can be used
        # to add a Transfer step at the end to waste_phase_to_vessel
        self._waste_phase_in_buffer = None

        # More than one separation required
        if self.n_separations > 1:
            # Get wash steps
            if self.purpose == 'wash':
                return self._get_multi_wash_steps()

            # Get extract steps
            elif self.purpose == 'extract':
                return self._get_multi_extract_steps()

            # Purpose not recognised
            raise XDLError('Invalid purpose given to Separate step.\nValid\
 purposes: "wash" or "extract"')

        # Get default steps
        else:
            return self._get_single_separation_steps()

    #################################
    # Separation Routine Components #
    #################################

    def _get_initial_reaction_mixture_transfer_step(self) -> List[Step]:
        """Transfer reaction mixture to separator

        Returns:
            List[Step]: Transfer steps
        """

        steps = []

        # from_vessel is not the separation vessel
        if self.from_vessel != self.separation_vessel:
            # Move from from_vessel to separation_vessel
            steps.append(
                Transfer(
                    from_vessel=self.from_vessel,
                    from_port=self.from_port,
                    to_vessel=self.separation_vessel,
                    to_port=BOTTOM_PORT,
                    volume='all'
                )
            )

        return steps

    def _get_add_solvent_step(self) -> List[Step]:
        """Add washing/extracting solvent to separator

        Returns:
            List[Step]: Add Steps
        """

        steps = []

        # Solvent is defined, add an Add step
        if self.solvent:
            # Move solvent to separation_vessel
            steps.append(
                Add(reagent=self.solvent,
                    vessel=self.separation_vessel,
                    port=BOTTOM_PORT,
                    volume=self.solvent_volume,
                    waste_vessel=self.waste_vessel)
            )

        return steps

    def _get_stir_separator_before_separation_steps(self) -> List[Step]:
        """Stir separator and wait for phases to appear

        Returns:
            List[Step]: Stirring steps
        """

        return [
            # Stir separation_vessel
            Stir(
                vessel=self.separation_vessel,
                time=self.mixing_time,
                stir_speed=self.mixing_stir_speed
            ),
            # Slow stirring step -- Potentially remove
            Stir(
                vessel=self.separation_vessel,
                time=DEFAULT_SEPARATION_SLOW_STIR_TIME,
                stir_speed=DEFAULT_SEPARATION_SLOW_STIR_SPEED
            ),
            # Wait for phases to separate
            Wait(time=self.settling_time),
        ]

    def _get_final_separate_phases_step(self) -> List[Step]:
        """Get final SeparatePhases step in separation routine.

        Returns:
            List[Step]: SeparatePhase steps
        """

        waste_phase_to_vessel_to_use = self.waste_phase_to_vessel_to_use
        waste_phase_to_port = self.waste_phase_to_port
        if self._waste_phase_in_buffer:
            waste_phase_to_vessel_to_use = self._waste_phase_in_buffer
            waste_phase_to_port = None

        # Product is in the bottom phase of the separator
        if self.product_bottom:
            # Not moving back into separator
            if self.to_vessel != self.separation_vessel:

                return [SeparatePhases(
                    separation_vessel=self.separation_vessel,
                    lower_phase_vessel=self.to_vessel,
                    lower_phase_port=self.to_port,
                    upper_phase_vessel=waste_phase_to_vessel_to_use,
                    upper_phase_port=waste_phase_to_port,
                    dead_volume_vessel=self.dead_volume_target,
                    dead_volume_through=self.through,
                    lower_phase_through=self.through,
                    failure_vessel=self.to_vessel
                )]

            # Moving back into separator
            else:
                return [
                    SeparatePhases(
                        separation_vessel=self.separation_vessel,
                        lower_phase_vessel=self.buffer_flasks[0],
                        upper_phase_vessel=self.waste_phase_to_vessel_to_use,
                        upper_phase_port=self.waste_phase_to_port,
                        dead_volume_vessel=self.dead_volume_target,
                        failure_vessel=self.to_vessel
                    ),
                    Transfer(
                        from_vessel=self.buffer_flasks[0],
                        to_vessel=self.separation_vessel,
                        volume='all'
                    )
                ]

        # Product in the top phase of the separator
        else:
            # Require more than one separation and moving back into the
            # separator
            if (
                self.n_separations > 1
                and self.to_vessel == self.separation_vessel
                and self.purpose == 'extract'
            ):
                return [
                    SeparatePhases(
                        separation_vessel=self.separation_vessel,
                        lower_phase_vessel=self.waste_phase_to_vessel_to_use,
                        lower_phase_port=self.waste_phase_to_port,
                        upper_phase_vessel=self.to_vessel,
                        dead_volume_vessel=self.dead_volume_target,
                        failure_vessel=self.to_vessel
                    ),
                    Transfer(
                        from_vessel=self.buffer_flasks[1],
                        to_vessel=self.separation_vessel,
                        volume='all'
                    )
                ]

            # Waste phase going back into separator
            elif self.waste_phase_to_vessel_to_use == self.separation_vessel:
                return [
                    SeparatePhases(
                        separation_vessel=self.separation_vessel,
                        lower_phase_vessel=self.buffer_flasks[0],
                        upper_phase_vessel=self.to_vessel,
                        upper_phase_port=self.to_port,
                        dead_volume_vessel=self.dead_volume_target,
                        upper_phase_through=self.through,
                        failure_vessel=self.to_vessel
                    ),
                    Transfer(
                        from_vessel=self.buffer_flasks[0],
                        to_vessel=self.waste_phase_to_vessel_to_use,
                        volume='all'
                    )
                ]

            # Default separation
            return [
                SeparatePhases(
                    separation_vessel=self.separation_vessel,
                    lower_phase_vessel=self.waste_phase_to_vessel_to_use,
                    lower_phase_port=self.waste_phase_to_port,
                    upper_phase_vessel=self.to_vessel,
                    upper_phase_port=self.to_port,
                    dead_volume_vessel=self.dead_volume_target,
                    upper_phase_through=self.through,
                    failure_vessel=self.to_vessel
                )
            ]

    def _get_multi_wash_loop_separate_phases(self) -> List[Step]:
        """Get CSeparatePhases in wash routine, if there is another separation
        to be performed after. Ensure product phase ends up in back in
        separator.

        Returns:
            List[Step]: Separate Phases steps
        """

        # List to hold the steps
        steps = []

        # Product is in the bottom phase of the separator
        if self.product_bottom:
            # Not moving back into the separator
            if self.to_vessel != self.separation_vessel:

                # Waste phase not going to separator
                if self.waste_phase_to_vessel != self.separation_vessel:
                    waste_phase_to_vessel_to_use =\
                        self.waste_phase_to_vessel_to_use
                    waste_phase_to_port = self.waste_phase_to_port

                # Waste phase going to separator, use buffer flask and transfer
                # at end
                else:
                    waste_phase_to_vessel_to_use = self.buffer_flasks[1]
                    self._waste_phase_in_buffer = self.buffer_flasks[1]
                    waste_phase_to_port = None

                steps.extend([
                    SeparatePhases(
                        separation_vessel=self.separation_vessel,
                        lower_phase_vessel=self.buffer_flasks[0],
                        upper_phase_vessel=waste_phase_to_vessel_to_use,
                        upper_phase_port=waste_phase_to_port,
                        dead_volume_vessel=self.buffer_flasks[0],
                        failure_vessel=self.to_vessel
                    ),
                    # Move to_vessel to separation_vessel
                    Transfer(
                        from_vessel=self.buffer_flasks[0],
                        to_vessel=self.separation_vessel,
                        volume='all'
                    ),
                ])

            # Moving back into separator
            else:
                steps.extend([
                    SeparatePhases(
                        separation_vessel=self.separation_vessel,
                        lower_phase_vessel=self.buffer_flasks[0],
                        upper_phase_vessel=self.waste_phase_to_vessel_to_use,
                        upper_phase_port=self.waste_phase_to_port,
                        dead_volume_vessel=self.buffer_flasks[0],
                        failure_vessel=self.to_vessel
                    ),
                    Transfer(
                        from_vessel=self.buffer_flasks[0],
                        to_vessel=self.separation_vessel,
                        volume='all'
                    ),
                ])

        # Product phase is in the top phase of the separator
        else:
            # Moving waste phase to different vessel
            if self.waste_phase_to_vessel_to_use != self.separation_vessel:
                steps.append(
                    SeparatePhases(
                        separation_vessel=self.separation_vessel,
                        lower_phase_vessel=self.waste_phase_to_vessel_to_use,
                        lower_phase_port=self.waste_phase_to_port,
                        upper_phase_vessel=self.separation_vessel,
                        dead_volume_vessel=self.waste_phase_to_vessel_to_use,
                        failure_vessel=self.to_vessel
                    )
                )

            # Moving waste phase back into separation vessel
            else:
                steps.append(
                    SeparatePhases(
                        separation_vessel=self.separation_vessel,
                        lower_phase_vessel=self.buffer_flasks[0],
                        upper_phase_vessel=self.separation_vessel,
                        dead_volume_vessel=self.buffer_flasks[0],
                        failure_vessel=self.to_vessel
                    )
                )

        # Separation Steps
        return steps

    def _get_multi_extract_loop_separate_phases(self) -> List[Step]:
        """Get SeparatePhases in extract routine, if there is another separation
        to be performed after. Ensure waste phase ends up in back in separator.

        Returns:
            List[Step]: SeparatePhases steps
        """

        # List to hold steps
        steps = []

        # Product is in the bottom phase of the separator
        if self.product_bottom:
            # Not moving back into the separator
            if self.to_vessel != self.separation_vessel:
                steps.append(
                    SeparatePhases(
                        separation_vessel=self.separation_vessel,
                        lower_phase_vessel=self.to_vessel,
                        lower_phase_port=self.to_port,
                        lower_phase_through=self.through,
                        upper_phase_vessel=self.separation_vessel,
                        dead_volume_vessel=self.to_vessel,
                        dead_volume_through=self.through,
                        failure_vessel=self.to_vessel
                    )
                )

            # Moving back into the separtor
            else:
                steps.append(
                    SeparatePhases(
                        separation_vessel=self.separation_vessel,
                        lower_phase_vessel=self.buffer_flasks[0],
                        upper_phase_vessel=self.separation_vessel,
                        dead_volume_vessel=self.buffer_flasks[0],
                        failure_vessel=self.to_vessel
                    )
                )

        # Product is in the top phase of the separator
        else:
            # Not moving back into the separator
            if self.to_vessel != self.separation_vessel:
                steps.extend([
                    SeparatePhases(
                        separation_vessel=self.separation_vessel,
                        lower_phase_vessel=self.buffer_flasks[0],
                        upper_phase_vessel=self.to_vessel,
                        upper_phase_port=self.to_port,
                        upper_phase_through=self.through,
                        dead_volume_vessel=self.buffer_flasks[0],
                        failure_vessel=self.to_vessel
                    ),
                    # Move waste phase in buffer flask back to separation_vessel
                    Transfer(
                        from_vessel=self.buffer_flasks[0],
                        to_vessel=self.separation_vessel,
                        volume='all'
                    ),
                ])

            # Moving back into the sepatator
            else:
                steps.extend([
                    SeparatePhases(
                        separation_vessel=self.separation_vessel,
                        lower_phase_vessel=self.buffer_flasks[0],
                        upper_phase_vessel=self.buffer_flasks[1],
                        dead_volume_vessel=self.buffer_flasks[0],
                        failure_vessel=self.to_vessel
                    ),
                    Transfer(
                        from_vessel=self.buffer_flasks[0],
                        to_vessel=self.separation_vessel,
                        volume='all',
                    )
                ])

        # Separation steps
        return steps

    ################################
    # Complete Separation Routines #
    ################################

    def _get_single_separation_steps(self) -> List[Step]:
        """Get full separation routine for 1 wash/extraction.

        Returns:
            List[Step]: Single separation routine
        """

        # If necessary, Transfer from_vessel to separation_vessel
        steps = self._get_initial_reaction_mixture_transfer_step()

        steps.extend(self._get_add_solvent_step())

        # Stir separator
        steps.extend(self._get_stir_separator_before_separation_steps())

        # Separate, vessels depending on self.product_bottom
        steps.extend(self._get_final_separate_phases_step())

        return steps

    def _get_multi_wash_steps(self) -> List[Step]:
        """Get full separation routine for >1 washes.

        Returns:
            List[Step]: Separation routine for > 1 wash
        """

        # If necessary, Transfer from_vessel to separation_vessel
        steps = self._get_initial_reaction_mixture_transfer_step()

        # Add solvent
        steps.extend(self._get_add_solvent_step())

        # Stir separator
        steps.extend(self._get_stir_separator_before_separation_steps())

        for _ in range(self.n_separations - 1):
            # Separate phases, and make sure product phase ends up back in
            # separator
            steps.extend(self._get_multi_wash_loop_separate_phases())

            # Add more solvent
            steps.extend(self._get_add_solvent_step())

            # Stir
            steps.extend(self._get_stir_separator_before_separation_steps())

        # Add final steps
        steps.extend(self._get_final_separate_phases_step())

        # Waste phase was sent to buffer, now send to waste_phase_to_vessel
        if self._waste_phase_in_buffer:
            steps.append(Transfer(
                from_vessel=self._waste_phase_in_buffer,
                to_vessel=self.waste_phase_to_vessel_to_use,
                volume='all'
            ))

        return steps

    def _get_multi_extract_steps(self) -> List[Step]:
        """Get full separation routine for >1 extractions.

        Returns:
            List[Step]: Separation routine for > 1 extraction.
        """

        # If necessary, Transfer from_vessel to separation_vessel
        steps = self._get_initial_reaction_mixture_transfer_step()

        # Add solvent
        steps.extend(self._get_add_solvent_step())

        # Stir separator
        steps.extend(self._get_stir_separator_before_separation_steps())

        for _ in range(self.n_separations - 1):
            # Separate phases, and make sure waste phase ends up back in
            # separator
            steps.extend(self._get_multi_extract_loop_separate_phases())

            # Add more solvent
            steps.extend(self._get_add_solvent_step())

            # Stir
            steps.extend(self._get_stir_separator_before_separation_steps())

        # Add final steps
        steps.extend(self._get_final_separate_phases_step())

        return steps

    ####################################
    #  Abstract Method implementations #
    ####################################

    def sanity_checks(self, graph: Dict) -> List[SanityCheck]:
        """Gets a list of Sanity checks to perform for the step

        Args:
            graph (Dict): Chemputer graph to check

        Returns:
            List[SanityCheck]: List of checks to perform
        """

        return [
            SanityCheck(
                condition=(len(self.buffer_flasks)
                           >= self.buffer_flasks_required),
                error_msg='Not enough buffer flasks in graph. Create buffer\
 flasks as ChemputerFlask nodes with an empty chemical property.'
            ),

            SanityCheck(
                condition=self.to_vessel != self.waste_phase_to_vessel_to_use,
                error_msg='Separate step `to_vessel` must be different to\
 `waste_phase_to_vessel` otherwise both phases end up in the same vessel.'
            ),

            SanityCheck(
                condition=not self.solvent or self.solvent_volume > 0,
                error_msg='Solvent volume must be greater than 0 mL if solvent\
 specified.'
            ),

            SanityCheck(
                condition=self.purpose in ['extract', 'wash'],
                error_msg=f'"{self.purpose}" is invalid for Separate `purpose`\
 property. Valid values: "extract" or "wash".'
            ),

            SanityCheck(
                condition=self.n_separations > 0,
                error_msg=f'Separate `n_separations` property must be > 1.\
 {self.n_separations} is an invalid value.'
            ),

            SanityCheck(
                condition=self.solvent is not None or self.n_separations == 1,
                error_msg='Multiple separations without adding any solvent\
 makes no sense.'
            )
        ]

    @property
    def buffer_flasks_required(self) -> int:
        """This was done pretty rigorously by going through get_steps and seeing
        what happens in every situation. Please update this
        if Separate get_steps is updated.

        Returns:
            int: Total number of buffer flasks required
        """

        n_buffer_flasks_required = 0

        # More than one separation
        if self.n_separations > 1:
            # Performing a Wash
            if self.purpose == 'wash':
                # Require 1 flask if product in bottom phase
                if self.product_bottom:
                    # Waste phase not going to separator
                    if self.waste_phase_to_vessel != self.separation_vessel:
                        n_buffer_flasks_required = 1

                    # Waste phase going to separator
                    else:
                        n_buffer_flasks_required = 2

                # Moving waste phase back to separator requires 1 flask
                else:
                    if (self.waste_phase_to_vessel
                            == self.separation_vessel):
                        n_buffer_flasks_required = 1

            # Performing an Extraction
            elif self.purpose == 'extract':
                # Product is in bottom phase
                if self.product_bottom:
                    # Moving back into separator requires 1 flask
                    if self.to_vessel == self.separation_vessel:
                        n_buffer_flasks_required = 1

                # Product is in the top phase of the separtator
                else:
                    # Moving back into separator requires 2 flasks in this case
                    if self.to_vessel == self.separation_vessel:
                        n_buffer_flasks_required = 2

                    # Not moving back, just require 1 flask
                    else:
                        n_buffer_flasks_required = 1

        # Performing single separation
        else:
            # Product is in the bottom phase of the separator
            if self.product_bottom:
                # Moving back into the separator requires 1 flask
                if self.to_vessel == self.separation_vessel:
                    n_buffer_flasks_required = 1

            # Product is in the top phase of the separator
            else:
                # Waste phase getting moved back into separation vessel
                if self.waste_phase_to_vessel == self.separation_vessel:
                    # Require 1 flask for this
                    n_buffer_flasks_required = 1

        # Total number of buffer flasks required
        return n_buffer_flasks_required

    def human_readable(self, language: str = 'en') -> str:
        """Get the human-readable text for this step.

        Args:
            language (str, optional): Localisation language. Defaults to 'en'.

        Raises:
            KeyError: Unsupported localisation language

        Returns:
            str: Human-readable text for this step.
        """

        # Get the props for the step
        props = self.formatted_properties()

        # No vessel for waste phase to go to defined
        if not self.waste_phase_to_vessel:
            props['waste_phase_to_vessel'] = 'waste'

        # Label phases
        phases = ['bottom', 'top']

        # Set appropriate properties
        props['waste_phase'] = phases[self.product_bottom]
        props['product_phase'] = phases[not self.product_bottom]

        # Attempt to get the human-readable text
        try:
            if self.purpose == 'wash':
                s = HUMAN_READABLE_STEPS['Separate (wash)'][language].format(
                    **props)
            elif self.purpose == 'extract':
                if not props['solvent']:
                    s = HUMAN_READABLE_STEPS['Separate (solvent_free)'][
                        language].format(**props)
                else:
                    s = HUMAN_READABLE_STEPS['Separate (extract)'][
                        language].format(**props)
            return s[0].upper() + s[1:]

        # Language not supported
        except KeyError:
            return self.name

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Get the requirements needed for this step

        Returns:
            Dict[str, Dict[str, Any]]: Step requirements
        """

        return {
            'separation_vessel': {
                'separator': True,
            }
        }
