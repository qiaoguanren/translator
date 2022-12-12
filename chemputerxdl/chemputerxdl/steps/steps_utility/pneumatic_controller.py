"""
.. module:: steps_utility.pneumatic_controller
    :platforms: Unix, Windows
    :synopsis: XDL steps to interface with Pneumatic controller panel to
                control vacuum and inert gas.

"""

from typing import Dict, List

# XDL
from xdl.steps.base_steps import Step
from xdl.steps.base_steps import AbstractStep
from xdl.utils.prop_limits import TIME_PROP_LIMIT
from xdl.constants import VESSEL_PROP_TYPE

# Relative
from .general import Wait
from ..base_step import ChemputerStep
from ..steps_base import CSwitchVacuum, CSwitchArgon
from ...utils.execution import get_pneumatic_controller
from ...utils.prop_limits import (
    PORT_PROP_LIMIT,
    PNEUMATIC_CONTROLLER_PORT_PROP_LIMIT,
    PNEUMATIC_CONTROLLER_PRESSURE_PROP_LIMIT,
)
from ...constants import PORT_PROP_TYPE

#: Time to wait after switching between argon/vacuum for pressure to change.
WAIT_AFTER_SWITCH_TIME = 30  # s

class SwitchVacuum(ChemputerStep, AbstractStep):
    """Supply given vessel with vacuum using PneumaticController.

    Args:
        vessel (str): Vessel to supply with vacuum.
        port (str): Port of vessel to supply with vacuum.
        pneumatic_controller (str): Internal property. Node name of pneumatic
            controller.
        pneumatic_controller_port (str): Internal property. Port of pneumatic
            controller attached to correct port of vessel.
    """

    DEFAULT_PROPS = {
        'after_switch_wait': '30 seconds',
        'port': None,
    }

    INTERNAL_PROPS = [
        'pneumatic_controller',
        'pneumatic_controller_port',
    ]

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'port': PORT_PROP_TYPE,
        'after_switch_wait': float,
        'pneumatic_controller': str,
        'pneumatic_controller_port': int
    }

    PROP_LIMITS = {
        'port': PORT_PROP_LIMIT,
        'after_switch_wait': TIME_PROP_LIMIT,
        'pneumatic_controller_port': PNEUMATIC_CONTROLLER_PORT_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,
        port: str = 'default',
        after_switch_wait: float = 'default',

        # Internal properties
        pneumatic_controller: str = None,
        pneumatic_controller_port: str = None,
        **kwargs,
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain the pneumatic controller if not defined
        if not self.pneumatic_controller:
            self.pneumatic_controller, self.pneumatic_controller_port =\
                get_pneumatic_controller(graph, self.vessel, self.port)

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        steps = [
            CSwitchVacuum(
                pneumatic_controller=self.pneumatic_controller,
                port=self.pneumatic_controller_port
            ),
        ]

        # Add Wait step if the wait flag is set
        if self.after_switch_wait:
            steps.append(
                Wait(time=self.after_switch_wait)
            )

        return steps

class SwitchArgon(ChemputerStep, AbstractStep):
    """Supply given vessel with argon using PneumaticController.

    Args:
        vessel (str): Vessel to supply with argon.
        port (str): Port of vessel to supply with argon.
        pressure (str): Argon pressure. 'high' or 'low'. Defaults to 'low'.
        pneumatic_controller (str): Internal property. Node name of pneumatic
            controller.
        pneumatic_controller_port (str): Internal property. Port of pneumatic
            controller attached to correct port of vessel.
    """

    DEFAULT_PROPS = {
        'after_switch_wait': '30 seconds',
        'port': None,
        'pressure': 'low',
    }

    INTERNAL_PROPS = [
        'pneumatic_controller',
        'pneumatic_controller_port',
    ]

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'port': PORT_PROP_TYPE,
        'pressure': str,
        'after_switch_wait': float,
        'pneumatic_controller': str,
        'pneumatic_controller_port': int
    }

    PROP_LIMITS = {
        'port': PORT_PROP_LIMIT,
        'after_switch_wait': TIME_PROP_LIMIT,
        'pneumatic_controller_port': PNEUMATIC_CONTROLLER_PORT_PROP_LIMIT,
        'pressure': PNEUMATIC_CONTROLLER_PRESSURE_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,
        port: str = 'default',
        pressure: str = 'default',
        after_switch_wait: float = 'default',

        # Internal properties
        pneumatic_controller: str = None,
        pneumatic_controller_port: str = None,
        **kwargs,
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain the pneumatic controller if not defined
        if not self.pneumatic_controller:
            self.pneumatic_controller, self.pneumatic_controller_port =\
                get_pneumatic_controller(graph, self.vessel, self.port)

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        steps = [
            CSwitchArgon(
                pneumatic_controller=self.pneumatic_controller,
                port=self.pneumatic_controller_port,
                pressure=self.pressure
            )
        ]

        # Add Wait if wait flag is set
        if self.after_switch_wait:
            steps.append(
                Wait(time=self.after_switch_wait)
            )

        return steps
