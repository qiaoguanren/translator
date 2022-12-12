"""
.. module:: steps_utility.modular_wheel
    :platforms: Unix, Windows
    :synopsis: XDL steps to interact with the Modular Wheel system

"""

from typing import Optional, Dict, List

# XDL
from xdl.utils.misc import SanityCheck
from xdl.steps.base_steps import Step
from xdl.steps.base_steps import AbstractStep
from xdl.utils.prop_limits import VOLUME_PROP_LIMIT
from xdl.constants import VESSEL_PROP_TYPE

# Relative
from .liquid_handling import Transfer
from ..base_step import ChemputerStep
from ..steps_base.commanduino_labware import CTurnMotor
from ...utils.execution import node_in_graph

class MWAddAndTurn(ChemputerStep, AbstractStep):
    """Step for transfering liquid to the modular wheel and rotating it.

    Args:
        from_vessel (str): Vessel to move the liquid from
        to_vessel (str): Vessel to move the liquid to
        volume (float, optional): Volume to transfer
        motor_name (str, optional): Name of the motor on the modular wheel
        n_turns (int, optional): Number of turns to perform
    """

    DEFAULT_PROPS = {
        'volume': '25 mL',
        'n_turns': 1,
    }

    INTERNAL_PROPS = [
        'motor_name',
    ]

    PROP_TYPES = {
        'from_vessel': VESSEL_PROP_TYPE,
        'to_vessel': VESSEL_PROP_TYPE,
        'volume': float,
        'motor_name': str,
        'n_turns': int
    }

    PROP_LIMITS = {
        'volume': VOLUME_PROP_LIMIT,
    }

    def __init__(
        self,
        from_vessel: str,
        to_vessel: str,
        volume: Optional[float] = 'default',
        n_turns: Optional[int] = 'default',

        # Internal properties
        motor_name: Optional[str] = None,
        **kwargs
    ):
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain motor_name if not defined
        if not self.motor_name:
            self.motor_name = graph.nodes[self.to_vessel]['motor_name']

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        return [
            Transfer(
                from_vessel=self.from_vessel,
                to_vessel=self.to_vessel,
                volume=self.volume),
            CTurnMotor(
                device_name=self.to_vessel,
                motor_name=self.motor_name,
                n_turns=self.n_turns
            )
        ]

    def sanity_checks(self, graph: Dict) -> List[SanityCheck]:
        """Gets a list of Sanity checks to perform for the step

        Args:
            graph (Dict): Chemputer graph to check

        Returns:
            List[SanityCheck]: List of checks to perform
        """

        return [
            SanityCheck(
                condition=self.from_vessel and node_in_graph(
                    graph, self.from_vessel),
                error_msg="from_vessel must be node in the graph"
            ),
            SanityCheck(
                condition=self.to_vessel and node_in_graph(
                    graph, self.to_vessel),
                error_msg="to_vessel must be node in the graph"
            ),
            SanityCheck(
                condition=(0 <= self.volume < 100),
                error_msg="Volume must be between 0 and 100 mL"
            )
        ]
