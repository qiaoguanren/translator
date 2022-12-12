"""
.. module:: steps_synthesis.precipitate
    :platforms: Unix, Windows
    :synopsis: XDL step to cause precipitation by changing temperature and
                stirring for some time

"""

from typing import List, Dict, Any, Optional

#  XDL
from xdl.steps.base_steps import AbstractStep, Step
from xdl.utils.prop_limits import TEMP_PROP_LIMIT, TIME_PROP_LIMIT
from xdl.constants import VESSEL_PROP_TYPE

# Relative
from ..base_step import ChemputerStep
from ..steps_utility import Stir, HeatChillToTemp

class Precipitate(ChemputerStep, AbstractStep):
    """Step to cause precipitation by changing temperature and stirring for some
    time.

    Args:
        vessel (str): Vessel to trigger precipitation in.
        temp (float): Optional. Temperature to chill to to cause precipitation.
            If not given room temperature is used.
        time (float): Optional.  Time to stir vessel for after temp is reached.
    """

    DEFAULT_PROPS = {
        'temp': '25°C',
        'time': '60 mins',
    }

    PROP_TYPES = {
        'vessel': VESSEL_PROP_TYPE,
        'temp': float,
        'time': float
    }

    PROP_LIMITS = {
        'temp': TEMP_PROP_LIMIT,
        'time': TIME_PROP_LIMIT,
    }

    def __init__(
        self,
        vessel: str,
        temp: Optional[float] = 'default',
        time: Optional[float] = 'default'
    ) -> None:
        super().__init__(locals())

    def get_steps(self) -> List[Step]:
        """Get the list of steps/base steps to execute.

        Returns:
            List[Step]: Steps to execute.
        """

        return [
            HeatChillToTemp(vessel=self.vessel, temp=self.temp, stir=True),
            Stir(vessel=self.vessel, time=self.time),
        ]

    @property
    def requirements(self) -> Dict[str, Dict[str, Any]]:
        """Get the requirements needed for this step

        Returns:
            Dict[str, Dict[str, Any]]: Step requirements
        """

        return {
            'vessel': {
                'temp': [self.temp]
            }
        }
