"""
.. module:: steps_base.stirrer
    :platforms: Unix, Windows
    :synopsis: Base steps for the Chemputer stirrers

"""

from typing import Dict, Tuple, List

# XDL
from xdl.steps.base_steps import AbstractBaseStep
from xdl.utils.prop_limits import TEMP_PROP_LIMIT, ROTATION_SPEED_PROP_LIMIT
from xdl.utils.misc import SanityCheck
from xdl.constants import VESSEL_PROP_TYPE

# Relative
from ..base_step import ChemputerStep
from ...utils.execution import get_vessel_stirrer, get_heater

class CStir(ChemputerStep, AbstractBaseStep):
    """Starts the stirring operation of a hotplate or overhead stirrer.

    Args:
        vessel (str): Vessel name to stir.
    """

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'stirrer': str,
    }

    INTERNAL_PROPS = ['stirrer']

    def __init__(self, vessel: str, stirrer: str = None) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph):
        self.stirrer = get_vessel_stirrer(graph, self.vessel)

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

        return [self.vessel, self.stirrer], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        chempiler[self.stirrer].start_stirrer()
        return True

    def sanity_checks(self, graph):
        return [SanityCheck(
            condition=self.stirrer,
            error_msg=f"Can't find stirrer attached to {self.vessel}."
        )]

class CStirrerHeat(ChemputerStep, AbstractBaseStep):
    """Starts the heating operation of a hotplate stirrer.

    Args:
        vessel (str): Vessel name to heat.
    """

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'heater': str,
    }

    INTERNAL_PROPS = ['heater']

    def __init__(self, vessel: str, heater: str = None) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph):
        self.heater = get_heater(graph, self.vessel)

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

        return [self.vessel, self.heater], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        chempiler[self.heater].start_heater()
        return True

    def sanity_checks(self, graph):
        return [SanityCheck(
            condition=self.heater,
            error_msg=f"Can't find hotplate attached to {self.vessel}."
        )]

class CStopStir(ChemputerStep, AbstractBaseStep):
    """Stops the stirring operation of a hotplate or overhead stirrer.

    Args:
        vessel (str): Vessel name to stop stirring.
    """

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'stirrer': str
    }

    INTERNAL_PROPS = ['stirrer']

    def __init__(self, vessel: str, stirrer: str = None) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph):
        self.stirrer = get_vessel_stirrer(graph, self.vessel)

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

        return [self.vessel, self.stirrer], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        chempiler[self.stirrer].stop_stirrer()
        return True

    def sanity_checks(self, graph):
        return [SanityCheck(
            condition=self.stirrer,
            error_msg=f"Can't find stirrer attached to {self.vessel}."
        )]

class CStopHeat(ChemputerStep, AbstractBaseStep):
    """Stop heating hotplace stirrer.

    Args:
        vessel (str): Vessel name to stop heating.
    """

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'heater': str,
    }

    INTERNAL_PROPS = ['heater']

    def __init__(self, vessel: str, heater: str = None) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph):
        self.heater = get_heater(graph, self.vessel)

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

        return [self.vessel, self.heater], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        chempiler[self.heater].stop_heater()
        return True

    def sanity_checks(self, graph):
        return [SanityCheck(
            condition=self.heater,
            error_msg=f"Can't find hotplate attached to {self.vessel}."
        )]

class CStirrerSetTemp(ChemputerStep, AbstractBaseStep):
    """Sets the temperature setpoint of a hotplate stirrer. This command is NOT
    available for overhead stirrers!

    Args:
        vessel (str): Vessel name to set temperature of hotplate stirrer.
        temp (float): Temperature in °C
    """

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'temp': float,
        'heater': str,
    }

    PROP_LIMITS = {
        'temp': TEMP_PROP_LIMIT,
    }

    INTERNAL_PROPS = ['heater']

    def __init__(self, vessel: str, temp: float, heater: str = None) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph):
        self.heater = get_heater(graph, self.vessel)

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

        return [self.vessel, self.heater], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        chempiler[self.heater].temperature_sp = self.temp
        return True

    def sanity_checks(self, graph):
        return [SanityCheck(
            condition=self.heater,
            error_msg=f"Can't find hotplate attached to {self.vessel}."
        )]

class CSetStirRate(ChemputerStep, AbstractBaseStep):
    """Sets the stirring speed setpoint of a hotplate or overhead stirrer.

    Args:
        vessel (str): Vessel name to set stir speed.
        stir_speed (float): Stir speed in RPM.
    """

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'stir_speed': float,
        'stirrer': str,
    }

    PROP_LIMITS = {
        'stir_speed': ROTATION_SPEED_PROP_LIMIT,
    }

    INTERNAL_PROPS = ['stirrer']

    def __init__(
        self, vessel: str, stir_speed: float, stirrer: str = None
    ) -> None:
        super().__init__(locals())

    def on_prepare_for_execution(self, graph):
        self.stirrer = get_vessel_stirrer(graph, self.vessel)

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

        return [self.vessel, self.stirrer], [], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        chempiler[self.stirrer].stir_rate_sp = self.stir_speed
        return True

    def sanity_checks(self, graph):
        return [SanityCheck(
            condition=self.stirrer,
            error_msg=f"Can't find stirrer attached to {self.vessel}."
        )]

class CStirrerWaitForTemp(ChemputerStep, AbstractBaseStep):
    """Delays the script execution until the current temperature of the
    hotplate is within 0.5 °C of the setpoint. This command is NOT available
    for overhead stirrers!

    Args:
        vessel (str): Vessel name to wait for temperature.
    """

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE
    }

    def __init__(self, vessel: str) -> None:
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

        return [], [self.vessel], []

    def execute(self, chempiler, logger=None, level=0) -> bool:
        """Executes the XDL step.

        Args:
            chempiler (Chempiler): Chempiler object
            logger (Logger, optional): Logging object. Defaults to None.
            level (int, optional): Logging level. Defaults to 0.

        Returns:
            bool: Step executed successfully.
        """

        chempiler.stirrer.wait_for_temp(self.vessel)
        return True

    def duration(self, graph: Dict) -> float:
        """Calculate duration of the step

        Args:
            graph (Dict): Graph to search

        Returns:
            float: Duration of the step
        """

        return 60 * 60  # arbitrary value for the moment
