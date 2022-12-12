"""
.. module:: steps_utility.stirring
    :platforms: Unix, Windows
    :synopsis: XDL steps to interact with stirring hardware

"""

from typing import Optional, Dict, Any, List

# XDL
from xdl.steps.base_steps import AbstractStep, Step
from xdl.utils.graph import undirected_neighbors
from xdl.constants import VESSEL_PROP_TYPE

# Relative
from .general import Wait
from .rotavap import RotavapStir
from ..base_step import ChemputerStep
from ..steps_base import (
    CStir,
    CSetStirRate,
    CStopStir,
    CRotavapSetRotationSpeed,
    CRotavapStartRotation,
    CRotavapStopRotation,
)
from ...constants import (
    DEFAULT_DISSOLVE_ROTAVAP_ROTATION_SPEED,
    HEIDOLPH_TORQUE_100
)
from ...utils.execution import get_vessel_stirrer, get_vessel_type
from xdl.utils.prop_limits import (
    ROTATION_SPEED_PROP_LIMIT,
    TIME_PROP_LIMIT
)
from ...utils.prop_limits import VESSEL_TYPE_PROP_LIMIT

class SetStirRate(ChemputerStep, AbstractStep):
    """Set stir rate. Works on rotavap, reactor or filter.

    Args:
        vessel (str): Vessel to set stir rate for.
        stir_speed (float): Stir rate in RPM
        vessel_type (str): Given internally. 'filter', 'rotavap' or 'reactor'.
        stirrer_is_heitorque (str): Internal prop.  True if stirrer is Heidolph
            HeiTorque100. Necessary as this stirrer starts stirring when stir
            speed is set so needs to be treated differently to get uniform
            behaviour.
    """

    INTERNAL_PROPS = [
        'vessel_type',
        'stirrer_is_heitorque',
    ]

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'stir_speed': float,
        'vessel_type': str,
        'stirrer_is_heitorque': bool,
    }

    PROP_LIMITS = {
        'stir_speed': ROTATION_SPEED_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,
        stir_speed: float,

        # Internal properties
        vessel_type: Optional[str] = None,
        stirrer_is_heitorque: Optional[bool] = False
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain the vessel type if not defined
        if not self.vessel_type:
            self.vessel_type = get_vessel_type(graph, self.vessel)

        for _, data in undirected_neighbors(graph, self.vessel, data=True):
            if data['class'] == HEIDOLPH_TORQUE_100:
                self.stirrer_is_heitorque = True
                break

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        # Set rotation speed if a rotavap
        if self.vessel_type == 'rotavap':
            return [CRotavapSetRotationSpeed(rotavap_name=self.vessel,
                                             rotation_speed=self.stir_speed)]
        elif self.stirrer_is_heitorque:
            return [
                CSetStirRate(vessel=self.vessel, stir_speed=self.stir_speed),
                CStopStir(self.vessel)]
        else:
            return [
                CSetStirRate(
                    vessel=self.vessel,
                    stir_speed=self.stir_speed
                )
            ]

class StartStir(ChemputerStep, AbstractStep):
    """Start stirring given vessel.

    Args:
        vessel (str): Vessel name to stir.
        stir_speed (int, optional): Speed in RPM to stir at.
    """

    DEFAULT_PROPS = {
        'stir_speed': '250 RPM',
    }

    INTERNAL_PROPS = [
        'vessel_type'
    ]

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'stir_speed': float,
        'vessel_type': str,
    }

    PROP_LIMITS = {
        'stir_speed': ROTATION_SPEED_PROP_LIMIT,
        'vessel_type': VESSEL_TYPE_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,
        stir_speed: Optional[float] = 'default',

        # Internal properties
        vessel_type: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain the vessel type if not defined
        if not self.vessel_type:
            self.vessel_type = get_vessel_type(graph, self.vessel)

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        # Set rotation speed and start rotating if a Rotavap
        if self.vessel_type == 'rotavap':
            #  Limit RPM if high one meant for stirrer passed in by accident.
            stir_speed = min(
                self.stir_speed, DEFAULT_DISSOLVE_ROTAVAP_ROTATION_SPEED
            )

            return [
                CRotavapSetRotationSpeed(
                    rotavap_name=self.vessel,
                    rotation_speed=stir_speed
                ),
                CRotavapStartRotation(rotavap_name=self.vessel)
            ]

        # Set the stir rate and start stirring if default
        return [
            CStir(vessel=self.vessel),
            CSetStirRate(vessel=self.vessel, stir_speed=self.stir_speed),
        ]

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Get the requirements needed for this step

        Returns:
            Dict[str, Dict[str, Any]]: Step requirements
        """

        return {
            'vessel': {
                'stir': True
            }
        }

class StopStir(ChemputerStep, AbstractStep):
    """Stop stirring given vessel.

    Args:
        vessel (str): Vessel name to stop stirring.
        vessel_has_stirrer (bool): True if vessel has stirrer, otherwise False.
            The point of this is that StopStir can be used and if there is no
            stirrer then it is just ignored rather than an error being raised.
    """

    INTERNAL_PROPS = [
        'vessel_type',
        'vessel_has_stirrer',
    ]

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'vessel_type': str,
        'vessel_has_stirrer': bool
    }

    PROP_LIMIT = {
        'vessel_type': VESSEL_TYPE_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,

        # Internal properties
        vessel_type: str = None,
        vessel_has_stirrer: bool = True,
        **kwargs
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain the vessel type if not defined
        if not self.vessel_type:
            self.vessel_type = get_vessel_type(graph, self.vessel)

        # Check if the vessel has a stirrer attached
        self.vessel_has_stirrer = (
            True if get_vessel_stirrer(graph, self.vessel)
            else False
        )

    def get_steps(self) -> Optional[List[Step]]:
        """Get the list of steps/base steps to execute.

        Returns:
            Optional[List[Step]]: Steps to execute. None if no stirrer
        """

        # Stop stirring if stirrer is present
        if self.vessel_has_stirrer:
            return [CStopStir(vessel=self.vessel)]

        # Stop rotating if vessel is a rotavap
        elif self.vessel_type == 'rotavap':
            return [CRotavapStopRotation(rotavap_name=self.vessel)]

        # No stirrer present
        return []

class Stir(ChemputerStep, AbstractStep):
    """Stir given vessel for given time at room temperature.

    Args:
        vessel (str): Vessel to stir.
        time (float): Time to stir for.
        continue_stirring (bool): Continue stirring after stirring time elapses.
        stir_speed (float): Stir rate in RPM.
        vessel_type (str): Given internally. 'reactor', 'filter', 'rotavap',
            'flask' or 'separator'.
    """

    DEFAULT_PROPS = {
        'stir_speed': '250 RPM',
        'continue_stirring': False,
    }

    INTERNAL_PROPS = [
        'vessel_type'
    ]

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'time': float,
        'continue_stirring': bool,
        'stir_speed': float,
        'vessel_type': str,
    }

    PROP_LIMITS = {
        'stir_speed': ROTATION_SPEED_PROP_LIMIT,
        'vessel_type': VESSEL_TYPE_PROP_LIMIT,
        'time': TIME_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,
        time: float,
        continue_stirring: bool = 'default',
        stir_speed: Optional[float] = 'default',

        # Internal properties
        vessel_type: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph: Dict):
        """Prepares the current step for execution.
        Gets/sets/cleans up appropriate items in preparation for exection.

        Args:
            graph (Dict): Chemputer Graph to check
        """

        # Obtain the vessel type if not defined
        if not self.vessel_type:
            self.vessel_type = get_vessel_type(graph, self.vessel)

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        # Start rotation if vessel is a rotavap
        if self.vessel_type == 'rotavap':
            # Limit stir_speed as rotavap can't rotate as fast as stirrer.
            stir_speed = min(
                self.stir_speed, DEFAULT_DISSOLVE_ROTAVAP_ROTATION_SPEED
            )

            return [
                RotavapStir(
                    rotavap_name=self.vessel,
                    stir_speed=stir_speed,
                    time=self.time,
                    continue_stirring=self.continue_stirring,
                ),
            ]

        # Start stirring and wait for given time
        else:
            steps = [
                StartStir(vessel=self.vessel, stir_speed=self.stir_speed),
                Wait(time=self.time),
            ]

            # Stirring should continue, return
            if self.continue_stirring is True:
                return steps

            # Stirring should stop, add a StopStir
            else:
                steps.append(StopStir(vessel=self.vessel))
                return steps

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Get the requirements needed for this step

        Returns:
            Dict[str, Dict[str, Any]]: Step requirements
        """

        return {
            'vessel': {
                'stir': True,
            }
        }
