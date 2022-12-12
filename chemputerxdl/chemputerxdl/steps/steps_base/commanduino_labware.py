"""
.. module:: steps_base.commanduino_labware
    :platforms: Unix, Windows
    :synopsis: Base steps for CommanduinoLabware in context of the Chemputer

"""

from typing import Optional, Tuple, List

# XDL
from xdl.steps.base_steps import AbstractBaseStep
from xdl.utils.prop_limits import TIME_PROP_LIMIT, PropLimit

# Relative
from ..base_step import ChemputerStep
from ...utils.prop_limits import INT_0_255_PROP_LIMIT

class CTurnMotor(ChemputerStep, AbstractBaseStep):
    """Turns a motor on a Commanduino Labware device

    Args:
        device_name (str): Name of the node representing the labware device
        motor_name (str): Name of the motor on the device
        n_turns (int): How many turns to make the motor perform
        increment (int): NUmber of steps which represent 1 single turn
    """

    DEFAULT_PROPS = {
        'n_turns': 1,
        'increment': 6400
    }

    PROP_TYPES = {
        'device_name': str,
        'motor_name': str,
        'n_turns': int,
        'increment': int
    }

    def __init__(
        self,
        device_name: str,
        motor_name: str,
        n_turns: int = 'default',
        increment: Optional[int] = 'default',
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

        return [self.device_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step

        Args:
            chempiler (Chempiler): Chempiler object.
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        device = chempiler[self.device_name]

        device.turn_motor(
            self.motor_name, n_turns=self.n_turns, increment=self.increment
        )

        return True

class CMoveMotor(ChemputerStep, AbstractBaseStep):
    """Moves a motor a number of steps

    Args:
        device_name (str): Name of the node representing the labware device
        motor_name (str): Name of the motor on the device
        steps (int): Number of steps to move
    """

    PROP_TYPES = {
        'device_name': str,
        'motor_name': str,
        'steps': int
    }

    def __init__(self, device_name: str, motor_name: str, steps: int):
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

        return [self.device_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step

        Args:
            chempiler (Chempiler): Chempiler object.
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        device = chempiler[self.device_name]
        device.move_motor(self.motor_name, self.steps)
        return True

class CMoveMotorToPosition(ChemputerStep, AbstractBaseStep):
    """Moves a motor to a given position, in steps

    Args:
        device_name (str): Name of the node representing the labware device
        motor_name (str): Name of the motor on the device
        position (int): POsition to move the motor to
    """

    PROP_TYPES = {
        'device_name': str,
        'motor_name': str,
        'position': int
    }

    def __init__(self, device_name: str, motor_name: str, position: int):
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

        return [self.device_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object.
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        device = chempiler[self.device_name]
        device.move_motor_to_position(self.motor_name, self.position)
        return True

class CHomeMotor(ChemputerStep, AbstractBaseStep):
    """Moves a motor to its home position.
    Requires a home switch to be present.

    Args:
        device_name (str): Name of the node representing the labware device.
        motor_name (str): Name of the motor on the device
    """

    PROP_TYPES = {
        'device_name': str,
        'motor_name': str
    }

    def __init__(self, device_name: str, motor_name: str):
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

        return [self.device_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        device = chempiler[self.device_name]
        device.home_motor(self.motor_name)
        return True

class CRunMotor(ChemputerStep, AbstractBaseStep):
    """Runs a motor for a given period of time, in seconds

    Args:
        device_name (str): Name of the node representing the labware device
        motor_name (str): Name of the motor on the device
        timescale (int): Length of time to run for, in seconds
        increment (int, optional): Increment in steps. Defaults to 8000.
    """

    DEFAULT_PROPS = {
        'increment': 8000
    }

    PROP_TYPES = {
        'device_name': str,
        'motor_name': str,
        'timescale': int,
        'increment': int
    }

    PROP_LIMITS = {
        'timescale': TIME_PROP_LIMIT,
    }

    def __init__(
        self,
        device_name: str,
        motor_name: str,
        timescale: int,
        increment: Optional[int] = 'default'
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

        return [self.device_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        device = chempiler[self.device_name]
        device.run_motor(
            self.motor_name,
            self.timescale,
            increment=self.increment
        )
        return True

class CSetPin(ChemputerStep, AbstractBaseStep):
    """Sets the value of a digital pin to HIGH or LOW state, dependent on level

    Args:
        device_name (str): Name of the node representing the labware device.
        pin_name (str): Name of the pin on the device.
        level (int, optional): Level to set, either 0 or 1. Defaults to 0.
    """

    DEFAULT_PROPS = {
        'level': 0
    }

    PROP_TYPES = {
        'device_name': str,
        'pin_name': str,
        'level': int
    }

    PROP_LIMITS = {
        'level': PropLimit(
            enum=['0', '1'],
            default='0'
        ),
    }

    def __init__(
        self,
        device_name: str,
        pin_name: str,
        level: Optional[int] = 'default'
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

        return [self.device_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        device = chempiler[self.device_name]
        device.set_pin(self.pin_name, level=self.level)
        return True

class CSetPinPWM(ChemputerStep, AbstractBaseStep):
    """Sets the PWm value of an analog pin between 0 and 255.

    Args:
        device_name (str): Name of the node representing the labware device.
        pin_name (str): Name of the pin on the device
        value (int, optional): PWM value between 0 and 255. Defaults to 0.
    """

    DEFAULT_PROPS = {
        'value': 0
    }

    PROP_TYPES = {
        'device_name': str,
        'pin_name': str,
        'value': int
    }

    PROP_LIMITS = {
        'value': INT_0_255_PROP_LIMIT,
    }

    def __init__(
        self,
        device_name: str,
        pin_name: str,
        value: Optional[int] = 'default'
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
        return [self.device_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        device = chempiler[self.device_name]
        device.set_pin_pwm(self.pin_name, value=self.value)
        return True

class CReadPin(ChemputerStep, AbstractBaseStep):
    """Reads the current state of a digital pin. HIGH or LOW.

    Args:
        device_name (str): Name of the node representing the labware device.
        pin_name (str): Name of the pin on the device.
    """

    PROP_TYPES = {
        'device_name': str,
        'pin_name': str
    }

    def __init__(self, device_name: str, pin_name: str):
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

        return [self.device_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        device = chempiler[self.device_name]
        device.read_pin(self.pin_name)
        return True

class CReadPinPWM(ChemputerStep, AbstractBaseStep):
    """Reads the current PWM value of an analog pin. Between 0 and 255.

    Args:
        device_name (str): Name of the node representing the labware device.
        pin_name (str): Name of the pin on the device
    """

    PROP_TYPES = {
        'device_name': str,
        'pin_name': str
    }

    def __init__(self, device_name: str, pin_name: str):
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

        return [self.device_name], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        device = chempiler[self.device_name]
        device.read_pin_pwm(self.pin_name)
        return True
