"""
.. module:: steps_synthesis.filter
    :platforms: Unix, Windows
    :synopsis: XDL steps for using any type of Filter mechanism

"""

from typing import Optional, List, Dict, Any

# XDL
from xdl.steps.base_steps import Step, AbstractStep
from xdl.utils.misc import SanityCheck
from xdl.utils.prop_limits import (
    VOLUME_PROP_LIMIT,
    TIME_PROP_LIMIT,
    ROTATION_SPEED_PROP_LIMIT
)
from xdl.constants import VESSEL_PROP_TYPE

# Relative
from ..base_step import ChemputerStep
from ..steps_base import CMove
from ..steps_utility import (
    StopStir, StartStir, Transfer, ApplyVacuum)
from ...constants import (
    BOTTOM_PORT,
    DEFAULT_FILTER_EXCESS_REMOVE_FACTOR,
    DEFAULT_FILTER_ANTICLOGGING_ASPIRATION_SPEED,
)
# from ...utils.execution import get_vacuum_configuration, get_nearest_node
from ...constants import CHEMPUTER_WASTE

class Filter(ChemputerStep, AbstractStep):
    """Filter contents of filter vessel. Apply vacuum for given time.
    Assumes liquid is already in the top of the filter vessel.

    Args:
        filter_vessel (str): Filter vessel.
        filter_top_volume (float): Volume (mL) of contents of filter top.
        wait_time (float): Time to leave vacuum on filter vessel after contents
            have been moved. (optional)
        aspiration_speed (float): Speed in mL / min to draw liquid from
            filter_vessel.
        stir (bool): True to stir, False to stop stirring.
        stir_speed (float): Speed to stir at in RPM.
        waste_vessel (float): Given internally. Vessel to move waste material
            to.
        filtrate_vessel (str): Optional. Vessel to send filtrate to. Defaults to
            waste_vessel.
        vacuum (str): Given internally. Name of vacuum flask.
        vacuum_device (str): Given internally. Name of vacuum device attached to
            vacuum flask. Can be None if vacuum is just from fumehood vacuum
            line.
        vacuum_valve (str): Given internally. Name of valve connecting filter
            bottom to vacuum.
        valve_unused_port (str): Given internally. Random unused position on
            valve.
    """

    DEFAULT_PROPS = {
        'wait_time': '2 minutes',
        'aspiration_speed': 5,  # mL / min
        'stir': True,
        'stir_speed': '500 RPM',
        'anticlogging': False,
        'filtrate_vessel': None,
    }

    PROP_TYPES = {
        'filter_vessel': VESSEL_PROP_TYPE,
        'wait_time': float,
        'aspiration_speed': float,
        'stir': bool,
        'stir_speed': float,
        'filtrate_vessel': VESSEL_PROP_TYPE,
        'anticlogging': bool,
        'waste_vessel': str,
        'filter_top_volume': float,
        'inline_filter': bool,
        'vacuum_attached': bool
    }

    INTERNAL_PROPS = [
        'waste_vessel',
        'filter_top_volume',
        'inline_filter',
        'vacuum_attached',
    ]

    PROP_LIMITS = {
        'wait_time': TIME_PROP_LIMIT,
        'stir_speed': ROTATION_SPEED_PROP_LIMIT,
        'filter_top_volume': VOLUME_PROP_LIMIT,
    }

    def __init__(
        self,
        filter_vessel: str,
        wait_time: Optional[float] = 'default',
        aspiration_speed: Optional[float] = 'default',
        stir: Optional[bool] = 'default',
        stir_speed: Optional[float] = 'default',
        filtrate_vessel: Optional[str] = 'default',
        anticlogging: Optional[bool] = 'default',

        # Internal properties
        waste_vessel: Optional[str] = None,
        filter_top_volume: Optional[float] = 0,
        inline_filter: Optional[bool] = False,
        vacuum_attached: Optional[bool] = False,
        **kwargs
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain waste vessel if not defined
        if not self.waste_vessel:
            self.waste_vessel = get_nearest_node(
                graph, self.filter_vessel, CHEMPUTER_WASTE
            )

        # Get the filter vessel from the graph
        filter_vessel = graph.nodes[self.filter_vessel]

        # Determine if an in-line filter is present
        if (filter_vessel['class'] != 'ChemputerFilter'
                and ('can_filter' in filter_vessel
                     and filter_vessel['can_filter'] is True)):
            self.inline_filter = True

        # Check a vacuum is attached
        if get_vacuum_configuration(graph, self.filter_vessel)['source']:
            self.vacuum_attached = True

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        # Normal filtering in ChemputerFilter
        if not self.inline_filter:
            return self.get_normal_filtering_steps()

        else:
            # Inline filtering in reactor or rotavap with vacuum
            if self.vacuum_attached:
                return self.get_inline_filtering_with_vacuum_steps()

            # Inline filtering in reactor or rotavap without vacuum
            else:
                return self.get_inline_filtering_without_vacuum_steps()

    def get_normal_filtering_steps(self) -> List[Step]:
        """Get the normal filtering steps when ChemputerFilter is attached to
        a vacuum.

        Returns:
            List[Step]: List of filtering steps
        """

        return (
            self.get_initial_stir()
            + self.get_normal_filter_liquid_transfer()
            + self.get_vacuum_stop_stir()
            + self.apply_vacuum(port=BOTTOM_PORT)
        )

    def get_inline_filtering_with_vacuum_steps(self) -> List[Step]:
        """Get the inline filtering steps when a reactor or rotavap is
        attached to vacuum.

        Returns:
            List[Step]: Filtering steps
        """

        return (
            self.get_initial_stir()
            + self.get_inline_filter_to()
            + self.get_vacuum_stop_stir()
            + self.apply_vacuum()
        )

    def get_inline_filtering_without_vacuum_steps(self) -> List[Step]:
        """Get the inline filtering steps when a reactor or rotavap has no
        vacuum attached.

        Returns:
            List[Step]: Filtering steps
        """

        return (
            self.get_initial_stir()
            + self.get_inline_filter_to()
        )

    def get_normal_filter_liquid_transfer(self) -> List[Step]:
        """Moves liquid from the filter vessel to the filtrate vessel

        Returns:
            List[Step]: Movement step
        """

        return [
            CMove(
                from_vessel=self.filter_vessel,
                to_vessel=self.get_filtrate_vessel(),
                from_port=BOTTOM_PORT,
                volume=(
                    self.filter_top_volume * DEFAULT_FILTER_EXCESS_REMOVE_FACTOR
                ),
                aspiration_speed=self.get_aspiration_speed()
            )
        ]

    def get_inline_filter_to(self) -> List[Step]:
        """Get the inline FilterTo step

        Returns:
            List[Step]: FilterTo Step
        """

        return [
            FilterTo(
                from_vessel=self.filter_vessel, to_vessel=self.filtrate_vessel
            )
        ]

    def get_start_stir(self) -> Step:
        """Get the StartStir step

        Returns:
            Step: StartStir step
        """

        return StartStir(vessel=self.filter_vessel, stir_speed=self.stir_speed)

    def get_stop_stir(self) -> Step:
        """Get the StopStir step

        Returns:
            Step: StopStir step
        """

        return StopStir(vessel=self.filter_vessel)

    def get_initial_stir(self) -> List[Step]:
        """Get the StartStir or StopStir step dependent on the stir flag

        Returns:
            List[Step]: StartStir or StopStir step
        """

        return (
            [self.get_start_stir()]
            if self.stir is True else [self.get_stop_stir()]
        )

    def get_vacuum_stop_stir(self) -> Optional[List[Step]]:
        """Get the StopStir step for the vacuum

        Returns:
            Optional[List[Step]]: StopStir step if required, else []
        """

        # Stirring already stopped at start of step
        if self.stir is False:
            return []

        # Using filtrate so no point drying solid.
        elif (self.filtrate_vessel is not None
                and self.filtrate_vessel != self.waste_vessel):
            return []

        else:
            return [self.get_stop_stir()]

    def apply_vacuum(self, port: Optional[str] = None) -> Optional[List[Step]]:
        """Get an ApplyVacuum step if required

        Args:
            port (Optional[str], optional): Vacuum port. Defaults to None.

        Returns:
            Optional[List[Step]]: ApplyVacuum step if required, else []s
        """

        # Using filtrate so no point drying solid.
        if (self.filtrate_vessel is not None
                and self.filtrate_vessel != self.waste_vessel):
            return []

        else:
            return [
                ApplyVacuum(
                    vessel=self.filter_vessel,
                    time=self.wait_time,
                    port=port
                )
            ]

    def get_aspiration_speed(self) -> float:
        """Get the aspiration speed for this step

        Returns:
            float: Aspiration speed
        """
        return (
            self.aspiration_speed if not self.anticlogging
            else DEFAULT_FILTER_ANTICLOGGING_ASPIRATION_SPEED
        )

    def get_filtrate_vessel(self) -> str:
        """Get the vessel to use for Filtrate

        Returns:
            str: Filtrate vessel
        """

        return (
            self.filtrate_vessel if self.filtrate_vessel else self.waste_vessel
        )

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Get the requirements needed for this step

        Returns:
            Dict[str, Dict[str, Any]]: Step requirements
        """

        return {
            'filter_vessel': {
                'filter': True
            }
        }

class FilterTo(ChemputerStep, AbstractStep):
    """FilterTo step.
    Move filtrate from one Filter to another

    Args:
        from_vessel (str): Vessel filtering from
        to_vessel (str): Vessel filtering to
    """

    PROP_TYPES = {
        'from_vessel': VESSEL_PROP_TYPE,
        'to_vessel': VESSEL_PROP_TYPE,
    }

    def __init__(
        self,
        from_vessel: str,
        to_vessel: str,
    ):
        super().__init__(locals())

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """
        return [
            Transfer(
                from_vessel=self.from_vessel,
                to_vessel=self.to_vessel,
                volume='all',
            )
        ]

    def sanity_checks(self, graph: Dict) -> List[SanityCheck]:
        """Gets a list of Sanity checks to perform for the step

        Args:
            graph (Dict): Chemputer graph to check

        Returns:
            List[SanityCheck]: List of checks to perform
        """

        # Get all information for the from_vessel node
        full_node = graph.nodes[self.from_vessel]

        return [
            SanityCheck(
                condition='can_filter' in full_node and full_node['can_filter'],
                error_msg=f"from_vessel ({self.from_vessel}) doesn't have\
 can_filter property == True"
            ),

            SanityCheck(
                condition=self.from_vessel != self.to_vessel,
                error_msg=f"from_vessel and to_vessel can't be the same node\
 ({self.from_vessel})."
            )
        ]
