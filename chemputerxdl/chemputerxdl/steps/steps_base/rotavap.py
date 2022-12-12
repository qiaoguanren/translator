"""
.. module:: steps_base.rotavap
    :platforms: Unix, Windows
    :synopsis: Base steps for the Chemputer Rotavaps

"""

from typing import Optional, Dict, Tuple, List

# XDL
from xdl.steps.base_steps import AbstractBaseStep
from xdl.utils.prop_limits import (
    TIME_PROP_LIMIT,
    PRESSURE_PROP_LIMIT,
    TEMP_PROP_LIMIT,
    ROTATION_SPEED_PROP_LIMIT,
    PropLimit,
)
from xdl.constants import VESSEL_PROP_TYPE

# Relative
from ..base_step import ChemputerStep
from ...constants import DEFAULT_ROTAVAP_WAIT_FOR_ARM_TIME

class CRotavapStartHeater(ChemputerStep, AbstractBaseStep):
    """Starts the heating bath of a rotary evaporator.

    Args:
        rotavap_name (str): Name of the node representing the rotary evaporator.
    """

    PROP_TYPES = {
        'rotavap_name': VESSEL_PROP_TYPE
    }

    def __init__(self, rotavap_name: str) -> None:
        super().__init__(locals())

    def locks(self, chempiler) -> Tuple[List[str], List[str], List[str]]:
        """Returns a series of locked nodes used by the Paralleliser.

        Args:
            chempiler (Chempiler): Chempiler object

        Returns:
            Tuple[List[str], List[str], List[str]]: Locked nodes in the order:
                                    1.) Current Locks -- Currently locked
                                    2.) Ongoing locks -- Continually locked
                                    3.) Unlocks -- Unlocked
        """

        return [self.rotavap_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        rotavap = chempiler[self.rotavap_name]
        rotavap.start_heater()
        return True

class CRotavapStopHeater(ChemputerStep, AbstractBaseStep):
    """Stops the heating bath of a rotary evaporator.

    Args:
        rotavap_name (str): Name of the node representing the rotary evaporator.
    """

    PROP_TYPES = {
        'rotavap_name': VESSEL_PROP_TYPE
    }

    def __init__(self, rotavap_name: str) -> None:
        super().__init__(locals())

    def locks(self, chempiler) -> Tuple[List[str], List[str], List[str]]:
        """Returns a series of locked nodes used by the Paralleliser.

        Args:
            chempiler (Chempiler): Chempiler object

        Returns:
            Tuple[List[str], List[str], List[str]]: Locked nodes in the order:
                                    1.) Current Locks -- Currently locked
                                    2.) Ongoing locks -- Continually locked
                                    3.) Unlocks -- Unlocked
        """

        return [self.rotavap_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        rotavap = chempiler[self.rotavap_name]
        rotavap.stop_heater()
        return True

class CRotavapStartRotation(ChemputerStep, AbstractBaseStep):
    """Starts the rotation of a rotary evaporator.

    Args:
        rotavap_name (str): Name of the node representing the rotary evaporator.
    """

    PROP_TYPES = {
        'rotavap_name': VESSEL_PROP_TYPE
    }

    def __init__(self, rotavap_name: str) -> None:
        super().__init__(locals())

    def locks(self, chempiler) -> Tuple[List[str], List[str], List[str]]:
        """Returns a series of locked nodes used by the Paralleliser.

        Args:
            chempiler (Chempiler): Chempiler object

        Returns:
            Tuple[List[str], List[str], List[str]]: Locked nodes in the order:
                                    1.) Current Locks -- Currently locked
                                    2.) Ongoing locks -- Continually locked
                                    3.) Unlocks -- Unlocked
        """

        return [self.rotavap_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        rotavap = chempiler[self.rotavap_name]
        rotavap.start_rotation()
        return True

class CRotavapStopRotation(ChemputerStep, AbstractBaseStep):
    """Stops the rotation of a rotary evaporator.

    Args:
        rotavap_name (str): Name of the node representing the rotary evaporator.
    """

    PROP_TYPES = {
        'rotavap_name': VESSEL_PROP_TYPE
    }

    def __init__(self, rotavap_name: str) -> None:
        super().__init__(locals())

    def locks(self, chempiler) -> Tuple[List[str], List[str], List[str]]:
        """Returns a series of locked nodes used by the Paralleliser.

        Args:
            chempiler (Chempiler): Chempiler object

        Returns:
            Tuple[List[str], List[str], List[str]]: Locked nodes in the order:
                                    1.) Current Locks -- Currently locked
                                    2.) Ongoing locks -- Continually locked
                                    3.) Unlocks -- Unlocked
        """

        return [self.rotavap_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        rotavap = chempiler[self.rotavap_name]
        rotavap.stop_rotation()
        return True

class CRotavapLiftUp(ChemputerStep, AbstractBaseStep):
    """Lifts the rotary evaporator arm up.

    Args:
        rotavap_name (str): Name of the node representing the rotary evaporator.
    """

    PROP_TYPES = {
        'rotavap_name': VESSEL_PROP_TYPE
    }

    def __init__(self, rotavap_name: str) -> None:
        super().__init__(locals())

    def locks(self, chempiler) -> Tuple[List[str], List[str], List[str]]:
        """Returns a series of locked nodes used by the Paralleliser.

        Args:
            chempiler (Chempiler): Chempiler object

        Returns:
            Tuple[List[str], List[str], List[str]]: Locked nodes in the order:
                                    1.) Current Locks -- Currently locked
                                    2.) Ongoing locks -- Continually locked
                                    3.) Unlocks -- Unlocked
        """

        return [self.rotavap_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        rotavap = chempiler[self.rotavap_name]
        rotavap.lift_up()
        return True

    def duration(self, graph: Dict) -> float:
        """Get the duration of the step.

        Args:
            graph (Dict): Chemputer graph to check

        Returns:
            float: Duration of the step.
        """

        return DEFAULT_ROTAVAP_WAIT_FOR_ARM_TIME

class CRotavapLiftDown(ChemputerStep, AbstractBaseStep):
    """Lifts the rotary evaporator down.

    Args:
        rotavap_name (str): Name of the node representing the rotary evaporator.
    """

    PROP_TYPES = {
        'rotavap_name': VESSEL_PROP_TYPE
    }

    def __init__(self, rotavap_name: str) -> None:
        super().__init__(locals())

    def locks(self, chempiler) -> Tuple[List[str], List[str], List[str]]:
        """Returns a series of locked nodes used by the Paralleliser.

        Args:
            chempiler (Chempiler): Chempiler object

        Returns:
            Tuple[List[str], List[str], List[str]]: Locked nodes in the order:
                                    1.) Current Locks -- Currently locked
                                    2.) Ongoing locks -- Continually locked
                                    3.) Unlocks -- Unlocked
        """

        return [self.rotavap_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        rotavap = chempiler[self.rotavap_name]
        rotavap.lift_down()
        return True

    def duration(self, graph: Dict) -> float:
        """Get the duration of the step.

        Args:
            graph (Dict): Chemputer graph to check

        Returns:
            float: Duration of the step.
        """

        return DEFAULT_ROTAVAP_WAIT_FOR_ARM_TIME

class CRotavapReset(ChemputerStep, AbstractBaseStep):
    """
    Resets the rotary evaporator.

    Args:
        rotavap_name (str): Name of the node representing the rotary evaporator.
    """

    PROP_TYPES = {
        'rotavap_name': VESSEL_PROP_TYPE
    }

    def __init__(self, rotavap_name: str) -> None:
        super().__init__(locals())

    def locks(self, chempiler) -> Tuple[List[str], List[str], List[str]]:
        """Returns a series of locked nodes used by the Paralleliser.

        Args:
            chempiler (Chempiler): Chempiler object

        Returns:
            Tuple[List[str], List[str], List[str]]: Locked nodes in the order:
                                    1.) Current Locks -- Currently locked
                                    2.) Ongoing locks -- Continually locked
                                    3.) Unlocks -- Unlocked
        """

        return [self.rotavap_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        rotavap = chempiler[self.rotavap_name]
        rotavap.reset_rotavap()
        return True

class CRotavapSetTemp(ChemputerStep, AbstractBaseStep):
    """Sets the temperature setpoint for the heating bath.

    Args:
        rotavap_name (str): Name of the node representing the rotary evaporator.
        temp (float): Temperature in °C.
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

    def locks(self, chempiler) -> Tuple[List[str], List[str], List[str]]:
        """Returns a series of locked nodes used by the Paralleliser.

        Args:
            chempiler (Chempiler): Chempiler object

        Returns:
            Tuple[List[str], List[str], List[str]]: Locked nodes in the order:
                                    1.) Current Locks -- Currently locked
                                    2.) Ongoing locks -- Continually locked
                                    3.) Unlocks -- Unlocked
        """

        return [self.rotavap_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        rotavap = chempiler[self.rotavap_name]
        rotavap.temperature_sp = self.temp
        return True

class CRotavapSetRotationSpeed(ChemputerStep, AbstractBaseStep):
    """Sets the rotation speed setpoint for the rotary evaporator.

    Args:
        rotavap_name (str): Name of the node representing the rotary evaporator.
        rotation_speed (float): Rotation speed setpoint in RPM.
    """

    PROP_TYPES = {
        'rotavap_name': VESSEL_PROP_TYPE,
        'rotation_speed': float
    }

    PROP_LIMITS = {
        'rotation_speed': ROTATION_SPEED_PROP_LIMIT,
    }

    def __init__(self, rotavap_name: str, rotation_speed: float) -> None:
        super().__init__(locals())

    def locks(self, chempiler) -> Tuple[List[str], List[str], List[str]]:
        """Returns a series of locked nodes used by the Paralleliser.

        Args:
            chempiler (Chempiler): Chempiler object

        Returns:
            Tuple[List[str], List[str], List[str]]: Locked nodes in the order:
                                    1.) Current Locks -- Currently locked
                                    2.) Ongoing locks -- Continually locked
                                    3.) Unlocks -- Unlocked
        """

        return [self.rotavap_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        rotavap = chempiler[self.rotavap_name]
        rotavap.rotation_speed_sp = self.rotation_speed
        return True

class CRotavapSetInterval(ChemputerStep, AbstractBaseStep):
    """Sets the interval time for the rotary evaporator, causing it to
    periodically switch direction. Setting this to 0 deactivates interval
    operation.

    Args:
        rotavap_name (str): Name of the node representing the rotary evaporator.
        interval (int): Interval time in seconds.
    """

    PROP_TYPES = {
        'rotavap_name': VESSEL_PROP_TYPE,
        'interval': int
    }

    PROP_LIMITS = {
        'interval': TIME_PROP_LIMIT,
    }

    def __init__(self, rotavap_name: str, interval: int) -> None:
        super().__init__(locals())

    def locks(self, chempiler) -> Tuple[List[str], List[str], List[str]]:
        """Returns a series of locked nodes used by the Paralleliser.

        Args:
            chempiler (Chempiler): Chempiler object

        Returns:
            Tuple[List[str], List[str], List[str]]: Locked nodes in the order:
                                    1.) Current Locks -- Currently locked
                                    2.) Ongoing locks -- Continually locked
                                    3.) Unlocks -- Unlocked
        """

        return [self.rotavap_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        rotavap = chempiler[self.rotavap_name]
        rotavap.set_interval(self.interval)
        return True

class CRotavapAutoEvaporation(ChemputerStep, AbstractBaseStep):
    """Perform the rotavap built-in auto-evaporation routine.

    Args:
        rotavap_name (str): Node name of the rotavap.
        sensitivity (int): Sensitivity mode to use. 0, 1 or 2 (Low, medium, high
            respectively).
        vacuum_limit (float): Minimum pressure for the process.
        time_limit (float): Maximum time to use for the process.
        vent_after (bool): If True, vacuum will be vented after the process is
            complete.
    """

    DEFAULT_PROPS = {
        'vent_after': True
    }

    PROP_TYPES = {
        'rotavap_name': VESSEL_PROP_TYPE,
        'sensitivity': int,
        'vacuum_limit': float,
        'time_limit': float,
        'vent_after': bool
    }

    PROP_LIMITS = {
        'sensitivity': PropLimit(
            enum=['0', '1', '2'],
            default='0'
        ),
        'vacuum_limit': PRESSURE_PROP_LIMIT,
        'time_limit': TIME_PROP_LIMIT,
    }

    def __init__(
        self,
        rotavap_name: str,
        sensitivity: int,
        vacuum_limit: float,
        time_limit: float,
        vent_after: Optional[bool] = 'default'
    ):
        super().__init__(locals())

    def locks(self, chempiler) -> Tuple[List[str], List[str], List[str]]:
        """Returns a series of locked nodes used by the Paralleliser.

        Args:
            chempiler (Chempiler): Chempiler object

        Returns:
            Tuple[List[str], List[str], List[str]]: Locked nodes in the order:
                                    1.) Current Locks -- Currently locked
                                    2.) Ongoing locks -- Continually locked
                                    3.) Unlocks -- Unlocked
        """

        return [self.rotavap_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        chempiler.vacuum.auto_evaporation(
            node_name=self.rotavap_name,
            auto_mode=self.sensitivity,
            vacuum_limit=self.vacuum_limit,
            duration=self.time_limit / 60,
            vent_after=self.vent_after
        )

        return True

    def duration(self, graph: Dict) -> float:
        """Calculates duration of the step

        Args:
            graph (Dict): Graph to search

        Returns:
            float: Duration of step
        """

        return self.time_limit
