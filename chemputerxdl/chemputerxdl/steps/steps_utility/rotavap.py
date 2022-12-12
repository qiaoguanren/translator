"""
.. module:: steps_utility.rotavap
    :platforms: Unix, Windows
    :synopsis: XDL steps to interact with Rotavaps

"""

from typing import Optional, List, Dict, Any

# XDL
from xdl.steps.base_steps import AbstractStep, Step
from xdl.constants import VESSEL_PROP_TYPE
from xdl.utils.prop_limits import (
    ROTATION_SPEED_PROP_LIMIT,
    TEMP_PROP_LIMIT,
    TIME_PROP_LIMIT,
    PRESSURE_PROP_LIMIT
)

# Relative
from .general import Wait
from ..base_step import ChemputerStep
from ..steps_base import (
    CRotavapSetRotationSpeed,
    CRotavapStartRotation,
    CRotavapStopRotation,
    CStopVacuum,
    CVentVacuum,
    CRotavapLiftUp,
    CRotavapStopHeater,
    CSetVacuumSetPoint,
    CStartVacuum,
    CRotavapSetTemp,
    CRotavapStartHeater,
)

class RotavapStartRotation(ChemputerStep, AbstractStep):
    """Start stirring given vessel.

    Args:
        rotavap_name (str): Rotavap name to start rotation for.
        rotation_speed (float): Speed in RPM to rotate rotavap flask at.
    """

    DEFAULT_PROPS = {
        'rotation_speed': '150 RPM',
    }

    PROP_TYPES = {
        'rotavap_name': VESSEL_PROP_TYPE,
        'rotation_speed': float
    }

    PROP_LIMITS = {
        'rotation_speed': ROTATION_SPEED_PROP_LIMIT,
    }

    def __init__(
        self,
        rotavap_name: str,
        rotation_speed: Optional[float] = 'default',
        **kwargs
    ) -> None:
        super().__init__(locals())

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        return [
            CRotavapSetRotationSpeed(
                rotavap_name=self.rotavap_name,
                rotation_speed=self.rotation_speed
            ),
            CRotavapStartRotation(rotavap_name=self.rotavap_name)
        ]

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Get the requirements needed for this step

        Returns:
            Dict[str, Dict[str, Any]]: Step requirements
        """

        return {
            'rotavap_name': {
                'rotavap': True,
            }
        }

class RotavapStopRotation(ChemputerStep, AbstractStep):
    """Stop stirring given vessel.

    Args:
        rotavap_name (str): Rotavap name to start rotation for.
    """

    PROP_TYPES = {
        'rotavap_name': VESSEL_PROP_TYPE
    }

    def __init__(
        self, rotavap_name: str, **kwargs
    ) -> None:
        super().__init__(locals())

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        return [CRotavapStopRotation(rotavap_name=self.rotavap_name)]

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Get the requirements needed for this step

        Returns:
            Dict[str, Dict[str, Any]]: Step requirements
        """

        return {
            'rotavap_name': {
                'rotavap': True,
            }
        }

class RotavapStir(ChemputerStep, AbstractStep):
    """Stir given vessel for given time at room temperature.

    Args:
        rotavap_name (str): Rotavap name to start rotation for.
        time (float): Time to stir for.
        continue_stirring (bool): Continue stirring after stirring time elapses.
        stir_speed (float): Speed to rotate rotavap flask at.
    """

    DEFAULT_PROPS = {
        'stir_speed': '250 RPM',
        'continue_stirring': False,
    }

    PROP_TYPES = {
        'rotavap_name': VESSEL_PROP_TYPE,
        'time': float,
        'continue_stirring': bool,
        'stir_speed': float
    }

    PROP_LIMITS = {
        'stir_speed': ROTATION_SPEED_PROP_LIMIT,
        'time': TIME_PROP_LIMIT,
    }

    def __init__(
        self,
        rotavap_name: str,
        time: float,
        continue_stirring: bool = 'default',
        stir_speed: Optional[float] = 'default',
        **kwargs
    ) -> None:
        super().__init__(locals())

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        # Start the rotation and wait
        steps = [
            RotavapStartRotation(
                rotavap_name=self.rotavap_name,
                rotation_speed=self.stir_speed
            ),
            Wait(time=self.time),
        ]

        # Flagged to kee pstirring, just return
        if self.continue_stirring is True:
            return steps

        # Add a stop rotation and return
        steps.append(RotavapStopRotation(rotavap_name=self.rotavap_name))

        return steps

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Get the requirements needed for this step

        Returns:
            Dict[str, Dict[str, Any]]: Step requirements
        """

        return {
            'rotavap_name': {
                'rotavap': True,
            }
        }

class RotavapStopEverything(ChemputerStep, AbstractStep):
    """Stop vacuum, lift rotavap flask up, vent vacuum, stop heater and stop
    rotation.

    Args:
        rotavap_name (str): Name of rotavap to stop evaporating with.
    """

    PROP_TYPES = {
        'rotavap_name': VESSEL_PROP_TYPE
    }

    def __init__(self, rotavap_name: str) -> None:
        super().__init__(locals())

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        return [
            CStopVacuum(self.rotavap_name),
            CRotavapLiftUp(self.rotavap_name),
            CVentVacuum(self.rotavap_name),
            CRotavapStopHeater(self.rotavap_name),
            CRotavapStopRotation(self.rotavap_name),
        ]

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Get the requirements needed for this step

        Returns:
            Dict[str, Dict[str, Any]]: Step requirements
        """

        return {
            'rotavap_name': {
                'rotavap': True,
            }
        }

class RotavapStartVacuum(ChemputerStep, AbstractStep):
    """Start vacuum at given pressure.

    Args:
        rotavap_name (str): Name of rotavap to start vacuum.
        pressure (float): Pressure in mbar to set vacuum to.
    """

    PROP_TYPES = {
        'rotavap_name': VESSEL_PROP_TYPE,
        'pressure': float
    }

    PROP_LIMITS = {
        'pressure': PRESSURE_PROP_LIMIT,
    }

    def __init__(self, rotavap_name: str, pressure: float) -> None:
        super().__init__(locals())

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        return [
            CSetVacuumSetPoint(self.rotavap_name, self.pressure),
            CStartVacuum(self.rotavap_name),
        ]

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Get the requirements needed for this step

        Returns:
            Dict[str, Dict[str, Any]]: Step requirements
        """

        return {
            'rotavap_name': {
                'rotavap': True,
            }
        }

class RotavapHeatToTemp(ChemputerStep, AbstractStep):
    """Set rotavap temperature to given temp and start heater.

    Args:
        rotavap_name (str): Name of rotavap to start heating.
        temp (float): Temperature to heat rotavap to.
    """

    PROP_TYPES = {
        'rotavap_name': VESSEL_PROP_TYPE,
        'temp': float
    }

    PROP_LIMITS = {
        'temp': TEMP_PROP_LIMIT,
    }

    def __init__(self, rotavap_name: str, temp: float) -> None:
        super().__init__(locals())

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        return [
            CRotavapSetTemp(self.rotavap_name, self.temp),
            CRotavapStartHeater(self.rotavap_name),
        ]

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Get the requirements needed for this step

        Returns:
            Dict[str, Dict[str, Any]]: Step requirements
        """

        return {
            'rotavap_name': {
                'rotavap': True,
            }
        }
