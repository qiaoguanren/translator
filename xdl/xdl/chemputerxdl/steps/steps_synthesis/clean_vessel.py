"""
.. module:: steps_synthesis.clean_vessel
    :platforms: Unix, Windows
    :synopsis: XDL Step for cleaning a vessel

"""

from typing import Optional, Dict, List

# XDL
from xdl.steps import Step
from xdl.steps.base_steps import AbstractStep
from xdl.constants import VESSEL_PROP_TYPE, REAGENT_PROP_TYPE
from xdl.utils.misc import SanityCheck
from xdl.utils.prop_limits import (
    TIME_PROP_LIMIT,
    TEMP_PROP_LIMIT,
    ROTATION_SPEED_PROP_LIMIT,
    VOLUME_PROP_LIMIT,
)
from xdl.utils.graph import undirected_neighbors

# Relative
from .dry import Dry
from ..base_step import ChemputerStep
from ..steps_utility import (
    StartStir,
    StopStir,
    Wait,
    HeatChillToTemp,
    HeatChillReturnToRT
)
from ..steps_base import CMove
# from ...utils.execution import (
#     get_vacuum_configuration,
#     get_nearest_node,
#     get_reagent_vessel,
#     get_heater_chiller,
#     get_vessel_type,
# )
from ...constants import CHEMPUTER_WASTE, STIRRER_CLASSES
from ...utils.prop_limits import VESSEL_TYPE_PROP_LIMIT

class CleanVessel(ChemputerStep, AbstractStep):
    """Clean given vessel with given solvent.

    Args:
        vessel (str): Vessel to clean.
        solvent (str): Solvent to clean vessel with.
        stir_time (float): Time to stir for after solvent is added.
        stir_speed (float): Speed to stir at in RPM.
        volume (float): Volume of solvent to use. If not supplied will be
            given internally according to vessel max volume.
        cleans (int): Number of cleans to do.
        solvent_vessel (str): Given internally. Flask containing solvent.
        waste_vessel (str): Given internally. Vessel to send waste solvent
            to.
        vacuum (str): Internal property. Used to tell if drying is possible.
    """

    DEFAULT_PROPS = {
        'temp': None,
        'volume': None,
        'stir_time': '1 minute',
        'stir_speed': '500 RPM',
        'dry': False,
        'cleans': 2,
    }

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'solvent': REAGENT_PROP_TYPE,
        'stir_time': float,
        'stir_speed': float,
        'temp': float,
        'dry': bool,
        'volume': float,
        'cleans': int,
        'solvent_vessel': str,
        'waste_vessel': str,
        'vacuum': str,
        'vessel_type': str,
        'heater': str,
        'chiller': str,
        'has_stirrer': bool,
    }

    INTERNAL_PROPS = [
        'solvent_vessel',
        'waste_vessel',
        'vacuum',
        'vessel_type',
        'heater',
        'chiller',
        'has_stirrer',
    ]

    PROP_LIMITS = {
        'stir_time': TIME_PROP_LIMIT,
        'stir_speed': ROTATION_SPEED_PROP_LIMIT,
        'temp': TEMP_PROP_LIMIT,
        'volume': VOLUME_PROP_LIMIT,

        'vessel_type': VESSEL_TYPE_PROP_LIMIT,
    }

    DO_NOT_SCALE = True

    #: Fraction of vessel max volume to use as solvent volume in CleanVessel
    # step.
    CLEAN_VESSEL_VOLUME_FRACTION: float = 0.5

    def __init__(
        self,
        vessel: str,
        solvent: str,
        stir_time: Optional[float] = 'default',
        stir_speed: Optional[float] = 'default',
        temp: Optional[float] = 'default',
        dry: Optional[bool] = 'default',
        volume: Optional[float] = 'default',
        cleans: Optional[int] = 'default',

        # Internal properties
        solvent_vessel: Optional[str] = None,
        waste_vessel: Optional[str] = None,
        vacuum: Optional[str] = None,
        vessel_type: Optional[str] = None,
        heater: Optional[str] = None,
        chiller: Optional[str] = None,
        has_stirrer: Optional[bool] = False,
        **kwargs
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain volume is not defined
        if self.volume is None:
            self.volume = (
                graph.nodes[self.vessel]['max_volume']
                * self.CLEAN_VESSEL_VOLUME_FRACTION
            )

        # Obtain vessel type if not defined
        if not self.vessel_type:
            self.vessel_type = get_vessel_type(graph, self.vessel)

        # Obtain the heater and chiller attached to current vessel
        self.heater, self.chiller = get_heater_chiller(graph, self.vessel)

        # Obtain waste vessel if not defined
        if not self.waste_vessel:
            self.waste_vessel = get_nearest_node(
                graph, self.vessel, CHEMPUTER_WASTE)

        # Obtain solvent vessel if not defined
        if not self.solvent_vessel:
            self.solvent_vessel = get_reagent_vessel(graph, self.solvent)

        # Obtain vacuum configuration
        vacuum_info = get_vacuum_configuration(graph, self.vessel)

        # Vacuum is present as a source
        if vacuum_info['source']:
            # Set dry flag
            self.dry = True

            # Obtian vacuum if not defined
            if not self.vacuum:
                self.vacuum = vacuum_info['source']

        # Iterate through all nodes in the graph
        for node in graph.nodes():
            # Found a ChemputerFlask
            if graph.nodes[node]['class'] == 'ChemputerFlask':
                # Node's chemical matches out solvent, set solvent vessel
                if graph.nodes[node]['chemical'] == self.solvent:
                    self.solvent_vessel = node
                    break

        # Check for attached heaters
        self.check_for_heater()

        # Check for stirrer
        for _, data in undirected_neighbors(graph, self.vessel, data=True):
            if data['class'] in STIRRER_CLASSES:
                self.has_stirrer = True

    def check_for_heater(self):
        """Checks if a heater is present
        """

        # Set temp to None if temp is defined but no heater/chiller set
        if (
                self.temp is not None and not (
                    self.heater or self.chiller or self.vessel_type == 'rotavap'
                )
        ):
            self.temp = None

    def sanity_checks(self, graph: Dict) -> List[SanityCheck]:
        """Gets a list of Sanity checks to perform for the step

        Args:
            graph (Dict): Chemputer graph to check

        Returns:
            List[SanityCheck]: List of checks to perform
        """

        return [
            SanityCheck(
                condition=self.solvent_vessel,
                error_msg=f'No solvent vessel found in graph for {self.solvent}'
            ),

            SanityCheck(
                condition=self.waste_vessel,
                error_msg=f'No waste vessel found for "{self.vessel}".'
            ),

            SanityCheck(
                condition=self.cleans > 0,
                error_msg=f'`cleans` property must be > 0. {self.cleans} is an\
 invalid value.'
            ),

            SanityCheck(
                condition=self.volume and self.volume > 0,
                error_msg=f'`volume` must be > 0. {self.volume} is an invalid\
 value.'
            ),
        ]

    def get_steps(self) -> List[Step]:
        """Get the list of steps to execute

        Returns:
            List[Step]: Steps to execute
        """

        # List to hold steps
        steps = []

        # Iterate through total number of cleans to perform
        for _ in range(self.cleans):
            steps.extend(
                # Get the StartStir steps
                self.get_start_stir_steps()

                # Append movement steps
                + [
                    CMove(
                        from_vessel=self.solvent_vessel,
                        to_vessel=self.vessel,
                        volume=self.volume
                    ),
                    Wait(time=self.stir_time),
                    CMove(
                        from_vessel=self.vessel,
                        to_vessel=self.waste_vessel,
                        volume=self.volume
                    ),
                ]

                # Get the StopStir steps
                + self.get_stop_stir_steps()
            )

        # Dry flag is set, add a Dry step
        if self.dry:
            steps.append(Dry(vessel=self.vessel))

        # Temperature is defined, add steps to ramp up/down temp
        if self.temp is not None and (self.temp < 20 or self.temp > 25):
            steps.insert(
                1, HeatChillToTemp(vessel=self.vessel, temp=self.temp)
            )

            steps.append(HeatChillReturnToRT(vessel=self.vessel, stir=False))

        # Return all steps
        return steps

    def get_start_stir_steps(self) -> List[Optional[Step]]:
        """Get steps associated with starting stirring

        Returns:
            List[Optional[Step]]: Steps for StartStir
        """

        # Stirrer is defined, add StartStir
        if self.has_stirrer:
            return [StartStir(vessel=self.vessel)]

        # Default to no steps
        return []

    def get_stop_stir_steps(self) -> List[Optional[Step]]:
        """Get steps associated with stopping stirring.

        Returns:
            List[Optional[Step]]: Steps for StopStir
        """

        # Stirrer is defined, add StopStir
        if self.has_stirrer:
            return [StopStir(vessel=self.vessel)]

        # Default to no steps
        return []
