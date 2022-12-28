"""
.. module:: steps_utility.evacuate
    :platforms: Unix, Windows
    :synopsis: XDL steps to deal with evacuating a vessel with an inert gas
                or vacuum

"""

from typing import Optional, Dict, List
from xdl.steps.base_steps import AbstractStep, Step
from ..base_step import ChemputerStep
from ..steps_utility import (
    Wait, StartVacuum, StopVacuum, SwitchArgon, SwitchVacuum)
from ..steps_base import CConnect
from xdl.steps.special_steps import Repeat
from xdl.constants import VESSEL_PROP_TYPE
# from ...utils.execution import (
#     get_pneumatic_controller, get_vacuum_configuration, get_vessel_type)
from xdl.utils.misc import SanityCheck
from xdl.utils.prop_limits import TIME_PROP_LIMIT, PRESSURE_PROP_LIMIT
from ...utils.prop_limits import VESSEL_TYPE_PROP_LIMIT

class Evacuate(ChemputerStep, AbstractStep):
    """Evacuate given vessel with inert gas.

    Args:
        vessel (str): Vessel to evacuate with inert gas.
        evacuations (int): Number of evacuations to perform. Defaults to 3.
        after_inert_gas_wait_time (int): Time to wait for after connecting to
            inert gas. Defaults to 1 min.
        after_vacuum_wait_time (int): Time to wait for after connecting to
            vacuum. Defaults to 1 min.
        inert_gas (str): Internal property. Inert gas flask.
        vacuum (str): Internal property. Valve connected to vacuum.
    """

    DEFAULT_PROPS = {
        'after_inert_gas_wait_time': '1 minute',
        'after_vacuum_wait_time': '1 minute',
        'evacuations': 3,
        'vacuum_pressure': '50 mbar',
    }

    INTERNAL_PROPS = [
        'inert_gas',
        'vacuum',
        'vacuum_device',
        'vessel_type',
        'pneumatic_controller',
    ]

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'evacuations': int,
        'after_inert_gas_wait_time': float,
        'after_vacuum_wait_time': float,
        'vacuum_pressure': float,
        'inert_gas': str,
        'vacuum': str,
        'vacuum_device': str,
        'vessel_type': str,
        'pneumatic_controller': str
    }

    PROP_LIMITS = {
        'after_inert_gas_wait_time': TIME_PROP_LIMIT,
        'after_vacuum_wait_time': TIME_PROP_LIMIT,
        'vacuum_pressure': PRESSURE_PROP_LIMIT,
        'vessel_type': VESSEL_TYPE_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,
        evacuations: int = 'default',
        after_inert_gas_wait_time: Optional[float] = 'default',
        after_vacuum_wait_time: Optional[float] = 'default',
        vacuum_pressure: Optional[float] = 'default',

        # Internal properties
        inert_gas: Optional[str] = None,
        vacuum: Optional[str] = None,
        vacuum_device: Optional[str] = None,
        vessel_type: Optional[str] = None,
        pneumatic_controller: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain the pneumatic controller if not defined
        self.pneumatic_controller, _ = get_pneumatic_controller(
            graph, self.vessel
        )

        # Obtaint he vessel type if not defined
        if not self.vessel_type:
            self.vessel_type = get_vessel_type(graph, self.vessel)

        # Get the vacuum information
        vacuum_info = get_vacuum_configuration(graph, self.vessel)

        # Obtain the vacuum if not defined frm the vacuum info
        if not self.vacuum:
            self.vacuum = vacuum_info['source']

        # Obtain the vacuum device if not defined from the vacuum info
        if not self.vacuum_device:
            self.vacuum_device = vacuum_info['device']

        # Obtain the inert gas if not defined from the vacuum info
        if not self.inert_gas:
            self.inert_gas = vacuum_info['valve_inert_gas']

    def sanity_checks(self, graph: Dict) -> List[SanityCheck]:
        """Gets a list of Sanity checks to perform for the step

        Args:
            graph (Dict): Chemputer graph to check

        Returns:
            List[SanityCheck]: List of checks to perform
        """

        return [
            SanityCheck(
                self.pneumatic_controller or (self.vacuum and self.inert_gas),
                f'Cannot find pneumatic controller or vacuum and inert gas\
 connected to {self.vessel}. No way to perform evacuation.',
            ),
        ]

    def get_steps(self) -> Optional[List[Step]]:
        """Get the list of steps/base steps to execute.

        Returns:
            Optional[List[Step]]: Steps to execute. None if no vacuum or gas
        """

        # Get the Steps using the pneumatic controller
        if self.pneumatic_controller:
            return self.get_pneumatic_controller_steps()

        # Get the steps using thew vacuum and inert gas
        elif self.vacuum and self.inert_gas:
            return self.get_vacuum_inert_gas_valve_steps()

        # No steps
        else:
            return []

    def get_vacuum_inert_gas_valve_steps(self) -> List[Step]:
        """Get list of steps to evacuate a vessel with vacuum and inert gas

        Returns:
            List[Step]: Steps to execute
        """

        # Get the vacuum vessel
        vacuum_vessel = (
            self.vessel if self.vessel_type == 'rotavap' else self.vacuum
        )

        # Have a vacuum device
        if self.vacuum_device:
            steps = [
                # Start the vacuum
                StartVacuum(
                    vessel=vacuum_vessel, pressure=self.vacuum_pressure
                ),

                # Connect the vessel to the vacuum
                CConnect(self.vessel, self.vacuum),

                # Wait for evacuation
                Wait(self.after_vacuum_wait_time * 2),

                # Connect vessel to inert gas line
                CConnect(self.inert_gas, self.vessel),

                # Wait for purge of inert gas
                Wait(self.after_inert_gas_wait_time),

                # Repeat for the evacuation and inert gas purge for the total
                # number of evacuations required
                Repeat(
                    repeats=self.evacuations - 1,
                    children=[
                        CConnect(self.vessel, self.vacuum),
                        Wait(self.after_vacuum_wait_time),
                        CConnect(self.inert_gas, self.vessel),
                        Wait(self.after_inert_gas_wait_time),
                    ]
                ),

                # Finally stop the vacuum
                StopVacuum(vessel=vacuum_vessel)
            ]

        # No vacuum device
        else:
            # Steps are a repeat of the connection to vacuum and inert gas
            steps = [
                Repeat(
                    repeats=self.evacuations,
                    children=[
                        CConnect(self.vessel, self.vacuum),
                        Wait(self.after_vacuum_wait_time),
                        CConnect(self.inert_gas, self.vessel),
                        Wait(self.after_inert_gas_wait_time),
                    ]
                )
            ]

        return steps

    def get_pneumatic_controller_steps(self) -> List[Step]:
        """Get steps related to using the Pneumatic controller for
        evacuations.

        Returns:
            List[Step]: Steps to execute
        """

        steps = [
            # Repeat steps of switching to vacuum and switching to Argon
            Repeat(
                repeats=self.evacuations,
                children=[
                    SwitchVacuum(
                        vessel=self.vessel,
                        after_switch_wait=self.after_vacuum_wait_time
                    ),
                    SwitchArgon(
                        vessel=self.vessel,
                        pressure='high',
                        after_switch_wait=self.after_inert_gas_wait_time
                    )
                ]
            ),

            # End with finally switching to Argon
            SwitchArgon(
                vessel=self.vessel,
                pressure='low',
            ),
        ]

        return steps

    def human_readable(self, language: str = 'en') -> str:
        """Get the Human-readable text for this step.

        Args:
            language (str, optional): Localisation language. Defaults to 'en'.

        Returns:
            str: Human-readable text for the step.
        """

        return f'Perform {self.evacuations} evacuations of {self.vessel} with\
 inert gas.'
