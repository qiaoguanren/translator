"""
.. module:: steps_utility.purge
    :platforms: Unix, Windows
    :synopsis: XDL steps related to purging the system with gases

"""

from typing import Dict, List, Optional

# XDL
from xdl.steps.base_steps import Step
from xdl.steps.base_steps import AbstractStep
from xdl.constants import INERT_GAS_SYNONYMS, VESSEL_PROP_TYPE
from xdl.utils.misc import SanityCheck
from xdl.utils.prop_limits import TIME_PROP_LIMIT

# Relative
from .general import Wait
from ..steps_utility.pneumatic_controller import SwitchArgon
from ..steps_base import CConnect, CValveMoveToPosition
from ..base_step import ChemputerStep
from ..steps_utility.cleaning import CleanBackboneDeprecated
# from ...utils.execution import (
#     get_vacuum_configuration, get_pneumatic_controller, node_in_graph
# )
from ...utils.prop_limits import VALVE_PORT_PROP_LIMIT

class StartPurge(ChemputerStep, AbstractStep):

    INTERNAL_PROPS = [
        'pneumatic_controller',
        'inert_gas'
    ]

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'pneumatic_controller': str,
        'inert_gas': str
    }

    def __init__(
        self,
        vessel: str,

        # Internal properties
        pneumatic_controller: str = None,
        inert_gas: str = None,
        **kwargs,
    ):
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Reset the pneumatic controller and gas to None
        self.pneumatic_controller = self.inert_gas = None

        # Obtain the pneumatic controller from the graph
        self.pneumatic_controller, _ = get_pneumatic_controller(
            graph, self.vessel
        )

        # No pneumatic controller was found
        if not self.pneumatic_controller:
            # Get the vacuum information
            vacuum_info = get_vacuum_configuration(graph, self.vessel)

            # Still no pneumatic controller or inert gas
            if not self.pneumatic_controller and not self.inert_gas:
                # Set to valve connected to inert gas line
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
                condition=self.pneumatic_controller or self.inert_gas,
                error_msg=f'Cannot find pneumatic controller or inert gas connected to\
 {self.vessel} so cannot purge.'
            )
        ]

    def get_steps(self) -> Optional[List[Step]]:
        """Get the list of steps/base steps to execute.

        Returns:
            Optional[List[Step]]: Steps to execute. None if no method to purge
        """

        # Pneumatic controller is used, use argon line
        if self.pneumatic_controller:
            return [
                SwitchArgon(
                    vessel=self.vessel,
                    pressure='high',
                    after_switch_wait=None,
                ),
            ]

        # Using inert gas valve, switch valve to position
        elif self.inert_gas:
            return [
                CConnect(
                    from_vessel=self.inert_gas,
                    to_vessel=self.vessel,
                ),
            ]

        # No way to purge, return nothing
        else:
            return []

class StopPurge(ChemputerStep, AbstractStep):

    INTERNAL_PROPS = [
        'pneumatic_controller',
        'inert_gas',
        'inert_gas_valve',
        'inert_gas_valve_unused_port',
    ]

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'pneumatic_controller': str,
        'inert_gas': str,
        'inert_gas_valve': str,
        'inert_gas_valve_unused_port': int
    }

    PROP_LIMITS = {
        'inert_gas_valve_unused_port': VALVE_PORT_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,

        # Internal properties
        pneumatic_controller: str = None,
        inert_gas: str = None,
        inert_gas_valve: str = None,
        inert_gas_valve_unused_port: str = None,
        **kwargs
    ):
        super().__init__(locals())

    def sanity_checks(self, graph: Dict):
        """Gets a list of Sanity checks to perform for the step

        Args:
            graph (Dict): Chemputer graph to check

        Returns:
            List[SanityCheck]: List of checks to perform
        """

        return [
            SanityCheck(
                condition=self.pneumatic_controller or self.inert_gas,
                error_msg=f'Cannot find pneumatic controller or inert gas connected to\
 {self.vessel} so cannot purge.'
            ),

            SanityCheck(
                condition=node_in_graph(graph, self.vessel),
                error_msg=f'Unable to find {self.vessel} in graph.'
            )
        ]

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Reset the pneumatic controller and inert gas to None
        self.pneumatic_controller = self.inert_gas = None

        # Obtian the pneumatic controller from the graph
        self.pneumatic_controller, _ = get_pneumatic_controller(
            graph, self.vessel
        )

        # No pneumatic controller found
        if not self.pneumatic_controller:
            # Get vacuum information form the graph instead
            vacuum_info = get_vacuum_configuration(graph, self.vessel)

            # Obtain inert gas if not defined from vacuum info
            if not self.inert_gas:
                self.inert_gas = vacuum_info['valve_inert_gas']

            # Obtain inert gas valve if not defined from vacuum info
            if not self.inert_gas_valve:
                self.inert_gas_valve = vacuum_info['valve']

            # Obtian the unused port on the inert gas valve from vacuum info
            if self.inert_gas_valve_unused_port is None:
                self.inert_gas_valve_unused_port = vacuum_info[
                    'valve_unused_port'
                ]

    def get_steps(self) -> Optional[List[Step]]:
        """Get the list of steps/base steps to execute.

        Returns:
            Optional[List[Step]]: Steps to execute.
        """

        # Using pneumatic controller, switch to Argon
        if self.pneumatic_controller:
            return [
                SwitchArgon(
                    vessel=self.vessel,
                    pressure='low',
                    after_switch_wait=None,
                )
            ]

        # Using inert gas valve
        elif self.inert_gas:
            return [
                CValveMoveToPosition(
                    valve_name=self.inert_gas_valve,
                    position=self.inert_gas_valve_unused_port
                )
            ]

        # No method to purge, return nothing
        else:
            return []

class Purge(ChemputerStep, AbstractStep):

    DEFAULT_PROPS = {
        'time': '5 minutes',
    }

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'time': float
    }

    PROP_LIMITS = {
        'time': TIME_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,
        time: float = 'default',
        **kwargs,
    ):
        super().__init__(locals())

    def sanity_checks(self, graph: Dict) -> List[SanityCheck]:
        """Gets a list of Sanity checks to perform for the step

        Args:
            graph (Dict): Chemputer graph to check

        Returns:
            List[SanityCheck]: List of checks to perform
        """

        return [
            SanityCheck(
                condition=node_in_graph(graph, self.vessel),
                error_msg=f'Unable to find {self.vessel} in graph.',
            ),
            SanityCheck(
                condition=self.time > 0,
                error_msg='Purge time must be > 0.'
            )
        ]

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        return

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        return [
            StartPurge(vessel=self.vessel),
            Wait(time=self.time),
            StopPurge(vessel=self.vessel)
        ]

class PurgeBackbone(ChemputerStep, AbstractStep):

    PROP_TYPES = {
        'purge_gas': str
    }

    DEFAULT_PROPS = {
        'purge_gas': None,
    }

    def __init__(
        self,
        purge_gas: str = 'default',
        **kwargs
    ):
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Purge gas is defined
        if self.purge_gas is None:
            # Iterate through all nodes in the graph
            for _, data in graph.nodes(data=True):
                # Current node is an inert gas flask, set the purge gas to that
                if (data['class'] == 'ChemputerFlask'
                        and data['chemical'] in INERT_GAS_SYNONYMS):
                    self.purge_gas = data['chemical']
                    break

    def sanity_checks(self, graph: Dict) -> List[SanityCheck]:
        """Gets a list of Sanity checks to perform for the step

        Args:
            graph (Dict): Chemputer graph to check

        Returns:
            List[SanityCheck]: List of checks to perform
        """

        return [
            SanityCheck(
                condition=self.purge_gas,
            ),
        ]

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        return [
            CleanBackboneDeprecated(
                solvent=self.purge_gas,
            )
        ]
